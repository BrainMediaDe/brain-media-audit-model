# Roadmap

Diese Roadmap beschreibt die Entwicklungsrichtung von BAM Core. Sie
nennt bewusst **keine Termine**, sondern eine Reihenfolge.

Der Grund: Die Prioritäten von BAM ergeben sich nicht aus einer
internen Planung, sondern aus einer externen Uhr. Der Cyber Resilience
Act macht seine Meldepflichten am 11.09.2026 anwendbar, die
Hochrisiko-Fristen des EU AI Act laufen nach der Omnibus-Staffelung am
02.12.2027 und am 02.08.2028 aus, die Nachweispflichten nach dem
neugefassten BSIG greifen bis Ende 2028. Was in dieser Liste oben
steht, steht dort, weil ein Gesetz es dorthin gestellt hat.

Stand: BAM Core 2.0

---

## Aktueller Stand (2.0)

Verfügbar und dokumentiert:

- 59 BAM-Objekte über NIS-2, DORA, CRA, EU AI Act, DSGVO und
  Cross-Framework-Verknüpfungen
- ISO 27001:2022 Control-Mapping über alle 93 Controls (74 Prozent
  Abdeckung)
- Regulatory Change Management mit Lifecycle, Delta-Einordnung und
  Live-Impact-Berechnung
- Lokale REST-API, Single-User-Dashboard, RAG-Anbindung

---

## In Arbeit

### 2.1 Fristenmanagement

Fristen werden zu eigenständigen Objekten mit vier Typen:

| Typ | Bedeutung | Beispiel |
|---|---|---|
| `statutory` | Fester Stichtag aus dem Rechtsakt | CRA Art. 14 ab 11.09.2026 |
| `recurring` | Wiederkehrende Pflicht | Jährliche Überprüfung, TLPT-Zyklus |
| `event_triggered` | Startet mit einem Ereignis, nicht mit einem Datum | 24h/72h/1 Monat nach NIS-2 Art. 23 |
| `derived` | Selbst gesetztes Zieldatum | Interne Umsetzungsplanung |

Der wichtigste Typ ist `event_triggered`. Meldefristen sind kein
Kalender, sondern eine Stoppuhr: Sie starten mit der Kenntniserlangung
und laufen in Stunden. BAM Core 2.1 bildet diese Ketten als Ablauf ab,
nicht als Termin.

Fristen werden außerdem an `regulatory_change_management` gekoppelt.
Ein Change-Eintrag wie der AI-Omnibus verschiebt dann die Frist, statt
ihr zu widersprechen.

---

## Als Nächstes

### 2.2 Instanz-Layer

Trennung von Kanon und Zustand. `bam_database.json` bleibt das
versionierte, frei lizenzierte Modell. Der Bewertungszustand einer
Organisation wandert in eine eigene Persistenz: Gap-Status je
`bam_id`, Begründung, Verantwortlicher, Zieldatum, Änderungshistorie.
Dazu schreibende API-Endpunkte und ein append-only Audit-Log.

Ohne diesen Layer ist eine Frist nur Anzeige, weil sie keinen
Verantwortlichen und keinen persistenten Erledigungsstatus hat.

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

### 2.5 Nationale Umsetzungsebene und Schema-Härtung

BAM bildet NIS-2 heute auf EU-Artikelebene ab. Geprüft wird in
Deutschland gegen das neugefasste BSI-Gesetz. Geplant ist ein Feld
`national_implementation` je Objekt, das die Zuordnung zu den
nationalen Vorschriften aufnimmt, zunächst für Deutschland.

Parallel: JSON Schema für das Datenmodell und Validierung in der CI.
Ohne Schema sind Beiträge von außen nicht handhabbar.

Reihenfolge bei der Framework-Erweiterung: BSIG vor vollständiger
ISO-27001-Abdeckung vor ISO 42001 vor BSI IT-Grundschutz vor ISO 22301.

### 3.0 Mandantenfähigkeit

Mehrere Organisationen, Rollen (Owner, Reviewer, Auditor),
Freigabeworkflow, revisionssicheres Protokoll. Die Schwelle vom
Einzelplatzwerkzeug zum mehrbenutzerfähigen System.

---

## Erwogen, noch nicht entschieden

- **BAM als MCP-Server.** Strukturierter Zugriff auf Anforderungen,
  Controls und Change-Impact für Agenten und LLM-Workflows.
- **Konnektoren für technische Nachweise.** Verzeichnisdienst,
  Schwachstellenscanner, Backup-Reports. Der Schritt von der
  Selbstauskunft zur Messung.
- **Lieferkette.** Eigener Objekttyp für Dienstleister, orientiert am
  DORA-Informationsregister und an NIS-2 Art. 21 Abs. 2 Buchst. d.
- **Risikoquantifizierung.** Erwartungswerte statt der heutigen
  Likelihood-Impact-Heuristik. Die Bußgeldrahmen liegen bereits im
  Modell.
- **Englische Fassung** des Datenmodells.

---

## Nicht geplant

Diese Punkte sind bewusst ausgeschlossen. Entsprechende Issues werden
geschlossen, nicht diskutiert.

- **Kein vollständiges GRC-Werkzeug.** BAM ist ein Datenmodell mit
  Referenzimplementierung. Der Wert liegt im Modell, nicht in der
  Oberfläche.
- **Keine automatische Erzeugung von Anforderungsobjekten aus
  Gesetzestexten durch Sprachmodelle.** Die fachliche Kuratierung ist
  der Kern des Modells. Für noch nicht entschiedene Verfahren werden
  weiterhin keine spekulativen Objekte angelegt, siehe `policy_rule`
  je Eintrag im Regulatory Change Management.
- **Keine Breite vor Tiefe.** Zusätzliche Frameworks werden nur
  aufgenommen, wenn sie auf allen sechs Ebenen ausgearbeitet sind.

---

## Kompatibilität des Datenmodells

Wer eigene Bewertungen an `bam_id`-Werte hängt, braucht Verlässlichkeit
beim Upgrade. Ab 2.1 gilt:

- `bam_id` ist stabil. IDs werden nicht wiederverwendet.
- Entfernte oder ersetzte Objekte werden über `superseded_by`
  gekennzeichnet, nicht gelöscht.
- Jede Version führt im `CHANGELOG.md` neue, geänderte und ersetzte
  IDs einzeln auf.
- Änderungen am Schema selbst erhöhen `schema_version`.

---

## Mitwirken

Beiträge sind willkommen, insbesondere zu fehlenden Frameworks und zur
nationalen Umsetzungsebene. Hinweise dazu in `docs/CONTRIBUTING.md`.

Vorschläge zur Roadmap gerne als Issue mit dem Label `roadmap`. Bitte
vorher den Abschnitt "Nicht geplant" lesen.
