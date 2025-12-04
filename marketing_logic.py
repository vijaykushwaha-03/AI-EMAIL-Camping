import pandas as pd
import re
from typing import List, Dict, Optional

def validate_email(email: str) -> bool:
    """Basic email validation using regex."""
    if not isinstance(email, str):
        return False
    # Simple regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email.strip()))

def process_csv(file) -> pd.DataFrame:
    """
    Reads a CSV file and standardizes column names.
    Expected columns: Name, Email, Company (optional).
    """
    try:
        df = pd.read_csv(file)
        # Normalize column names to lowercase for easier matching
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Map common variations to standard names
        col_map = {
            'name': 'name', 'full name': 'name', 'fullname': 'name',
            'email': 'email', 'email address': 'email', 'mail': 'email',
            'company': 'company', 'company name': 'company', 'organization': 'company'
        }
        
        df.rename(columns=col_map, inplace=True)
        
        # Ensure required columns exist
        if 'email' not in df.columns:
            raise ValueError("CSV must contain an 'Email' column.")
        
        if 'name' not in df.columns:
            # If no name, use a default or empty
            df['name'] = ''
            
        if 'company' not in df.columns:
            df['company'] = ''

        # Clean emails
        df['email'] = df['email'].astype(str).str.strip()
        
        # Validate emails
        df['is_valid_email'] = df['email'].apply(validate_email)
        
        return df
    except Exception as e:
        raise ValueError(f"Error processing CSV: {str(e)}")

def get_recipient_data(df: pd.DataFrame) -> List[Dict]:
    """
    Extracts valid recipients from the DataFrame.
    Returns a list of dictionaries.
    """
    valid_df = df[df['is_valid_email']].copy()
    return valid_df.to_dict('records')
