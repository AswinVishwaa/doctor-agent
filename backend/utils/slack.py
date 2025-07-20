import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_notification(message: str):
    if not SLACK_WEBHOOK_URL:
        print("⚠️ Slack webhook URL not set.")
        return

    payload = {"text": message}
    try:
        res = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if res.status_code != 200:
            print("❌ Slack error:", res.text)
    except Exception as e:
        print("❌ Slack exception:", str(e))
