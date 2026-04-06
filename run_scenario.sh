#!/bin/bash

echo "Starting SwarmRescue-NG Scenario..."
echo "Starting local Python MQTT Broker on port 1883"

# Kill existing processes on exit
trap 'kill $(jobs -p)' EXIT

# Start Python Broker
python simple_broker.py &
sleep 2

# Start HTTP Server for UI
python3 -m http.server 8000 &

# Start HUD Server
python hud_server.py &
sleep 2

# Start 5 Drones
# Drone 01: NW, scout (finds victim after 20s)
python drone_agent.py --username agent --password secret --agent-id drone_01 --sector NW --role scout &

# Drone 02: NE, scout (fails after 30s)
python drone_agent.py --username agent --password secret --agent-id drone_02 --sector NE --role scout --fail-after 30 &

# Drone 03: SW, scout
python drone_agent.py --username agent --password secret --agent-id drone_03 --sector SW --role scout &

# Drone 04: SE, scout
python drone_agent.py --username agent --password secret --agent-id drone_04 --sector SE --role scout &

# Drone 05: CENTER, leader
python drone_agent.py --username agent --password secret --agent-id drone_05 --sector CENTER --role leader &

echo "All nodes started."
echo "Open index.html in your browser to view the HUD."
echo "Press Ctrl+C to stop all nodes."
wait
