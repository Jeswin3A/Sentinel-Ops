import re

# Simulated Vector Database Document Store
# In production, these text snippets would be embedded as vectors in Qdrant
PLAYBOOKS = [
    {
        "id": "playbook-01",
        "service": "Database-Cluster",
        "topic": "Connection Pool Exhaustion",
        "tags": ["database", "connections", "exhausted", "socket", "rds"],
        "solution": (
            "1. Access the primary RDS console.\n"
            "2. Execute 'SHOW PROCESSLIST;' to identify hanging client queries.\n"
            "3. Terminate inactive sleep connections using: CALL mysql.rds_kill(thread_id);\n"
            "4. Temporarily scale max_connections from 150 to 300 via Parameter Groups."
        )
    },
    {
        "id": "playbook-02",
        "service": "Auth-Service",
        "topic": "Latency Spikes / Timeout",
        "tags": ["latency", "spike", "login", "timeout", "slow"],
        "solution": (
            "1. Check Auth redis-cache latency metrics.\n"
            "2. If Redis CPU is >90%, execute a hot-failover to the secondary replica.\n"
            "3. Enable rate limiting on the /login endpoint to throttle burst traffic."
        )
    },
    {
        "id": "playbook-03",
        "service": "Nginx-Ingress",
        "topic": "DDOS & Rate Limiting Alerts",
        "tags": ["ddos", "ingress", "rate limit", "requests", "ip"],
        "solution": (
            "1. Extract the offending IP address from the log telemetry.\n"
            "2. Apply a temporary Cloudflare WAF block or iptables rule to drop all traffic from the IP.\n"
            "3. Enable Cloudflare 'Under Attack Mode' if traffic spikes persist across multiple edge nodes."
        )
    },
    {
        "id": "playbook-04",
        "service": "Storage-Service",
        "topic": "S3 Capacity Warnings",
        "tags": ["storage", "s3", "capacity", "bucket", "utilization"],
        "solution": (
            "1. Run lifecycle rules to transition files older than 30 days to S3 Glacier.\n"
            "2. Check for incomplete multipart uploads and purge them using AWS CLI: 'aws s3api abort-multipart-upload'.\n"
            "3. Temporarily increase the bucket quota limit if business requirements demand active files."
        )
    }
]

class MockVectorDB:
    def __init__(self):
        self.documents = PLAYBOOKS

    def search(self, query_text: str):
        """
        Simulates a Vector Cosine-Similarity Search.
        Extracts key phrases from the error log and matches them against database tags.
        """
        query_words = set(re.findall(r'\w+', query_text.lower()))
        best_match = None
        highest_score = 0
        
        for doc in self.documents:
            # Score matches based on tag intersection
            matches = query_words.intersection(set(doc["tags"]))
            score = len(matches)
            
            # Additional contextual matching on service name
            if doc["service"].lower() in query_text.lower():
                score += 2
                
            if score > highest_score:
                highest_score = score
                best_match = doc
                
        return best_match if highest_score > 0 else None

# Local verification test
if __name__ == "__main__":
    db = MockVectorDB()
    test_query = "Help! Database-Cluster reports connection pool exhausted!"
    print(f"🔍 Querying Mock Vector Store: '{test_query}'\n")
    
    result = db.search(test_query)
    if result:
        print(f"✅ Match Found! [ID: {result['id']}] - Topic: {result['topic']}")
        print(f"📋 Solution Steps:\n{result['solution']}")
    else:
        print("❌ No matching playbook found in Vector DB.")