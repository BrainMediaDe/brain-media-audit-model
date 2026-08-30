"""
Brain-Media Audit Model (BAM) Core - bam_api_local.py

Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
https://brain-media.de

Lizenz: GNU Affero General Public License v3.0 (AGPLv3)
Siehe LICENSE-Datei im Repository-Root.

Teil von "Brain-Media Audit Model (BAM) Core"
https://github.com/BrainMediaDe/brain-media-audit-model

Minimale lokale REST-API fuer bam_dashboard.html (Single-User,
ohne Multi-Tenant, ohne Authentifizierung). Liest bam_database.json
und stellt die Inhalte unter /api/v2 bereit.

Fuer produktiven Betrieb auf einem eigenen Server siehe
docs/DEPLOYMENT.md.

Starten:
    pip3 install flask flask-cors --break-system-packages
    python3 bam_api_local.py
"""

import json
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

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


@app.route("/api/v2/meta")
def get_meta():
    data = load_db()
    return jsonify({
        "schema_version": data.get("schema_version"),
        "description": data.get("description"),
        "publisher": data.get("_publisher"),
        "license": data.get("_license"),
    })


@app.route("/")
def dashboard():
    return send_from_directory(BASE_DIR, "bam_dashboard.html")


if __name__ == "__main__":
    print("BAM Core lokale API laeuft auf http://localhost:5000")
    print("Dashboard: http://localhost:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
