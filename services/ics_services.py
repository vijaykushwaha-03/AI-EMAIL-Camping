from datetime import datetime, timezone
import os
import uuid


ICS_TEMPLATE = """BEGIN:VCALENDAR
PRODID:-//YourCompany//AI Scheduler//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:REQUEST
{event_block}
END:VCALENDAR
"""


EVENT_TEMPLATE = """BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}
ORGANIZER:mailto:{organizer}
ATTENDEE;CN={attendee_name};RSVP=TRUE:mailto:{attendee}
END:VEVENT
"""

def _format_dt(dt: datetime) -> str:
    """Return UTC formatted datetime for ICS (YYYYMMDDTHHMMSSZ)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc.strftime("%Y%m%dT%H%M%SZ")

def create_ics_file(
title: str,
description: str,
start_dt: datetime,
end_dt: datetime,
organizer_email: str,
attendee_email: str,
filepath: str,
attendee_name: str = "Attendee",
) -> str:
    """Create a standards-compliant .ics file for a meeting invite.


    Returns the path to the saved .ics file (same as filepath argument).
    """
    if not all([title, start_dt, end_dt, organizer_email, attendee_email, filepath]):
        raise ValueError("title, start_dt, end_dt, organizer_email, attendee_email and filepath are required")
    
    uid = f"{uuid.uuid4()}"
    dtstamp = _format_dt(datetime.utcnow())
    dtstart = _format_dt(start_dt)
    dtend = _format_dt(end_dt)

    event_block = EVENT_TEMPLATE.format(
        uid=uid,
        dtstamp=dtstamp,
        dtstart=dtstart,
        dtend=dtend,
        summary=title.replace('\n', ' '),
        description=(description or "").replace('\n', '\\n'),
        organizer=organizer_email,
        attendee=attendee_email,
        attendee_name=attendee_name,
        )
    ics = ICS_TEMPLATE.format(event_block=event_block)
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(ics)


    return filepath