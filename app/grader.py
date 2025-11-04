import re
import pandas as pd
from task_data_generator import make_noisy_df
from importlib import import_module

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,10}$")
E164_RE = re.compile(r"^\+\d{8,}$")


def _is_valid_email(s: str) -> bool:
    return bool(EMAIL_RE.match(s or ""))


def _is_valid_e164(s: str) -> bool:
    return (s == "") or bool(E164_RE.match(s))


def grade_one(seed: int = 0, n: int = 60) -> dict:
    df0 = make_noisy_df(n=n, seed=seed)
    sol = import_module("student_solution")
    out = sol.clean_contacts(df0)
    assert isinstance(out, pd.DataFrame), "Output must be a pandas DataFrame"
    assert list(out.columns) == ["name", "email", "phone", "country"], "Column order mismatch"
    assert out["email"].map(_is_valid_email).all(), "Found invalid emails in output"
    assert (out["email"] == out["email"].str.lower()).all(), "Emails must be lowercased"
    assert out["name"].map(lambda s: "  " not in (s or "") and (s or "") == (
                s or "").strip()).all(), "Names must be trimmed and internal spaces collapsed"
    assert out["phone"].map(_is_valid_e164).all(), "Phones must be E.164 or empty"
    assert not out.duplicated(subset=["email", "phone"]).any(), "Duplicates remain"
    passed = True
    return {"seed": seed, "rows_in": len(df0), "rows_out": len(out), "passed": passed}


def grade_many(runs: int = 10, n: int = 60, start_seed: int = 0) -> dict:
    results = []
    ok = 0
    for i in range(runs):
        seed = start_seed + i
        try:
            r = grade_one(seed=seed, n=n)
            results.append(r)
            ok += 1 if r["passed"] else 0
        except AssertionError as e:
            results.append({"seed": seed, "error": str(e), "passed": False})
        except Exception as e:
            results.append({"seed": seed, "error": repr(e), "passed": False})
    pass_rate = ok / runs
    return {"pass_rate": pass_rate, "runs": runs, "details": results}
