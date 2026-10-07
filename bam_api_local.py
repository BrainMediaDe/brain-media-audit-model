"""
Brain-Media Audit Model (BAM) Core - bam_api_local.py

Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
https://brain-media.de

Lizenz: GNU Affero General Public License v3.0 (AGPLv3)
Siehe LICENSE-Datei im Repository-Root.

Teil von "Brain-Media Audit Model (BAM) Core"
https://github.com/BrainMediaDe/brain-media-audit-model

BAM Core 2.0.3

Minimale lokale REST-API fuer bam_dashboard.html (Single-User,
ohne Multi-Tenant, ohne Authentifizierung). Liest bam_database.json
und stellt die Inhalte unter /api/v2 bereit.

Fuer produktiven Betrieb auf einem eigenen Server siehe
docs/DEPLOYMENT.md.

Starten:
    pip3 install flask flask-cors openpyxl --break-system-packages
    python3 bam_api_local.py
"""

import json
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS

import bam_export

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "bam_database.json"

app = Flask(__name__)
CORS(app)


def load_db():
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.route("/api/v2/objects")
def get_objects():
    data = load_db()
    return jsonify(data.get("objects", []))


@app.route("/api/v2/regulations")
def get_regulations():
    data = load_db()
    return jsonify(data.get("regulations", []))


@app.route("/api/v2/iso27001")
def get_iso27001():
    data = load_db()
    return jsonify(data.get("iso27001_2022", {}))


@app.route("/api/v2/regulatory-changes")
def get_regulatory_changes():
    """Liste aller getrackten regulatorischen Aenderungsverfahren."""
    data = load_db()
    return jsonify(data.get("regulatory_change_management", {}))


@app.route("/api/v2/regulatory-changes/<change_id>/impact")
def get_regulatory_change_impact(change_id):
    """
    Berechnet den Impact eines Regulatory-Change-Eintrags LIVE, statt
    sich auf eine manuell gepflegte Liste zu verlassen:

    1. Direkt betroffene Objekte (affected_bam_ids aus dem Change-Eintrag)
    2. Indirekt betroffene Objekte (ein Hop ueber cross_refs der direkt
       betroffenen Objekte) - das ist der Teil, der "Change Once, Trace
       Everywhere" tatsaechlich einloest: neue Objekte mit passendem
       cross_ref tauchen automatisch auf, ohne dass jemand die Liste
       von Hand nachpflegen muss.
    3. Falls vorhanden: die manuell kuratierten 'deltas' (change_type,
       Impact je Komponente) - siehe _delta_note im Wurzelobjekt.
    """
    data = load_db()
    rcm = data.get("regulatory_change_management", {})
    initiatives = rcm.get("tracked_initiatives", [])

    change = next((i for i in initiatives if i["change_id"] == change_id), None)
    if change is None:
        return jsonify({"error": f"change_id '{change_id}' nicht gefunden"}), 404

    objects_by_id = {o["bam_id"]: o for o in data.get("objects", [])}
    direct_ids = set(change.get("affected_bam_ids", []))

    # Ein Hop ueber cross_refs: cross_refs verweisen oft auf Artikel-Strings
    # ("CRA Art. 6", "ISO 27001 A.8.2.1"), nicht direkt auf bam_ids - daher
    # matchen wir ueber Regulation UND Artikel gemeinsam im cross_ref-String
    # (nicht nur die Regulation allein - siehe UPDATE_README zum urspruenglichen Bugfix).
    indirect_ids = set()
    for did in direct_ids:
        obj = objects_by_id.get(did)
        if not obj:
            continue
        for ref in obj.get("cross_refs", []):
            for other in data.get("objects", []):
                if other["bam_id"] in direct_ids:
                    continue
                art = other.get("article", "")
                if not art:
                    continue
                if other["regulation"] in ref and art in ref:
                    indirect_ids.add(other["bam_id"])

    return jsonify({
        "change_id": change_id,
        "title": change.get("title"),
        "status": change.get("status"),
        "direct_impact": [objects_by_id[i] for i in direct_ids if i in objects_by_id],
        "indirect_impact": [objects_by_id[i] for i in indirect_ids if i in objects_by_id],
        "direct_count": len(direct_ids),
        "indirect_count": len(indirect_ids),
        "deltas": change.get("deltas", []),
    })


@app.route("/api/v2/objects/<bam_id>/changes")
def get_object_changes(bam_id):
    """
    Alternative Routenform (siehe Paper Abschnitt 14): direkt die
    Aenderungen zu einem bestimmten BAM-Objekt abfragen, inkl. des
    dazugehoerigen Delta-Eintrags, falls vorhanden.
    """
    data = load_db()
    rcm = data.get("regulatory_change_management", {})
    result = []
    for init in rcm.get("tracked_initiatives", []):
        if bam_id in init.get("affected_bam_ids", []):
            delta = next((d for d in init.get("deltas", []) if d["bam_id"] == bam_id), None)
            result.append({
                "change_id": init["change_id"],
                "title": init["title"],
                "status": init["status"],
                "delta": delta,
            })
    return jsonify({"bam_id": bam_id, "changes": result})


