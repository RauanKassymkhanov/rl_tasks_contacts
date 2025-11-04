import sys, re
from pathlib import Path
import google.generativeai as genai
from config import get_settings

root = Path(__file__).parent
prompt_path = root / "task_prompt.md"
target = root / "student_solution.py"

task_prompt = prompt_path.read_text(encoding="utf-8")

system = (
    "You are a coding agent. Output only a complete Python module that defines "
    "clean_contacts(df: pandas.DataFrame) -> pandas.DataFrame. "
    "No prose. No markdown. No comments. No code fences. No triple quotes. "
    "Imports allowed: pandas, re."
)
user = (
        task_prompt
        + "\n\nStrict output rule: return only valid Python code for student_solution.py. "
          "Do not wrap the code in markdown fences or triple quotes."
)


def sanitize_code(text: str) -> str:
    s = text.strip()

    # strip markdown code fences ``` or ```python
    s = re.sub(r"^\s*```(?:python)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```\s*$", "", s)

    # if entire output is a single triple-quoted string, unwrap it
    m = re.fullmatch(r'\s*(?P<q>("{3}|\'{3}))(.*?)(?P=q)\s*', s, flags=re.DOTALL)
    if m:
        s = m.group(3).strip()

    # if it still starts with a triple-quoted comment (docstring) that encloses everything, unwrap once
    if re.match(r'^\s*(?:r|u|f|rf|fr)?("{3}|\'{3})', s, flags=re.IGNORECASE):
        parts = re.split(r'("{3}|\'{3})', s, maxsplit=2)
        if len(parts) == 3:
            # parts = [before, quote, after]; before is likely empty
            after = parts[2]
            # drop up to the closing triple quotes
            end = re.search(r'("{3}|\'{3})', after)
            if end:
                s = after[end.end():].lstrip()

    return s


settings = get_settings()
if not settings.GEMINI_API_KEY:
    print("Set GEMINI_API_KEY in .env or environment")
    sys.exit(1)

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)

resp = model.generate_content([{"role": "user", "parts": [system + "\n\n" + user]}])
code = getattr(resp, "text", "") or ""
code = sanitize_code(code)

if "def clean_contacts(" not in code:
    print("Model did not return a clean_contacts implementation")
    sys.exit(1)

target.write_text(code, encoding="utf-8")
print("student_solution.py written")
