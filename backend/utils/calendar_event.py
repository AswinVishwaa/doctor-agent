# calendar.py
import os
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
# Define scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up from utils to project root
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")# or use full path if needed

# Load Google Calendar ID from environment variable
calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
print("📂 Using credentials path:", SERVICE_ACCOUNT_FILE)
print("🗂️ Calendar ID is:", calendar_id)


if not calendar_id:
    raise ValueError("❌ GOOGLE_CALENDAR_ID not set. Set it in your environment.")

def create_calendar_event(patient_name, doctor_name, slot_time_iso):
    """
    Creates a 30-minute Google Calendar event for the appointment.
    """
    try:
        print("🔐 Loading credentials...")
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        print(f"✅ Credentials loaded for service account.")

        # Initialize Google Calendar API client
        service = build("calendar", "v3", credentials=credentials)

        # Parse the start and end time
        slot_time = datetime.fromisoformat(slot_time_iso)
        end_time = slot_time + timedelta(minutes=30)

        print(f"🕒 Creating event from {slot_time} to {end_time} in timezone Asia/Kolkata")

        # Event body
        event = {
            'summary': f'Appointment: {patient_name} with {doctor_name}',
            'description': 'Auto-booked via MCP Doctor Assistant',
            'start': {'dateTime': slot_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        }

        # Insert event into calendar
        event_response = service.events().insert(calendarId=calendar_id, body=event).execute()

        print("✅ Event created successfully!")
        print("🔗 Event link:", event_response.get('htmlLink'))

        return event_response

    except Exception as e:
        import traceback
        print("❌ Failed to create Google Calendar event.")
        print("Error Message:", str(e))
        traceback.print_exc()
        return None
        
# calendar.py
# (your existing code remains above)
"""
if __name__ == "__main__":
    # MOCK DATA for testing
    test_patient_name = "John Doe"
    test_doctor_name = "Dr. Strange"
    test_slot_time = (datetime.now() + timedelta(minutes=10)).isoformat()  # 10 mins from no
    print("🚀 Running calendar event creation test...")

    # Optionally override env variable directly for testing
    calendar_id = "61bd94b277f047aa2c556bdfa3c53750e193509291a117eb443b1a5e36ae466c@group.calendar.google.com"

    # Call the function
    response = create_calendar_event(test_patient_name, test_doctor_name, test_slot_time)
    if response:
        print("🎉 Test event created!")
    else:
        print("⚠️ Test failed.")
"""
