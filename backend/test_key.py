import os
from openai import OpenAI
from dotenv import load_dotenv

# Try loading from current directory first, then parent
if os.path.exists('.env'):
    load_dotenv('.env')
elif os.path.exists('../.env'):
    load_dotenv('../.env')

api_key = os.getenv('OPENROUTER_API_KEY')
print(f"Loaded Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: Key not found")
    exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

try:
    print("Testing connection...")
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say hello"}
        ],
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"FAILED: {e}")
