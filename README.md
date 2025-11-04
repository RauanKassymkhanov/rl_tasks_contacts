# RL Task: Contacts Cleaning

## Setup (uv)
```bash
uv venv
. .venv/bin/activate
uv add pandas
```

## Run
```bash
uv run python app/run_once.py
uv run python app/run_many.py
```
## Optional LLM Integration (Anthropic)
```bash
uv add anthropic pydantic pydantic-settings
cp .env.example .env
uv run python app/llm_harness_anthropic.py
uv run python app/run_many.py
```
## Local Harness (no API)
# Put your code into candidate_solution.py implementing clean_contacts
```bash
uv run python app/llm_harness_local.py
```
