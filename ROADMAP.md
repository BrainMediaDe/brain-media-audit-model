# Roadmap

Diese Roadmap nennt eine Reihenfolge, bewusst keine Termine. BAM Core
ist ein Solo-Projekt neben laufender Verlagsarbeit — feste Daten
würden Erwartungen wecken, die sich nicht verlässlich halten lassen.

## 2.0 — aktuell

Regulatory Change Management, ISO/IEC 27001:2022 Control-Mapping,
Lebenszyklusfelder je Objekt, stabile BAM-IDs
([`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md)), Zitierfähigkeit über
`CITATION.cff` und Zenodo-Archivierung je Release.

## 2.1 — Fristenmanagement

Eine Dashboard-Erweiterung, die aus bereits vorhandenen Daten eine
persönliche Fristenübersicht berechnet: Gap-Check-Antworten
(clientseitig, wie bisher) verknüpft mit den Terminen aus
`regulatory_change_management`. Keine neue Serverkomponente, keine
Bezahlschranke — reine Verknüpfung bestehender, bereits kostenloser
Bausteine.

Vier offene Fundstellenprüfungen (siehe `CHANGELOG.md`, Abschnitt „Zu
prüfen") werden vor 2.1 abgeschlossen.

## 2.2 — Instanz-Layer

Ein Objekt kann pro Organisation unterschiedlich weit umgesetzt sein.
Der Instanz-Layer trennt das allgemeingültige BAM-Objekt von der
organisationsspezifischen Umsetzung, ohne das offene Datenmodell
selbst zu verändern.

## 2.3 — Evidence Layer

Strukturierte Nachweisverwaltung je Objekt, über das bisherige reine
Textfeld `evidence` hinaus — Dateianhänge, Versionierung, Verweis auf
den auslösenden Gap-Check.

## 2.4 — Reporting

Export vordefinierter Auditberichte aus dem Datenmodell heraus, auf
Basis der bis dahin vorhandenen Instanz- und Evidence-Daten.

## 2.5 — Nationale Umsetzungsebene

EU-Richtlinien wie NIS-2 werden national unterschiedlich umgesetzt.
Diese Ebene bildet die Abweichungen einzelner Mitgliedstaaten ab, ohne
die EU-weite Basis der jeweiligen BAM-Objekte zu duplizieren.

## Nicht geplant

- Multi-Tenant-Betrieb oder ein gehostetes Angebot. BAM Core bleibt
  selbst zu betreiben.
- Automatische Übernahme rechtlicher Änderungen ohne fachliche
  Prüfung. Die Einordnung jeder Änderung bleibt kuratiert.
- Eigene ID-Vergabe durch Beitragende, siehe
  [`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md#9-vergabe).

## Stabilität der Bezeichner

Alle BAM-IDs sind ab Version 2.0 stabil im Sinne von
[`docs/IDENTIFIERS.md`](docs/IDENTIFIERS.md). Keine der hier
genannten Versionen sieht eine erneute Umbenennung vor.
