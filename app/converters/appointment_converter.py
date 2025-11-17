from datetime import datetime

from app.models.appointment import Appointment as AppointmentModel
from app.schemas.appointment import Appointment as AppointmentSchema


class AppointmentConverter:
    @classmethod
    def from_model(cls, appointment: AppointmentModel) -> AppointmentSchema:
        return AppointmentSchema(
            id=appointment.id if appointment.id else None,
            user_id=appointment.user_id,
            title=appointment.title,
            start_at=appointment.start_at.strftime("%Y-%m-%d %H:%M"),
            location=appointment.location,
            notes=appointment.notes,
        )

    @classmethod
    def from_schema(cls, appointment: AppointmentSchema) -> AppointmentModel:
        return AppointmentModel(
            id=appointment.id,
            user_id=appointment.user_id,
            title=appointment.title,
            start_at=datetime.fromisoformat(appointment.start_at),
            location=appointment.location,
            notes=appointment.notes,
        )

    @classmethod
    def from_model_list(
        cls, appointments: list[AppointmentModel]
    ) -> list[AppointmentSchema]:
        return [cls.from_model(appointment) for appointment in appointments]

    @classmethod
    def from_schema_list(
        cls, appointments: list[AppointmentSchema]
    ) -> list[AppointmentModel]:
        return [cls.from_schema(appointment) for appointment in appointments]
