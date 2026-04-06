import asyncio
import json
import threading
import argparse
import time
import websockets
import paho.mqtt.client as mqtt
import node
import copy

# We'll store the latest state here and broadcast it to all WS clients
LATEST_STATE = {}
TASKS_STATE = {}
EVENTS_LOG = []
WS_CLIENTS = set()
MAIN_LOOP = None
STATE_LOCK = threading.Lock()

def on_message(client, userdata, message):
    # Parse just like node.py but we only care about maintaining state to send to frontend
    payload = message.payload.decode("utf-8")
    
    try:
        envelope = json.loads(payload)
        data = envelope.get("payload", {})
        msg_type = data.get("type")
        
        # Append to event log for the dashboard
        event_record = {
            "ts": node.now_ms(),
            "type": msg_type,
            "peer_id": data.get("peer_id", "system"),
            "raw": data
        }
        with STATE_LOCK:
            EVENTS_LOG.append(event_record)
            if len(EVENTS_LOG) > 100:
                EVENTS_LOG.pop(0)

            # Update latest state if heartbeat
            if msg_type == "HEARTBEAT":
                peer_id = data.get("peer_id")
                # Get existing drone state or create a new one
                drone_state = LATEST_STATE.get(peer_id, {})
                drone_state.update({
                    "peer_id": peer_id,
                    "position": data.get("position", drone_state.get("position")),
                    "sector": data.get("sector", drone_state.get("sector")),
                    "battery": data.get("battery", drone_state.get("battery")),
                    "sector_progress": data.get("sector_progress", drone_state.get("sector_progress")),
                    "role": data.get("role", drone_state.get("role")),
                    "status": data.get("status", drone_state.get("status", "ready")),
                    "last_seen_ms": node.to_millis(data.get("ts", node.now_ms()))
                })
                LATEST_STATE[peer_id] = drone_state
                
            elif msg_type == "TASK_CREATE":
                task = data.get("task", {})
                task_id = task.get("task_id")
                if task_id:
                    TASKS_STATE[task_id] = task
                    TASKS_STATE[task_id]["state"] = "CREATED"
                    TASKS_STATE[task_id]["assignees"] = []
                    
            elif msg_type == "TASK_RESULT":
                task_id = data.get("task_id")
                if task_id in TASKS_STATE:
                    TASKS_STATE[task_id]["state"] = "COMPLETED"
                
    except Exception as e:
        print(f"[HUD] Error parsing msg: {e}")

    # Broadcast update to all websocket clients using the main loop
    if MAIN_LOOP and WS_CLIENTS:
        MAIN_LOOP.call_soon_threadsafe(trigger_broadcast)

def trigger_broadcast():
    if MAIN_LOOP:
        asyncio.create_task(broadcast_state())

async def broadcast_state():
    if not WS_CLIENTS:
        return
        
    with STATE_LOCK:
        drones_copy = copy.deepcopy(LATEST_STATE)
        tasks_copy = copy.deepcopy(TASKS_STATE)
        events_copy = copy.deepcopy(EVENTS_LOG[-10:])
        
    msg = json.dumps({
        "type": "STATE_UPDATE",
        "drones": drones_copy,
        "tasks": tasks_copy,
        "events": events_copy
    })
    
    websockets_to_remove = set()
    for ws in list(WS_CLIENTS):
        try:
            await ws.send(msg)
        except websockets.exceptions.ConnectionClosed:
            websockets_to_remove.add(ws)
            
    WS_CLIENTS.difference_update(websockets_to_remove)

async def ws_handler(websocket):
    WS_CLIENTS.add(websocket)
    try:
        # Send initial state
        with STATE_LOCK:
            drones_copy = copy.deepcopy(LATEST_STATE)
            tasks_copy = copy.deepcopy(TASKS_STATE)
            events_copy = copy.deepcopy(EVENTS_LOG[-10:])
        await websocket.send(json.dumps({
            "type": "STATE_UPDATE",
            "drones": drones_copy,
            "tasks": tasks_copy,
            "events": events_copy
        }))
        async for _ in websocket:
            pass # Keep connection open
    finally:
        WS_CLIENTS.remove(websocket)

def start_mqtt(host, port, username, password):
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION1,
        client_id="hud_server",
        protocol=mqtt.MQTTv311
    )
    client.username_pw_set(username, password)
    
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"[HUD] Connected to MQTT broker at {host}:{port}")
            client.subscribe(node.TOPIC_SWARM, qos=1)
            client.subscribe(node.TOPIC_HELLO, qos=1)
        else:
            print(f"[HUD] Failed to connect, rc={rc}")

    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"[HUD] Connecting to {host}:{port}...")
    try:
        client.connect(host, port, keepalive=60)
        client.loop_forever()
    except Exception as e:
        print(f"[HUD] MQTT error: {e}")

async def main():
    global MAIN_LOOP
    MAIN_LOOP = asyncio.get_running_loop()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=1883, type=int)
    parser.add_argument("--username", default="hud")
    parser.add_argument("--password", default="secret")
    parser.add_argument("--ws-port", default=8081, type=int)
    args = parser.parse_args()

    # Start MQTT in background thread
    threading.Thread(target=start_mqtt, args=(args.host, args.port, args.username, args.password), daemon=True).start()

    # Start WebSocket server
    print(f"[HUD] Starting WebSocket server on ws://0.0.0.0:{args.ws_port}")
    async with websockets.serve(ws_handler, "0.0.0.0", args.ws_port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
