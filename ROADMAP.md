# Roadmap

Diese Roadmap beschreibt die Entwicklungsrichtung von BAM Core. Sie
nennt bewusst **keine Termine**, sondern eine Reihenfolge.

Der Grund: Die Prioritäten von BAM ergeben sich nicht aus einer
internen Planung, sondern aus einer externen Uhr. Die Meldepflichten
des Cyber Resilience Act sind am 11.09.2026 anwendbar geworden, seine
Hauptpflichten greifen am 11.12.2027. Die Hochrisiko-Fristen des EU AI
Act laufen nach der Omnibus-Staffelung am 02.12.2027 und am 02.08.2028
aus, die Nachweispflichten nach dem neugefassten BSIG bis Ende 2028.
Was in dieser Liste oben steht, steht dort, weil ein Gesetz es dorthin
gestellt hat.

Stand: Modellversion 2.0, Release 2.0.3

---

## Aktueller Stand (2.0)

- 59 BAM-Objekte über NIS-2, DORA, CRA, EU AI Act, DSGVO und
  Cross-Framework-Verknüpfungen
- ISO/IEC 27001:2022 Control-Mapping über alle 93 Controls (74 Prozent
  Abdeckung)
- Regulatory Change Management mit Lifecycle, Delta-Einordnung und
  Berechnung der betroffenen Objekte
