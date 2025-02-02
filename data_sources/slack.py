from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

def list_channels():
    try:
        response = client.conversations_list()
        channels = response['channels']
        return channels
    except SlackApiError as e:
        print(f"Error listing channels: {e.response['error']}")

def filter_channels(channels, prefix):
    return [channel for channel in channels if channel['name'].startswith(prefix)]

def pull_messages(channel_id):
    try:
        response = client.conversations_history(channel=channel_id)
        messages = response['messages']
        return [msg for msg in messages if 'reply_count' in msg and msg['reply_count'] > 0]
    except SlackApiError as e:
        print(f"Error pulling messages: {e.response['error']}")
