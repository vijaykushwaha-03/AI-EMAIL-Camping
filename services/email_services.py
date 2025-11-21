import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


load_dotenv()


EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

def _make_message(subject: str, html_body: str, recipients: list[str], ics_bytes: bytes | None = None) -> MIMEMultipart:
    """Constructs an email message with HTML body and optional calendar attachment. Returns MIMEMultipart."""


    if not isinstance(recipients, list):
        recipients = [recipients]


    outer = MIMEMultipart('mixed')
    outer['Subject'] = subject
    outer['From'] = EMAIL_ADDRESS
    outer['To'] = ', '.join(recipients)


    # Alternative: HTML body (for email clients)
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(html_body, 'html'))


    outer.attach(alt)


    if ics_bytes:
        part = MIMEBase('text', 'calendar', method='REQUEST', name='invite.ics')
        part.set_payload(ics_bytes)
        encoders.encode_base64(part)


        # Important headers to trigger Accept/Decline UI in Gmail/Outlook
        part.add_header('Content-Type', 'text/calendar; method=REQUEST; charset=UTF-8')
        part.add_header('Content-Disposition', 'attachment; filename="invite.ics"')
        part.add_header('Content-Class', 'urn:content-classes:calendarmessage')


        outer.attach(part)


    return outer

def send_email(subject: str, body_html: str, to_emails: list[str], attachment_path: str | None = None) -> bool:
    """Send email to one or many recipients. If attachment_path provided, read and attach as calendar invite."""


    recipients = to_emails if isinstance(to_emails, list) else [to_emails]


    ics_bytes = None
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            ics_bytes = f.read()


    msg = _make_message(subject, body_html, recipients, ics_bytes)


    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        server.quit()
        print('Email sent to:', recipients)
        return True
    except Exception as e:
        print('Error sending email:', e)
        return False