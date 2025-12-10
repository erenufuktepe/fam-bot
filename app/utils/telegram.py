from unittest.mock import DEFAULT

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

from app.utils.formatting import bold

DEFAULT_TITLE = "What would you like to do?"


def _build_keyboard(options: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in options.items()
    ]
    return InlineKeyboardMarkup(keyboard)


async def message_reply_with_buttons(
    update: Update,
    ctx: ContextTypes.DEFAULT_TYPE,
    options: dict[str, str],
    title: str = DEFAULT_TITLE,
) -> None:
    if update.message:
        ctx.user_data["user_id"] = update.message.from_user.id
        await update.message.reply_text(
            bold(title),
            parse_mode="HTML",
            reply_markup=_build_keyboard(options),
        )
    else:
        query = update.callback_query
        await query.edit_message_text(
            bold(title),
            parse_mode="HTML",
            reply_markup=_build_keyboard(options),
        )
