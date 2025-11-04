## Task: Clean & Normalize Contacts (Phones + Emails) and Filter by Rules

You are given a CSV file of noisy contacts with columns:
- `name` (string, may contain leading/trailing/multiple spaces)
- `email` (string, may be invalid or mixed-case)
- `phone` (string, in many messy formats, may be missing)
- `country` (ISO 2-letter like "US", "GB", "DE", "KZ", may be missing)

Goal: Write a Python function `clean_contacts(df)` that:
1. Trims whitespace in `name` and collapses internal multiple spaces to a single space.
2. Lowercases `email`, and keeps only rows where `email` is a valid RFC-like pattern:
   must contain exactly one `@`; a non-empty local part; a domain with at least one dot and TLD 2–10 letters.
3. Normalizes `phone` into E.164 (e.g., `+14155552671`) using `country` as default region if the number lacks a `+` prefix.
   If impossible to parse → set `phone` to empty string `""`.
4. Drops exact duplicates by the pair (`email`, `phone`) after normalization.
5. Returns a new DataFrame with columns exactly in order:
   `["name", "email", "phone", "country"]`.

Filtering requirement:
Return only rows that satisfy BOTH:
- `email` valid (as specified above), AND
- If `phone` is non-empty, it MUST be valid E.164; rows with empty `phone` are allowed.

Implementation rules:
- You may use `pandas` and `re`. No external phone libraries.
- Your function will be imported as `from student_solution import clean_contacts`.
- Do not read or write files in your function; you receive a pandas DataFrame and must return a DataFrame.
- Your function must be deterministic for a given input.
