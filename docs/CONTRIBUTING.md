# Beitragen zu BAM Core

Danke für Ihr Interesse an BAM Core. Dieses Dokument fasst zusammen,
wie ein Beitrag eingereicht wird und was dabei nicht Ihre Aufgabe ist.

## Eine Anforderung einreichen

1. Prüfen Sie zuerst, ob die Fundstelle bereits als Objekt existiert
   — durchsuchen Sie `bam_database.json` oder die aufgelösten Seiten
   unter `bam.brain-media.de/id/`.
2. Öffnen Sie einen Pull Request mit dem vorgeschlagenen Objekt in
   demselben Format wie die bestehenden Einträge: `regulation`,
   `article`, `requirement`, `gap_check`, `remediation`, `risk`,
   `control`, `evidence`, `cross_refs`.
3. Belegen Sie die Fundstelle mit einem Verweis auf den Gesetzestext.
   Ohne nachvollziehbare Quelle wird ein Vorschlag nicht übernommen.

Kleinere Korrekturen (Tippfehler, falsch zugeordnete Artikelnummern)
können Sie direkt als Pull Request gegen die betroffene Zeile stellen.

## Was Sie nicht selbst vergeben

**BAM-IDs vergibt ausschließlich die Modellpflege** — das gilt auch für
eigene, im Pull Request vorgeschlagene Objekte. Schlagen Sie den
Inhalt vor, nicht den Bezeichner; die endgültige ID wird beim Merge
nach den Regeln in [`IDENTIFIERS.md`](IDENTIFIERS.md) vergeben.

Hintergrund: Ohne diese Regel würde jeder externe Beitrag eigene
ID-Konventionen mitbringen, und das Modell würde an genau dieser
Stelle zerfasern.

## Was bewusst nicht geplant ist

Bevor Sie einen größeren Vorschlag ausarbeiten, lohnt sich ein Blick
in den Abschnitt [„Nicht geplant"](../ROADMAP.md#nicht-geplant) der
Roadmap — unter anderem Multi-Tenant-Betrieb und automatische
Übernahme rechtlicher Änderungen ohne fachliche Prüfung stehen dort
bewusst nicht auf der Liste.

## Fragen vorab

Bei größeren Änderungen oder wenn unklar ist, ob etwas als Änderung
oder neues Objekt zählt (siehe [`IDENTIFIERS.md`, Abschnitt 5](IDENTIFIERS.md#5-ändern-vs-neuanlegen)),
öffnen Sie gerne zuerst ein Issue, bevor Sie den Pull Request
ausarbeiten.
