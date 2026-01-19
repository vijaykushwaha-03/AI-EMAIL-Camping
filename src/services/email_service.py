import os
import smtplib
import pandas as pd
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

def generate_html_email(title: str, body: str, cta_text: str, cta_link: str, company_name: str) -> str:
    """
    Generates a responsive HTML email string with the provided content.
    """
    # Convert newlines in body to <br> for HTML rendering
    formatted_body = body.replace('\\n', '<br>').replace('\n', '<br>')
    
    html_template = f"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta content="width=device-width,initial-scale=1" name="viewport" />
    <title>{title}</title>
    <style>
      body, p, h1, h2, h3, h4, h5, h6 {{ margin: 0; padding: 0; }}
      body {{ font-family: 'Arial', sans-serif; font-size: 16px; line-height: 1.5; background-color: #F4F4F4; color: #333333; }}
      .container {{ max-width: 600px; margin: 0 auto; background-color: #FFFFFF; border-radius: 8px; overflow: hidden; margin-top: 20px; margin-bottom: 20px; }}
      .header {{ background-color: #000000; color: #FFFFFF; padding: 20px; text-align: center; }}
      .content {{ padding: 30px 20px; text-align: center; }}
      .button {{ display: inline-block; padding: 12px 24px; background-color: #007BFF; color: #FFFFFF; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 20px; }}
      .footer {{ background-color: #F4F4F4; padding: 20px; text-align: center; font-size: 12px; color: #888888; }}
      @media only screen and (max-width: 600px) {{
        .container {{ width: 100%; border-radius: 0; margin-top: 0; margin-bottom: 0; }}
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <!-- Header / Company Name -->
      <div class="header">
        <h2>{company_name}</h2>
      </div>
      
      <!-- Main Content -->
      <div class="content">
        <h1 style="margin-bottom: 20px;">{title}</h1>
        <div style="text-align: left; margin-bottom: 30px;">
          {formatted_body}
        </div>
        
        <!-- CTA Button -->
        <a href="{cta_link}" class="button">{cta_text}</a>
      </div>
      
      <!-- Footer -->
      <div class="footer">
        &copy; {pd.Timestamp.now().year} {company_name}. All rights reserved.
      </div>
    </div>
  </body>
</html>
    """
    return html_template