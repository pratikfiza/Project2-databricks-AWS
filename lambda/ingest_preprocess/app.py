import os, json, uuid
from datetime import datetime
import boto3
import requests

KINESIS_STREAM = os.getenv("KINESIS_STREAM", "youtube-stream")
REGION = os.getenv("AWS_REGION", "us-east-1")
YT_API_KEY = os.getenv("YT_API_KEY")
DEFAULT_CHANNEL = os.getenv("YT_CHANNEL_ID")

kinesis = boto3.client("kinesis", region_name=REGION)

def normalize_youtube_item(item):
    # Flatten youtube API item to a simple dict
    snippet = item.get("snippet", {})
    video_id = (item.get("id") or {}).get("videoId") or item.get("videoId")
    return {
        "event_id": str(uuid.uuid4()),
        "video_id": video_id,
        "title": snippet.get("title"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "raw": item,
        "ingested_at": datetime.utcnow().isoformat()
    }

def send_to_kinesis(rec):
    kinesis.put_record(
        StreamName=KINESIS_STREAM,
        Data=json.dumps(rec),
        PartitionKey=rec.get("video_id") or "default"
    )

def fetch_channel_videos(api_key, channel_id, max_results=10):
    url = ("https://www.googleapis.com/youtube/v3/search"
           f"?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults={max_results}")
    r = requests.get(url)
    r.raise_for_status()
    return r.json().get("items", [])

def lambda_handler(event, context):
    # Event can be from API Gateway (body) or scheduled invocation with channel_id
    body = event.get("body")
    if body:
        try:
            body = json.loads(body)
        except:
            pass

    channel = (body or {}).get("channel_id") or DEFAULT_CHANNEL
    items = fetch_channel_videos(YT_API_KEY, channel, max_results=10)
    for item in items:
        rec = normalize_youtube_item(item)
        send_to_kinesis(rec)

    return {"statusCode": 200, "body": json.dumps({"ingested": len(items)})}

if __name__ == "__main__":
    # local quick test (requires env vars)
    print("Run lambda_handler with a test event if env vars are set.")
