# AI Email Marketing Agent 🤖📧

> **Transform your email marketing with AI-powered personalization and beautiful HTML templates.**

Built by an AI enthusiast, this project has evolved from a simple meeting scheduler into a powerful **AI Email Marketing Agent**. It leverages advanced LLMs (via OpenRouter, OpenAI, or Gemini) to generate persuasive, personalized email content and injects it into professional HTML templates.

## Key Features ✨

-   **Multi-Provider AI Support**: Choose between **OpenAI**, **OpenRouter** (access to GPT-5.1, Claude 3.5, etc.), and **Gemini**.
-   **Custom HTML Templates**: Uses a professional, responsive HTML template ("Fresh Colors" style) for all emails.
-   **Dynamic Content Injection**: AI automatically generates the **Subject**, **Title**, **Body**, and **Call-to-Action** based on your campaign goals.
-   **Bulk Sending**: Upload a CSV of contacts and send personalized emails in batches (Test, 15, 50, 100, or All).
-   **Live Preview & Edit**: Review the AI-generated content and the final rendered HTML before sending.
-   **Attachment Support**: Send PDF brochures or images along with your emails.
-   **Detailed Reporting**: Download a CSV report of sent emails and their status.

## Installation 🛠️

### Prerequisites

-   Python 3.8 or higher
-   Gmail account with **App Password** enabled (for SMTP)
-   API Key for **OpenAI**, **OpenRouter**, or **Gemini**

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vijaykushwaha-03/AI-EMAIL-Camping.git
    cd AI-EMAIL-Camping
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # .\venv\Scripts\activate  # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your credentials:
    ```env
    # Email Configuration
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_app_specific_password
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587

    # AI Configuration (Add at least one)
    OPENAI_API_KEY=sk-...
    OPENROUTER_API_KEY=sk-or-...
    GEMINI_API_KEY=...
    ```

## Usage 🚀

1.  **Run the App:**
    ```bash
    streamlit run src/app.py
    ```
2.  **Configure AI:**
    -   In the sidebar, select your **AI Provider** (e.g., OpenRouter).
    -   Enter the **Model Name** (e.g., `openai/gpt-5.1` or `gpt-4o`).

3.  **Create Campaign:**
    -   **Upload Contacts**: Upload a CSV file with `Name` and `Email` columns.
    -   **Campaign Details**: Enter your Company Name, Product Name, Description, and Goal.
    -   **Generate Template**: Click "Generate Email Template". The AI will create a persuasive email.
    -   **Preview & Edit**: Review the generated text and the beautiful HTML preview. You can edit the Subject, Title, Body, and CTA text directly.

4.  **Send Emails:**
    -   Select a batch size (start with "Test (1 email)").
    -   Click **Send Emails**.
    -   Download the status report when finished.

## File Structure 📂

```
AI-EMAIL-Camping/
├── src/                        # Source code
│   ├── app.py                  # Main Streamlit application
│   ├── core/                   # Core business logic
│   │   ├── marketing.py        # CSV processing & logic
│   │   └── scheduler.py        # Scheduling logic
│   ├── services/               # External services
│   │   ├── email_service.py    # SMTP email sending
│   │   ├── ai_service.py       # AI integration
│   │   └── ics_service.py      # ICS file generation
│   └── templates/
│       └── custom_email_template.html  # HTML template
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
├── .env                        # Secrets (DO NOT COMMIT)
└── README.md                   # Documentation
```

## Contributing 🤝

Contributions are welcome! Feel free to submit pull requests for new features, bug fixes, or additional email templates.

---

**Made with ❤️ by an AI Enthusiast | Always Learning, Always Building**
