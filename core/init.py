from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from cache import redis_client


def initialize():
    print("Initializing...")

    # Create a scheduler instance
    scheduler = AsyncIOScheduler()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Starting scheduler...")
        scheduler.start()
        yield
        print("Stopping scheduler...")
        scheduler.shutdown()

    app = FastAPI(lifespan=lifespan)

    # Schedule the job to run at midnight every day
    scheduler.add_job(redis_client.flushdb, trigger=CronTrigger(hour=0, minute=0))

    return app
