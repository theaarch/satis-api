import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from redis import Redis
from rq import Queue

from tasks import dispatch
from config import REDIS_HOST, REDIS_PORT, QUEUE_NAME, GITHUB_WEBHOOK_SECRET

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/github/webhook")
async def github_webhook(request: Request):
    event = request.headers.get("X-GitHub-Event")

    if event != "push":
        return {"message": "ignored"}

    if GITHUB_WEBHOOK_SECRET:
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature:
            raise HTTPException(status_code=401, detail="Signature missing")
        if not signature.startswith("sha256="):
            raise HTTPException(status_code=400, detail="Invalid signature format")
        
        body = await request.body()
        expected_sig = hmac.new(
            GITHUB_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature[7:], expected_sig):
            raise HTTPException(status_code=401, detail="Invalid signature")
    else:
        import logging
        logging.warning("GITHUB_WEBHOOK_SECRET is not configured. Webhook signature verification is skipped.")

    redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
    queue = Queue(QUEUE_NAME, connection=redis)

    data = await request.json()
    repo = data["repository"]["ssh_url"]
    job = queue.enqueue(dispatch, repo)

    return {"message": "queued", "job": job.id, "repo": repo}