@app.route("/api/v2/objects/<bam_id>")
def get_object_detail(bam_id):
    """
    Einzelnes BAM-Objekt PLUS live berechnete aktive Regulatory Changes,
    die dieses Objekt betreffen - die eigentliche Umkehr-Abfrage, die im
    Dashboard als Warnhinweis angezeigt werden kann.
    """
    data = load_db()
    obj = next((o for o in data.get("objects", []) if o["bam_id"] == bam_id), None)
    if obj is None:
        return jsonify({"error": f"bam_id '{bam_id}' nicht gefunden"}), 404

    rcm = data.get("regulatory_change_management", {})
    active_changes = [
        {"change_id": i["change_id"], "title": i["title"], "status": i["status"]}
        for i in rcm.get("tracked_initiatives", [])
        if bam_id in i.get("affected_bam_ids", [])
    ]

    result = dict(obj)
    result["active_regulatory_changes"] = active_changes
    return jsonify(result)


@app.route("/api/v2/meta")
def get_meta():
    data = load_db()
    return jsonify({
        "version": data.get("version"),
        "released": data.get("released"),
        "schema_version": data.get("schema_version"),
        "description": data.get("description"),
        "publisher": data.get("_publisher"),
        "license": data.get("_license"),
    })


# ─────────────────────────────────────────────────────────────────
# EXPORT (ab 2.0.3)
#
# Die Endpunkte sind zustandslos: der Bewertungsstand wird im Request
# uebergeben, nicht gespeichert. BAM Core 2.0.x haelt den Zustand im
# Browser (localStorage); eine serverseitige Persistenz kommt erst mit
# dem Instanz-Layer in 2.2. POST bedeutet hier also "Daten mitgeben",
# nicht "Daten anlegen".
# ─────────────────────────────────────────────────────────────────

MIME = {
    "csv": "text/csv; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "xlsx": ("application/vnd.openxmlformats-officedocument"
             ".spreadsheetml.sheet"),
}


@app.route("/api/v2/export/formats")
def get_export_formats():
    """Welche Formate diese Installation ausliefern kann."""
    formats = ["csv", "json"]
    try:
        import openpyxl  # noqa: F401
        formats.append("xlsx")
    except ImportError:
        pass
    return jsonify({
        "formats": formats,
        "note": ("xlsx benoetigt openpyxl: "
                 "pip3 install openpyxl --break-system-packages"),
    })


def _export(payload):
    fmt = (payload.get("format") or "csv").lower()
    if fmt not in MIME:
        return jsonify({"error": f"Unbekanntes Format '{fmt}'. "
                                 f"Erlaubt: {', '.join(MIME)}"}), 400

    gaps = payload.get("gaps") or {}
    if not isinstance(gaps, dict):
        return jsonify({"error": "'gaps' muss ein Objekt "
                                 "{bam_id: 'ja'|'teil'|'nein'} sein"}), 400

    only_gaps = bool(payload.get("only_gaps"))
    data = load_db()

    rows = bam_export.build_rows(data, gaps, only_gaps=only_gaps)
    summary_rows, summary_total = bam_export.build_summary(data, gaps)
    meta = bam_export.build_meta(
        data,
        organisation=payload.get("organisation", ""),
        assessor=payload.get("assessor", ""),
        note=payload.get("note", ""),
    )

    if fmt == "csv":
        body = bam_export.to_csv(rows)
    elif fmt == "json":
        body = bam_export.to_json(rows, meta, summary_rows, summary_total)
    else:
        try:
            body = bam_export.to_xlsx(rows, meta, summary_rows, summary_total)
        except ImportError:
            return jsonify({
                "error": "xlsx benoetigt openpyxl. Installieren mit: "
                         "pip3 install openpyxl --break-system-packages, "
                         "oder format=csv verwenden."
            }), 501

    name = bam_export.filename(fmt, payload.get("organisation", ""), only_gaps)
    return Response(body, mimetype=MIME[fmt], headers={
        "Content-Disposition": f'attachment; filename="{name}"',
        "X-BAM-Rows": str(len(rows)),
    })


@app.route("/api/v2/export/gap", methods=["POST"])
def post_export_gap():
    """
    Export der Gap-Analyse. Body (alle Felder optional):

        {
          "gaps": {"NIS2-020-GOVERNANCE": "ja", "...": "teil"},
          "format": "csv" | "xlsx" | "json",
          "organisation": "Musterfirma GmbH",
          "assessor": "Interne Revision",
          "note": "Zwischenstand Q4",
          "only_gaps": false
        }

    only_gaps = true liefert nur Positionen mit Feststellung
    (teilweise/nicht erfuellt), also die eigentliche Maengelliste.
    """
    return _export(request.get_json(silent=True) or {})


@app.route("/api/v2/export/gap", methods=["GET"])
def get_export_gap():
    """
    Leeres Arbeitspapier: alle Objekte, Spalte 'Bewertung' auf
    'nicht bewertet'. Praktisch als Vorlage oder zum Ausdrucken.

        /api/v2/export/gap?format=xlsx&organisation=Musterfirma
    """
    return _export({
        "format": request.args.get("format", "csv"),
        "organisation": request.args.get("organisation", ""),
        "assessor": request.args.get("assessor", ""),
        "note": request.args.get("note", ""),
    })


@app.route("/")
def dashboard():
    return send_from_directory(BASE_DIR, "bam_dashboard.html")


if __name__ == "__main__":
    print("BAM Core lokale API laeuft auf http://localhost:5000")
    print("Dashboard: http://localhost:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
