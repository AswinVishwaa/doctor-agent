from typing import List

def get_tool_registry() -> List[dict]:
    return [
        {
            "name": "check_availability",
            "description": "Check if a doctor is available on a given date. Required parameters: doctor_name, date.",
            "method": "GET",
            "endpoint": "/mcp/tool/check_availability",
            "params": {
                "doctor_name": "Doctor's full name. Required.",
                "date": "Optional. Date string in YYYY-MM-DD or 'today'/'tomorrow'"
            }
        },
        {
            "name": "schedule_appointment",
            "description": "Book an appointment with a doctor. Requires: 'doctor_name', 'patient_name', 'patient_email', and 'slot' (ISO format).",
            "method": "GET",
            "endpoint": "/mcp/tool/schedule_appointment",
            "params": {
                "doctor_name": "Doctor's full name. Example: 'Dr. Ahuja'",
                "patient_name": "Full name of the patient. Example: 'Aswin Vishwaa'",
                "patient_email": "Email address of the patient. Example: 'aswin@example.com'",
                "slot": "Appointment datetime in full ISO format, combining the selected time slot with the known date context. Example: '2025-07-21T08:00:00'. Do NOT guess the date."
            }
        },
      #  {
       #     "name": "generate_summary",
        #    "description": "Generate a summary of a past appointment using appointment ID.",
        #    "method": "GET",
        #    "endpoint": "/mcp/tool/generate_summary",
        #    "params": {
        #        "appointment_id": "Unique ID of the appointment. Example: 1"
        #    }
       # },
       # {
        #    "name": "get_latest_appointment",
         #   "description": "Get the most recent appointment for a patient using their email.",
          #  "method": "GET",
           # "endpoint": "/mcp/tool/get_latest_appointment",
            #"params": {
           #     "patient_email": "Email address of the patient. Example: 'aswinvishwaa@gmail.com'"
           # }
       # },'''
        {
            "name": "doctor_summary",
            "description": "Generate a summary of doctor's appointments for a specific date or symptom filter.",
            "method": "GET",
            "endpoint": "/mcp/tool/doctor_summary",
            "params": {
                "doctor_name": "Doctor's full name. Example: 'Dr. Khan'",
                "date": "Date string: 'today', 'tomorrow', 'yesterday', or YYYY-MM-DD",
                "symptom": "Optional. Filter by symptom. Example: 'fever'"
            }
        }


    ]
