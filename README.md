# Brain-Media Audit Model (BAM) Core

**Offenes Datenmodell und Referenzimplementierung fuer
Multi-Framework-Compliance (NIS-2, DORA, CRA, EU AI Act, ISO 27001).
BAM Core 2.0: Regulatory Change Management (AI-Omnibus implementiert)**

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
| `bam_database.json` | Das BAM-Datenmodell: 59 BAM-Objekte (Requirement -> Evidence) fuer NIS-2, DORA, CRA, EU AI Act, DSGVO sowie Cross-Framework-Verknuepfungen, plus ISO 27001:2022 Control-Mapping (93 Controls) |
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
| EU AI Act | 8 | Art. 3-14, 26, 62, 74, plus AI-Omnibus-Fristobjekt |
| DSGVO | 13 | Art. 5, 6, 13-14, 15-22, 24, 25, 28, 30, 32-39, 44-49 |
| Cross-Framework | 7 | Mehrfachverknuepfungen (inkl. gemeinsames VVT/Asset/KI-Inventar) |
| ISO 27001:2022 | 93 Controls | 74 % Coverage (69 vollstaendig, 24 teilweise) |

**Nicht (oder noch nicht) in BAM Core enthalten:** ISO 42001, Cyber
Solidarity Act (CSA), vollstaendige ISO-27001-Abdeckung (100 %).

Contributions zur Erweiterung der Framework-Abdeckung sind
willkommen - siehe [CONTRIBUTING.md](docs/CONTRIBUTING.md).

---

## Regulatory Change Management (BAM Core 2.0)

BAM beantwortet damit nicht nur "Was gilt?" (Objekte) und "Sind wir
compliant?" (Gap-Check), sondern zusaetzlich "Was aendert sich?".
Laufende Gesetzesaenderungen werden im Bereich
`regulatory_change_management` getrackt, getrennt von den eigentlichen
BAM-Objekten - so bleiben die Requirement-Objekte faktenbasiert, auch
waehrend ein Gesetzgebungsverfahren noch offen ist.

**Lifecycle:** Jeder Eintrag durchlaeuft `proposal` -> `negotiation` ->
`adopted` -> `published` -> `effective` (oder `withdrawn` /
`repealed` / `superseded`). Nur im Status `effective` ist ein Eintrag
mit vollstaendigen BAM-Objekten verknuepft.

**Grundregel:** Fuer noch nicht entschiedene Verfahren (Status
`negotiation` o.ae.) werden KEINE spekulativen BAM-Objekte angelegt -
siehe `policy_rule` je Eintrag. Pro betroffenem Objekt haelt ein
`deltas`-Eintrag zusaetzlich die fachliche Einordnung fest:
`change_type`, sowie Impact getrennt nach `requirement_impact`,
`control_impact`, `evidence_impact`, plus ein `human_review_required`-
Flag. Diese Einordnung ist manuell fachlich kuratiert, keine
automatische Texterkennung.

**Vier API-Endpunkte dafuer:**

| Endpunkt | Zweck |
|---|---|
| `GET /api/v2/regulatory-changes` | Liste aller getrackten Aenderungsverfahren |
| `GET /api/v2/regulatory-changes/<id>/impact` | Direkt betroffene Objekte + indirekt betroffene Objekte (ueber `cross_refs` eine Ebene weiter), inkl. Deltas |
| `GET /api/v2/objects/<bam_id>/changes` | Alle Aenderungen, die ein bestimmtes BAM-Objekt betreffen |
| `GET /api/v2/objects/<bam_id>` | Einzelnes Objekt inkl. `active_regulatory_changes` (Basis fuer den Dashboard-Warnhinweis) |

Im Dashboard: eigener Tab "Regulatory Changes", zusaetzlich ein
Warnhinweis (⚠) bei Controls, die von einer laufenden Aenderung
betroffen sind.

**Aktueller Stand, drei getrackte Initiativen:**

- **AI-Omnibus** (VO (EU) 2026/1744, Status `effective`): hat die
  EU-AI-Act-Hochrisikofristen verschoben (Anhang III: 02.12.2027,
  Anhang I: 02.08.2028) - vollstaendiges BAM-Objekt
  (`AIACT-090-OMNIBUS-FRIST`) plus Deltas fuer alle drei betroffenen
  Objekte.
- **Digital Omnibus - DSGVO/Data Act** (Status `negotiation`): 2
  bestehende DSGVO-Objekte als beobachtet vermerkt, bewusst ohne neues
  BAM-Objekt, solange das Verfahren offen ist.
- **Digital Omnibus - ePrivacy/NIS-2/DORA/CER** (Status
  `negotiation`): noch kein bestaetigtes Trilog-Datum, rein zur
  Beobachtung vermerkt.

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

## Ueber Brain-Media.de

Brain-Media.de ist seit 2003 Herausgeber von IT-Sicherheits- und
Compliance-Fachliteratur (100+ Titel, u. a. CISM/CISA-Vorbereitung)
und Anbieter von Executable Compliance als integrierter
Infrastruktur. Das BAM-Modell entstand aus realen Audit-Projekten.

Kontakt: Dr. Holger Reibold, Hubert-Mueller-Str. 52c, 66113
Saarbruecken - info@brain-media.de
