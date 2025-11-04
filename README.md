# RL Task: Contacts Cleaning

**Summary:** 
A small, self-contained RL-style task for LLMs. The model must implement `clean_contacts(df)` using only `pandas` and `re`: normalize names, validate emails, convert phones to strict E.164, drop duplicates, and return the exact schema. A property-based grader checks every requirement; you can run locally or generate a solution via an LLM harness.


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
