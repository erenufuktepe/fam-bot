from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.appointment import Appointment


class AppointmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> Optional[list[Appointment]]:
        today_ct = datetime.now(ZoneInfo("America/Chicago")).date()
        appointments = (
            self.session.query(Appointment)
            .filter(Appointment.user_id == user_id, Appointment.start_at >= today_ct)
            .order_by(Appointment.start_at.asc())
            .all()
        )
        return appointments

    def get_appointments_by_date(
        self, user_id: int, start_at: datetime
    ) -> Optional[list[Appointment]]:
        appointments = (
            self.session.query(Appointment)
            .filter(Appointment.start_at == start_at)
            .all()
        )
        return appointments

    def add_appointment(self, appointment: Appointment) -> Appointment:
        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment
