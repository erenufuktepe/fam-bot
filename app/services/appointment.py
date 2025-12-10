from app.model_mapper import ModelMapper
from app.models import Appointment
from app.repositories import AppointmentRepository
from app.schemas import AppointmentDTO


class AppointmentService:
    """Application logic related to Appointments."""

    def __init__(self, repository: AppointmentRepository):
        self.repository = repository

    def get_by_id(self, id: int) -> AppointmentDTO:
        try:
            appointment = self.repository.get_by_id(id)
            if not appointment:
                return None
            return ModelMapper.from_model(appointment, AppointmentDTO)
        except Exception as exc:
            raise Exception(exc) from exc

    def add(self, dto: AppointmentDTO) -> AppointmentDTO:
        try:
            appointment = ModelMapper.from_schema(dto, Appointment)
            appointment = self.repository.upsert(appointment)
            return ModelMapper.from_model(appointment, AppointmentDTO)
        except Exception as exc:
            raise Exception(exc) from exc

    def get_upcoming_appointments(self, user_id: int) -> list[AppointmentDTO]:
        try:
            appointments = self.repository.get_upcoming_appointments(user_id)
            return ModelMapper.from_model_list(appointments, AppointmentDTO)
        except Exception as exc:
            raise Exception(exc) from exc

    def cancel(self, id: int) -> bool:
        try:
            appointment = self.repository.get_by_id(id)

            if not appointment:
                raise Exception("Appointment doesn't exists")

            return self.repository.delete(appointment)
        except Exception as exc:
            raise Exception(exc) from exc

    def update(self, id: int, field: str, value: any):
        try:
            appointment = self.repository.get_by_id(id)

            if not appointment:
                raise Exception("Appointment not found.")

            setattr(appointment, field, value)
            return self.repository.upsert(appointment)
        except Exception as exc:
            raise Exception(f"Error creating appointment: {exc}")
