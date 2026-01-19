import streamlit as st
import pandas as pd
import os
import tempfile
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.marketing import process_csv, get_recipient_data
from src.services.ai_service import generate_email_template
from src.services.email_service import send_email

st.set_page_config(page_title='AI Email Marketing Agent', layout='wide')

st.title('AI Email Marketing Agent')

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("Configuration")
    st.info("Ensure your .env file has valid SMTP and AI credentials.")
    
    ai_provider = st.selectbox("Select AI Provider", ["OpenAI", "OpenRouter", "Gemini"])
    
    model_name = "gpt-4o-mini" # Default
    if ai_provider == "OpenAI":
        model_name = st.text_input("Model Name", "gpt-4o-mini")
    elif ai_provider == "OpenRouter":
        model_name = st.text_input("Model Name", "openai/gpt-5.1")
    elif ai_provider == "Gemini":
        model_name = st.text_input("Model Name", "google/gemini-pro")


# --- Step 1: Upload Contacts ---
st.header("1. Upload Contacts (CSV)")
uploaded_file = st.file_uploader("Upload CSV file (must contain 'Name' and 'Email' columns)", type=['csv'])

if uploaded_file:
    try:
        df = process_csv(uploaded_file)
        st.success(f"Loaded {len(df)} contacts.")
        st.dataframe(df.head())
        
        valid_recipients = get_recipient_data(df)
        st.write(f"Valid recipients: {len(valid_recipients)}")
    except Exception as e:
        st.error(f"Error processing CSV: {e}")
        valid_recipients = []
else:
    valid_recipients = []

# --- Step 2: Campaign Details ---
st.header("2. Campaign Details")
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Your Company Name")
    sender_name = st.text_input("Sender Name")
with col2:
    product_name = st.text_input("Product/Service Name")
    
product_description = st.text_area("Product/Service Description", height=100)
campaign_goal = st.text_input("Campaign Goal (e.g., Schedule a demo, Sign up for trial)", "Schedule a demo")

# --- Step 3: Attachments ---
st.header("3. Attachments")
uploaded_attachments = st.file_uploader("Upload Attachments (PDF, Images, etc.)", accept_multiple_files=True)

# --- Step 4: AI Email Generation ---
st.header("4. Generate Email Template")

if st.button("Generate Email Template"):
    if not company_name or not product_description:
        st.error("Please provide Company Name and Product Description.")
    else:
        prompt = f"""
        Write a professional and persuasive cold email for a marketing campaign.
        
        Sender: {sender_name} from {company_name}
        Product: {product_name}
        Description: {product_description}
        Goal: {campaign_goal}
        
        The email should be personalized (use [Name] as placeholder).
        Keep it concise, engaging, and professional.
        """
        with st.spinner("Generating email..."):
            # Now returns a dict
            ai_data = generate_email_template(prompt, provider=ai_provider, model=model_name)
            st.session_state['ai_data'] = ai_data
            st.success("Email generated!")

if 'ai_data' in st.session_state:
    st.subheader("Preview")
    
    # Allow editing the AI content
    with st.expander("Edit Content"):
        subject = st.text_input("Subject", st.session_state['ai_data'].get('subject', ''))
        title = st.text_input("Title", st.session_state['ai_data'].get('title', ''))
        body = st.text_area("Body", st.session_state['ai_data'].get('body', ''), height=200)
        cta_text = st.text_input("CTA Text", st.session_state['ai_data'].get('cta_text', ''))
        cta_link = st.text_input("CTA Link", "https://your-website.com") # Default or input
        
        # Update session state
        st.session_state['ai_data']['subject'] = subject
        st.session_state['ai_data']['title'] = title
        st.session_state['ai_data']['body'] = body
        st.session_state['ai_data']['cta_text'] = cta_text
        st.session_state['ai_data']['cta_link'] = cta_link

    # Render HTML
    try:
        with open("src/templates/custom_email_template.html", "r") as f:
            template_html = f.read()
            
        rendered_html = template_html.replace("{{ EMAIL_TITLE }}", title) \
                                     .replace("{{ EMAIL_BODY }}", body) \
                                     .replace("{{ CTA_TEXT }}", cta_text) \
                                     .replace("{{ CTA_LINK }}", cta_link) \
                                     .replace("{{ COMPANY_NAME }}", company_name)
        
        st.session_state['final_html'] = rendered_html
        
        st.subheader("HTML Preview")
        st.components.v1.html(rendered_html, height=600, scrolling=True)
        
    except FileNotFoundError:
        st.error("Template file not found. Please ensure 'templates/custom_email_template.html' exists.")


# --- Step 5: Send Emails ---
st.header("5. Send Emails")

if 'final_html' in st.session_state and valid_recipients:
    batch_size = st.selectbox("Select Batch Size", ["Test (1 email)", "15", "50", "100", "All"])
    
    if st.button("Send Emails"):
        # Determine number of emails to send
        if batch_size == "Test (1 email)":
            limit = 1
        elif batch_size == "All":
            limit = len(valid_recipients)
        else:
            limit = int(batch_size)
            
        recipients_to_send = valid_recipients[:limit]
        
        # Handle attachments
        attachment_paths = []
        if uploaded_attachments:
            temp_dir = tempfile.mkdtemp()
            for uploaded_file in uploaded_attachments:
                path = os.path.join(temp_dir, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                attachment_paths.append(path)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_log = []
        
        for i, recipient in enumerate(recipients_to_send):
            # Personalize email
            # Note: The template might not have [Name] placeholder in the body if AI didn't put it there.
            # But we can try to replace it if it exists in the rendered HTML.
            personalized_html = st.session_state['final_html'].replace("[Name]", recipient.get('name', 'there'))
            
            subject = st.session_state['ai_data'].get('subject', f"Regarding {product_name}")
            
            success = send_email(subject, personalized_html, [recipient['email']], attachment_paths)
            
            status_log.append({
                "Email": recipient['email'],
                "Name": recipient.get('name', ''),
                "Status": "Sent" if success else "Failed",
                "Timestamp": pd.Timestamp.now()
            })
            
            progress_bar.progress((i + 1) / len(recipients_to_send))
            
        st.success(f"Process completed. Attempted: {len(recipients_to_send)}")
        
        # Show status and download
        status_df = pd.DataFrame(status_log)
        st.dataframe(status_df)
        
        csv = status_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Status Report",
            csv,
            "email_campaign_status.csv",
            "text/csv",
            key='download-csv'
        )