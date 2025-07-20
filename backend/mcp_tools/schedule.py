from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Doctor, Patient, Appointment
from datetime import datetime
from utils.email import send_confirmation_email
from utils.calendar import create_calendar_event

router = APIRouter(tags=["tools"])

@router.get("/")
def schedule_appointment(
    doctor_name: str = Query(...),
    patient_name: str = Query(...),
    patient_email: str = Query(...),
    slot: str = Query(...),
    db: Session = Depends(get_db)
):
    print(f"📥 Received appointment request → Doctor: {doctor_name}, Patient: {patient_name}, Email: {patient_email}, Slot: {slot}")

    try:
        # Parse slot time
        try:
            slot_time = datetime.fromisoformat(slot)
        except Exception as e:
            print("❌ Slot parsing failed:", str(e))
            raise HTTPException(status_code=400, detail="Invalid slot datetime format. Must be ISO 8601.")

        slot_time = slot_time.replace(microsecond=0)

        # Fetch doctor
        doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        print("✅ Doctor found:", doctor.name)

        # Normalize and compare available slots
        available = [s.replace(microsecond=0) for s in doctor.available_slots]
        print("📅 Available slots (normalized):", available)

        if slot_time not in available:
            raise HTTPException(status_code=400, detail="Slot not available")

        # Fetch or create patient
        patient = db.query(Patient).filter(Patient.email == patient_email).first()
        if not patient:
            patient = Patient(name=patient_name, email=patient_email)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            print("👤 New patient created.")

        # Create appointment
        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            slot=slot_time,
            symptoms=""
        )
        db.add(appointment)

        # Remove booked slot from availability
        doctor.available_slots = [s for s in doctor.available_slots if s.replace(microsecond=0) != slot_time]
        db.commit()
        print("📦 Appointment saved and slot removed.")

        # Send confirmation (Google Calendar + Email)
        try:
            create_calendar_event(
                patient_name=patient_name,
                doctor_name=doctor.name,
                slot_time_iso=slot  # must be full ISO string like "2025-07-22T12:00:00"
            )
            print("📅 Google Calendar event created.")
        except Exception as e:
            print(f"⚠️ Calendar error: {e}")

        try:
            send_confirmation_email(
                to_email=patient_email,
                patient_name=patient_name,
                doctor_name=doctor.name,
                slot=slot
            )
            print("📧 Confirmation email sent.")
        except Exception as e:
            print(f"⚠️ Email error: {e}")

        return {"message": f"✅ Appointment booked for {patient_name} with Dr. {doctor_name} at {slot}"}

    except Exception as e:
        import traceback
        print("💥 Unhandled Exception in schedule_appointment:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")
