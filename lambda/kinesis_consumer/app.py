import os, json
import boto3
from base64 import b64decode
from datetime import datetime

RAW_BUCKET = os.getenv("RAW_BUCKET", "my-youtube-bucket")
DDB_TABLE = os.getenv("METADATA_TABLE", "youtube-metadata")
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client("s3", region_name=REGION)
ddb = boto3.resource("dynamodb", region_name=REGION).Table(DDB_TABLE)

def s3_key(event_id):
    datepart = datetime.utcnow().strftime("%Y/%m/%d")
    return f"raw/{datepart}/{event_id}.json"

def lambda_handler(event, context):
    records = event.get("Records", [])
    processed = 0
    for rec in records:
        payload = b64decode(rec['kinesis']['data'])
        data = json.loads(payload)
        event_id = data.get("event_id")
        key = s3_key(event_id)
        s3.put_object(Bucket=RAW_BUCKET, Key=key, Body=json.dumps(data))
        # store metadata in DynamoDB
        try:
            ddb.put_item(Item={
                "event_id": event_id,
                "video_id": data.get("video_id"),
                "s3_key": key,
                "ingested_at": data.get("ingested_at")
            })
        except Exception as e:
            print("ddb put_item error", e)
        processed += 1
    return {"processed": processed}
