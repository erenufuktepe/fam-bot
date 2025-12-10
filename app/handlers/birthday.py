from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db import session_scope
from app.enums import Month
from app.repositories import BirthdayRepository
from app.schemas import BirthdayDTO
from app.services import BirthdayService
from app.utils import datetime, formatting, telegram

BDAY_MENU, ASKING = range(2)


async def birthday_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["user_id"] = update.message.from_user.id
    buttons_list = {
        "Add new birthday to calendar. 🎂": "birthday:add",
        "Delete birthday from calendar. ❌": "birthday:delete",
        "List this month's birthdays.🗓️": "birthday:list",
    }
    await telegram.message_reply_with_buttons(update, ctx, options=buttons_list)
    return BDAY_MENU


async def handle_birthday_cmd_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    match action:
        case "add":
            ctx.user_data["step"] = "person_name"
            await query.edit_message_text("Who is the birthday for?")
            return ASKING
        case "delete":
            ctx.user_data["step"] = "delete"
            await query.edit_message_text("Who is the birthday do you want to delete?")
            return ASKING
        case "list":
            message = formatting.bold(
                f"{Month.from_number(datetime.get_current_month()).title()} Birthdays:"
            )
            await query.edit_message_text(message, parse_mode="HTML")

            with session_scope() as session:
                repository = BirthdayRepository(session)
                service = BirthdayService(repository)
                birthdays = service.get_upcoming_birthdays()

            bday_format = "🔵 {name} - {month}/{day}"
            message = "No birthdays found for this month."
            message_list = [
                bday_format.format(
                    name=bday.person_name,
                    month=str(bday.month).zfill(2),
                    day=str(bday.day).zfill(2),
                )
                for bday in birthdays
            ]
            message = "\n".join(message_list) if message_list else message
            await query.message.reply_text(message, parse_mode="HTML")
            return ConversationHandler.END


async def handle_birthday_steps(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    step = ctx.user_data.get("step")
    user_id = ctx.user_data.get("user_id")
    text = update.message.text

    match step:
        case "person_name":
            ctx.user_data["person_name"] = text.title()
            ctx.user_data["step"] = "date"
            await update.message.reply_text("Enter the date (MM/DD):")
            return ASKING
        case "date":
            if not datetime.validate_mmdd_format(text):
                await update.message.reply_text("Enter the date (MM/DD):")
                return ASKING

            with session_scope() as session:
                month, day = datetime.parse_mmdd_format(text)
                repository = BirthdayRepository(session)
                service = BirthdayService(repository)
                birthday = BirthdayDTO(
                    user_id=user_id,
                    person_name=ctx.user_data["person_name"],
                    month=month,
                    day=day,
                )
                is_added = service.add(birthday)

            message = f"Saved birthday for {ctx.user_data["person_name"]} on {text}. 🎉"
            if not is_added:
                message = "Birthday already exists for this person."

            await update.message.reply_text(message)
            return ConversationHandler.END
        case "delete":
            with session_scope() as session:
                repository = BirthdayRepository(session)
                service = BirthdayService(repository)
                service.delete(text)
            await update.message.reply_text(f"{text.title()}'s birthday is deleted.")
            return ConversationHandler.END
