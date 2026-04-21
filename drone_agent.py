import argparse
import time
import threading
import json
import sys
import os
from dataclasses import asdict
import paho.mqtt.client as mqtt
from google.cloud import aiplatform

import node

# Configuration
# Drones and their assigned sectors (default)
# NW, NE, SW, SE, CENTER
# We can pass these as arguments.

class DroneAgent:
    def __init__(self, host, port, username, password, agent_id, sector, role="scout", fail_after=0, protocol=mqtt.MQTTv5, vertex_project=None, vertex_endpoint=None):
        self.agent_id = agent_id
        self.sector = sector
        self.role = role
        self.position = [0, 0] # x, y on a grid
        self.battery = 100
        self._battery_offset = 0  # tracks recharge additions
        self.sector_progress = 0
        self.fail_after = fail_after
        
        # Vertex AI Live Integration
        self.vertex_project = vertex_project
        self.vertex_endpoint = vertex_endpoint
        self.vertex_client = None
        
        if self.vertex_project and self.vertex_endpoint:
            try:
                aiplatform.init(project=self.vertex_project)
                self.vertex_client = aiplatform.Endpoint(self.vertex_endpoint)
                print(f"[{self.agent_id}] Vertex AI integration initialized. Endpoint: {self.vertex_endpoint}")
            except Exception as e:
                print(f"[{self.agent_id}] WARNING: Failed to initialize Vertex AI: {e}")
                self.vertex_client = None
        else:
            print(f"[{self.agent_id}] Vertex AI parameters missing. Falling back to local simulation logic.")
        
        self.victim_detected = False
        self.victim_position = None
        self.relay_target = None

        # Hook into node.py's heartbeat
        node.HEARTBEAT_EXTRA_HOOK = self.get_heartbeat_data

        # Build MQTT client (FoxMQ supports MQTTv5)
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=agent_id,
            protocol=protocol,
            userdata={"host": host, "port": port, "agent_id": agent_id},
        )
        self.client.username_pw_set(username, password)
        self.client.on_connect = node.on_connect
        # Override on_message to inject our own custom handlers if needed,
        # but node.py's on_message handles TASK_CREATE, TASK_RESULT, etc.
        # We'll wrap it to intercept VICTIM_DETECTED if needed.
        self._original_on_message = node.on_message
        self.client.on_message = self.on_message
        self.client.on_disconnect = node.on_disconnect
        
        self.host = host
        self.port = port
        
        self.sim_thread = threading.Thread(target=self.simulation_loop, daemon=True)

    def get_heartbeat_data(self):
        my_state = node.STATE.get(self.agent_id)
        return {
            "position": self.position,
            "sector": self.sector,
            "battery": self.battery,
            "sector_progress": self.sector_progress,
            "role": self.role,
            "score": my_state.score if my_state else 100,
        }

    def on_message(self, client, userdata, message):
        # Let node.py handle standard state/task parsing
        self._original_on_message(client, userdata, message)
        
        # We can also parse it ourselves to listen for VICTIM_DETECTED or TASK_SECURE
        try:
            payload = message.payload.decode("utf-8")
            event = node.parse_message(message.topic, payload)
            if event is None:
                return

            msg_type = event.get("type")
            
            if msg_type == "BATTERY_TRANSFER" and event.get("target_id") == self.agent_id:
                amount = int(event.get("amount", 20))
                self._battery_offset += amount
                self.battery = min(100, self.battery + amount)
                print(f"[{self.agent_id}] Battery recharged +{amount}% by {event.get('peer_id')} -> {self.battery}%")

            elif msg_type == "VICTIM_DETECTED" and event.get("peer_id") != self.agent_id:
                print(f"[{self.agent_id}] Heard VICTIM_DETECTED from {event.get('peer_id')} at {event.get('position')}")
                # A scout could create a TASK_SECURE here, or a leader could.
                # Let's say if we hear VICTIM_DETECTED, the leader creates a TASK_SECURE
                if self.role == "leader" or node.STATE.get(self.agent_id, node.PeerState(peer_id="", last_seen_ms=0, role="", status="")).role == "leader":
                    self.create_secure_task(event.get("position"))
            
            elif msg_type == "TASK_CREATE":
                task_spec = event.get("task", {})
                if task_spec.get("type") == node.TASK_SECURE:
                    print(f"[{self.agent_id}] Received TASK_SECURE for victim confirmation.")
                    
        except Exception as e:
            pass

    def create_secure_task(self, victim_pos):
        task_id = f"SECURE_VICTIM_{int(time.time())}"
        task = {
            "task_id": task_id,
            "type": node.TASK_SECURE,
            "requirements": {"min_agents": 2, "required_role": "any", "max_latency_ms": 2000, "redundancy": 2},
            "payload": {"target_position": victim_pos}
        }
        create_msg = {
            "type": "TASK_CREATE",
            "peer_id": self.agent_id,
            "ts": node.now_ms(),
            "task": task
        }
        node.publish_json(self.client, node.TOPIC_SWARM, create_msg)

    def publish_victim_detected(self):
        msg = {
            "type": "VICTIM_DETECTED",
            "peer_id": self.agent_id,
            "ts": node.now_ms(),
            "position": self.position
        }
        node.publish_json(self.client, node.TOPIC_SWARM, msg)
        print(f"[{self.agent_id}] Published VICTIM_DETECTED!")

    def publish_task_result(self, task_id, result_str):
        msg = {
            "type": "TASK_RESULT",
            "peer_id": self.agent_id,
            "ts": node.now_ms(),
            "task_id": task_id,
            "result": result_str
        }
        node.publish_json(self.client, node.TOPIC_SWARM, msg)

    def simulation_loop(self):
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            
            # Failure injection
            if self.fail_after > 0 and elapsed > self.fail_after:
                print(f"[{self.agent_id}] CRITICAL FAILURE INJECTED. Drone offline.")
                os._exit(1)
                
            # Update battery and progress
            self.battery = max(0, min(100, 100 - int(elapsed / 2) + self._battery_offset))
            if self.sector_progress < 100:
                self.sector_progress = min(100, int((elapsed / 60) * 100))

            # Only move while battery > 0
            if self.battery > 0:
                if self.role == "relay":
                    self._relay_behavior()
                else:
                    self.position[0] += 1
                    self.position[1] += 1
            
            # Mock finding a victim (e.g., if agent_01 after 20 seconds)
            if not self.victim_detected and elapsed > 20 and self.agent_id == "drone_01":
                if self.vertex_client:
                    # Live Vertex AI Integration
                    # Simulate passing camera telemetry or IR sensor data to the Vertex Endpoint
                    sensor_payload = {"instances": [{"position": self.position, "thermal_signature": "high"}]}
                    try:
                        print(f"[{self.agent_id}] Querying Vertex AI Endpoint for victim confirmation...")
                        response = self.vertex_client.predict(instances=sensor_payload["instances"])
                        
                        # Process response. A real model might return [{"confidence": 0.95, "class": "victim"}]
                        # We'll assume the endpoint confirms it if we get a successful 200 response
                        if response and response.predictions:
                            self.victim_detected = True
                            print(f"[{self.agent_id}] Vertex AI confirmed victim! Predictions: {response.predictions}")
                            self.publish_victim_detected()
                    except Exception as e:
                        print(f"[{self.agent_id}] Vertex AI prediction failed: {e}")
                else:
                    # Fallback to deterministic logic
                    self.victim_detected = True
                    self.publish_victim_detected()
                
            # Check if we are assigned any TASK_SECURE or TASK_RECOVERABLE
            tasks_to_execute = []
            with node.TASKS_LOCK:
                for task_id, task in list(node.TASKS.items()):
                    if task["state"] in [node.TASK_ASSIGNED, node.TASK_EXECUTING]:
                        if self.agent_id in task["assignees"]:
                            if self.agent_id not in task.get("results", {}):
                                tasks_to_execute.append((task_id, task['type']))
            
            for task_id, t_type in tasks_to_execute:
                print(f"[{self.agent_id}] Executing assigned task {task_id} ({t_type})")
                time.sleep(2) # simulate work
                # For TASK_SECURE, all assignees must return the EXACT same result
                result_str = "TARGET_CONFIRMED" if t_type == node.TASK_SECURE else f"SEARCH_OK"
                self.publish_task_result(task_id, result_str)
                                
            time.sleep(2)

    def _relay_behavior(self):
        BATTERY_LOW = 25
        TRANSFER_AMOUNT = 30
        TRANSFER_DISTANCE = 5

        with node.STATE_LOCK:
            peers = {pid: asdict(p) for pid, p in node.STATE.items()
                     if pid != self.agent_id and p.status == "ready"}

        # Find the lowest-battery peer that needs help
        target_id, target_pos, lowest = None, None, BATTERY_LOW
        for pid, p in peers.items():
            batt = p.get("battery") or 100
            pos = p.get("position")
            if batt <= lowest and pos is not None:
                lowest, target_id, target_pos = batt, pid, pos

        if target_id is None:
            self.position[0] += 1  # patrol slowly
            self.relay_target = None
            return

        self.relay_target = target_id
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        dist = (dx**2 + dy**2) ** 0.5
        if dist > TRANSFER_DISTANCE:
            self.position[0] += int(dx / dist) if dist else 0
            self.position[1] += int(dy / dist) if dist else 0
        else:
            msg = {
                "type": "BATTERY_TRANSFER",
                "peer_id": self.agent_id,
                "ts": node.now_ms(),
                "target_id": target_id,
                "amount": TRANSFER_AMOUNT,
                "position": self.position,
            }
            node.publish_json(self.client, node.TOPIC_SWARM, msg)
            print(f"[{self.agent_id}] BATTERY_TRANSFER -> {target_id} +{TRANSFER_AMOUNT}%")

    def start(self):
        print(f"[INFO] Connecting DroneAgent {self.agent_id} to FoxMQ at {self.host}:{self.port}")
        self.client.connect(self.host, self.port, keepalive=60)
        self.sim_thread.start()
        
        # Publish initial RECOVERABLE_TASK for the sector search
        # Wait a bit for connection
        threading.Thread(target=self.init_sector_task, daemon=True).start()
        
        self.client.loop_forever()
        
    def init_sector_task(self):
        time.sleep(5) # wait for mesh to settle
        # Create a TASK_RECOVERABLE for our own sector
        task_id = f"SEARCH_{self.sector}_{self.agent_id}"
        task = {
            "task_id": task_id,
            "type": node.TASK_RECOVERABLE,
            "requirements": {"min_agents": 1, "required_role": "any", "max_latency_ms": 5000, "redundancy": 1},
            "payload": {"sector": self.sector}
        }
        create_msg = {
            "type": "TASK_CREATE",
            "peer_id": self.agent_id,
            "ts": node.now_ms(),
            "task": task
        }
        node.publish_json(self.client, node.TOPIC_SWARM, create_msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=1883, type=int)
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--role", default="scout")
    parser.add_argument("--fail-after", type=int, default=0, help="Seconds before simulated crash")
    parser.add_argument("--protocol", type=int, default=5, help="MQTT protocol version (4 = 3.1.1, 5 = 5.0)")
    parser.add_argument("--tls", action="store_true", help="Use TLS for MQTT connection")
    parser.add_argument("--vertex-project", help="Google Cloud Project ID for Vertex AI")
    parser.add_argument("--vertex-endpoint", help="Vertex AI Endpoint ID")
    args = parser.parse_args()

    agent = DroneAgent(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        agent_id=args.agent_id,
        sector=args.sector,
        role=args.role,
        fail_after=args.fail_after,
        protocol=args.protocol,
        vertex_project=args.vertex_project,
        vertex_endpoint=args.vertex_endpoint
    )
    if args.tls:
        import ssl
        agent.client.tls_set(cert_reqs=ssl.CERT_NONE)
        agent.client.tls_insecure_set(True)
    agent.start()
