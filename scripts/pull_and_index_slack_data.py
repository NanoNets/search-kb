from data_sources.slack import list_channels, pull_messages
from embeddings.embedder import Embedder
from indexing.indexer import Indexer
from utils.db import Database
from dotenv import load_dotenv
from config import Config
import os
from datetime import datetime

load_dotenv()

def main():
    # Initialize services
    db = Database()
    indexer = Indexer(db)
    embedder = Embedder()

    # List Slack channels
    all_channels = list_channels()

    # Load channel filtering criteria from .env
    channel_prefix = os.getenv('SLACK_CHANNEL_PREFIX')
    channel_include = os.getenv('SLACK_CHANNEL_INCLUDE').split(',')
    channel_exclude = os.getenv('SLACK_CHANNEL_EXCLUDE').split(',')

    # Filter channels based on criteria
    selected_channels = [ch for ch in all_channels if ch['name'].startswith(channel_prefix)]
    selected_channels.extend([ch for ch in all_channels if ch['name'] in channel_include])
    selected_channels = [ch for ch in selected_channels if ch['name'] not in channel_exclude]

    # Load message filtering criteria from config
    start_time = Config.START_TIME
    include_threads = Config.INCLUDE_THREADS
    include_bots = Config.INCLUDE_BOTS

    for channel in selected_channels:
        # Pull messages from the channel
        messages = pull_messages(channel['id'])

        for message in messages:
            # Filter messages based on criteria
            message_time = datetime.fromtimestamp(float(message['ts']))
            if message_time < start_time:
                continue
            if include_threads and 'reply_count' not in message:
                continue
            if not include_bots and message.get('subtype') == 'bot_message':
                continue

            # Generate embeddings for the message
            embedding = embedder.generate_embeddings(message['text'])

            # Index the data
            indexer.index_data({
                'type': 'slack',
                'embedding': embedding,
                'resource_id': message['ts'],
                'time_stamp': message['ts']
            })

if __name__ == "__main__":
    main()