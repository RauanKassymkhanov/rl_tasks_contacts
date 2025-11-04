import sys, re
from pathlib import Path
from anthropic import Anthropic
from anthropic._exceptions import BadRequestError, AuthenticationError, APIStatusError
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
    s = re.sub(r"^\s*```(?:python)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```\s*$", "", s)
    m = re.fullmatch(r'\s*(?P<q>("{3}|\'{3}))(.*?)(?P=q)\s*', s, flags=re.DOTALL)
    if m:
        s = m.group(3).strip()
    if re.match(r'^\s*(?:r|u|f|rf|fr)?("{3}|\'{3})', s, flags=re.IGNORECASE):
        parts = re.split(r'("{3}|\'{3})', s, maxsplit=2)
        if len(parts) == 3:
            after = parts[2]
            end = re.search(r'("{3}|\'{3})', after)
            if end:
                s = after[end.end():].lstrip()
    return s


settings = get_settings()
if not settings.ANTHROPIC_API_KEY:
    print("Set ANTHROPIC_API_KEY in .env or environment")
    sys.exit(1)

client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

try:
    resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=2000,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    code = "".join([p.text for p in resp.content if getattr(p, "type", None) == "text"])
    code = sanitize_code(code)
    if "def clean_contacts(" not in code:
        print("Model did not return a clean_contacts implementation")
        sys.exit(1)
    target.write_text(code, encoding="utf-8")
    print("student_solution.py written")
except (BadRequestError, AuthenticationError, APIStatusError) as e:
    print(f"Anthropic API error: {e}")
    sys.exit(1)
