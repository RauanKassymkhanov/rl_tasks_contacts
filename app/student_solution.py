import pandas as pd
import re
from typing import Optional

def clean_contacts(df: pd.DataFrame) -> pd.DataFrame:
    result_df = df.copy()
    
    result_df['name'] = result_df['name'].astype(str).str.strip()
    result_df['name'] = result_df['name'].apply(lambda x: re.sub(r'\s+', ' ', x))
    
    result_df['email'] = result_df['email'].astype(str).str.strip().str.lower()
    email_pattern = r'^[^@\s]+@[^@\s]+\.[A-Za-z]{2,10}$'
    result_df = result_df[result_df['email'].str.match(email_pattern, na=False)]
    
    cc_map = {"US": "1", "GB": "44", "DE": "49", "KZ": "7", "FR": "33", "ES": "34"}
    
    def normalize_phone(phone, country):
        if pd.isna(phone):
            return ""
        
        phone = str(phone)
        phone = re.sub(r'[^\d+]', '', phone)
        
        if phone.startswith('+'):
            phone = '+' + re.sub(r'[^\d]', '', phone[1:])
            if re.match(r'^\+\d{8,}$', phone):
                return phone
            else:
                return ""
        else:
            digits = re.sub(r'[^\d]', '', phone)
            if not digits:
                return ""
            
            if pd.isna(country) or country not in cc_map:
                country = "US"
            
            cc = cc_map[country]
            
            if country in ["GB", "DE"] and digits.startswith('0'):
                digits = digits[1:]
            
            if country == "US" and len(digits) == 11 and digits.startswith('1'):
                final_phone = '+' + digits
            else:
                final_phone = '+' + cc + digits
            
            if re.match(r'^\+\d{8,}$', final_phone):
                return final_phone
            else:
                return ""
    
    result_df['phone'] = result_df.apply(lambda row: normalize_phone(row['phone'], row['country']), axis=1)
    
    result_df = result_df.drop_duplicates(subset=['email', 'phone'])
    
    return result_df[['name', 'email', 'phone', 'country']]