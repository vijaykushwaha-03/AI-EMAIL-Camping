import unittest
import pandas as pd
import io
from marketing_logic import process_csv, validate_email

class TestMarketingLogic(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email(""))
        
    def test_csv_processing(self):
        csv_content = "Name,Email,Company\nJohn Doe,john@example.com,Acme Corp\nJane Smith,jane@test.com,Beta Inc"
        file = io.StringIO(csv_content)
        df = process_csv(file)
        
        self.assertEqual(len(df), 2)
        self.assertIn('name', df.columns)
        self.assertIn('email', df.columns)
        self.assertTrue(df.iloc[0]['is_valid_email'])

if __name__ == '__main__':
    unittest.main()
