# Brain-Media Audit Model (BAM) Core

**Offenes Datenmodell und Referenzimplementierung fuer
Multi-Framework-Compliance (NIS-2, DORA, CRA, EU AI Act, ISO 27001).**

Entwickelt von [Dr. Holger Reibold](https://brain-media.de) /
[Brain-Media.de](https://brain-media.de) auf Basis von 23 Jahren
Praxiserfahrung in IT-Sicherheits- und Compliance-Audits.

---

## Was ist BAM?

Regulatorische Anforderungen (NIS-2, DORA, CRA, EU AI Act, ISO 27001
u. a.) sind kein Wissensproblem, sondern ein Umsetzungsproblem. Das
**Brain-Media Audit Model (BAM)** bricht jede Anforderung in sechs
operative Ebenen herunter:

```
Requirement -> Gap-Check -> Remediation -> Risk -> Control -> Evidence
```

Eine einzelne Massnahme kann so gleichzeitig mehrere Frameworks
erfuellen ("Collect Once. Comply Many."). BAM ist kein Framework,
sondern ein maschinenlesbares Datenmodell - nutzbar in eigenen
GRC-Tools, Skripten, RAG-Pipelines und KI-Agenten.

Mehr Hintergrund: [Whitepaper "Executable Compliance"](Executable_Compliance_White_Paper.pdf)
und das SSRN-Paper (#5278869).

---

## Was ist in diesem Repository enthalten?

| Datei | Inhalt |
|---|---|
| `bam_database.json` | Das BAM-Datenmodell: 44 BAM-Objekte (Requirement -> Evidence) fuer NIS-2, DORA, CRA, EU AI Act sowie Cross-Framework-Verknuepfungen, plus ISO 27001:2022 Control-Mapping (93 Controls) |
| `bam_dashboard.html` | Single-User-Cockpit zur Anzeige und Bearbeitung der BAM-Objekte |
| `bam_api_local.py` | Minimale lokale REST-API (Flask) fuer das Dashboard |
| `bam_rag.py` | RAG-Anbindung an ein lokales LLM (LM Studio) - "Fragen Sie BAM" |
| `requirements.txt` | Python-Abhaengigkeiten |
| `deploy/setup_wsl.sh` | Ein-Befehl-Setup fuer WSL / Linux / macOS (lokal) |
| `deploy/setup_debian13.sh` | Ein-Befehl-Setup fuer Debian 13 Server (systemd) |
| `deploy/bam-core.service` | systemd-Unit fuer produktiven Betrieb |
| `deploy/nginx-bam-core.conf` | Nginx-Reverse-Proxy-Vorlage (inkl. TLS) |
| `docs/DEPLOYMENT.md` | Vollstaendiger Deployment Guide (lokal, Debian 13, Docker) |
| `docs/CONTRIBUTING.md` | Hinweise fuer Beitraege (fehlende Frameworks etc.) |
| `LICENSE` | AGPLv3 (Code) |
| `LICENSE-DATA` | CC BY-SA 4.0 (Datenmodell `bam_database.json`) |

---

## Framework-Abdeckung (Stand dieser Version)

| Framework | BAM-Objekte | Status |
|---|---|---|
| NIS-2 | 15 | Art. 20, 21 (alle Absaetze), 23 |
| DORA | 9 | Art. 5-30 (Kernanforderungen) |
| CRA | 7 | Anhang I, Art. 6-8, 23-28 |
| EU AI Act | 7 | Art. 3-14, 26, 62, 74 |
| DSGVO | 13 | Art. 5, 6, 13-14, 15-22, 24, 25, 28, 30, 32-39, 44-49 |
| Cross-Framework | 7 | Mehrfachverknuepfungen (inkl. gemeinsames VVT/Asset/KI-Inventar) |
| ISO 27001:2022 | 93 Controls | 74 % Coverage (69 vollstaendig, 24 teilweise) |

**Nicht (oder noch nicht) in BAM Core enthalten:** ISO 42001, Cyber
Solidarity Act (CSA), vollstaendige ISO-27001-Abdeckung (100 %).
Diese Frameworks sowie kontinuierliche Updates, Multi-Tenant-Betrieb,
White-Label und Hosting sind Bestandteil von **BAM Enterprise**
(siehe unten).

Contributions zur Erweiterung der Framework-Abdeckung sind
willkommen - siehe [CONTRIBUTING.md](docs/CONTRIBUTING.md).

---

## Schnellstart

```bash
git clone https://github.com/BrainMediaDe/brain-media-audit-model.git
cd brain-media-audit-model
chmod +x deploy/setup_wsl.sh
./deploy/setup_wsl.sh
```

Danach ist das Dashboard unter `http://localhost:5000` erreichbar.

Fuer produktiven Betrieb auf einem eigenen Server (Debian 13,
systemd, Nginx, TLS, Docker) siehe den vollstaendigen
**[Deployment Guide](docs/DEPLOYMENT.md)**.

### BAM per RAG befragen (optional)

Voraussetzung: [LM Studio](https://lmstudio.ai/) laeuft lokal mit
einem geladenen Modell (z. B. Gemma) auf Port 1234.

```bash
pip3 install openai --break-system-packages
python3 bam_rag.py
```

---

## Lizenzierung

Dieses Repository nutzt **zwei Lizenzen**:

- **Code** (`bam_dashboard.html`, `bam_api_local.py`, `bam_rag.py`,
  Skripte): [GNU AGPLv3](LICENSE). Wird der Code (auch modifiziert)
  zum Betrieb eines Online-Dienstes genutzt, muss der vollstaendige
  Quellcode den Nutzern dieses Dienstes zur Verfuegung gestellt
  werden (§13 AGPLv3).

- **Datenmodell** (`bam_database.json`):
  [CC BY-SA 4.0](LICENSE-DATA). Nutzung, Veraenderung und
  kommerzielle Verwendung sind erlaubt, **Namensnennung ist
  Pflicht**:

  > "Brain-Media Audit Model (BAM), Dr. Holger Reibold,
  > brain-media.de"

  Abgeleitete Datenmodelle muessen unter derselben Lizenz
  weitergegeben werden.

Bitte entfernen Sie die Copyright- und Lizenzhinweise in den
Dateien nicht (siehe AGPLv3 §4/§5 und CC BY-SA 4.0 §3).

---

## BAM Enterprise

Fuer Unternehmen, die BAM produktiv einsetzen wollen, ohne eigene
Infrastruktur zu betreiben:

| | BAM Core (dieses Repo) | BAM Enterprise |
|---|---|---|
| Frameworks | NIS-2, DORA, CRA, EU AI Act, DSGVO, ISO 27001 (74 %) | + ISO 42001, CSA, ISO 27001 (100 %) |
| Betrieb | Selbst gehostet (lokal/eigener Server) | Dedizierte Instanz, DE-Standorte (Saarbruecken/Frankfurt), DSGVO-konform |
| API | Single-User, lokal | Multi-Tenant, White-Label, REST/Webhooks |
| Updates | Manuell (Community/Releases) | Kontinuierliche Experten-Updates |
| Integration | - | Konnektoren fuer GRC, ITSM, SIEM, ERP |
| Support | Community (GitHub Issues) | SLA, persoenlicher Support |
| KI/RAG | Basis-RAG (lokal, `bam_rag.py`) | RAG v2 (Embeddings, semantische Suche, Multi-Tenant) |

Mehr Informationen, kostenloser Quick Check und Kontakt:
**[brain-media.de](https://brain-media.de)**

---

## Ueber Brain-Media.de

Brain-Media.de ist seit 2003 Herausgeber von IT-Sicherheits- und
Compliance-Fachliteratur (100+ Titel, u. a. CISM/CISA-Vorbereitung)
und Anbieter von Executable Compliance als integrierter
Infrastruktur. Das BAM-Modell entstand aus realen Audit-Projekten.

Kontakt: Dr. Holger Reibold, Hubert-Mueller-Str. 52c, 66113
Saarbruecken - info@brain-media.de
