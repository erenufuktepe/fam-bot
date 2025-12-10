from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from app.db import session_scope
from app.repositories import UserRepository
from app.services import UserService


async def _is_allowed_async(id: int, first_name: str, last_name: str) -> bool:
    with session_scope() as session:
        repository = UserRepository(session)
        service = UserService(repository)
        username = f"{first_name} {last_name}"
        return service.is_allowed(id, username)


def require_allowed_user(handler: callable):
    @wraps(handler)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user = update.effective_user
        chat = update.effective_chat

        if not user:
            return  # no user, ignore

        if not await _is_allowed_async(user.id, user.first_name, user.last_name):
            if chat:
                await chat.send_message("🚫 You are not allowed to use this bot.")
            return

        return await handler(update, context, *args, **kwargs)

    return wrapper
