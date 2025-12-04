# AI Meeting Scheduler 🤖📅

> Built by an AI enthusiast who is always ready to learn and implement cutting-edge AI agent technologies. This project showcases the power of AI-driven automation in everyday business workflows.

## About Me 👨‍💻





he

I'm an AI enthusiast passionate about leveraging artificial intelligence to solve real-world problems. I'm constantly learning and implementing new AI agent technologies to create intelligent, automated solutions that make life easier. This AI Meeting Scheduler is one of my projects that combines multiple AI capabilities into a seamless user experience.

## Project Description

The AI Meeting Scheduler is an intelligent automation tool that revolutionizes how we schedule meetings. Instead of manually crafting meeting invitations, this AI-powered application generates professional, contextual meeting emails using OpenAI's advanced language models. It seamlessly integrates with email systems to send calendar invites, making meeting coordination effortless.

**Key Highlights:**
- **AI-Powered Email Generation**: Uses OpenAI GPT models to create personalized, professional meeting invitations
- **Automated Calendar Integration**: Generates and sends industry-standard .ics calendar files
- **Smart Timezone Handling**: Automatically converts between local time and UTC for global compatibility
- **User-Friendly Interface**: Built with Streamlit for an intuitive, modern web experience
- **Multi-Recipient Support**: Send meeting invites to multiple attendees simultaneously

## Features

✨ **AI Email Generation** - Leverages OpenAI to craft professional meeting invitation emails  
📧 **Email Integration** - Sends emails via SMTP with calendar attachments  
📅 **Calendar Files** - Creates standards-compliant .ics files for all calendar applications  
🌍 **Timezone Support** - Handles Asia/Kolkata to UTC conversion seamlessly  
👥 **Multiple Recipients** - Invite multiple attendees with a single click  
👀 **Email Preview** - Review AI-generated content before sending  
🎨 **Clean UI** - Intuitive Streamlit interface for easy interaction

## Installation

### Prerequisites
- Python 3.8 or higher
- Gmail account with app-specific password enabled
- OpenAI API key

### Step-by-Step Setup

1. **Clone or download the repository:**
   ```bash
   cd path/to/your/folder
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   - Copy `.env.example` to `.env`
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your credentials:
     - `EMAIL_ADDRESS`: Your Gmail address
     - `EMAIL_PASSWORD`: Your Gmail app-specific password ([How to generate](https://support.google.com/accounts/answer/185833))
     - `OPENAI_API_KEY`: Your OpenAI API key ([Get it here](https://platform.openai.com/api-keys))
     - `SMTP_HOST`: smtp.gmail.com (default)
     - `SMTP_PORT`: 587 (default)

6. **Run the application:**
   ```bash
   streamlit run app.py
   ```

7. **Access the app:**
   - Open your browser and navigate to `http://localhost:8501`

## Usage

1. Enter meeting details:
   - Meeting title
   - Date and time
   - Duration
   - Recipient email addresses (comma-separated)
   - Optional notes

2. Click "Generate Email" to preview the AI-generated invitation

3. Click "Send Invite" to send the meeting invite with calendar attachment

## File Structure

```
Agent/
│
├── app.py                      # Main Streamlit application
├── scheduler_logic.py          # Core scheduling and AI logic
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (private)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
│
└── services/
    ├── email_services.py      # Email sending via SMTP
    ├── ics_services.py        # Calendar .ics file generation
    └── openai_services.py     # OpenAI API integration
```

## Technologies Used

- **Streamlit** - Modern web UI framework
- **OpenAI GPT-4** - AI-powered email generation
- **Python SMTP** - Email delivery
- **pytz** - Timezone management
- **iCalendar** - Standard calendar format

## Important Notes

⚠️ **Gmail Security**: Gmail requires an app-specific password for SMTP access. Regular passwords won't work.  
📧 **Calendar Format**: Invites are sent as .ics attachments compatible with all major calendar apps (Google Calendar, Outlook, Apple Calendar)  
🌏 **Timezone**: Default timezone is set to Asia/Kolkata. Modify in `app.py` if needed.  
🔒 **Security**: Never commit your `.env` file to version control. It contains sensitive credentials.

## Troubleshooting

**Email not sending?**
- Verify your Gmail app-specific password is correct
- Ensure `SMTP_HOST` is set to `smtp.gmail.com` (not your email address)
- Check that 2-factor authentication is enabled on your Gmail account

**AI not generating emails?**
- Verify your OpenAI API key is valid and has credits
- Check your internet connection

**Package installation errors?**
- Ensure you're using Python 3.8 or higher
- Try upgrading pip: `python -m pip install --upgrade pip`

## Future Enhancements

- 🔄 Support for other email providers (Outlook, Yahoo, etc.)
- 🗓️ Integration with Google Calendar API
- 🔔 Meeting reminders and follow-ups
- 📊 Meeting analytics and scheduling insights
- 🌐 Support for multiple timezones
- 💬 Multi-language support

## Contributing

As an AI enthusiast always eager to learn, I welcome contributions, suggestions, and feedback! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Share your use cases

## License

This project is open-source and available for learning and implementation purposes.

---

**Made with ❤️ by an AI Enthusiast | Always Learning, Always Building**
