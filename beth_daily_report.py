# beth_daily_report.py

from ics_pull import get_calendar_summary
from tasks_pull import get_todays_tasks
from weather_pull import get_weather_forecast
from market_pull2 import get_market_summary
from beth_email_sender import send_email_report
from datetime import datetime
import os

def compose_beth_email(calendar, tasks, weather, markets):
    today = datetime.now().strftime("%A, %B %d, %Y")

    return f"""Subject: 🗓️ Beth's Daily Report — {today}

Hi there! 

Here's your daily scoop from Beth ☀️

──────────────────────────────
📅 Calendar:
──────────────────────────────
{calendar.strip() or "• No events today."}


──────────────────────────────
✅ Tasks:
──────────────────────────────
{tasks.strip() or "• No tasks for today."}


──────────────────────────────
🌤️ Weather:
──────────────────────────────
{weather.strip()}


──────────────────────────────
📈 Markets:
──────────────────────────────
{markets.strip()}


—
🧠 Beth | Your Personal Daily Assistant
"""

# ✨ Pull data
calendar_summary = get_calendar_summary()
tasks_summary = get_todays_tasks()
weather_summary = get_weather_forecast()
market_summary = get_market_summary()

# ✨ Compose the report
final_report = compose_beth_email(
    calendar=calendar_summary,
    tasks=tasks_summary,
    weather=weather_summary,
    markets=market_summary
)

# ✨ Save to text file
with open("beth_report.txt", "w") as f:
    f.write(final_report)

print("✅ Beth's daily report written to 'beth_report.txt'")

# 📬 Email Configuration (replace with your own .env variables or config)
SENDER_EMAIL = os.getenv("BETH_SENDER_EMAIL", "your.email@example.com")
RECIPIENT_EMAIL = os.getenv("BETH_RECIPIENT_EMAIL", "recipient@example.com")

send_email_report(
    sender=SENDER_EMAIL,
    recipient=RECIPIENT_EMAIL,
    subject="🗓️ Beth's Daily Report — " + datetime.now().strftime("%A, %B %d, %Y"),
    body=final_report
)

