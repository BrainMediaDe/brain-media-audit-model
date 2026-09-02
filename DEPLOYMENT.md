# BAM Core - Deployment Guide

Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
Lizenz: AGPLv3 (Code) / CC BY-SA 4.0 (Datenmodell) - siehe
[LICENSE](../LICENSE) und [LICENSE-DATA](../LICENSE-DATA).

Dieser Guide beschreibt drei Wege, BAM Core zu betreiben:

- **Teil A - Lokal (WSL/Linux/macOS):** zum Ausprobieren, Entwickeln,
  fuer Einzelnutzer
- **Teil B - Debian 13 Server:** produktiver Betrieb mit systemd +
  Nginx + TLS
- **Teil C - Docker:** containerisierter Betrieb (optional)

---

## Teil A - Lokal (WSL / Linux / macOS)

### Voraussetzungen

- Python 3.10+
- `pip3`

### Setup

```bash
git clone https://github.com/BrainMediaDe/brain-media-audit-model.git
cd brain-media-audit-model
chmod +x deploy/setup_wsl.sh
./deploy/setup_wsl.sh
```

Das Skript installiert `flask` und `flask-cors`, prueft das
Datenmodell und startet die lokale API + Dashboard im Vordergrund.

Dashboard: **http://localhost:5000**

Beenden mit `Strg+C`. Erneuter Start:

```bash
python3 bam_api_local.py
```

### BAM per RAG befragen (optional)

