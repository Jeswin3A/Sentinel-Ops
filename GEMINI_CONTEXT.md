Sentinel-Ops: Executive Project Anchor

Domain: LLMOps / SRE Automation / Multi-Agent Systems
Core Objective: Build a self-healing, cloud-native operations platform where a stateful agent fleet (LangGraph) triages system alerts, queries standard troubleshooting manuals (RAG over Vector DB), and executes human-approved mitigations with complete cost, trace, and evaluation guardrails.

📐 System Architecture & Flow

Ingestion Layer (app.py): FastAPI gateway receiving real-time JSON log telemetry (INFO, WARNING, CRITICAL).

Knowledge Layer (vector_db.py / Embedded): Simulated vector store matching incoming incident text to structured SRE Playbooks using keyword similarity.

Orchestration Layer (agent_supervisor.py): Stateful multi-agent supervisor simulating a LangGraph workflow. Includes:

INGEST_NODE: Pulls active anomalies.

TRIAGE_NODE: Evaluates event severity.

HUMAN_APPROVAL_GUARD: Pauses state transition on CRITICAL alerts to demand manual CLI/UI confirmation before executing mock code fixes.

LLMOps Observability (/dashboard): Real-time HTML control panel serving live metrics, token cost audits, chain trace latencies, and simulation statistics.

🛠️ Complete Tech Stack

Languages/Frameworks: Python, FastAPI, Uvicorn, Requests

UI & Telemetry: Tailwind CSS, Lucide Icons, Vanilla JS Polling

AI Core: LangChain concepts, LangGraph state machine flow (simulated locally)