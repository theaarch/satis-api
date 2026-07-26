from rq import Worker, Queue
from redis import Redis
from config import REDIS_URL, QUEUE_NAME

redis = Redis.from_url(REDIS_URL)
queue = Queue(QUEUE_NAME, connection=redis)

if __name__ == "__main__":
    worker = Worker(queues=[queue], connection=redis)
    worker.work()
