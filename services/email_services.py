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

def _make_message(subject: str, html_body: str, recipients: list[str], attachment_paths: list[str] | None = None) -> MIMEMultipart:
    """Constructs an email message with HTML body and optional attachments. Returns MIMEMultipart."""


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


    if attachment_paths:
        for path in attachment_paths:
            try:
                with open(path, 'rb') as f:
                    file_data = f.read()
                    filename = os.path.basename(path)
                
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_data)
                encoders.encode_base64(part)
                
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                outer.attach(part)
            except Exception as e:
                print(f"Failed to attach file {path}: {e}")


    return outer

def send_email(subject: str, body_html: str, to_emails: list[str], attachment_paths: list[str] | None = None) -> bool:
    """Send email to one or many recipients. If attachment_paths provided, read and attach files."""


    recipients = to_emails if isinstance(to_emails, list) else [to_emails]


    msg = _make_message(subject, body_html, recipients, attachment_paths)


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