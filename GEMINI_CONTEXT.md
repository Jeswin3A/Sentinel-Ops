# Sentinel-Ops: Executive Project Anchor Context

## 🎯 Strategic Objective
To build an automated, cloud-native Site Reliability Engineering (SRE) observability gateway and multi-agent mitigation fleet. The system intercepts real-time cloud errors, fetches exact troubleshooting playbooks via vector similarity searching (RAG), maps mitigation paths through a stateful workflow, and provides strict human gatekeeping barriers alongside programmatic LLMOps telemetry auditing.

## 🏗️ Technical Core Stack
- **Backend Gateway:** Python 3.11+, FastAPI, Uvicorn, Pydantic (v2)
- **Stateful AI Core:** LangChain, LangGraph State Engine
- **Vector Storage:** Qdrant DB (Using Semantic Dense Vector Embeddings)
- **LLMOps Governance:** Langfuse Observability Framework & GitHub Actions CI/CD
- **UI Panel:** HTML5, Tailwind CSS, JavaScript Polling, Lucide Telemetry Icons

## 🔐 Strict Architectural Operational Invariants
1. Nodes within the LangGraph structure must strictly return a state update dictionary rather than trying to perform in-place mutation of the shared state schema.
2. Under no circumstance can a system remediation script or mutating configuration command execute autonomously for a `CRITICAL` alert without passing a human verification checkpoint (`interrupt_before`).