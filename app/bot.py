import logging
from datetime import datetime

import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

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

BDAY_MENU, ASKING = range(2)


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


def create_inline_keyboard_button(
    text: str, callback_data: str
) -> list[InlineKeyboardButton]:
    """Helper function to create an inline keyboard button."""
    return [InlineKeyboardButton(text=text, callback_data=callback_data)]


async def reply_with_options(
    update: Update, ctx: ContextTypes.DEFAULT_TYPE, buttons_list: dict
) -> None:
    """Helper function to reply with inline keyboard options."""
    keyboard = [
        create_inline_keyboard_button(text, callback_data)
        for text, callback_data in buttons_list.items()
    ]
    await update.message.reply_text(
        "<b>What would you like to do?</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def birthday_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handle the /birthday command."""
    if _is_allowed(update.message.from_user):
        buttons_list = {
            "Add new birthday to calendar. 🎂": "birthday:add",
            "Delete birthday from calendar. ❌": "birthday:delete",
            "List this month's birthdays from calendar.🗓️": "birthday:list",
        }
        await reply_with_options(update, ctx, buttons_list)
        return BDAY_MENU


async def handle_birthday_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handle birthday related button presses."""
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    match action:
        case "add":
            await query.edit_message_text("You chose: Add birthday 🎂")
            ctx.user_data["step"] = "person_name"
            await query.message.reply_text("Who is the birthday for?")
            return ASKING
        case "delete":
            await query.edit_message_text("You chose: Delete birthday ❌")
            ctx.user_data["step"] = "delete"
            await query.message.reply_text("Who is the birthday do you want to delete?")
            return ASKING
        case "list":
            month = datetime.now().month
            await query.edit_message_text("You chose: List birthdays 🗓️")
            await query.message.reply_text(
                f"<b>{Month.from_number(month).title()} Birthdays</b>",
                parse_mode="HTML",
            )
            service = get_birthday_service()
            birthdays = await service.get_upcoming_birthdays()

            message = "No birthdays found for this month."
            if birthdays:
                message_list = [
                    f"🔵 {birthday.person_name} - {str(birthday.month).zfill(2)}/{str(birthday.day).zfill(2)}"
                    for birthday in birthdays
                ]
                message = "\n".join(message_list)
            await query.message.reply_text(
                message,
                parse_mode="HTML",
            )
            return ConversationHandler.END


async def handle_birthday_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    step = ctx.user_data.get("step")
    text = update.message.text
    user_id = update.message.from_user.id

    match step:
        case "person_name":
            ctx.user_data["person_name"] = text.title()
            ctx.user_data["step"] = "date"
            await update.message.reply_text("Enter the date (MM/DD):")
            return ASKING
        case "date":
            person_name = ctx.user_data["person_name"]
            date = text
            service = get_birthday_service()
            await service.add_birthday(user_id, person_name, date)
            await update.message.reply_text(
                f"Saved birthday for {person_name} on {date}. 🎉"
            )
            return ConversationHandler.END
        case "delete":
            person_name = text.title()
            service = get_birthday_service()
            await service.delete_birthday(person_name)
            await update.message.reply_text(f"{person_name}'s birthday is deleted.")
            return ConversationHandler.END


async def appointment_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
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


ASK_NAME = 0  # state id


# 1) MUST return ASK_NAME from the entry point
async def start_cmd(update, context) -> int:
    await update.message.reply_text("Hi! What is your name?")
    return ASK_NAME


# 2) This will be called when we are in ASK_NAME state
async def get_name(update, context) -> int:
    name = update.message.text
    await update.message.reply_text(f"Nice to meet you, {name}!")
    return ConversationHandler.END  # or another state


def build_bot():
    app = (
        ApplicationBuilder().token(settings.BOT_TOKEN).concurrent_updates(True).build()
    )
    # app.add_handler(CommandHandler("birthday", birthday_cmd))
    app.add_handler(CommandHandler("appointment", appointment_cmd))
    app.add_handler(CommandHandler("shop", shop_cmd))
    # app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(CommandHandler("task", recurring_task_cmd))

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", start_cmd)],
    #     states={ASK_NAME: [MessageHandler(filters.TEXT, get_name)]},
    #     fallbacks=[],
    # )
    # app.add_handler(conv_handler)

    conv = ConversationHandler(
        entry_points=[CommandHandler("birthday", birthday_cmd)],
        states={
            BDAY_MENU: [
                CallbackQueryHandler(handle_birthday_button, pattern=r"^birthday:")
            ],
            ASKING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_birthday_chat,
                )
            ],
        },
        fallbacks=[],
    )

    app.add_handler(conv)

    return app
