import os
from dotenv import load_dotenv

load_dotenv()

SATIS_DIR = os.getenv("SATIS_DIR", "/Users/x/Herd/satis")

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

QUEUE_NAME = os.getenv("QUEUE_NAME", "satis")

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
