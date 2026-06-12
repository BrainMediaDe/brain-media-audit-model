#!/bin/bash
#
# Brain-Media Audit Model (BAM) Core - setup_wsl.sh
#
# Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
# https://brain-media.de
#
# Lizenz: GNU Affero General Public License v3.0 (AGPLv3)
# Siehe LICENSE-Datei im Repository-Root.
#
# Teil von "Brain-Media Audit Model (BAM) Core"
# https://github.com/BrainMediaDe/brain-media-audit-model
#
# Einfaches Setup fuer WSL / lokales Linux / macOS.
# Installiert Abhaengigkeiten und startet die lokale API + Dashboard.
#
# Verwendung:
#   chmod +x deploy/setup_wsl.sh
#   ./deploy/setup_wsl.sh
#

set -e

echo "=== BAM Core - lokales Setup ==="

# Ins Repository-Root wechseln (Skript liegt in deploy/)
cd "$(dirname "$0")/.."

echo "[1/3] Python-Abhaengigkeiten installieren..."
pip3 install flask flask-cors --break-system-packages

echo "[2/3] Datenmodell pruefen..."
python3 -c "import json; d=json.load(open('bam_database.json')); print(f\"  -> {len(d.get('objects', []))} BAM-Objekte, Schema v{d.get('schema_version')}\")"

echo "[3/3] Starte lokale API + Dashboard auf http://localhost:5000 ..."
python3 bam_api_local.py
