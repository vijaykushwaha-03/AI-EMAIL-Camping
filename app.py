import streamlit as st
import pandas as pd
import os
import tempfile
from marketing_logic import process_csv, get_recipient_data
from services.openai_services import generate_email_template
from services.email_services import send_email

st.set_page_config(page_title='AI Email Marketing Agent', layout='wide')

st.title('AI Email Marketing Agent')

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("Configuration")
    st.info("Ensure your .env file has valid SMTP and OpenAI credentials.")

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
            generated_email = generate_email_template(prompt)
            st.session_state['generated_email'] = generated_email
            st.success("Email generated!")

if 'generated_email' in st.session_state:
    st.subheader("Preview")
    email_content = st.text_area("Edit Email Content", st.session_state['generated_email'], height=300)
    st.session_state['generated_email'] = email_content # Update if edited

# --- Step 5: Send Emails ---
st.header("5. Send Emails")

if 'generated_email' in st.session_state and valid_recipients:
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
            personalized_body = st.session_state['generated_email'].replace("[Name]", recipient.get('name', 'there'))
            
            # Simple HTML wrapper
            html_body = f"<html><body><p>{personalized_body.replace(chr(10), '<br>')}</p></body></html>"
            
            subject = f"Regarding {product_name}" # You might want to make this customizable too
            
            success = send_email(subject, html_body, [recipient['email']], attachment_paths)
            
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
        
        # Cleanup temp files
        # (In a real app, you'd want more robust cleanup)