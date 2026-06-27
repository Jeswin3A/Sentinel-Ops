import requests
import time 
import sys

API_URL = "http://127.0.0.1:8000/logs"

class AgentState:
    """Tracks the state schema of our LangGraph workflow simulation."""
    def __init__(self):
        self.current_node = "START"
        self.active_incident = None
        self.mitigation_plan = None
        self.status = "IDLE"

def run_agent_workflow():
    state = AgentState()
    print("\033[96m🤖 Sentinel-Ops Agent Supervisor initialized...\033[0m")
    print("Connecting to live state pipeline at http://127.0.0.1:8000/logs ...")
    
    while True:
        try:
            # Step 1: START Node (Ingest logs from server state)
            state.current_node = "INGEST_NODE"
            response = requests.get(API_URL, timeout=3)
            logs = response.json().get("logs", [])
            
            if not logs:
                print("💤 No active incidents in database. Standing by...")
                time.sleep(3)
                continue
                
            # Grab the latest ingested log (which now includes populated RAG fields from app.py)
            latest_log = logs[-1]
            state.active_incident = latest_log
            
            # Step 2: TRIAGE Node (Evaluate Risk State)
            state.current_node = "TRIAGE_NODE"
            severity = latest_log.get("severity", "INFO")
            print(f"\n[Node: TRIAGE_NODE] Assessing severity for incident from {latest_log.get('service_name', 'Unknown')}...")
            
            # Step 3: Routing Decisions (Simulating LangGraph Conditional Edges)
            if severity == "INFO":
                state.current_node = "RESOLVE_DIRECTLY"
                print(f"🟢 [Action] Route directly: Log categorized as standard telemetry. No intervention required.")
                
            elif severity == "WARNING":
                state.current_node = "AUTO_MITIGATION"
                print(f"🟡 [Action] Route to Auto-Mitigation: Triggering low-risk playbook routine...")
                print(f"   Executing: 'Verify subsystem heartbeat configurations.'")
                
            elif severity == "CRITICAL":
                state.current_node = "HUMAN_APPROVAL_GUARD"
                print(f"🔴 [Action] Route to Guardrail: CRITICAL incident detected!")
                print(f"   Message: {latest_log.get('message')}")
                print(f"   ⚠️ WARNING: Automated script drafted to execute infrastructure mitigation.")
                
                # Fetch target resolution playbook (RAG visualization)
                print("   🔄 Fetching target resolution playbook...")
                time.sleep(1)
                
                # Retrieve the actual RAG metadata resolved by our FastAPI server
                resolved_topic = latest_log.get("playbook_topic", "Triage Needed")
                
                # --- HUMAN-IN-THE-LOOP (HITL) GUARDRAIL ---
                print("\n=================== ✋ HUMAN-IN-THE-LOOP GUARDRAIL ===================")
                print(f" Target Resource : {latest_log.get('infrastructure_id', 'Unknown Resource')}")
                print(f" Action Drafted   : Apply Cloud Security Network Filter/Configuration block.")
                print(f" Playbook Match  : {resolved_topic}")
                print("=======================================================================")
                
                # Dynamic terminal prompt for your live presentation demo
                user_input = input("\033[93m👉 Approve automated mitigation execution? (Y/N/Skip): \033[0m").strip().upper()
                
                if user_input == "Y":
                    state.current_node = "EXECUTION_NODE"
                    print("\n🚀 [Node: EXECUTION_NODE] Admin approved! Deploying container configuration fix...")
                    print("   [SUCCESS] Traffic anomaly isolated. Gateway status restored to nominal.")
                elif user_input == "N":
                    state.current_node = "ESCALATE_TO_SEC_OPS"
                    print("\n❌ [Action] Admin rejected. Aborting script execution. Escalating to Security Operations.")
                else:
                    print("\n⏭️ Mitigation deferred. Moving incident to holding queue.")
                    
            print("-" * 65)
            # Sleep to allow logs to generate and avoid overloading
            time.sleep(4)
            
        except requests.exceptions.ConnectionError:
            print("❌ Unable to connect to http://127.0.0.1:8000. Is the API Server running?")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n👋 Supervisor stopped.")
            sys.exit(0)

if __name__ == "__main__":
    run_agent_workflow()