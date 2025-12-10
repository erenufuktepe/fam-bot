from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db import session_scope
from app.enums import Month
from app.repositories import ShoppingItemRepository
from app.schemas import ShoppingItemDTO
from app.services import ShoppingItemService
from app.utils import datetime, formatting, telegram

SHOP_MENU, ASKING = range(2)


async def shop_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["user_id"] = update.message.from_user.id
    buttons_list = {
        "Add new shopping item. 🛒": "shop:add",
        "List grocery items.📋": "shop:list",
    }
    user_id = ctx.user_data.get("user_id")
    await telegram.message_reply_with_buttons(update, ctx, options=buttons_list)
    return SHOP_MENU


async def handle_shop_cmd_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    match action:
        case "add":
            ctx.user_data["step"] = "item_name"
            await query.edit_message_text("What is the name of the item?")
            return ASKING
        case "list":
            message = formatting.bold("Grocery List:")
            await query.edit_message_text(message, parse_mode="HTML")

            with session_scope() as session:
                repository = ShoppingItemRepository(session)
                service = ShoppingItemService(repository)
                items = service.get_shopping_items()

            if not items:
                message = "No grocery item found."
                await query.message.reply_text(message, parse_mode="HTML")
                return ConversationHandler.END

            buttons_list = format_grocery_list(items)
            title = "Select items to delete or complete to close."
            await telegram.message_reply_with_buttons(
                update, ctx, options=buttons_list, title=title
            )
            return ASKING


def format_grocery_list(items: list[ShoppingItemDTO]) -> dict[str, str]:
    buttons_list = {}
    for obj in items:
        key = f"🛒 {obj.item_name} - {obj.quantity}"
        if obj.note:
            key += f"\n{obj.note}"
        buttons_list[key] = f"shop:delete:{obj.id}"
    buttons_list["Complete"] = "shop:complete"
    return buttons_list


async def handle_shop_steps(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    step = ctx.user_data.get("step")
    text = update.message.text

    match step:
        case "item_name":
            ctx.user_data["item_name"] = text.title()
            ctx.user_data["step"] = "quantity"
            await update.message.reply_text("How many do you need?")
            return ASKING
        case "quantity":
            if not text.isnumeric():
                await update.message.reply_text(
                    "Please enter a valid number. How many do you need?"
                )
                return ASKING
            ctx.user_data["quantity"] = int(text)
            ctx.user_data["step"] = "note"
            await update.message.reply_text("Add a note for the item or type no:")
            return ASKING
        case "note":
            item = ShoppingItemDTO(
                user_id=ctx.user_data["user_id"],
                item_name=ctx.user_data["item_name"],
                quantity=ctx.user_data["quantity"],
            )
            if not text.lower() == "no":
                item.note = text
            with session_scope() as session:
                repository = ShoppingItemRepository(session)
                service = ShoppingItemService(repository)
                service.add(item)
                await update.message.reply_text("Shopping item added. ✅")
            return ConversationHandler.END


# TODO: delete and complete
