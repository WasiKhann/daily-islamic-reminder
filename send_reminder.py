from notion_client import Client
import os
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

# Load secrets
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

def fetch_plain_text_blocks(page_id):
    blocks = notion.blocks.children.list(page_id).get("results")
    content = []
    for block in blocks:
        if block["type"] in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
            text = block[block["type"]]["rich_text"]
            line = "".join([t["plain_text"] for t in text])
            if line.strip():
                content.append(line.strip())
    return content

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

def main():
    entries = fetch_plain_text_blocks(NOTION_PAGE_ID)
    if not entries:
        print("No content found.")
        return
    chosen = random.choice(entries)
    subject = f"📿 Islamic Reminder for {datetime.date.today().strftime('%B %d, %Y')}"
    send_email(subject, chosen)

if __name__ == "__main__":
    main()
