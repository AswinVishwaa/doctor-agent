from db.database import SessionLocal
from db.models import Doctor, Patient, Appointment
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query

router = APIRouter(tags=["tools"])

@router.get("/")
def generate_summary(
    appointment_id: int = Query(...),
    doctor_name: str = Query(None)
):
    db: Session = SessionLocal()

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return {"summary": f"No appointment found with ID {appointment_id}."}

    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        return {"summary": f"No doctor found for appointment ID {appointment_id}."}

    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        return {"summary": f"No patient found for the appointment."}

    time_str = appointment.slot.strftime("%B %d, %Y at %I:%M %p")

    summary = (
        f"Dr. {doctor.name}, a specialist in {doctor.specialty}, "
        f"had an appointment with {patient.name} ({patient.email}) "
        f"on {time_str}. The booking ID is {appointment.id}."
    )

    return {"summary": summary}
