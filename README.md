# SwarmRescue-NG — "The Fallen Comrade Protocol"

**Track 2: Search & Rescue (Dual-Submit Track 1)**

Ten drones. One blackout. One relay. No cloud. SwarmRescue-NG proves that a search-and-rescue swarm can lose a unit mid-mission, autonomously redistribute its unsearched territory in under 5 seconds, and keep every remaining drone airborne through peer-to-peer battery relay — without a single message leaving the mesh. The Proof of Coordination log gives incident commanders an immutable audit trail of who searched where and when, even if every drone crashes afterward.

## Live Integrations

This submission includes full live integrations for the Vertex Swarm Challenge:

- **FoxMQ Integration**: The swarm leverages FoxMQ's Byzantine fault-tolerant MQTT 5.0 broker for decentralized coordination. It natively handles `TASK_RECOVERABLE`, `TASK_SECURE`, and `BATTERY_TRANSFER` messaging across the mesh, maintaining a consensus-ordered state.
- **Google Cloud Vertex AI**: We use Vertex AI for target intelligence. Instead of relying purely on deterministic rules, `drone_01` acts as a scout that streams sensor data to a deployed Vertex AI Endpoint. Only when the Vertex AI model returns a positive classification does the swarm initiate the `TASK_SECURE` target confirmation consensus.

## Architecture
- `node.py`: Core mesh coordination logic, state replication, stale node detection, and proof-of-coordination audit log. Connects natively to FoxMQ.
- `drone_agent.py`: Wraps `node.py` to add search & rescue specific payloads (battery, grid position, search progress) and handle mission-level events. Connects to Google Cloud Vertex AI using `google-cloud-aiplatform` for intelligent target detection. Also implements the relay drone behavior for autonomous battery transfer.
- `hud_server.py`: Listens to the swarm state topic and broadcasts state to the browser dashboard via WebSockets.
- `index.html`: Browser dashboard to visualise the real-time simulation, including relay drone tracking and battery transfer events.

## Drone Roles

| Role | Count | Behaviour |
|------|-------|-----------|
| `scout` | 8 | Searches assigned sector, reports victim detection, executes assigned tasks |
| `leader` | 1 | Elected deterministically (lexicographic); initiates `TASK_SECURE` on victim confirmation |
| `relay` | 1 (`drone_10`) | Patrols the mesh; autonomously intercepts any drone below 25% battery and transfers 30% charge via `BATTERY_TRANSFER` consensus message |

## Battery Relay Protocol

`drone_10` continuously scans the shared FoxMQ consensus state for the lowest-battery peer. When it finds one at or below 25%:

1. It moves toward that drone's last known position on the tactical grid.
2. On arrival (within transfer distance), it publishes a signed `BATTERY_TRANSFER` message to the swarm topic.
3. The target drone receives the message and adds the charge to its battery — persisted across simulation ticks.
4. The event is recorded in the Proof of Coordination log and shown in the HUD with an amber highlight.

Drones with depleted batteries stop moving. The relay ensures scouts stay operational without leaving their sectors.

## How to Run the Scenario & Record the Demo

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and Run FoxMQ**:

   **On Windows (Git Bash):**
   ```bash
   # Download the Windows binary
   curl -LO https://github.com/tashigit/foxmq/releases/download/v0.3.1/foxmq_0.3.1_windows-amd64.zip
   powershell -NoProfile -NonInteractive -Command "Expand-Archive -LiteralPath 'foxmq_0.3.1_windows-amd64.zip' -DestinationPath '.' -Force"

   # Initialize address book (skip if foxmq.d/ already exists)
   foxmq.exe address-book from-range 127.0.0.1 19793 19793

   # Start the broker
   start /B foxmq.exe run --secret-key-file=foxmq.d/key_0.pem
   ```

   **On Linux/macOS:**
   ```bash
   ./install_foxmq.sh
   ./foxmq run --secret-key-file=foxmq.d/key_0.pem &
   ```

   Users (`producer` / `password` and `hud` / `secret`) are pre-configured in `foxmq.d/users.toml`.

3. **Configure Live Integrations (Optional for Vertex AI)**:
   If you have a live Vertex AI Endpoint, export the following environment variables. If omitted, the script falls back to local simulation logic.
   ```bash
   # FoxMQ Live Credentials (if running remotely)
   # export FOXMQQ_HOST="<foxmq-broker-url>"
   # export FOXMQQ_PORT=1883
   # export FOXMQQ_USER="producer"
   # export FOXMQQ_PASS="password"
   # export FOXMQQ_PROTOCOL=5
   # export FOXMQQ_TLS="true"

   # Vertex AI Live Credentials
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   export VERTEX_PROJECT="<your-gcp-project-id>"
   export VERTEX_ENDPOINT="<your-vertex-endpoint-id>"
   ```

4. **Run the scenario**:
   ```bash
   ./run_scenario_10.sh
   ```

5. **Demo Walkthrough (For Video Recording)**:
   - **Step 1**: Start your screen recorder. Show the terminal starting up all 10 nodes and establishing connections to FoxMQ.
   - **Step 2**: Open `http://localhost:8000/index.html` in your browser. Note the amber dot — that is `drone_10`, the relay drone, patrolling the grid.
   - **Step 3**: At T=20s, point out `drone_01` in the terminal logs as it queries the Vertex AI Endpoint. Once Vertex AI confirms the target, the UI updates with a red `VICTIM_DETECTED` event and the mesh locks in a `TASK_SECURE` perimeter.
   - **Step 4**: At T=30s, `drone_02` suffers a critical failure and drops offline. Show the UI as its status dot turns red.
   - **Step 5**: Within 5 seconds, the mesh detects `drone_02` is stale and the Proof of Coordination log shows its `TASK_RECOVERABLE` sector search automatically reassigned to another available scout.
   - **Step 6**: As scouts deplete their batteries, watch `drone_10` (amber) move across sectors toward the lowest-battery drone. When it arrives, an amber `BATTERY_TRANSFER` event appears in the log and the target drone's battery climbs back up in the status panel.
   - **Step 7**: Conclude by pointing out that every action — victim detection, task assignment, fault recovery, and battery relay — happened entirely through FoxMQ consensus with no central command.

## Why this wins
- **Live Intelligence**: Vertex AI is actively queried for mission-critical target confirmation.
- **Mesh survival**: The swarm dynamically reconfigures after node failure without any central command.
- **Energy resilience**: The relay drone autonomously extends mission endurance through peer-to-peer battery transfer — a capability unique to this submission.
- **Robustness**: Fault injection (`drone_02`'s simulated crash) proves the "Fallen Comrade" scenario works at scale with 10 nodes.
- **Auditability**: Every state transition, task assignment, and battery transfer is recorded in the append-only Proof of Coordination log, signed with HMAC and consensus-ordered by FoxMQ.
