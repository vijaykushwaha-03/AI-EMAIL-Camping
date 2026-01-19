import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client(provider: str):
    """
    Returns an OpenAI-compatible client based on the selected provider.
    """
    if provider == "OpenRouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = "https://openrouter.ai/api/v1"
        if not api_key:
            raise ValueError("OpenRouter API Key not found in .env")
        if "your-" in api_key.lower() or "..." in api_key:
            raise ValueError(f"Invalid API Key detected: '{api_key}'. Please update your .env file with your actual OpenRouter API key.")
        return OpenAI(base_url=base_url, api_key=api_key)
    
    elif provider == "Gemini":
        # Using OpenRouter to access Gemini models is often easiest if the user has an OpenRouter key.
        # However, if they have a direct Gemini key, we might use google-generativeai.
        # For this implementation, we'll assume OpenRouter usage for 'Gemini' models if selected there,
        # OR we can implement direct Gemini support. 
        # Given the user provided an OpenRouter key and said "GEMINI ALSO", 
        # let's support Gemini via OpenRouter for now as it's cleaner, 
        # but also allow for a direct OpenAI-compatible endpoint if they have one.
        # Actually, let's stick to the plan: use OpenAI client structure.
        # If the user wants direct Gemini, they usually need the google-generativeai lib.
        # Let's use OpenRouter for Gemini models as a primary path if 'provider' is OpenRouter.
        # If 'provider' is OpenAI, use standard.
        pass

    # Default to OpenAI
    # Default to OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API Key not found in .env")
    if "your-" in api_key.lower() or "..." in api_key:
        raise ValueError(f"Invalid API Key detected: '{api_key}'. Please update your .env file with your actual OpenAI API key.")
    return OpenAI(api_key=api_key)

def generate_email_template(prompt: str, max_tokens: int = 500, provider: str = "OpenAI", model: str = "gpt-4o-mini") -> dict:
    """
    Call the selected AI provider and return a structured dictionary for the email template.
    Expected keys: 'subject', 'title', 'body', 'cta_text'
    """
    try:
        client = get_client(provider)
        
        system_prompt = """
        You are a professional marketing copywriter. 
        You must output a valid JSON object with the following keys:
        - subject: The email subject line.
        - title: A catchy headline for the email body (2-5 words).
        - body: The main persuasive email content (2-3 paragraphs). HTML tags like <br> and <b> are allowed.
        - cta_text: A short, punchy call-to-action button text (2-4 words).
        
        Do not include markdown formatting (like ```json). Just return the raw JSON string.
        """
        
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )

        content = resp.choices[0].message.content.strip()
        
        # Clean up potential markdown code blocks if the model adds them
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        import json
        try:
            data = json.loads(content.strip())
            return data
        except json.JSONDecodeError:
            # Fallback if JSON fails
            return {
                "subject": "Exclusive Offer",
                "title": "Special Update",
                "body": content, # Return raw text as body
                "cta_text": "Learn More"
            }
            
            
    except Exception as e:
        # Re-raise the exception to be handled by the UI
        raise e