# ics_pull.py

import requests
from ics import Calendar
from datetime import date
import os

# Replace with your own published iCal URL via environment variable
ICS_URL = os.getenv("ICS_CALENDAR_URL", "https://your.ics.url.here")

def get_calendar_summary():
    resp = requests.get(ICS_URL)
    raw_ics = resp.text
    calendars = Calendar.parse_multiple(raw_ics)
    today = date.today()
    summary = []

    for cal in calendars:
        for event in cal.timeline.today():
            summary.append(f"{event.begin.format('HH:mm')} — {event.name}")

    return "\n".join(summary) if summary else "• No events today."

if __name__ == "__main__":
    print(get_calendar_summary())
