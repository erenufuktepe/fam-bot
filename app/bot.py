import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.auth import require_allowed_user
from app.handlers import appointment, birthday, shop
from app.settings import settings

logger = logging.getLogger(__name__)

# async def send_message():
#     TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
#     BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

#     url = f"{BASE_URL}/sendMessage"
#     payload = {
#         "chat_id": "CHAT_ID",
#         "text": "Hi! This is a scheduled message from your bot.",
#     }

#     async with httpx.AsyncClient() as client:
#         resp = await client.post(url, json=payload)
#         resp.raise_for_status()


def build_appointment_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("appointment", appointment.appointment_cmd)],
        states={
            appointment.APPT_MENU: [
                CallbackQueryHandler(
                    appointment.handle_appointment_cmd_action,
                    pattern=r"^appointment:(add|edit|cancel|list)$",
                )
            ],
            appointment.ASKING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    appointment.handle_appointment_step,
                ),
                CallbackQueryHandler(
                    appointment.handle_optional_menu,
                    pattern=r"^appointment:(date|location|note|complete)$",
                ),
                CallbackQueryHandler(
                    appointment.handle_appointment_list_menu,
                    pattern=r"^appointment:(edit|cancel)(:\d+)?$",
                ),
            ],
        },
        fallbacks=[],
    )


def build_birthday_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("birthday", require_allowed_user(birthday.birthday_cmd))
        ],
        states={
            birthday.BDAY_MENU: [
                CallbackQueryHandler(
                    birthday.handle_birthday_cmd_action, pattern=r"^birthday:"
                )
            ],
            birthday.ASKING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    birthday.handle_birthday_steps,
                )
            ],
        },
        fallbacks=[],
    )


def build_shop_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("shop", require_allowed_user(shop.shop_cmd))],
        states={
            shop.SHOP_MENU: [
                CallbackQueryHandler(shop.handle_shop_cmd_action, pattern=r"^shop:")
            ],
            shop.ASKING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    shop.handle_shop_steps,
                )
            ],
        },
        fallbacks=[],
    )


def build_bot():
    app = (
        ApplicationBuilder().token(settings.BOT_TOKEN).concurrent_updates(True).build()
    )

    app.add_handler(build_appointment_handler())
    app.add_handler(build_birthday_handler())
    app.add_handler(build_shop_handler())

    return app
