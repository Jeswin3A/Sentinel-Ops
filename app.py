from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json

# Import the Mock Vector Database class we verified in the Canvas
from vector_db import MockVectorDB

app = FastAPI(title="Sentinel-Ops Gateway", description="Mock Log Ingestion Service with Integrated RAG")

# Initialize our simulated vector database
vector_store = MockVectorDB()
received_logs = []

class SystemLog(BaseModel):
    timestamp: str
    service_name: str
    severity: str  # INFO, WARNING, CRITICAL
    message: str
    infrastructure_id: str

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "service": "Sentinel-Ops Cloud Gateway (RAG Active)",
        "total_ingested_logs": len(received_logs)
    }

@app.post("/ingest")
def ingest_log(log: SystemLog):
    log_data = log.dict()
    received_logs.append(log_data)
    
    # 1. Terminal Visual Styling
    color = "\033[94m" # Blue for INFO
    if log.severity == "WARNING":
        color = "\033[93m" # Yellow
    elif log.severity == "CRITICAL":
        color = "\033[91m" # Red
    reset = "\033[0m"
    
    print(f"\n⚡ {color}[INGESTED - {log.severity}]{reset} From: {log.service_name} | IP: {log.infrastructure_id}")
    print(f"   Message: {log.message}")
    
    # 2. Automated RAG Pipeline: Query the Vector DB using the error message
    print(f"   🔍 Querying Sentinel-Ops Knowledge Store...")
    playbook = vector_store.search(log.message)
    
    if playbook:
        print(f"   ✅ {color}MATCH FOUND:{reset} Playbook Topic: '{playbook['topic']}'")
        # Format the solution steps cleanly for the console presentation
        indented_solution = "\n".join(f"      {line}" for line in playbook["solution"].split("\n"))
        print(f"   📋 Recommended Mitigation Steps:\n{indented_solution}")
    else:
        print("   ❌ No direct matching mitigation playbook found.")
        
    print("-" * 65)
    
    return {
        "status": "success", 
        "mitigation_found": playbook is not None,
        "playbook_topic": playbook["topic"] if playbook else None
    }

@app.get("/logs")
def get_all_logs():
    return {"logs": received_logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
#Open your browser and navigate to: http://127.0.0.1:8000/

