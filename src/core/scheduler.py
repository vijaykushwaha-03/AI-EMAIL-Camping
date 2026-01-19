import os
import tempfile
from datetime import datetime
from src.services.ai_service import generate_email_template
from src.services.ics_service import create_ics_file
from src.services.email_service import send_email




def get_meeting_prompt(meeting_title: str, start_dt: datetime, end_dt: datetime,
                        duration: int, extra_notes: str = "") -> str:
    return f"""
    You are an executive assistant writing a concise, professional meeting invitation message.


    Meeting: {meeting_title}
    When: {start_dt.strftime('%A, %B %d, %Y')} at {start_dt.strftime('%I:%M %p')} – {end_dt.strftime('%I:%M %p')} ({duration} minutes)
    Notes: {extra_notes or 'None'}


    Write the email body only. Do not include sign-offs or script tags. Keep it friendly and clear.
    """.strip()




def generate_ai_email(prompt: str) -> str:
    ai_body = generate_email_template(prompt)


    # Simple cleaning to remove any script tags or JSON-LD
    cleaned = []
    for line in ai_body.splitlines():
        if line.strip().lower().startswith('<script'):
            break
        cleaned.append(line)


    email_text = '\n'.join([l.strip() for l in cleaned if l.strip()])
    if 'calendar invite' not in email_text.lower():
        email_text += '\n\nPlease find the calendar invite attached.'


    # Wrap into simple HTML body
    html_body = f"<html><body><p>{email_text.replace('\n', '<br>')}</p></body></html>"
    return html_body




def send_meeting_invite(subject: str, body: str, recipients: list[str], meeting_title: str,
                        start_dt: datetime, end_dt: datetime, extra_notes: str = "") -> bool:


    duration = int((end_dt - start_dt).total_seconds() // 60)
    prompt = get_meeting_prompt(meeting_title, start_dt, end_dt, duration, extra_notes)
    html_body = generate_ai_email(prompt)


    success = True
    for r in recipients:
        # create a temp file for each recipient to include their attendee address (helps RSVP tracking)
        fd, path = tempfile.mkstemp(suffix='.ics', prefix='invite_')
        os.close(fd)


        try:
            create_ics_file(
                title=meeting_title,
                description=extra_notes or body,
                start_dt=start_dt,
                end_dt=end_dt,
                organizer_email=os.getenv('EMAIL_ADDRESS'),
                attendee_email=r,
                filepath=path,
            )


            ok = send_email(subject, html_body, [r], attachment_path=path)
            success = success and ok


        finally:
            try:
                os.remove(path)
            except Exception:
                pass


    return success