import os, json
import boto3
import requests
from datetime import datetime

RAW_BUCKET = os.getenv("RAW_BUCKET", "my-youtube-bucket")
YT_API_KEY = os.getenv("YT_API_KEY")
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client("s3", region_name=REGION)

def fetch_videos(channel_id, max_results=50):
    url = ("https://www.googleapis.com/youtube/v3/search"
           f"?key={YT_API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={max_results}")
    r = requests.get(url)
    r.raise_for_status()
    return r.json().get("items", [])

def lambda_handler(event, context):
    channel = event.get("channel_id")
    items = fetch_videos(channel, max_results=50)
    key = f"raw/batch/{channel}/{datetime.utcnow().strftime('%Y/%m/%d')}/batch.json"
    s3.put_object(Bucket=RAW_BUCKET, Key=key, Body=json.dumps(items))
    return {"s3_key": key, "count": len(items)}
