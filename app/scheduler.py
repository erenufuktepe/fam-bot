# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
