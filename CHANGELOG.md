# Changelog

Alle nennenswerten Änderungen am Brain-Media Audit Model werden hier
dokumentiert.

Das Format folgt lose [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

**Zwei Versionsnummern, zwei Bedeutungen.** Die Modellversion
bezeichnet den Stand des Datenmodells und ist das, was zitiert und mit
einem DOI versehen wird. Die Release-Nummer bezeichnet den Stand des
Repositorys einschließlich der Referenzimplementierung. Ein Release wie
2.0.3 kann die Implementierung erweitern, ohne die Modellversion zu
berühren, und berührt damit auch keine Zitation.

Ab Modellversion 2.0 gelten die Zusagen aus
[`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md): BAM-IDs sind stabil,
werden nicht wiederverwendet und nicht gelöscht.

---

## [2.0.4] – 2026-10-07

Modellversion unverändert 2.0. Das Datenmodell wurde nicht angefasst.

### Neu: Bericht und Druckansicht

Neben dem Arbeitspapier aus 2.0.3 gibt es jetzt eine Dokumentfassung
für Leitungsorgan, Ablage und Prüfer.

- Schaltfläche **Bericht drucken (PDF)** im Reiter Export. Sie erzeugt
  Deckblatt, Zusammenfassung je Regulierung und die Feststellungen als
  Fließtext, nach Risikoscore absteigend, dazu eine Liste der noch
  nicht bewerteten Prüffragen.
- Eigenes Druck-Stylesheet (A4, Seitenumbrüche vor jedem Abschnitt,
  keine umbrochenen Einzelpositionen). Das PDF entsteht über den
  Druckdialog des Browsers; es wird **keine PDF-Bibliothek** benötigt.
- Der Bericht ist bewusst kein ausgedrucktes Tabellenblatt. Die
  21-spaltige Matrix bleibt dem Export in CSV und XLSX vorbehalten,
  der serverseitige Berichtsgenerator kommt mit 2.4.
- Der Erfüllungsgrad wird als Untergrenze ausgewiesen, solange nicht
  alle Prüffragen bewertet sind.

### Neu: Container-Image

- `Dockerfile`, `compose.yml`, `.dockerignore` und `requirements.txt`.
  `docker compose up` genügt, danach ist das Dashboard unter
  `http://localhost:5000` erreichbar.
- Im Container läuft waitress statt des Flask-Entwicklungsservers, der
  Prozess läuft nicht als root, und ein Healthcheck prüft
  `/api/v2/meta`.
- `bam_database.json` ist als Volume eingebunden, sodass ein eigener
  Modellstand ohne Neubau des Images verwendet werden kann.
- Der Port ist in `compose.yml` bewusst auf `127.0.0.1` gebunden. BAM
  Core 2.0.x kennt weder Authentifizierung noch Mandanten und gehört
  nicht ungeschützt ins Netz.

### Geändert

- Das Dashboard lädt beim Start zusätzlich `/api/v2/meta`, damit
  Modellversion und Modellstand im Bericht erscheinen.

---

## [2.0.3] – 2026-10-07

Modellversion unverändert 2.0. Das Datenmodell wurde nicht angefasst,
alle BAM-IDs bleiben gültig, bestehende Zitate und der DOI der
Modellversion 2.0 sind davon nicht betroffen.

### Neu: Export der Gap-Analyse

Ergebnisse lassen sich jetzt in einer Form ausgeben, die in
Audit-Arbeitspapieren weiterverwendbar ist.

- Neues Modul `bam_export.py` mit den Formaten CSV, XLSX und JSON.
- Neuer Endpunkt `POST /api/v2/export/gap`. Der Bewertungsstand wird im
  Request übergeben; der Endpunkt ist zustandslos und speichert nichts.
  `POST` bedeutet hier "Daten mitgeben", nicht "Daten anlegen".
- Neuer Endpunkt `GET /api/v2/export/gap` liefert dasselbe
  Arbeitspapier ohne Bewertung, also eine leere Vorlage.
- Neuer Endpunkt `GET /api/v2/export/formats` nennt die Formate, die
  die jeweilige Installation ausliefern kann.
- Neuer Reiter **Export** im Dashboard, mit Feldern für Organisation,
  bewertende Stelle und Anmerkung sowie der Option, nur Feststellungen
  auszugeben. Ist der API-Endpunkt nicht erreichbar, erzeugt das
  Dashboard ersatzweise eine CSV im Browser.

Das Arbeitspapier umfasst 21 Spalten: Identifikation, Anforderung mit
Fundstelle, Prüffrage, Bewertung, Feststellung, Priorität, Risikoscore,
Bußgeldrahmen, Maßnahme mit Aufwandsschätzung in Personentagen,
Zeithorizont, Control, Nachweisart, ISO-27001-Zuordnung, Querverweise
und die dauerhafte Adresse des Bezeichners.

Die XLSX-Mappe enthält zusätzlich ein Deckblatt mit Organisation,
bewertender Stelle, Exportzeitpunkt und Modellstand sowie eine
Zusammenfassung je Regulierung mit Erfüllungsgrad. Die Punktlogik
entspricht der des Dashboards: erfüllt zählt 1, teilweise erfüllt 0,5,
nicht erfüllt 0, bezogen auf alle Objekte mit Prüffrage.

### Geändert

- `GET /api/v2/meta` gibt zusätzlich `version` und `released` zurück.
- `bam_database.json` führt die Felder `version` und `released`, damit
  Modellversion und Modellstand nicht mehr aus `schema_version`
  abgeleitet werden müssen.

### Abhängigkeiten

- XLSX benötigt `openpyxl`. Fehlt das Paket, antwortet der Endpunkt mit
  einem Hinweis und `501`; CSV und JSON funktionieren unverändert.

---

## [2.0.2] – 2026-09-09 und [2.0.1] – 2026-09-08

Technische Re-Releases ohne inhaltliche Änderung gegenüber 2.0. Sie
wurden angelegt, damit die Zenodo-Verknüpfung greift und ein DOI
vergeben wird; das ursprüngliche 2.0-Release lag vor der Aktivierung.

---

## [2.0] – 2026-09-08

Modellversion 2.0.

### Neu

- **Regulatory Change Management.** Änderungsvorgänge werden als eigene
  Einträge geführt, mit Lebenszyklus, Delta-Einordnung und Berechnung
  der betroffenen Objekte.
- **ISO/IEC 27001:2022 Control-Mapping** über alle 93 Controls des
  Annex A.
- **Lebenszyklusfelder** je Objekt: `lifecycle`, `valid_from`, sowie
  `superseded_by` und `supersedes`, wo einschlägig.
- **`docs/IDENTIFIERS.md`** mit den verbindlichen Zusagen zu Aufbau,
  Stabilität und Zitierweise der BAM-IDs.
- **`CITATION.cff`** und **`.zenodo.json`**, damit das Modell zitierfähig
  ist und je Modellversion einen DOI erhält.
- **`build_ids.py`** erzeugt Compliance Trace, die auflösbaren Seiten
  unter `bam.brain-media.de/id/<BAM-ID>`, menschenlesbar und als JSON.

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

Offen ist außerdem die Vereinheitlichung der Control-Nummern in
`iso27001_mapping`: Ein Teil der Zuordnungen verwendet die Annex-A-
Nummerierung aus ISO/IEC 27001:2013, ein Teil die aus der Fassung 2022.

---

## [1.x] – bis 2026-08

Frühere Stände ohne durchgehende Versionierung. Die Stabilitätszusage
für Bezeichner gilt ab Modellversion 2.0.

---

## Geplant

Siehe [`ROADMAP.md`](ROADMAP.md). Die Roadmap nennt bewusst keine
Termine, sondern eine Reihenfolge.
