import pandas as pd
import re

def clean_contacts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["name"] = df["name"].str.strip().str.replace(r"\s+", " ", regex=True)

    def is_valid_email(email):
        if not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$"
        return bool(re.match(pattern, email)) and email.count('@') == 1

    df["email"] = df["email"].str.lower()
    df = df[df["email"].apply(is_valid_email)]

    def normalize_phone(row):
        phone = row["phone"]
        country = row["country"]
        if not isinstance(phone, str):
            return ""

        phone = "".join(filter(str.isdigit, phone))

        if not phone:
            return ""

        if phone.startswith("+"):
            plus_removed = phone[1:]
            if len(plus_removed) < 7 or len(plus_removed) > 15:
                return ""
            return "+" + plus_removed
        else:
            if not isinstance(country, str) or len(country) != 2:
                return ""
            
            if country.upper() == "US":
                if len(phone) == 10:
                    return "+1" + phone
                elif len(phone) == 11 and phone.startswith("1"):
                    return "+" + phone
                else:
                    return ""
            
            return ""

    df["phone"] = df.apply(normalize_phone, axis=1)

    def is_valid_e164(phone):
        if not phone:
            return True
        pattern = r"^\+\d{7,15}$"
        return bool(re.match(pattern, phone))
    
    df = df[df.apply(lambda row: is_valid_e164(row["phone"]), axis=1) | (df['phone'] == "")]

    df = df.drop_duplicates(subset=["email", "phone"], keep="first")

    return df[["name", "email", "phone", "country"]]