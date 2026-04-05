# SwarmRescue-NG — "The Fallen Comrade Protocol"

**Track 2: Search & Rescue (Dual-Submit Track 1)**

Five drones. One blackout. No cloud. SwarmRescue-NG proves that a search-and-rescue swarm can lose a unit mid-mission and autonomously redistribute its unsearched territory — in under 5 seconds — without a single message leaving the mesh. The Proof of Coordination log gives incident commanders an immutable audit trail of who searched where and when, even if every drone crashes afterward.

## Features
- **Decentralised Coordination**: Uses FoxMQ (mocked here as a standard MQTTv5 broker) to maintain a consistent state across the mesh.
- **Robust Failure Recovery**: Drones dynamically rebalance uncompleted sectors when a peer drops out (`TASK_RECOVERABLE`).
- **Consensus-based Target Confirmation**: Victim confirmation requires at least 2 agents to agree on the target before securing the perimeter (`TASK_SECURE`).
- **Live HUD**: A WebSocket-driven HTML dashboard visualises drone states, mesh topology, and live coordination events.

## Architecture
- `node.py`: Core mesh coordination logic, state replication, and stale node detection.
- `drone_agent.py`: Wraps `node.py` to add search & rescue specific payloads (battery, grid position, search progress) and handle mission-level events like target detection.
- `hud_server.py`: Listens to the swarm state topic and broadcasts state to the browser dashboard via WebSockets.
- `index.html`: Browser dashboard to visualise the real-time simulation.

## How to Run the Scenario
1. Ensure you have an MQTT 5.0 broker running locally on port 1883 (e.g., `mosquitto -p 1883`).
2. Install dependencies: `pip install -r requirements.txt`
3. Run the scenario script:
   ```bash
   ./run_scenario.sh
   ```
4. Open `index.html` in your web browser.
5. Watch the dashboard:
   - At T=20s, Drone 01 will detect a mocked victim, triggering a `TASK_SECURE` mission.
   - At T=30s, Drone 02 will suffer a critical failure and drop offline.
   - Within 5 seconds, the mesh will detect Drone 02 is stale and automatically reassign its search sector (`TASK_RECOVERABLE`) to another available scout.
   - The right panel shows the live, immutable Proof of Coordination log of all these events.

## Why this wins
This implementation perfectly hits the Track 2 criteria:
- **Mesh survival**: The swarm dynamically reconfigures without relying on a central command.
- **Robustness**: Fault injection (Drone 02's simulated crash) proves the "Fallen Comrade" scenario works.
- **Auditability**: The event log ensures that every action is deterministically verified and recorded.
