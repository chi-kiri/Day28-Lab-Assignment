import requests

grafana_url = "http://localhost:3000"
auth = ("admin", "admin")

# Create Prometheus data source if it doesn't exist
print("Creating Prometheus data source...")
ds_payload = {
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "access": "proxy",
    "isDefault": True
}
requests.post(f"{grafana_url}/api/datasources", json=ds_payload, auth=auth)

# Dashboard JSON payload
dashboard_payload = {
    "dashboard": {
        "id": None,
        "uid": "api_gateway_dashboard",
        "title": "API Gateway Metrics",
        "tags": [ "templated" ],
        "timezone": "browser",
        "schemaVersion": 16,
        "version": 0,
        "refresh": "5s",
        "panels": [
            {
                "type": "timeseries",
                "title": "Total Requests",
                "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
                "targets": [
                    { "expr": "sum(rate(http_requests_total{job=\"api-gateway\"}[5m])) by (status)", "refId": "A" }
                ]
            },
            {
                "type": "gauge",
                "title": "API Gateway Uptime",
                "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 },
                "targets": [
                    { "expr": "up{job=\"api-gateway\"}", "refId": "A" }
                ],
                "options": {
                    "reduceOptions": { "values": False, "calcs": [ "lastNotNull" ], "fields": "" },
                    "orientation": "auto",
                    "showThresholdLabels": False,
                    "showThresholdMarkers": True
                }
            }
        ]
    },
    "overwrite": True
}

print("Creating Dashboard...")
response = requests.post(f"{grafana_url}/api/dashboards/db", json=dashboard_payload, auth=auth)
print(response.json())
print("Dashboard created! Refresh your browser.")
