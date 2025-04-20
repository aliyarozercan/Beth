# Beth
A personal daily assistant that emails weather, tasks, and more.


# 🧠 Beth - Your Personal Daily Assistant

Beth is a personal assistant script that sends you a daily email report every morning at 7:00 AM with:

- 📅 **Today and Tomorrow's Calendar Events**
- ✅ **Google Tasks** (Due Today and Upcoming)
- 🌤️ **Hourly Weather Forecast**
- 📈 **Crypto Market Trends**

The goal is to have a gentle, useful email start your day — with no fluff and no distractions.

---

## 📬 What You’ll Get

```text
Subject: 🗓️ Beth's Daily Report — Monday, April 21, 2025

Hi! 

Here's your daily scoop from Beth ☀️

📅 Calendar:
• Meeting with Emma — Monday, Apr 21
• Doctor Appointment — Tuesday, Apr 22

✅ Tasks:
• Buy groceries — Monday, Apr 21
• Finish report — Tuesday, Apr 22

🌤️ Weather (08:00–22:00):
08:00 → 13.7°C - 11.9°C - 0% ☁️ - 0% 🌧️ | ☀️ Looks clear!
...

📈 Markets:
📉 Bitcoin: $84,635.25 (-0.86%) in last 24h
📈 Solana: $139.10 (+0.01%) in last 24h
```

---

## ⚙️ Setup & Configuration

### 1. Clone the Project
```bash
git clone https://github.com/YOUR_USERNAME/beth.git
cd beth
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Enable Required APIs in Google Cloud Console
- Gmail API
- Google Calendar API
- Google Tasks API

Create OAuth 2.0 credentials:
- Type: **Desktop App**
- Add yourself to **Test Users** under OAuth consent screen settings

### 4. Add Credentials
Save downloaded `credentials.json` as:
```bash
./gmail_credentials.json        # for email sending
./task_credentials.json         # for tasks access
./calendar_credentials.json     # for calendar access
```

### 5. First-Time Auth
Run manually to authenticate and store tokens:
```bash
python beth_daily_report.py
```

### 6. Schedule via Cron
```bash
crontab -e
# Add the line below to run at 7:00 AM daily
0 7 * * * /path/to/venv/bin/python /path/to/beth/beth_daily_report.py
```

---

## 🔐 Privacy & Security
Beth is for **personal use only**. Your Google credentials are stored locally on your machine and never transmitted or shared. No data is stored outside your device.

---

## ✨ Planned Features
- Daily affirmations
- Habit tracking summaries
- Voice-enabled daily report reading

---

## 🤝 License
MIT License — use it, remix it, make it your own!

---

## 🧠 Inspired by
The joy of starting the day with clarity and purpose.

---

Have fun with Beth 💌 and let her take care of your mornings!
