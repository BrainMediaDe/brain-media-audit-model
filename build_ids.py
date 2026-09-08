"""
Brain-Media Audit Model (BAM) Core - build_ids.py

Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
Lizenz: GNU Affero General Public License v3.0 (AGPLv3)

Statischer Seitengenerator fuer die auflösbaren BAM-IDs. Liest
bam_database.json und erzeugt fuer jedes Objekt:

  public/id/<BAM-ID>/index.html   - menschenlesbar, mit schema.org/
                                     DefinedTerm-Markup fuer Suchmaschinen
  public/id/<BAM-ID>/index.json   - maschinenlesbar, identischer Inhalt

Dazu public/sitemap.xml und public/robots.txt fuer den gesamten
Bestand. Das Ergebnis (public/) wird unveraendert auf die Subdomain
bam.brain-media.de hochgeladen - kein Server, kein Backend noetig,
rein statische Dateien.

Aufruf:
    python3 build_ids.py
"""

import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "bam_database.json"
OUT_DIR = BASE_DIR / "public"
BASE_URL = "https://bam.brain-media.de"

CSS = """
:root{
  --white:#FAF8F4;--black:#0F0F0D;
  --gray-50:#F5F5F2;--gray-100:#E8E8E4;--gray-200:#D0D0CA;
  --gray-400:#9A9A92;--gray-600:#5C5C56;--gray-800:#2A2A26;
  --amber:#B87318;--amber-bg:#FAF0E0;
  --sans:'DM Sans',sans-serif;--mono:'DM Mono',monospace;
  --r:2px;--rmd:4px;--max:800px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);background:var(--white);color:var(--black);line-height:1.6;padding:3rem 1.5rem}
.wrap{max-width:var(--max);margin:0 auto}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gray-400);margin-bottom:.5rem}
h1{font-size:26px;font-weight:400;letter-spacing:-.02em;margin-bottom:.25rem;word-break:break-word}
.regulation{font-family:var(--mono);font-size:14px;color:var(--gray-600);margin-bottom:2rem}
.field{border-top:1px solid var(--gray-100);padding:1.25rem 0}
.field:first-of-type{border-top:none;padding-top:0}
.field-label{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gray-400);margin-bottom:.4rem}
.field-value{font-size:16px;color:var(--black)}
.changes{margin-top:2rem;background:var(--amber-bg);border-radius:var(--rmd);padding:1.25rem 1.5rem}
.changes-label{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.5rem}
.change-item{font-size:15px;padding:.4rem 0}
.footer{margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--gray-100);font-family:var(--mono);font-size:12px;color:var(--gray-400)}
.footer a{color:var(--gray-600)}
.jsonlink{font-size:13px}
.jsonlink a{color:var(--gray-600)}
"""

FIELD_LABELS = [
    ("requirement", "Requirement"),
    ("gap_check", "Gap-Check"),
    ("remediation", "Remediation"),
    ("risk", "Risk"),
    ("control", "Control"),
    ("evidence", "Evidence"),
]


def load_db():
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


def active_changes_for(bam_id, rcm):
    return [
        {"change_id": i["change_id"], "title": i["title"], "status": i["status"]}
        for i in rcm.get("tracked_initiatives", [])
        if bam_id in i.get("affected_bam_ids", [])
    ]


def object_to_json(obj, active_changes):
    result = dict(obj)
    result["active_regulatory_changes"] = active_changes
    result["_id_url"] = f"{BASE_URL}/id/{obj['bam_id']}"
    return result


def render_html(obj, active_changes):
    bam_id = obj["bam_id"]

    fields_html = "".join(
        f'<div class="field"><p class="field-label">{label}</p>'
        f'<p class="field-value">{obj.get(key, "")}</p></div>'
        for key, label in FIELD_LABELS
        if obj.get(key)
    )

    changes_html = ""
    if active_changes:
        items = "".join(
            f'<div class="change-item">⚠ {c["title"]} ({c["status"]})</div>'
            for c in active_changes
        )
        changes_html = (
            f'<div class="changes"><p class="changes-label">'
            f'Laufende regulatorische Änderung</p>{items}</div>'
        )

    # schema.org/DefinedTerm - macht das Objekt fuer Suchmaschinen als
    # eigenstaendigen, definierten Begriff erkennbar, nicht nur als Text.
    jsonld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": bam_id,
        "description": obj.get("requirement", ""),
        "inDefinedTermSet": "https://github.com/BrainMediaDe/brain-media-audit-model",
        "url": f"{BASE_URL}/id/{bam_id}",
    }

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{bam_id} · BAM Core · Brain-Media.de</title>
<link rel="canonical" href="{BASE_URL}/id/{bam_id}">
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<p class="eyebrow">BAM Core</p>
<h1>{bam_id}</h1>
<p class="regulation">{obj.get('regulation','')} · {obj.get('article','')}</p>
{fields_html}
{changes_html}
<div class="footer">
<p class="jsonlink"><a href="index.json">Als JSON abrufen</a></p>
<p style="margin-top:.5rem">Teil von <a href="https://github.com/BrainMediaDe/brain-media-audit-model">BAM Core</a> ·
AGPLv3 / CC BY-SA 4.0 · <a href="https://www.brain-media.de/executable_compliance.html">brain-media.de</a></p>
</div>
</div>
</body></html>"""


def build_sitemap(bam_ids):
    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{BASE_URL}/id/{bid}</loc><lastmod>{today}</lastmod></url>"
        for bid in bam_ids
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""


def build_robots():
    return f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"


def main():
    data = load_db()
    rcm = data.get("regulatory_change_management", {})
    objects = data.get("objects", [])

    id_dir = OUT_DIR / "id"
    id_dir.mkdir(parents=True, exist_ok=True)

    bam_ids = []
    for obj in objects:
        bam_id = obj["bam_id"]
        bam_ids.append(bam_id)
        obj_dir = id_dir / bam_id
        obj_dir.mkdir(exist_ok=True)

        changes = active_changes_for(bam_id, rcm)

        (obj_dir / "index.html").write_text(
            render_html(obj, changes), encoding="utf-8"
        )
        (obj_dir / "index.json").write_text(
            json.dumps(object_to_json(obj, changes), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    (OUT_DIR / "sitemap.xml").write_text(build_sitemap(bam_ids), encoding="utf-8")
    (OUT_DIR / "robots.txt").write_text(build_robots(), encoding="utf-8")

    print(f"{len(bam_ids)} BAM-IDs erzeugt unter {id_dir}/")
    print(f"sitemap.xml und robots.txt erzeugt unter {OUT_DIR}/")
    print("public/ kann unveraendert auf bam.brain-media.de hochgeladen werden.")


if __name__ == "__main__":
    main()
