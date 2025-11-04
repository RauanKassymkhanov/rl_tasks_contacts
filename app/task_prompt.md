Implementation spec (must follow exactly):
- Use only: pandas, re, typing.Optional.
- Normalize name: strip, collapse internal whitespace to a single space.
- Normalize and validate email:
  - Convert to lowercase and strip.
  - Keep ONLY rows where email matches: ^[^@\s]+@[^@\s]+\.[A-Za-z]{2,10}$
  - Do NOT set invalid emails to an empty string; DROP those rows instead.
- Normalize phone to strict E.164:
  - Strip all characters except digits and a leading '+'.
  - If starts with '+': keep '+' + digits only; valid iff it matches ^\+\d{8,}$; else set to "".
  - If no '+':
    - Let CC map = {"US":"1","GB":"44","DE":"49","KZ":"7","FR":"33","ES":"34"}; default "US" if country is missing or unknown.
    - If country in {"GB","DE"} and the national number starts with a single leading '0', drop that one leading '0'.
    - If country == "US" and national number is 11 digits starting with '1', allow it as "+<11 digits>".
    - Else construct "+<CC><national_digits>".
    - After building, accept only if it matches ^\+\d{8,}$; otherwise set to "".
- After normalization, drop exact duplicates by (email, phone).
- Return columns in this exact order: ["name","email","phone","country"].
- Empty phones ("") are allowed; any non-empty phone must match ^\+\d{8,}$.

Output rules:
- Return only valid Python source code for student_solution.py.
- Do NOT wrap the code in Markdown code fences.
- Do NOT wrap the code in triple-quoted strings.
- No comments or prose; only imports and code.
