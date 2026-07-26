import os
from dotenv import load_dotenv

load_dotenv()

SATIS_DIR = os.getenv("SATIS_DIR", "/Users/x/Herd/satis")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

QUEUE_NAME = os.getenv("QUEUE_NAME", "satis")

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
