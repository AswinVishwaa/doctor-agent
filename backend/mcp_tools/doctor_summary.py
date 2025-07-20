from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Doctor, Appointment, Patient
from datetime import datetime, timedelta
from typing import Optional
from utils.slack import send_slack_notification


router = APIRouter(tags=["tools"])

@router.get("/")
def doctor_summary(
    doctor_name: str = Query(...),
    date: Optional[str] = Query("today"),
    symptom: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        return {"summary": f"No doctor found with name {doctor_name}"}

    if date == "today":
        target_date = datetime.now().date()
    elif date == "tomorrow":
        target_date = datetime.now().date() + timedelta(days=1)
    elif date == "yesterday":
        target_date = datetime.now().date() - timedelta(days=1)
    else:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            return {"summary": f"Invalid date: {date}"}

    # Get appointments for that day
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor.id,
            Appointment.slot >= datetime.combine(target_date, datetime.min.time()),
            Appointment.slot <= datetime.combine(target_date, datetime.max.time())
        )
        .all()
    )

    if not appointments:
        summary_msg = f"No appointments found for {doctor_name} on {target_date}"
        send_slack_notification(summary_msg)
        return {"summary": summary_msg}

    total = len(appointments)

    if symptom:
        matching = [a for a in appointments if symptom.lower() in (a.symptoms or "").lower()]
        summary_msg = f"{len(matching)} out of {total} appointments on {target_date} had symptom: '{symptom}'."
        send_slack_notification(summary_msg)
        return {"summary": summary_msg}

    # Just count summary
    summary_msg = f"Dr. {doctor.name} has {total} appointment(s) scheduled for {target_date.strftime('%B %d, %Y')}."
    send_slack_notification(summary_msg)
    return {"summary": summary_msg}
