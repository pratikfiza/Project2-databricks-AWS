import os,json, requests

DATABRICKS_INSTANCE = os.getenv("DATABRICKS_INSTANCE")  # https://<region>.azuredatabricks.net or AWS URL
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
JOB_ID = os.getenv("DATABRICKS_JOB_ID")

def lambda_handler(event, context):
    url = f"{DATABRICKS_INSTANCE}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    payload = {"job_id": int(JOB_ID)}
    # Optionally pass notebook params
    if event.get("job_params"):
        payload["notebook_params"] = event["job_params"]
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return {"job_run": data}
