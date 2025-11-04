import shutil, subprocess, sys
from pathlib import Path

root = Path(__file__).parent
candidate = root / "candidate_solution.py"
target = root / "student_solution.py"

if not candidate.exists():
    print("candidate_solution.py not found")
    sys.exit(1)

shutil.copyfile(candidate, target)
print("Wrote candidate_solution.py -> student_solution.py")
subprocess.run([sys.executable, "run_many.py"], check=True)
