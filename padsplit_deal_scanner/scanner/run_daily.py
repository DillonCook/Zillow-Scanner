from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def ensure_requirements_installed() -> None:
    requirements_path = PROJECT_ROOT / "requirements.txt"
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
        stdout=subprocess.DEVNULL,
    )


def main() -> None:
    ensure_requirements_installed()

    from scanner.sources.hillsborough_hcpa import fetch_hcpa_parcel_fields

    try:
        fields, sample_record = fetch_hcpa_parcel_fields(PROJECT_ROOT / "data")
    except Exception as exc:
        fields = []
        sample_record = {"error": str(exc)}

    print("HCPA fields detected:")
    for field in fields:
        print(field)

    print("Sample record:")
    print(sample_record)


if __name__ == "__main__":
    main()
