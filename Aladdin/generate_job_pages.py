import json
from pathlib import Path
import shutil


def main():
    base = Path(__file__).parent
    vm_path = base / "viewmodel2.json"
    template_path = base / "job_page_template.html"

    out_dir = base / "job_pages"
    # remove existing output directory (and its contents) then recreate
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not vm_path.exists():
        print(f"viewmodel.json not found at: {vm_path}")
        return

    if not template_path.exists():
        print(f"Template not found at: {template_path}")
        return

    with vm_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = data.get("jobs", [])

    template_text = template_path.read_text(encoding="utf-8")

    for job in jobs:
        job_id = job.get("id")
        if not job_id:
            print("Skipping job with no id")
            continue

        title = job.get("title", "")
        location = job.get("location", "")
        salary = job.get("salary", "")

        # build full description html from paragraphs
        full = job.get("fullDescription") or job.get("description") or ""
        paragraphs = [p.strip() for p in full.split("\n\n") if p.strip()]
        if paragraphs:
            full_html = "\n\n".join(f"<p>{p}</p>" for p in paragraphs)
        else:
            full_html = ""

        out_html = template_text.replace("{{title}}", title)
        out_html = out_html.replace("{{location}}", location)
        out_html = out_html.replace("{{salary}}", salary)
        out_html = out_html.replace("{{fullDescription}}", full_html)

        # adjust stylesheet path for pages placed in job_pages/
        out_html = out_html.replace('href="job-styles.css"', 'href="../job-styles.css"')

        out_path = out_dir / f"job_page_{job_id}.html"
        out_path.write_text(out_html, encoding="utf-8")
        print(f"Wrote {out_path.name}")


if __name__ == "__main__":
    main()
