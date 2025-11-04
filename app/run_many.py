import json
from grader import grade_many


if __name__ == "__main__":
    res = grade_many(runs=10, n=60, start_seed=0)
    print(json.dumps(res, indent=2))
