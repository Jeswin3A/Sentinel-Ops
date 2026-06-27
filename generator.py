#where we will build a script to stream simulated cloud infrastructure failures directly into your running gateway. This will give you a live, highly visual demo to show the panel tomorrow.

#We will generate a new script file, generator.py. This script will generate realistic SRE anomalies (such as high CPU loads, database connection timeouts, and security breaches) and send them as payloads to your FastAPI server.

import requests
import time
import random
from datetime import datetime

# URL of the running FastAPI server from your Canvas
INGEST_URL = "http://127.0.0.1:8000/ingest"

# Highly realistic simulation payloads for your SRE presentation
INCIDENTS = [
    {
        "service_name": "Auth-Service",
        "severity": "WARNING",
        "message": "Latency spike detected on /login endpoint: 1540ms",
        "infrastructure_id": "pod-104.22.81.9"
    },
    {
        "service_name": "Database-Cluster",
        "severity": "CRITICAL",
        "message": "Connection pool exhausted. Failed to allocate socket to client.",
        "infrastructure_id": "db-primary-rds-01"
    },
    {
        "service_name": "Payment-Gateway",
        "severity": "INFO",
        "message": "Webhook received from Stripe. Transaction TXN_88192 completed successfully.",
        "infrastructure_id": "gateway-node-abc"
    },
    {
        "service_name": "Nginx-Ingress",
        "severity": "CRITICAL",
        "message": "DDOS alert: Request rate from IP 198.51.100.42 exceeded rate limits (5000 req/sec)",
        "infrastructure_id": "ingress-edge-02"
    },
    {
        "service_name": "Storage-Service",
        "severity": "WARNING",
        "message": "S3 bucket space reaching capacity limits. Current utilization at 89.4%.",
        "infrastructure_id": "bucket-assets-prod"
    }
]

def stream_logs():
    print("🚀 Starting Sentinel-Ops Real-time Log Stream Generator...")
    print("Press Ctrl+C to stop streaming.\n")
    
    while True:
        # Pick a random system incident
        incident = random.choice(INCIDENTS)
        
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "service_name": incident["service_name"],
            "severity": incident["severity"],
            "message": incident["message"],
            "infrastructure_id": incident["infrastructure_id"]
        }
        
        try:
            # Send the simulated system log to our FastAPI gateway
            response = requests.post(INGEST_URL, json=payload, timeout=3)
            if response.status_code == 200:
                print(f"📡 Sent [{payload['severity']}] log from {payload['service_name']} -> Server Response: {response.json()['status']}")
            else:
                print(f"❌ Failed to stream log. Server returned status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️ Connection Error! Is your app.py server running on http://127.0.0.1:8000?")
            
        # Pause before sending the next system anomaly
        time.sleep(random.uniform(2.0, 4.0))

if __name__ == "__main__":
    stream_logs()