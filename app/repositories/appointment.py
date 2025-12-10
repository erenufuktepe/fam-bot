from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.repositories.base import BaseRepository


class AppointmentRepositoryException(Exception):
    pass


class AppointmentRepository(BaseRepository):
    """Repository for Appointment model."""

    def __init__(self, session: Session):
        super().__init__(session, Appointment)

    def get_upcoming_appointments(self, user_id: int) -> list[Appointment]:
        today_ct = datetime.now(ZoneInfo("America/Chicago"))
        appointments = (
            self.session.query(Appointment)
            .filter(
                Appointment.user_id == user_id,
                Appointment.start_datetime >= today_ct,
                extract("year", Appointment.start_datetime) == today_ct.year,
            )
            .order_by(Appointment.start_datetime.asc())
            .all()
        )
        return appointments
