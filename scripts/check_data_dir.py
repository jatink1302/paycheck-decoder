#!/usr/bin/env python3
"""Pre-commit guard: refuse any staged file under data/ that is not
under data/synthetic/. Real pay data must never enter this repository.

Wired as a local pre-commit hook (see README's setup section) and also
safe to run by hand: `python scripts/check_data_dir.py`.
"""

import subprocess
import sys

ALLOWED_PREFIX = "data/synthetic/"
DATA_PREFIX = "data/"


def staged_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    violations = [
        path
        for path in staged_files()
        if path.startswith(DATA_PREFIX) and not path.startswith(ALLOWED_PREFIX)
    ]
    if violations:
        print("Refusing commit: files staged under data/ outside data/synthetic/:")
        for path in violations:
            print(f"  {path}")
        print(
            "\nReal pay data must never be committed. If this is synthetic data, "
            "move it under data/synthetic/ instead."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
