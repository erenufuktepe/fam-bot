from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db import session_scope
from app.repositories import AppointmentRepository
from app.schemas import AppointmentDTO
from app.services import AppointmentService
from app.utils import datetime, formatting, telegram

APPT_MENU, ASKING = range(2)


async def appointment_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["user_id"] = update.message.from_user.id
    buttons_list = {
        "Add new appointment. 📌": "appointment:add",
        "Edit appointment. ✏️": "appointment:edit",
        "Cancel appointment. ❌": "appointment:cancel",
        "List upcoming appointments.🗓️": "appointment:list",
    }
    await telegram.message_reply_with_buttons(update, ctx, options=buttons_list)
    return APPT_MENU


async def appointment_edit_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    options = {
        "Edit date time": "appointment:date",
        "Edit location": "appointment:location",
        "Edit note": "appointment:note",
        "Complete": "appointment:complete",
    }
    await telegram.message_reply_with_buttons(update, ctx, options=options)
    return ASKING


async def appointment_optional_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    options = {
        "Add location": "appointment:location",
        "Add note": "appointment:note",
        "Complete": "appointment:complete",
    }
    if "location" in ctx.user_data.keys():
        options.pop("Add location")

    if "note" in ctx.user_data.keys():
        options.pop("Add note")

    await telegram.message_reply_with_buttons(update, ctx, options=options)
    return ASKING


async def handle_appointment_cmd_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    match action:
        case "add":
            await query.edit_message_text("What appointment is this for?")
            ctx.user_data["step"] = "title"
            return ASKING
        case "list":
            with session_scope() as session:
                repository = AppointmentRepository(session)
                service = AppointmentService(repository)
                appts = service.get_upcoming_appointments(ctx.user_data["user_id"])

            title = f"Appointments in {datetime.get_current_year()}"
            await query.edit_message_text(formatting.bold(title), parse_mode="HTML")
            message = f"No appointment found for {datetime.get_current_year()}."

            message_list = []
            for appt in appts:
                msg = f"🔵 {appt.title} - {appt.start_datetime}"
                if appt.location:
                    msg += f"\n → <b>Location:</b> {appt.location}"
                if appt.note:
                    msg += f"\n → <b>Note:</b> {appt.note}"
                message_list.append(msg)
            message = "\n".join(message_list) if message_list else message
            await query.message.reply_text(message, parse_mode="HTML")
            return ConversationHandler.END
        case "edit" | "cancel":
            with session_scope() as session:
                repository = AppointmentRepository(session)
                service = AppointmentService(repository)
                appts = service.get_upcoming_appointments(ctx.user_data["user_id"])
                return await handle_appointment_list(update, ctx, appts, action)


async def handle_appointment_list(
    update: Update,
    ctx: ContextTypes.DEFAULT_TYPE,
    appointments: list[AppointmentDTO],
    action: str,
):
    if not appointments:
        message = f"No appointment found for {datetime.get_current_year()}."
        await update.message.reply_text(message)
        return ConversationHandler.END
    options = {
        f"{appt.title} - {appt.start_datetime}": f"appointment:{action}:{appt.id}"
        for appt in appointments
    }
    title = (
        f"Which appointment in {datetime.get_current_year()} do you want to {action}?"
    )
    await telegram.message_reply_with_buttons(update, ctx, options=options, title=title)
    return ASKING


async def handle_appointment_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    step = ctx.user_data.get("step")
    text = update.message.text

    match step:
        case "title":
            ctx.user_data["title"] = text.title()
            ctx.user_data["step"] = "date"
            await update.message.reply_text("Enter the date (YYYY/MM/DD HH:MM):")
            return ASKING
        case "date":
            if datetime.validate_datetime(text):
                field = "start_datetime"
                value = datetime.to_datetime(text)
                if "appt_id" in ctx.user_data.keys():
                    with session_scope() as session:
                        repository = AppointmentRepository(session)
                        service = AppointmentService(repository)
                        service.update(ctx.user_data["appt_id"], field, value)
                        await appointment_edit_menu(update, ctx)
                        return ASKING
                ctx.user_data[field] = value
                await appointment_optional_menu(update, ctx)
            else:
                await update.message.reply_text(
                    "Enter valid datetime (YYYY/MM/DD HH:MM):"
                )
                return ASKING
        case "location":
            if "appt_id" in ctx.user_data.keys():
                with session_scope() as session:
                    repository = AppointmentRepository(session)
                    service = AppointmentService(repository)
                    service.update(ctx.user_data["appt_id"], "location", text)
                    await appointment_edit_menu(update, ctx)
                    return ASKING
            ctx.user_data["location"] = text
            await appointment_optional_menu(update, ctx)
            return ASKING
        case "note":
            if "appt_id" in ctx.user_data.keys():
                with session_scope() as session:
                    repository = AppointmentRepository(session)
                    service = AppointmentService(repository)
                    service.update(ctx.user_data["appt_id"], "note", text)
                    await appointment_edit_menu(update, ctx)
                    return ASKING
            ctx.user_data["note"] = text
            await appointment_optional_menu(update, ctx)
            return ASKING


async def handle_appointment_list_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data.split(":")[-2]
    id = int(query.data.split(":")[-1])

    match action:
        case "edit":
            await appointment_edit_menu(update, ctx)
            ctx.user_data["appt_id"] = id
            return ASKING
        case "cancel":
            with session_scope() as session:
                repository = AppointmentRepository(session)
                service = AppointmentService(repository)
                service.cancel(id)
                await query.edit_message_text("Appointment canceled ✅")
        case _:
            raise ValueError("Invalid appointment action.")
    return ConversationHandler.END


async def handle_optional_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    match action:
        case "location":
            await query.edit_message_text("Enter the location for the appointment:")
            ctx.user_data["step"] = action
            return ASKING
        case "note":
            await query.edit_message_text("Enter the note for the appointment:")
            ctx.user_data["step"] = action
            return ASKING
        case "date":
            await query.edit_message_text("Enter the date (YYYY/MM/DD HH:MM):")
            ctx.user_data["step"] = action
            return ASKING
        case "complete":
            if "appt_id" in ctx.user_data.keys():
                ctx.user_data.pop("appt_id")
                await query.edit_message_text("Appointment saved ✅")
                return ConversationHandler.END

            with session_scope() as session:
                repository = AppointmentRepository(session)
                service = AppointmentService(repository)
                appointment = AppointmentDTO(
                    user_id=ctx.user_data["user_id"],
                    title=ctx.user_data["title"],
                    start_datetime=ctx.user_data["start_datetime"],
                    location=(
                        ctx.user_data.pop("location")
                        if "location" in ctx.user_data.keys()
                        else None
                    ),
                    note=(
                        ctx.user_data.pop("note")
                        if "note" in ctx.user_data.keys()
                        else None
                    ),
                )
                service.add(appointment)
            await query.edit_message_text("Appointment saved ✅")
            return ConversationHandler.END
