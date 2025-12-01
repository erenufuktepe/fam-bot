import logging
from contextlib import asynccontextmanager

from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from telegram import Update

from app.bot import build_bot
from app.db import SessionLocal, engine
from app.models import Base
from app.scheduler import scheduler, shutdown_scheduler, start_scheduler
from app.schemas.user import User
from app.services.user_service import UserService, get_user_service
from app.settings import settings

logger = logging.getLogger(__name__)

tg = build_bot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        await tg.initialize()
        await tg.start()
        await tg.bot.delete_webhook(drop_pending_updates=True)
        await tg.bot.set_webhook(
            url=settings.WEBHOOK_URL.rstrip("/")
            + "/telegram/webhook/"
            + settings.WEBHOOK_SECRET,
            secret_token=settings.WEBHOOK_SECRET,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"],
        )

        # scheduler.add_job(
        #     send_message,  # the function
        #     CronTrigger(minute="*"),  # cron expression → every minute
        #     id="send_message",  # unique ID
        #     replace_existing=True,  # overwrite if already exists
        # )

        start_scheduler()
        yield
    finally:
        await tg.bot.delete_webhook(drop_pending_updates=False)
        await tg.stop()
        await tg.shutdown()
        shutdown_scheduler()


app = FastAPI(title="FamBot Webhook", lifespan=lifespan)


@app.post("/telegram/webhook/{secret}", status_code=200)
async def telegram_webhook(secret: str, request: Request):
    if secret != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="forbidden")

    sig = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if sig and sig != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="bad signature")

    data = await request.json()
    update = Update.de_json(data, tg.bot)

    if update.callback_query:
        logger.info("Received callback query")
    await tg.process_update(update)

    return {"ok": True}
