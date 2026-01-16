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

## Installation & Running 🛠️

You can run this project using **Docker** (recommended for production/clean environments) or **Locally** (for development).

### Prerequisites

-   **Docker** (if using Docker)
-   **Python 3.11+** (if running locally)
-   **Node.js 18+** (if running locally)
-   API Key for **OpenAI**, **OpenRouter**, or **Gemini**

### Configuration
1.  Copy `.env.example` to `.env` in the root directory.
    ```bash
    cp .env.example .env
    ```
2.  Fill in your API keys and email credentials in `.env`.

### Option 1: Run with Docker 🐳
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Option 2: Run Locally (Win-Only Script) 🏃‍♂️
We provide a PowerShell script to automate the setup (venv creation, dependencies, migrations) and startup.

1.  **Run the script:**
    ```powershell
    .\run_local.ps1
    ```
    This will open two new terminal windows: one for the Django backend and one for the React frontend.

- Frontend: http://localhost:5173
- Backend: http://localhost:8000/admin

### Option 3: Run Locally (Manual) 👨‍💻
If you prefer to run commands manually:

**Backend:**
```bash
cd backend
python -m venv venv
# Activate venv (Windows: .\venv\Scripts\activate, Unix: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## File Structure 📂

```
AI-EMAIL-Camping/
├── backend/                    # Django API
│   ├── campaigns/              # Campaign management
│   ├── contacts/               # Contact management
│   ├── ai_generator/           # AI content generation
│   └── config/                 # Project settings
├── frontend/                   # React + Vite UI
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   └── App.tsx
├── legacy_prototype/           # Old Streamlit version
├── run_local.ps1               # Local run automation script
├── docker-compose.yml          # Container orchestration
└── README.md                   # Documentation
```

## Contributing 🤝

Contributions are welcome! Feel free to submit pull requests for new features, bug fixes, or additional email templates.

---

**Made with ❤️ by an AI Enthusiast | Always Learning, Always Building**
