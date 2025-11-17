import shlex

from app.converters.appointment_converter import AppointmentConverter
from app.db import session_scope
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import Appointment
from app.utils import CLIParser

MAPPING = {"-t": "title", "-d": "start_at", "-l": "location", "-n": "notes"}


class AppointmentService:
    def __init__(self):
        self.converter = AppointmentConverter()
        self.parser = CLIParser(
            mapping=MAPPING,
            cls=Appointment,
        )

    def add_appointment(self, user_id, tokens: list) -> str:
        try:
            # TODO: user_id and start date uniqueness check
            with session_scope() as session:
                appointment = self.parser.parse(tokens)
                appointment.user_id = user_id
                repository = AppointmentRepository(session)
                _appointment = self.converter.from_schema(appointment)
                return self._present_added_appointment(
                    repository.add_appointment(_appointment)
                )
        except Exception as exc:
            raise Exception(f"Error creating appointment: {exc}")

    def get_appointments_by_user(self, user_id: int) -> str:
        try:
            with session_scope() as session:
                repository = AppointmentRepository(session)
                appointments = repository.get_by_user_id(user_id)
                return self._present_appointments(
                    self.converter.from_model_list(appointments)
                )
        except Exception as exc:
            raise Exception(f"Error getting appointments for user {user_id}: {exc}")

    def _present_added_appointment(self, appointment: Appointment) -> str:
        try:
            return f"Appointment added: {appointment.title.title()} 📅"
        except Exception as exc:
            raise Exception(f"Error presenting added appointment: {exc}")

    def _present_appointments(self, appointments: list[Appointment]) -> str:
        try:
            if not appointments:
                return "No appointments found."
            lines = ["<b>Your Upcoming Appointments 📅:</b>\n"]
            for appointment in appointments:
                line = f"\n🟢 {appointment.title.title()} appointment on <b>{appointment.start_at}</b>"
                if appointment.location:
                    line += f" at {appointment.location.title()}"
                if appointment.notes:
                    line += f"\n\t\t🔹 Notes: {appointment.notes}"
                lines.append(line)
            return "\n".join(lines)
        except Exception as exc:
            raise Exception(f"Error presenting appointments: {exc}")


def get_appointment_service() -> AppointmentService:
    return AppointmentService()
