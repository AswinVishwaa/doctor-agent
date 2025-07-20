from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Doctor, Patient, Appointment

now = datetime.now().replace(minute=0, second=0, microsecond=0)
db: Session = SessionLocal()

# Add doctors
doctors = [
    Doctor(
        name="Dr. Ahuja",
        specialty="Cardiology",
        email = "ahuja@gmail.com",
        available_slots=[
            now + timedelta(days=1, hours=2),  # Tomorrow
            now + timedelta(days=2, hours=3),  # Day after
        ]
    ),
    Doctor(
        name="Dr. Mehta",
        specialty="Dermatology",
        email = "mehta@gmail.com",
        available_slots=[
            now + timedelta(days=2, hours=1),
            now + timedelta(days=2, hours=3),
            now + timedelta(days=2, hours=4)
        ]
    ),
    Doctor(
        name="Dr. Khan",
        specialty="General",
        email = "khan@gmail.com",
        available_slots=[
            now + timedelta(days=1, hours=1)
        ]
    )
]


for d in doctors:
    existing = db.query(Doctor).filter(Doctor.name == d.name).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.add(d)

db.commit()

# Add patients
patients = [
    Patient(name="Aswin", email="aswin@example.com"),
    Patient(name="John Doe", email="john@example.com"),
    Patient(name="Alice", email="alice@example.com")
]

for p in patients:
    existing = db.query(Patient).filter(Patient.email == p.email).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.add(p)

db.commit()
print("✅ Seeded doctors and patients")