- Stabile, dauerhaft auflösbare BAM-IDs unter
  [bam.brain-media.de](https://bam.brain-media.de/) (Compliance Trace)
- Lokale REST-API (lesend), Single-User-Dashboard, RAG-Anbindung

---

## Grundlage: Stabilität der Bezeichner

Dieser Punkt steht vor allen Funktionen, weil alles Weitere darauf
aufsetzt. Er ist mit 2.0 eingelöst.

Für Schwachstellen gibt es CVE, für Fehlerklassen CWE, für
Angriffstechniken ATT&CK. Für regulatorische Anforderungen gab es
keinen etablierten Bezeichner. Es fehlte eine gemeinsame Sprache für
"die Anforderung, die NIS-2 Art. 21 Abs. 2 Buchst. d und DORA Art. 28
gleichzeitig abdeckt".

Seit 2.0 gilt verbindlich:

- `bam_id` ist stabil und wird nicht wiederverwendet.
- Ersetzte Objekte werden über `superseded_by` gekennzeichnet, nicht
  gelöscht.
- Jede Version führt im `CHANGELOG.md` neue, geänderte und ersetzte
  IDs einzeln auf.
- Änderungen am Schema erhöhen `schema_version`.
- Jede Objekt-ID ist über eine dauerhafte URL auflösbar.
- Jede Minor-Version wird archiviert und mit einem DOI versehen.

Die vollständigen Zusagen stehen in
[`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md).

---

## Zugänglichkeit: unabhängig von den Versionen

Diese Punkte hängen an keiner Modellversion und sind vorgezogen, weil
sie die Hürde senken, BAM überhaupt einzusetzen oder dagegen zu bauen.
Ohne sie bleibt jede weitere Funktion für Außenstehende schwer
erreichbar.

### Export der Gap-Analyse — erledigt mit 2.0.3

Ergebnisse kommen aus BAM heraus, in einer Form, die in
Audit-Arbeitspapieren weiterverwendbar ist: CSV, XLSX und JSON über
`/api/v2/export/gap` und einen eigenen Reiter im Dashboard.

Der Vorläufer des Reportings aus 2.4. Dort kommt die serverseitige
Erzeugung prüffähiger Dokumente dazu.

### Container-Image und Druckansicht

Heute setzt der Einstieg ein Repository-Klon, eine Python-Umgebung und
einen manuellen Start voraus. Ein `docker compose up` ersetzt das. Das
ist weniger eine Funktion als eine Entscheidung darüber, wie viele
Leute BAM je ausprobieren.

Dazu eine Druckansicht, die aus dem Bewertungsstand ein Dokument macht
statt eines ausgedruckten Tabellenblatts: Deckblatt, Zusammenfassung
und Feststellungen als Fließtext. Das PDF entsteht über den
Druckdialog des Browsers, ohne zusätzliche Bibliothek. Der
serverseitige Berichtsgenerator bleibt 2.4 vorbehalten.

### JSON Schema mit CI-Validierung

Ursprünglich in 2.5 eingeplant, hier vorgezogen. Das Schema ist keine
Dokumentationsaufgabe, sondern die Voraussetzung dafür, dass jemand
anderes gegen BAM entwickeln kann, ohne sich die Struktur aus den Daten
zu erschließen. Es wird bei jedem Commit geprüft, weil ein nicht
erzwungenes Schema nach wenigen Monaten falsch ist.

### Versionierte Daten-URLs

Das vollständige Modell unter einer stabilen Adresse, je Minor-Version
und zusätzlich als Verweis auf die aktuelle. Damit kann ein fremdes
System BAM beziehen, ohne das Repository anzufassen, und sich auf einen
Stand festlegen.

---

## In Arbeit

### 2.1 Fristenmanagement

Fristen werden zu eigenständigen Objekten mit vier Typen:

| Typ | Bedeutung | Beispiel |
|---|---|---|
| `statutory` | Fester Stichtag aus dem Rechtsakt | CRA Art. 14 seit 11.09.2026 |
| `recurring` | Wiederkehrende Pflicht | Jährliche Überprüfung, TLPT-Zyklus |
| `event_triggered` | Startet mit einem Ereignis, nicht mit einem Datum | 24h/72h/1 Monat nach NIS-2 Art. 23 |
| `derived` | Selbst gesetztes Zieldatum | Interne Umsetzungsplanung |

Der wichtigste Typ ist `event_triggered`. Meldefristen sind kein
Kalender, sondern eine Stoppuhr: Sie starten mit der Kenntniserlangung
und laufen in Stunden. BAM Core 2.1 bildet diese Ketten als Ablauf ab,
nicht als Termin.

Fristen werden außerdem an `regulatory_change_management` gekoppelt.
Ein Change-Eintrag wie die Omnibus-Verordnung verschiebt dann die
Frist, statt ihr zu widersprechen.

---

## Als Nächstes

### 2.2 Instanz-Layer

Trennung von Kanon und Zustand. `bam_database.json` bleibt das
versionierte, frei lizenzierte Modell. Der Bewertungszustand einer
Organisation wandert in eine eigene Persistenz: Gap-Status je
`bam_id`, Begründung, Verantwortlicher, Zieldatum, Änderungshistorie.
Dazu schreibende API-Endpunkte und ein append-only Audit-Log.

Ohne diesen Layer ist eine Frist nur Anzeige, weil sie keinen
Verantwortlichen und keinen persistenten Erledigungsstatus hat. Und
ohne ihn gibt es keinen Mehrbenutzerbetrieb, weil sich sonst alle
Nutzer einer Installation dieselbe Bewertung teilen.

### 2.3 Evidence Layer

Nachweise werden eigenständige Objekte mit N:M-Beziehung zu den
Anforderungen. Erst damit gilt "Collect Once. Comply Many." auch für
den Nachweis und nicht nur für die Anforderung: Ein
Berechtigungsreview belegt gleichzeitig Pflichten aus NIS-2, DORA und
ISO 27001.

Neu unter anderem: Gültigkeitszeitraum, Prüfintervall, Freigabestatus,
Integritätsnachweis. Nachweise altern, und ein abgelaufener Nachweis
erzeugt automatisch eine wiederkehrende Frist aus 2.1.

Zusätzlich ein eigener Zustand für "als erfüllt bewertet, aber kein
Nachweis hinterlegt". Das ist der Unterschied zwischen einer
Selbstauskunft und einem prüffähigen Ergebnis.

**Ablage über WebDAV.** Ein Nachweisobjekt verweist auf eine Datei,
statt sie zu enthalten: URI, Prüfsumme, Gültigkeitszeitraum. Die Datei
bleibt beim Betreiber. Die Anbindung wird generisch über WebDAV
umgesetzt und funktioniert damit mit Nextcloud, ownCloud, Seafile und
SharePoint gleichermaßen; Nextcloud dient als dokumentierter
Referenzfall, nicht als Abhängigkeit.

BAM wird dabei ausdrücklich kein Dokumentenmanagement. Prüfunterlagen
verbleiben dort, wo sie ohnehin liegen.

---

## Später

### 2.4 Reporting

Erzeugung prüffähiger Dokumente aus dem vorhandenen Modell:

- Anwendbarkeitserklärung (Statement of Applicability) aus dem
  ISO-27001-Mapping
- Managementbericht für das Leitungsorgan
- Maßnahmenplan mit Aufwandsschätzung und Priorisierung nach Risiko
  pro Personentag
- Prüferpaket mit Anforderung, Nachweisverweis und Änderungshistorie

Zusätzlich wird `book_reference` von der reinen Titelangabe auf eine
Kapitelzuordnung erweitert, damit Berichte auf die erläuternde Stelle
verweisen können statt auf den Gesamttitel.

### 2.5 Nationale Umsetzungsebene

BAM bildet NIS-2 heute auf EU-Artikelebene ab. Geprüft wird in
Deutschland gegen das neugefasste BSI-Gesetz. Geplant ist ein Feld
`national_implementation` je Objekt, das die Zuordnung zu den
nationalen Vorschriften aufnimmt, zunächst für Deutschland.

Reihenfolge bei der Framework-Erweiterung: BSIG vor vollständiger
ISO-27001-Abdeckung vor ISO 42001 vor BSI IT-Grundschutz vor
ISO 22301. Aufsichtsrechtliche Anforderungen aus MaRisk und BAIT sind
als eigener Zweig vorgemerkt, weil sie sich großflächig mit NIS-2,
DORA und ISO 27001 überschneiden und damit gut in die
Cross-Framework-Logik passen.

### 3.0 Mandantenfähigkeit

Mehrere Organisationen, Rollen (Owner, Reviewer, Auditor),
Freigabeworkflow, revisionssicheres Protokoll. Die Schwelle vom
Einzelplatzwerkzeug zum mehrbenutzerfähigen System.

---

## Erwogen, noch nicht entschieden

- **Nextcloud-Integration.** Eine schlanke App, die BAM in eine
  bestehende Nextcloud-Instanz einbindet und deren Anmeldung
  durchreicht. Setzt den Instanz-Layer aus 2.2 voraus, weil eine
  geteilte Installation ohne Zustand je Benutzer nicht funktioniert.
  Die tiefere Verzahnung, also Nachweise aus Files, Maßnahmen in Deck
  und Fristen im Kalender, wäre ein weiterer Schritt danach.
- **Maschinenlesbarer Änderungsfeed.** Die Einträge aus
  `regulatory_change_management` als eigene, abonnierbare Datei, damit
  nachgelagerte Systeme Änderungen auswerten können, ohne das gesamte
  Modell zu vergleichen. Entspricht dem, was redaktionell bereits als
  Compliance Delta erscheint.
- **Mehrländer-Mapping.** Dieselbe EU-Anforderung gegen mehrere
  nationale Umsetzungen. Fachlich der größte offene Punkt und
  gleichzeitig der, der am wenigsten allein zu leisten ist. Beiträge
  zu Österreich und zur Schweiz wären der naheliegende Anfang, siehe
  "Mitwirken".
- **MCP-Server.** Strukturierter Zugriff auf Anforderungen, Controls
  und Change-Impact für Agenten und LLM-Workflows. Wird günstig,
  sobald die Daten unter stabilen URLs liegen.
- **OpenAPI-Spezifikation.** Sinnvoll erst, wenn die schreibende API
  aus 2.2 steht.
- **Konnektoren für technische Nachweise.** Verzeichnisdienst,
  Schwachstellenscanner, Backup-Reports. Der Schritt von der
  Selbstauskunft zur Messung.
- **Lieferkette.** Eigener Objekttyp für Dienstleister, orientiert am
  DORA-Informationsregister und an NIS-2 Art. 21 Abs. 2 Buchst. d.
- **Risikoquantifizierung.** Erwartungswerte statt der heutigen
  Likelihood-Impact-Heuristik. Die Bußgeldrahmen liegen bereits im
  Modell.
- **OSCAL-Export.** Interoperabilität mit dem NIST-Format für Controls
  und Assessments. Derzeit ohne erkennbare Nachfrage im
  deutschsprachigen Raum.
- **Englische Fassung** des Datenmodells.

---

## Nicht geplant

Diese Punkte sind bewusst ausgeschlossen. Entsprechende Issues werden
geschlossen, nicht diskutiert.

- **Kein vollständiges GRC-Werkzeug.** BAM ist ein Datenmodell mit
  Referenzimplementierung. Der Wert liegt im Modell, nicht in der
  Oberfläche.
- **Kein Dokumentenmanagement.** Nachweisdateien verbleiben beim
  Betreiber. BAM speichert den Verweis, nicht das Dokument.
- **Keine automatische Erzeugung von Anforderungsobjekten aus
  Gesetzestexten durch Sprachmodelle.** Die fachliche Kuratierung ist
  der Kern des Modells. Für noch nicht entschiedene Verfahren werden
  weiterhin keine spekulativen Objekte angelegt, siehe `policy_rule`
  je Eintrag im Regulatory Change Management.
- **Keine Breite vor Tiefe.** Zusätzliche Frameworks werden nur
  aufgenommen, wenn sie auf allen sechs Ebenen ausgearbeitet sind.
- **Keine kryptografisch signierten Nachweise.** Technisch reizvoll,
  in der Prüfpraxis aber ohne erkennbare Nachfrage. Prüfer verlangen
  Plausibilität, nicht Beweisbarkeit.

---

## Mitwirken

Beiträge sind willkommen, insbesondere zu fehlenden Frameworks und zur
nationalen Umsetzungsebene. Wer die Umsetzung in Österreich oder der
Schweiz kennt, findet hier die größte offene Lücke. Hinweise dazu in
`docs/CONTRIBUTING.md`.

Vorschläge zur Roadmap gerne als Issue mit dem Label `roadmap`. Bitte
vorher den Abschnitt "Nicht geplant" lesen.
