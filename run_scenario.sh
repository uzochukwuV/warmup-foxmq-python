#!/bin/bash

echo "Starting SwarmRescue-NG Scenario..."

# Configuration for Live Integrations
# 1. FoxMQ Live Broker
MQTT_HOST=${FOXMQQ_HOST:-"127.0.0.1"}
MQTT_PORT=${FOXMQQ_PORT:-1883}
MQTT_USER=${FOXMQQ_USER:-"producer"}
MQTT_PASS=${FOXMQQ_PASS:-"password"}
MQTT_PROTOCOL=${FOXMQQ_PROTOCOL:-5} # 4=MQTTv311, 5=MQTTv5
MQTT_TLS_FLAG=""
if [ "$FOXMQQ_TLS" = "true" ]; then
    MQTT_TLS_FLAG="--tls"
fi

# 2. Google Cloud Vertex AI Integration
VERTEX_ARGS=""
if [ -n "$VERTEX_PROJECT" ] && [ -n "$VERTEX_ENDPOINT" ]; then
    echo "Live Vertex AI Integration Enabled (Project: $VERTEX_PROJECT, Endpoint: $VERTEX_ENDPOINT)"
    VERTEX_ARGS="--vertex-project $VERTEX_PROJECT --vertex-endpoint $VERTEX_ENDPOINT"
else
    echo "Vertex AI Integration Disabled (Running local simulation logic)"
fi

# Check for FoxMQ binary locally
if [ "$MQTT_HOST" = "127.0.0.1" ]; then
    if [ ! -f "./foxmq" ]; then
        echo "Error: ./foxmq binary not found!"
        echo "Please download FoxMQ and place it in this directory."
        echo "Example:"
        echo "  curl -LO https://github.com/tashigit/foxmq/releases/download/v0.3.1/foxmq_0.3.1_linux-amd64.zip"
        echo "  unzip foxmq_0.3.1_linux-amd64.zip && chmod +x foxmq"
        echo "  ./foxmq address-book from-range 127.0.0.1 19793 19793"
        echo "  ./foxmq run --secret-key-file=foxmq.d/key_0.pem &"
        exit 1
    fi
    echo "Using local FoxMQ broker."
fi

# Kill existing processes on exit
trap 'kill $(jobs -p)' EXIT

# Start HTTP Server for UI
python3 -m http.server 8000 &

# Start HUD Server
python hud_server.py --host $MQTT_HOST --port $MQTT_PORT --username hud --password secret --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &
sleep 2

# Start 5 Drones
# Drone 01: NW, scout (finds victim after 20s, uses Vertex AI if configured)
python drone_agent.py --host $MQTT_HOST --port $MQTT_PORT --username $MQTT_USER --password $MQTT_PASS --agent-id drone_01 --sector NW --role scout $VERTEX_ARGS --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &

# Drone 02: NE, scout (fails after 30s)
python drone_agent.py --host $MQTT_HOST --port $MQTT_PORT --username $MQTT_USER --password $MQTT_PASS --agent-id drone_02 --sector NE --role scout --fail-after 30 --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &

# Drone 03: SW, scout
python drone_agent.py --host $MQTT_HOST --port $MQTT_PORT --username $MQTT_USER --password $MQTT_PASS --agent-id drone_03 --sector SW --role scout --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &

# Drone 04: SE, scout
python drone_agent.py --host $MQTT_HOST --port $MQTT_PORT --username $MQTT_USER --password $MQTT_PASS --agent-id drone_04 --sector SE --role scout --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &

# Drone 05: CENTER, leader
python drone_agent.py --host $MQTT_HOST --port $MQTT_PORT --username $MQTT_USER --password $MQTT_PASS --agent-id drone_05 --sector CENTER --role leader --protocol $MQTT_PROTOCOL $MQTT_TLS_FLAG &

echo "All nodes started."
echo "Open http://localhost:8000/index.html in your browser to view the HUD."
echo "Press Ctrl+C to stop all nodes."
wait
