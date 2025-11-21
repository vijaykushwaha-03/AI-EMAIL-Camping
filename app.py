import streamlit as st
from datetime import datetime, time, timedelta
import pytz
from scheduler_logic import get_meeting_prompt, generate_ai_email, send_meeting_invite


st.set_page_config(page_title='AI Meeting Scheduler', layout='centered')


st.title('AI Meeting Scheduler')


meeting_title = st.text_input('Meeting Title', 'Team Sync')
meeting_date = st.date_input('Date', datetime.today())
meeting_time = st.time_input('Start time', time(14, 0))
duration = st.selectbox('Duration (minutes)', [15, 30, 45, 60], index=1)
recipients_raw = st.text_input('Recipient emails (comma separated)', '')
extra_notes = st.text_area('Notes (optional)')


if st.button('Generate Email'):
    start_dt_local = datetime.combine(meeting_date, meeting_time)
    end_dt_local = start_dt_local + timedelta(minutes=duration)

    # convert local (assumed Asia/Kolkata) to UTC for ICS
    ist = pytz.timezone('Asia/Kolkata')
    start_dt = ist.localize(start_dt_local).astimezone(pytz.utc)
    end_dt = ist.localize(end_dt_local).astimezone(pytz.utc)

    prompt = get_meeting_prompt(meeting_title, start_dt_local, end_dt_local, duration, extra_notes)
    st.session_state['generated'] = generate_ai_email(prompt)
    st.success('Email generated!')

if 'generated' in st.session_state:
    st.markdown('**Preview email (HTML)**')
    st.code(st.session_state['generated'])

if st.button('Send Invite'):
    recipients = [r.strip() for r in recipients_raw.split(',') if r.strip()]
    if not recipients:
        st.error('Provide at least one recipient')
    else:
        start_dt_local = datetime.combine(meeting_date, meeting_time)
        end_dt_local = start_dt_local + timedelta(minutes=duration)
        ist = pytz.timezone('Asia/Kolkata')
        start_dt = ist.localize(start_dt_local).astimezone(pytz.utc)
        end_dt = ist.localize(end_dt_local).astimezone(pytz.utc)

        ok = send_meeting_invite(
            meeting_title, 
            st.session_state.get('generated', ''), 
            recipients,
            meeting_title, 
            start_dt, 
            end_dt, 
            extra_notes
        )
        if ok:
            st.success('Meeting invite sent successfully!')
        else:
            st.error('Failed to send meeting invite. Check your email configuration.')