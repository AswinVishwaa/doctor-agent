from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Patient, Appointment
from datetime import datetime

router = APIRouter(tags=["tools"])

@router.get("/")
def get_latest_appointment(
    patient_email: str = Query(...),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.email == patient_email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    latest_appointment = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Appointment.slot.desc())
        .first()
    )

    if not latest_appointment:
        return {"message": "No past appointments found."}

    return {
        "appointment_id": latest_appointment.id,
        "doctor_id": latest_appointment.doctor_id,
        "slot": latest_appointment.slot.isoformat()
    }