Voraussetzung: [LM Studio](https://lmstudio.ai/) laeuft lokal mit
geladenem Modell (z. B. Gemma) auf Port 1234.

```bash
pip3 install openai --break-system-packages
python3 bam_rag.py
```

---

## Teil B - Debian 13 (Trixie) Server

Fuer den dauerhaften Betrieb auf einem eigenen Server (z. B. vServer,
Raspberry Pi, NAS) als systemd-Dienst mit Gunicorn, optional hinter
Nginx mit TLS.

### Architekturuebersicht

```
Internet -> Nginx (Port 443, TLS) -> Gunicorn (127.0.0.1:5000) -> bam_api_local.py -> bam_database.json
```

### B.1 Automatisches Setup

```bash
git clone https://github.com/BrainMediaDe/brain-media-audit-model.git
cd brain-media-audit-model
chmod +x deploy/setup_debian13.sh
sudo ./deploy/setup_debian13.sh
```

Das Skript:

1. installiert `python3`, `python3-venv`, `python3-pip`, `git`
2. legt einen unprivilegierten Benutzer `bam` an
3. kopiert das Projekt nach `/opt/bam-core`
4. erstellt ein Virtualenv und installiert `requirements.txt`
5. richtet `/var/log/bam-core` ein
6. installiert und startet `bam-core.service` (systemd)

Nach dem Lauf ist BAM Core lokal unter `http://127.0.0.1:5000`
erreichbar (noch nicht von aussen).

### B.2 Manuelles Setup (Schritt fuer Schritt)

Falls das Setup-Skript angepasst werden soll oder Sie die Schritte
nachvollziehen wollen:

```bash
# 1. Pakete
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# 2. Benutzer
sudo useradd --system --home /opt/bam-core --shell /usr/sbin/nologin bam

# 3. Dateien
sudo mkdir -p /opt/bam-core
sudo cp -r . /opt/bam-core/
sudo chown -R bam:bam /opt/bam-core

# 4. Virtualenv
sudo -u bam python3 -m venv /opt/bam-core/venv
sudo -u bam /opt/bam-core/venv/bin/pip install -r /opt/bam-core/requirements.txt

# 5. Logs
sudo mkdir -p /var/log/bam-core
sudo chown bam:bam /var/log/bam-core

# 6. systemd
sudo cp /opt/bam-core/deploy/bam-core.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now bam-core

# 7. Status pruefen
sudo systemctl status bam-core
curl http://127.0.0.1:5000/api/v2/meta
```

### B.3 Reverse Proxy & TLS (Nginx + Let's Encrypt)

BAM Core lauscht standardmaessig nur auf `127.0.0.1:5000`. Fuer den
Zugriff von aussen wird Nginx als Reverse Proxy mit TLS empfohlen.

```bash
# Nginx installieren
sudo apt install -y nginx certbot python3-certbot-nginx

# Konfiguration einrichten
sudo cp /opt/bam-core/deploy/nginx-bam-core.conf /etc/nginx/sites-available/bam-core
sudo nano /etc/nginx/sites-available/bam-core   # server_name anpassen!
sudo ln -s /etc/nginx/sites-available/bam-core /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# TLS-Zertifikat ausstellen (DNS muss bereits auf den Server zeigen)
sudo certbot --nginx -d bam.example.org
```

Nach erfolgreicher Zertifikatsausstellung ist BAM Core unter
`https://bam.example.org` erreichbar. Certbot richtet die
automatische Erneuerung des Zertifikats per Cron/Timer ein.

### B.4 Firewall

```bash
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### B.5 Updates einspielen

```bash
cd /opt/bam-core
sudo -u bam git pull
sudo -u bam venv/bin/pip install -r requirements.txt
sudo systemctl restart bam-core
```

### B.6 Logs & Monitoring

```bash
# Live-Logs des Dienstes
journalctl -u bam-core -f

# Zugriffs-/Fehlerlogs von Gunicorn
tail -f /var/log/bam-core/access.log
tail -f /var/log/bam-core/error.log
```

### B.7 Deinstallation

```bash
sudo systemctl disable --now bam-core
sudo rm /etc/systemd/system/bam-core.service
sudo systemctl daemon-reload
sudo rm -rf /opt/bam-core /var/log/bam-core
sudo userdel bam
```

---

## Teil C - Docker (optional)

Fuer Nutzer, die einen containerisierten Betrieb bevorzugen.

### Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "bam_api_local:app"]
```

### Build & Run

```bash
docker build -t bam-core .
docker run -d --name bam-core -p 5000:5000 bam-core
```

Dashboard: **http://localhost:5000**

### docker-compose (mit Nginx)

```yaml
version: "3.8"
services:
  bam-core:
    build: .
    restart: unless-stopped
    expose:
      - "5000"

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deploy/nginx-bam-core.conf:/etc/nginx/conf.d/default.conf:ro
      - ./certs:/etc/letsencrypt:ro
    depends_on:
      - bam-core
```

```bash
docker compose up -d
```

---

## Troubleshooting

| Problem | Loesung |
|---|---|
| `ModuleNotFoundError: flask` | `pip3 install -r requirements.txt --break-system-packages` (lokal) bzw. Virtualenv pruefen (Server) |
| Port 5000 bereits belegt | In `bam_api_local.py` und `bam-core.service` Port anpassen |
| `systemctl status bam-core` zeigt `failed` | `journalctl -u bam-core -e` fuer Details; meist fehlende Datei-Berechtigungen (`chown -R bam:bam /opt/bam-core`) |
| Dashboard laedt, aber keine Daten | Pruefen, ob `bam_database.json` im selben Verzeichnis wie `bam_api_local.py` liegt |
| Nginx 502 Bad Gateway | `systemctl status bam-core` pruefen - laeuft Gunicorn auf 127.0.0.1:5000? |
| `certbot` schlaegt fehl | DNS-Eintrag fuer die Domain pruefen (muss auf Server-IP zeigen), Port 80 muss von aussen erreichbar sein |

---

## Einsatzbereich dieses Deployments

Dieses Deployment ist **Single-User / Single-Tenant** und ohne
Authentifizierung gedacht fuer den internen Gebrauch (z. B. eigene
Compliance-Abteilung). Mandantenfaehigkeit (Multi-Tenant),
White-Label oder API-Key-Verwaltung sind nicht Bestandteil von
BAM Core und muessten bei Bedarf selbst implementiert werden.

Falls Sie BAM Core fuer mehrere Kunden/Mandanten als Dienst
anbieten moechten: Beachten Sie, dass dies gemaess AGPLv3 §13
(Network Use) die Pflicht zur Offenlegung Ihres (ggf. modifizierten)
Quellcodes an die Nutzer dieses Dienstes ausloest.
