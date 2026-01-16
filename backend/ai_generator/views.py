from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
import json


@api_view(['POST'])
def generate_email(request):
    """Generate email content using AI"""
    prompt = request.data.get('prompt')
    provider = request.data.get('provider', 'OpenRouter')
    model = request.data.get('model', 'openai/gpt-4o-mini')
    
    if not prompt:
        return Response(
            {'error': 'Prompt is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if API keys are configured
    if provider == 'OpenRouter' and not settings.OPENROUTER_API_KEY:
        return Response(
            {'error': 'OpenRouter API key not configured in .env file'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    elif provider == 'OpenAI' and not settings.OPENAI_API_KEY:
        return Response(
            {'error': 'OpenAI API key not configured in .env file'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Get client based on provider
        if provider == 'OpenRouter':
            api_key = settings.OPENROUTER_API_KEY
            base_url = "https://openrouter.ai/api/v1"
            client = OpenAI(base_url=base_url, api_key=api_key)
        else:
            api_key = settings.OPENAI_API_KEY
            client = OpenAI(api_key=api_key)
        
        system_prompt = """
        You are a professional marketing copywriter. 
        You must output a valid JSON object with the following keys:
        - subject: The email subject line.
        - title: A catchy headline for the email body (2-5 words).
        - body: The main persuasive email content (2-3 paragraphs). HTML tags like <br> and <b> are allowed.
        - cta_text: A short, punchy call-to-action button text (2-4 words).
        
        Do not include markdown formatting (like ```json). Just return the raw JSON string.
        """
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up markdown if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        try:
            data = json.loads(content.strip())
            return Response(data)
        except json.JSONDecodeError:
            return Response({
                'subject': 'Your Special Offer',
                'title': 'Exclusive Deal',
                'body': content,
                'cta_text': 'Learn More'
            })
            
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error message for common issues
        if '401' in error_msg or 'Unauthorized' in error_msg:
            error_msg = f"API Authentication failed. Please check your {provider} API key in .env file."
        elif 'User not found' in error_msg:
            error_msg = f"Invalid {provider} API key. Please update OPENROUTER_API_KEY in .env file."
        
        return Response(
            {'error': error_msg},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
