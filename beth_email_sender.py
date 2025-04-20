# beth_email_sender.py

import os
import base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API send permission scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists("gmail_token.json"):
        creds = Credentials.from_authorized_user_file("gmail_token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("gmail_credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("gmail_token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def create_message_with_attachments(sender, recipient, subject, body, attachments=[]):
    message = MIMEMultipart()
    message["to"] = recipient
    message["from"] = sender
    message["subject"] = subject

    # Add the email body
    message.attach(MIMEText(body, "plain"))

    # Add attachments, if they exist
    for file_path in attachments:
        if not os.path.exists(file_path):
            continue
        with open(file_path, "rb") as f:
            mime_part = MIMEBase("application", "octet-stream")
            mime_part.set_payload(f.read())
            encoders.encode_base64(mime_part)
            mime_part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}"
            )
            message.attach(mime_part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def send_email_report(sender, recipient, subject, body):
    service = get_gmail_service()

    attachments = [
        "beth_temperature_plot.png",
        "beth_cloud_cover_plot.png",
        "beth_rain_plot.png",  # Will be skipped if missing
    ]

    message = create_message_with_attachments(sender, recipient, subject, body, attachments)
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"📬 Email sent! Message ID: {sent_message['id']}")
