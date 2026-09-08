# Changelog

Alle nennenswerten Änderungen am Brain-Media Audit Model werden hier
dokumentiert.

Das Format folgt lose [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).
Die Versionsnummer bezeichnet den Stand des Datenmodells, nicht die
Referenzimplementierung.

Ab dieser Version gelten die Zusagen aus [`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md):
BAM-IDs sind stabil, werden nicht wiederverwendet und nicht gelöscht.

---

## [2.0] – 2026-09-08

### Neu

- **Regulatory Change Management.** Änderungsvorgänge werden als eigene
  Einträge geführt, mit Lebenszyklus, Delta-Einordnung und Berechnung
  der betroffenen Objekte.
- **ISO/IEC 27001:2022 Control-Mapping** über alle 93 Controls des
  Annex A, Abdeckung 74 Prozent.
- **Lebenszyklusfelder** je Objekt: `lifecycle`, `valid_from`, sowie
  `superseded_by` und `supersedes`, wo einschlägig.
- **`docs/IDENTIFIERS.md`** mit den verbindlichen Zusagen zu Aufbau,
  Stabilität und Zitierweise der BAM-IDs.
- **`CITATION.cff`** und **`.zenodo.json`**, damit das Modell zitierfähig
  ist und je Release einen DOI erhält.
- **`build_ids.py`** erzeugt die auflösbaren Seiten unter
  `bam.brain-media.de/id/<BAM-ID>`, menschenlesbar und als JSON.

### Einmalige ID-Normalisierung

Diese sechs Bezeichner wurden vor Inkrafttreten der Stabilitätszusage
angepasst. Es ist die letzte Umbenennung; künftige Änderungen an
Objekten erzeugen neue IDs mit `supersedes`.

| bisher | neu | Grund |
|---|---|---|
| `CRA-001-SECURITY-BY-DESIGN` | `CRA-001a-SECURITY-BY-DESIGN` | Symmetrie zu `CRA-001b`; ohne Buchstabe wäre die Vorschrift als Ganzes gemeint |
| `CRA-002b-CVD` | `CRA-002c-CVD` | Der Buchstabe in der ID widersprach der Fundstelle Anh. I §2c |
| `NIS2-021-NETZ` | `NIS2-901-NETZSEGMENTIERUNG` | Fasst §2e und §2i zusammen, ist damit eine eigene Ableitung ohne Fundstelle |
| `NIS2-090-PLAN` | `NIS2-900-UMSETZUNGSPLAN` | `090` war ein Zähler, keine Artikelnummer |
| `AIACT-090-OMNIBUS-FRIST` | `AIACT-900-OMNIBUS-FRIST` | wie vor |
| `CROSS-DSGVO-VVT-ROPA` | `CROSS-INVENTAR-001` | Bricht das Muster `CROSS-<THEMA>-<LFDNR>` |

Unverändert bleiben 53 Bezeichner. `NIS2-021-DOKU` behält seine Form,
weil die fehlende Buchstabenangabe hier Bedeutung trägt: Das Objekt
bezieht sich auf Art. 21 Abs. 2 insgesamt.

### Zu prüfen

Bei vier Objekten steht eine fachliche Prüfung der Fundstelle im Feld
`article` aus. Die IDs sind davon nicht betroffen und ändern sich auch
dann nicht, wenn die Angabe korrigiert wird.

- `AIACT-062-MELDUNG`
- `DORA-017-KLASSIFIZIERUNG`
- `DORA-018-MELDUNG`
- `DORA-026-DRITTPARTEI` und `DORA-030-REGISTER`

---

## [1.x] – bis 2026-08

Frühere Stände ohne durchgehende Versionierung. Die Stabilitätszusage
für Bezeichner gilt ab 2.0.

---

## Geplant

Siehe [`ROADMAP.md`](ROADMAP.md). Die Roadmap nennt bewusst keine
Termine, sondern eine Reihenfolge.
