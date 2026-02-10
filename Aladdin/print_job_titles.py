import json
from pathlib import Path


def main():
    base = Path(__file__).parent
    vm_path = base / "viewmodel.json"

    if not vm_path.exists():
        print(f"viewmodel.json not found at: {vm_path}")
        return

    with vm_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = data.get("jobs", [])
    for job in jobs:
        title = job.get("title", "<no title>")
        print(title)


if __name__ == "__main__":
    main()
