#!/usr/bin/env python3
"""
Render a concise rubric-style Markdown report from merged JSON.

Usage:
  python scripts/render_doc.py \
    --input merged/merged.json \
    --output reports/compiled.md \
    --per-category 12
"""
import argparse
import json
from collections import defaultdict, Counter
from pathlib import Path

try:
    from jinja2 import Template
except ImportError:  # pragma: no cover
    Template = None


def load_data(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def choose_building_type(reqs):
    counts = Counter(r.get("building_type", "") for r in reqs)
    if counts:
        return counts.most_common(1)[0][0]
    return "unspecified"


def group_by_category(reqs, per_category: int):
    grouped = defaultdict(list)
    for r in reqs:
        grouped[r.get("category_id", "uncategorized")].append(r)
    # sort each group by confidence desc
    for k in grouped:
        grouped[k] = sorted(grouped[k], key=lambda x: x.get("confidence", 0), reverse=True)[:per_category]
    return grouped


def render_markdown(building_type: str, grouped, total_conflicts: int):
    template_text = r"""
# Accessibility Rubric ({{ building_type }})

- Requirements covered: {{ total_reqs }}
- Categories: {{ total_categories }}
- Conflicts flagged: {{ total_conflicts }}

{% for category, items in grouped.items() %}
## {{ category }}
{% for r in items %}
- **{{ r.label }}** (id: {{ r.requirement_id }}, conf {{ '%.2f' % r.confidence }})
  - desc: {{ r.description }}
  - values: {{ r.values if r.values else 'n/a' }}
  - pages: {{ r.page_numbers if r.page_numbers else 'n/a' }}
  - source: {{ r.source.filename }}{% if r.conflict %} ⚠ conflict{% endif %}
{% endfor %}
{% endfor %}
"""
    if Template is None:
        # simple fallback formatting
        lines = [f"# Accessibility Rubric ({building_type})", ""]
        for category, items in grouped.items():
            lines.append(f"## {category}")
            for r in items:
                lines.append(f"- {r.get('label')} (conf {r.get('confidence', 0):.2f}) - {r.get('description')}")
        return "\n".join(lines)

    tmpl = Template(template_text)
    total_reqs = sum(len(v) for v in grouped.values())
    return tmpl.render(
        building_type=building_type,
        grouped=grouped,
        total_reqs=total_reqs,
        total_categories=len(grouped),
        total_conflicts=total_conflicts,
    )


def main():
    ap = argparse.ArgumentParser(description="Render merged JSON to Markdown rubric")
    ap.add_argument("--input", default="merged/merged.json", type=Path)
    ap.add_argument("--output", default="reports/compiled.md", type=Path)
    ap.add_argument("--per-category", type=int, default=12, help="Max items per category")
    args = ap.parse_args()

    data = load_data(args.input)
    reqs = data.get("requirements", [])
    building_type = choose_building_type(reqs)
    grouped = group_by_category(reqs, args.per_category)

    # conflicts count: any item with conflict True or alternates len>0
    total_conflicts = sum(1 for r in reqs if r.get("conflict"))

    md = render_markdown(building_type, grouped, total_conflicts)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
