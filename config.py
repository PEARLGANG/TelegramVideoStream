import os
from player.queue import Queue
instances = dict()
queues = Queue()
to_delete = []

API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME")
STREAM_URL = os.getenv("STREAM_URL")
