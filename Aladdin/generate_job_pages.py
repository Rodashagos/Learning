import json
from pathlib import Path
import shutil
from datetime import datetime


def main():
    base = Path(__file__).parent
    vm_path = base / "viewmodel3.json"
    template_path = base / "job_page_template.html"
    index_template_path = base / "index_template.html"

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

    if not index_template_path.exists():
        print(f"Index template not found at: {index_template_path}")
        return

    with vm_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = data.get("jobs", [])
    
    # Sort jobs by timestamp (newest first)
    jobs.sort(key=lambda job: job.get("timestamp", ""), reverse=True)

    template_text = template_path.read_text(encoding="utf-8")

    for job in jobs:
        job_id = job.get("id")
        if not job_id:
            print("Skipping job with no id")
            continue

        title = job.get("title", "")
        location = job.get("location", "")
        salary = job.get("salary", "")
        timestamp = job.get("timestamp", "")
        
        # Format timestamp for display (convert ISO format to readable date)
        if timestamp:
            # Parse ISO format and display as "Month Day, Year"
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_timestamp = dt.strftime("%B %d, %Y")
            except:
                formatted_timestamp = timestamp
        else:
            formatted_timestamp = "Date not specified"

        # build full description html from paragraphs
        full = job.get("fullDescription") or job.get("description") or ""
        paragraphs = [p.strip() for p in full.split("\n\n") if p.strip()]
        if paragraphs:
            full_html = "\n\n".join(f"<p>{p}</p>" for p in paragraphs)
        else:
            full_html = ""

        # build tags html
        tags = job.get('tags', []) or []
        if tags:
            tags_html = ' '.join(f'<span class="tag">{t}</span>' for t in tags)
            tags_html = f'<div class="job-tags">{tags_html}</div>'
        else:
            tags_html = ''

        out_html = template_text.replace("{{title}}", title)
        out_html = out_html.replace("{{location}}", location)
        out_html = out_html.replace("{{salary}}", salary)
        out_html = out_html.replace("{{timestamp}}", formatted_timestamp)
        out_html = out_html.replace("{{fullDescription}}", full_html)
        out_html = out_html.replace("{{tags}}", tags_html)

        # adjust stylesheet path for pages placed in job_pages/
        out_html = out_html.replace('href="job-styles.css"', 'href="../job-styles.css"')

        out_path = out_dir / f"job_page_{job_id}.html"
        out_path.write_text(out_html, encoding="utf-8")
        print(f"Wrote {out_path.name}")

    # Generate index.html from index_template.html
    index_path = base / "index.html"
    if index_path.exists():
        index_path.unlink()
    
    index_template_text = index_template_path.read_text(encoding="utf-8")

    # Build unique tag list for sidebar with counts
    tag_counts = {}
    tag_display = {}
    for job in jobs:
        for tag in job.get("tags", []) or []:
            if not isinstance(tag, str):
                continue
            cleaned = tag.strip()
            if not cleaned:
                continue
            normalized = cleaned.lower()
            tag_counts[normalized] = tag_counts.get(normalized, 0) + 1
            tag_display.setdefault(normalized, cleaned)

    sorted_tags = sorted(tag_display.items(), key=lambda item: item[1].lower())
    if sorted_tags:
        tag_items = [
            f"  <li><button class=\"tag-button is-active\" data-tag=\"all\">All ({len(jobs)})</button></li>"
        ]
        tag_items.extend(
            f"  <li><button class=\"tag-button\" data-tag=\"{normalized}\">{label} ({tag_counts.get(normalized, 0)})</button></li>"
            for normalized, label in sorted_tags
        )
        tag_list_html = f"<ul class=\"tag-list\">\n" + "\n".join(tag_items) + "\n</ul>"
    else:
        tag_list_html = "<p>No tags available</p>"
    
    listings = []
    for job in jobs:
        jid = job.get('id')
        if not jid:
            continue
        title = job.get('title', '')
        location = job.get('location', '')
        desc = job.get('description', '')
        full_desc = job.get('fullDescription', '')
        href = f"job_pages/job_page_{jid}.html"
        # build tags markup for index listing
        job_tags = job.get('tags', []) or []
        normalized_tags = [t.strip().lower() for t in job_tags if isinstance(t, str) and t.strip()]
        data_tags = "|".join(normalized_tags)
        if job_tags:
            tags_html = ' '.join(f'<span class="tag">{t}</span>' for t in job_tags)
            tags_html = f'\n        <div class="job-tags">{tags_html}</div>'
        else:
            tags_html = ''

        entry = (
            f'<a class="job-link" href="{href}" data-tags="{data_tags}" data-description="{full_desc}">\n'
            f'  <div class="job-listing">\n'
            f'    <div class="job-title">{title}</div>\n'
            f'    <div class="job-location">{location}</div>\n'
            f'    <div class="job-description">{desc}</div>{tags_html}\n'
            f'  </div>\n'
            f'</a>'
        )
        listings.append(entry)

    job_listings_html = '\n\n'.join(listings) if listings else '<!-- No job listings available -->'
    
    new_index = index_template_text.replace("{{jobListings}}", job_listings_html)
    new_index = new_index.replace("{{tagList}}", tag_list_html)
    index_path.write_text(new_index, encoding='utf-8')
    print('Generated index.html from template')


if __name__ == "__main__":
    main()
