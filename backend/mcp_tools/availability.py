from fastapi import APIRouter, Query, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from db.models import Doctor
from datetime import datetime, timedelta

router = APIRouter(tags=["tools"])

@router.get("/")
def check_availability(
    doctor_name: str = Query(...),
    date: str = Query(None),
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    print("📣 Doctor fetched:", doctor.name)
    print("📣 Raw available_slots:", doctor.available_slots)
    # Parse flexible date strings
    if date:
        date = date.lower().strip()
        if date == "today":
            req_date = datetime.now().date()
        elif date == "tomorrow":
            req_date = datetime.now().date() + timedelta(days=1)
        else:
            try:
                req_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD, 'today', or 'tomorrow'.")

        slots = [s.strftime("%I:%M %p") for s in doctor.available_slots if s.date() == req_date]
        if not slots:
            return {"message": f"No slots for {doctor_name} on {req_date}"}
        return {"available_slots": slots}
    
    # No date given — return grouped future slots
    today = datetime.now().date()
    future_slots = [s for s in doctor.available_slots if s.date() >= today]

    if not future_slots:
        return {"message": f"No future slots available for {doctor_name}"}

    grouped_slots = {}
    for slot in future_slots:
        date_key = slot.strftime("%Y-%m-%d")
        grouped_slots.setdefault(date_key, []).append(slot.strftime("%I:%M %p"))
        
    print("📣 Returning this grouped_slots:")
    print(grouped_slots if 'grouped_slots' in locals() else "Slots not grouped")


    return {"available_dates": grouped_slots}
