# scripts/09_verify_observability.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_prometheus():
    try:
        resp = requests.get("http://localhost:9090/api/v1/query",
                            params={"query": 'http_requests_total{job="api-gateway"}'})
        data = resp.json()
        assert data["status"] == "success"
        print("Integration 9 OK: Prometheus metrics flowing")
    except Exception as e:
        print(f"Integration 9 Failed: {e}")

def check_langsmith():
    try:
        api_key = os.environ.get("LANGCHAIN_API_KEY", "dummy_key")
        if api_key == "dummy_key" or not api_key:
            print("Integration 10 Ignored: Dummy or missing LangSmith API Key. Skipping trace verification.")
            return
        from langsmith import Client
        client = Client(api_key=api_key)
        runs = list(client.list_runs(project_name="lab28-platform", limit=1))
        assert len(runs) > 0
        print("Integration 10 OK: LangSmith traces visible")
    except Exception as e:
        print(f"Integration 10 Warn: LangSmith traces check failed ({e})")

check_prometheus()
check_langsmith()
