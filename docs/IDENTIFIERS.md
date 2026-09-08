# BAM-IDs: Aufbau, Stabilität, Zitierweise

## 1. Zweck

Regulatorische Anforderungen brauchen einen stabilen Bezugspunkt, auf
den sich Werkzeuge, Artikel und Audits verlassen können — vergleichbar
mit der Rolle, die CVE-Kennungen in der Schwachstellenverwaltung
einnehmen. BAM-IDs sollen diese Rolle übernehmen können. Dafür gilt ab
2.0 verbindlich:

## 2. Grundregel

Eine einmal vergebene BAM-ID wird **nicht wiederverwendet, nicht
gelöscht und nicht umbenannt** — auch dann nicht, wenn sich die zugrunde
liegende Vorschrift ändert oder neu nummeriert wird.

Die IDs sind ausdrücklich **opak**. Wenn NIS-2 neu gefasst wird, bleibt
`NIS2-021d-LIEFERKETTE` bestehen, auch wenn Art. 21 dann anders
nummeriert ist. Das fühlt sich beim Lesen falsch an und ist trotzdem
die einzige Variante, die trägt.

## 3. Aufbau

Das Muster lautet `<FRAMEWORK>-<ARTIKELNUMMER><BUCHSTABE>-<SLUG>`, zum
Beispiel `NIS2-021d-LIEFERKETTE`. Slug und Buchstabe sind reine
Lesehilfen, kein Bestandteil der Identität — die ID als Ganzes ist der
Schlüssel.

Fehlt der Buchstabe, obwohl die Fundstelle in Buchstaben gegliedert
ist, meint die ID **die Vorschrift als Ganzes**. `NIS2-021-DOKU`
bezieht sich damit auf Art. 21 Abs. 2 insgesamt, nicht auf einen
einzelnen Buchstaben.

`CROSS`-Objekte folgen dem Muster `CROSS-<THEMA>-<LFDNR>`, weil sie
keiner einzelnen Fundstelle zugeordnet sind.

## 4. Zitierweise

Ein bestimmter Modellstand wird als `BAM:<ID>@<VERSION>` referenziert,
zum Beispiel `BAM:NIS2-023-MELDUNG@2.0`. Das erlaubt, sich auf den
genauen Stand eines Objekts zu einem bestimmten Zeitpunkt zu beziehen,
unabhängig davon, wie sich das Objekt später weiterentwickelt.

Aufgelöst werden IDs unter `https://bam.brain-media.de/id/<BAM-ID>`,
menschenlesbar als HTML und maschinenlesbar als JSON.

## 5. Ändern vs. Neuanlegen

Nicht jede inhaltliche Präzisierung rechtfertigt ein neues Objekt.
Die Faustregel: **Wenn jemand mit bestehender Bewertung erneut prüfen
müsste, ist es ein neues Objekt.** Reine Formulierungsschärfung am
bestehenden Objekt bleibt dagegen eine Änderung an derselben ID.

## 6. Lebenszyklus

Jedes Objekt trägt ab 2.0 die Felder `lifecycle`, `valid_from` und
gegebenenfalls `superseded_by` beziehungsweise `supersedes`. Ein
abgelöstes Objekt wird nicht gelöscht, sondern bleibt mit Verweis auf
seinen Nachfolger stehen.

## 7. Synthetische Objekte

Synthetische Objekte bilden Sachverhalte ab, die sich nicht aus einem
einzelnen Artikel ergeben, etwa übergreifende Umsetzungsplanungen,
eigene Zusammenfassungen mehrerer Buchstaben oder Fristenobjekte aus
einem Änderungsvorgang.

Wo die Nummer bei einzelnen Objekten ein laufender Zähler statt einer
Fundstelle ist, bleibt sie nach Abschnitt 3 unverändert. Neu vergebene
IDs folgen dieser Aufteilung: **Nummernkreis ab 900** für synthetische
Objekte ohne eigene Fundstelle.

## 8. Fachliche Korrekturen

Stellt sich heraus, dass die Fundstelle (Feld `article`) eines Objekts
falsch zugeordnet war, wird das Feld korrigiert — die ID selbst ändert
sich dadurch nicht. Eine laufende Liste offener Prüfungen führt das
`CHANGELOG.md`.

## 9. Vergabe

Neue BAM-IDs vergibt ausschließlich die Modellpflege. Externe
Beiträge (siehe [`CONTRIBUTING.md`](CONTRIBUTING.md)) schlagen Inhalte
vor, nicht eigene Bezeichner — sonst zerfasert ein offenes Projekt an
genau dieser Stelle.
