# Brain-Media Audit Model (BAM) Core
# Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
# Lizenz: AGPLv3 (Code) / CC BY-SA 4.0 (Datenmodell)
#
# Bauen und starten:
#     docker compose up
# Danach: http://localhost:5000

FROM python:3.12-slim

LABEL org.opencontainers.image.title="BAM Core" \
      org.opencontainers.image.description="Brain-Media Audit Model - offenes Datenmodell fuer Multi-Framework-Compliance" \
      org.opencontainers.image.vendor="Brain-Media.de" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later" \
      org.opencontainers.image.source="https://github.com/BrainMediaDe/brain-media-audit-model" \
      org.opencontainers.image.url="https://bam.brain-media.de/"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Abhaengigkeiten zuerst, damit der Layer beim Aendern der Daten erhalten bleibt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bam_api_local.py bam_export.py bam_dashboard.html bam_database.json ./

# Kein root im Container
RUN useradd --system --no-create-home --uid 10001 bam \
    && chown -R bam:bam /app
USER bam

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=4s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; \
        sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/api/v2/meta', timeout=3).status==200 else 1)"

# waitress statt des Flask-Entwicklungsservers
CMD ["python", "-m", "waitress", "--host=0.0.0.0", "--port=5000", "bam_api_local:app"]
