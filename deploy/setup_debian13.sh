#!/bin/bash
#
# Brain-Media Audit Model (BAM) Core - setup_debian13.sh
#
# Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
# Lizenz: AGPLv3 - siehe LICENSE
#
# Ein-Befehl-Setup fuer Debian 13 (Trixie): installiert BAM Core
# als systemd-Service mit Gunicorn, optional hinter Nginx.
#
# Verwendung (als root oder mit sudo):
#   chmod +x deploy/setup_debian13.sh
#   sudo ./deploy/setup_debian13.sh
#
# Siehe DEPLOYMENT.md fuer Details, Nginx/TLS-Einrichtung und
# Troubleshooting.

set -e

INSTALL_DIR="/opt/bam-core"
SERVICE_USER="bam"
LOG_DIR="/var/log/bam-core"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ "$EUID" -ne 0 ]; then
    echo "Bitte als root oder mit sudo ausfuehren."
    exit 1
fi

echo "=== BAM Core - Debian 13 Setup ==="

echo "[1/7] System-Pakete installieren..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip git

echo "[2/7] Dienst-Benutzer '${SERVICE_USER}' anlegen (falls nicht vorhanden)..."
if ! id "${SERVICE_USER}" &>/dev/null; then
    useradd --system --home "${INSTALL_DIR}" --shell /usr/sbin/nologin "${SERVICE_USER}"
fi

echo "[3/7] Dateien nach ${INSTALL_DIR} kopieren..."
mkdir -p "${INSTALL_DIR}"
cp -r "${REPO_DIR}"/* "${INSTALL_DIR}/"
chown -R "${SERVICE_USER}:${SERVICE_USER}" "${INSTALL_DIR}"

echo "[4/7] Python-Virtualenv einrichten..."
sudo -u "${SERVICE_USER}" python3 -m venv "${INSTALL_DIR}/venv"
sudo -u "${SERVICE_USER}" "${INSTALL_DIR}/venv/bin/pip" install --quiet -r "${INSTALL_DIR}/requirements.txt"

echo "[5/7] Log-Verzeichnis anlegen..."
mkdir -p "${LOG_DIR}"
chown "${SERVICE_USER}:${SERVICE_USER}" "${LOG_DIR}"

echo "[6/7] Datenmodell pruefen..."
"${INSTALL_DIR}/venv/bin/python3" -c "import json; d=json.load(open('${INSTALL_DIR}/bam_database.json')); print(f'  -> {len(d.get(\"objects\", []))} BAM-Objekte, Schema v{d.get(\"schema_version\")}')"

echo "[7/7] systemd-Service installieren und starten..."
cp "${INSTALL_DIR}/deploy/bam-core.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now bam-core

echo ""
echo "=== Fertig ==="
echo "BAM Core laeuft lokal auf http://127.0.0.1:5000"
echo ""
echo "Status pruefen:   systemctl status bam-core"
echo "Logs ansehen:     journalctl -u bam-core -f"
echo ""
echo "Naechster Schritt (optional): Nginx als Reverse Proxy einrichten,"
echo "siehe DEPLOYMENT.md, Abschnitt 'Reverse Proxy & TLS'."
