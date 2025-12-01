import logging

import httpx
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

from app.enums import Month
from app.schemas.birthday import Birthday
from app.schemas.user import User
from app.services import (
    BirthdayServiceIntegrityException,
    get_appointment_service,
    get_birthday_service,
    get_recurring_task_service,
    get_shopping_item_service,
)
from app.services.user_service import get_user_service
from app.settings import settings

logger = logging.getLogger(__name__)


def _is_allowed(_from) -> bool:
    service = get_user_service()
    user = service.get_by_id(_from.id)
    if user and user.is_allowed:
        return True

    user = User(
        id=_from.id, username=f"{_from.first_name} {_from.last_name}", is_allowed=False
    )
    service.create_user(user)
    return False


async def start_cmd(update, ctx):
    if _is_allowed(update.message.from_user):
        await update.message.reply_text("Hi! Webhook mode is live.")


async def birthday_cmd(update, ctx):
    if _is_allowed(update.message.from_user):
        try:
            service = get_birthday_service()
            name, day, month = ctx.args
            day, month = int(day), int(month)
            name = name.replace("-", " ").title()

            if day < 1 and day > 31:
                raise ValueError(f"Invlaid day: {day}")

            if month < 1 and month > 12:
                raise ValueError(f"Invalid month: {month}")

            birthday = Birthday(
                id=None, person_name=name, month=Month.from_number(month), day=day
            )
            service.add_birthday(birthday)
            await update.message.reply_text(f"{name}'s birthday added! 🎉")
        except BirthdayServiceIntegrityException as exc:
            await update.message.reply_text(f"We already have {name}'s birthday. 😎")
        except Exception as exc:
            logger.error(f"Error adding birthday: {exc}")
            await update.message.reply_text(
                f"/birthday <first_name>-<last_name> <day_in_number> <month_in_number>"
            )


async def appointment_cmd(update, ctx):
    if _is_allowed(update.message.from_user):
        try:
            service = get_appointment_service()

            command, *_input = ctx.args
            user_id = update.message.from_user.id
            response = ""

            match command:
                # Usage: /appointment -add  -n <title> -d <start_at> -l <location> -l <notes>
                case "-add":
                    response = service.add_appointment(user_id, _input)
                # Usage: /appointment -list
                case "-list":
                    response = service.get_appointments_by_user(user_id)
                case _:
                    logger.info(f"Invalid appointment command: {command}")
                    response = appointment_usage()

            await update.message.reply_text(response, parse_mode="HTML")
        except ValueError as exc:
            logger.error(f"Value error adding appointment: {exc}")
            await update.message.reply_text(appointment_usage(), parse_mode="HTML")
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}")
            await update.message.reply_text(
                "Something went wrong while processing the appointment command.🤖"
            )


async def shop_cmd(update, ctx):
    if _is_allowed(update.message.from_user):
        try:
            service = get_shopping_item_service()
            command, *_input = ctx.args
            user_id = update.message.from_user.id
            keyboard = None
            response = ""

            match command:
                # Usage: /shop -add -i <item_name> -q <quantity> -n <notes>
                case "-add":
                    response = service.add_shopping_item(user_id, _input)
                case "-list":
                    response, keyboard = service.get_shopping_items()
                case _:
                    await update.message.reply_text("Invalid shopping item command.")
            await update.message.reply_text(
                response, parse_mode="HTML", reply_markup=keyboard
            )
        except Exception as exc:
            logger.error(f"Error in shopping item command: {exc}")
            await update.message.reply_text("Error in shopping item command.")


async def recurring_task_cmd(update, ctx):
    if _is_allowed(update.message.from_user):
        try:
            service = get_recurring_task_service()
            command, *_input = ctx.args
            user_id = update.message.from_user.id
            keyboard = None
            response = ""
        except Exception as exc:
            logger.error(f"Error in recurring task command: {exc}")
            await update.message.reply_text("Error in recurring task command.")


def appointment_usage() -> str:
    return (
        "<b>Appointment Usage:</b>\n"
        "\n⚬ /appointment -add -t &lt;title&gt; -d &lt;start_at&gt; -l &lt;location&gt; -n &lt;notes&gt;"
        "\n⚬ /appointment -list"
    )


async def on_callback(update, ctx):
    if _is_allowed(update.callback_query.from_user):
        try:
            if update.callback_query.data.startswith("shop:"):
                await handle_shopping_item_callback(update, ctx)
        except Exception as exc:
            logger.error(f"Error processing callback query: {exc}")


async def handle_shopping_item_callback(update, ctx):
    try:
        service = get_shopping_item_service()
        item_id = int(update.callback_query.data.split(":")[1])
        await ctx.bot.delete_message(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
        )
        service.remove_shopping_item(item_id)
        response, keyboard = service.get_shopping_items()
        await update.callback_query.message.reply_text(
            response, parse_mode="HTML", reply_markup=keyboard
        )
    except Exception as exc:
        logger.error(f"Error processing shopping item callback: {exc}")


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


def build_bot():
    app = (
        ApplicationBuilder().token(settings.BOT_TOKEN).concurrent_updates(True).build()
    )
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("birthday", birthday_cmd))
    app.add_handler(CommandHandler("appointment", appointment_cmd))
    app.add_handler(CommandHandler("shop", shop_cmd))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(CommandHandler("task", recurring_task_cmd))

    return app
