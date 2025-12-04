import os
from openai import OpenAI
from dotenv import load_dotenv
# opne ai
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_email_template(prompt: str, max_tokens: int = 300) -> str:
    """Call OpenAI and return a clean textual email body. You can replace engine/model as needed."""
    if not OPENAI_API_KEY:
        # Fallback short canned response to allow offline testing
        return "This meeting is scheduled. Please find the calendar invite attached."

    resp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes professional meeting emails."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.2,
    )

    text = resp.choices[0].message.content.strip()
    return text