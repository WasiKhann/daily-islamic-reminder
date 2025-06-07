import requests
from bs4 import BeautifulSoup
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

NOTION_URL = "https://wasikhan.notion.site/Most-imp-Notion-page-will-take-me-into-jannah-IA-1b51284063e7805fb121cac3d3104bc3?source=copy_link"

SENDER_EMAIL = os.getenv("EMAIL_USER")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def fetch_notion_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator='\n')
    reminders = [line.strip() for line in text.split('\n\n') if line.strip()]
    return reminders

def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

def main():
    reminders = fetch_notion_content(NOTION_URL)
    if reminders:
        selected_reminder = random.choice(reminders)
        today = datetime.date.today().strftime("%B %d, %Y")
        subject = f"📿 Islamic Reminder for {today}"
        send_email(subject, selected_reminder)
    else:
        print("No reminders found.")

if __name__ == "__main__":
    main()
