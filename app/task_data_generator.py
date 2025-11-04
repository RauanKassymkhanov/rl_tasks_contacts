import random
import re
import pandas as pd

DOMAINS = ["example.com", "corp.io", "mail.org", "research.ai", "lab.kz", "data.de"]
COUNTRIES = ["US", "GB", "DE", "KZ", "FR", "ES", None]


def _messy_phone(e164: str) -> str:
    s = e164
    s = s.replace("+", "" if random.random() < 0.5 else "+")
    s = re.sub(r"(\d)", lambda m: m.group(1) + (" " if random.random() < 0.2 else ""), s)
    if random.random() < 0.3:
        s = "(" + s + ")"
    if random.random() < 0.3:
        s = s.replace(" ", "-")
    return s


def _fake_e164(country: str) -> str:
    cc = {"US": "1", "GB": "44", "DE": "49", "KZ": "7", "FR": "33", "ES": "34"}.get(country or "US", "1")
    rest = "".join(str(random.randint(0, 9)) for _ in range(7 + random.randint(0, 3)))
    return f"+{cc}{rest}"


def make_noisy_df(n: int, seed: int) -> pd.DataFrame:
    random.seed(seed)
    rows = []
    for i in range(n):
        country = random.choice(COUNTRIES)
        name = f"  Alice   {i}  " if random.random() < 0.5 else f"Bob   {i}   "
        if random.random() < 0.75:
            local = f"user{i}"
            domain = random.choice(DOMAINS)
            email = f"{local}@{domain}"
            if random.random() < 0.3:
                email = email.upper()
        else:
            email = f"user{i}@@bad" if random.random() < 0.5 else f"user{i}@nodot"
        if random.random() < 0.7:
            e164 = _fake_e164(country or "US")
            phone = _messy_phone(e164)
        else:
            phone = "" if random.random() < 0.5 else "abcd123"
        rows.append({"name": name, "email": email, "phone": phone, "country": country})
    df = pd.DataFrame(rows)
    if n >= 6:
        df = pd.concat([df, df.sample(3, random_state=seed)], ignore_index=True)
    return df
