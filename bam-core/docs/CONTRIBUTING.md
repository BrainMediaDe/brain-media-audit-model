# Mitwirken an BAM Core

Danke fuer Ihr Interesse, das Brain-Media Audit Model zu erweitern!

## Womit kann ich helfen?

Die wertvollsten Beitraege sind aktuell:

1. **Fehlende Frameworks ergaenzen** - ISO 42001 und der Cyber
   Solidarity Act (CSA) sind noch nicht in `bam_database.json`
   enthalten. Neue BAM-Objekte fuer diese Frameworks (Struktur siehe
   unten) sind sehr willkommen.

2. **ISO 27001:2022 Coverage vervollstaendigen** - aktuell 74 % (69
   von 93 Controls vollstaendig, 24 teilweise).

3. **Cross-Framework-Verknuepfungen** - weitere `CROSS`-Objekte, die
   zeigen, wie eine Massnahme mehrere Frameworks gleichzeitig erfuellt.

4. **Korrekturen** - Aktualisierung von Artikel-Referenzen bei
   Aenderungen der zugrunde liegenden Rechtsakte.

5. **Uebersetzungen** - Englische Version des Datenmodells.

## Struktur eines BAM-Objekts

```json
{
  "bam_id": "NIS2-020-GOVERNANCE",
  "regulation": "NIS-2",
  "article": "Art. 20",
  "status": "ausstehend",
  "tags": ["governance", "leitungsverantwortung"],
  "cross_refs": ["DORA Art. 5", "ISO 27001 A.5.1"],
  "requirement": {
    "text": "...",
    "source": "NIS-2 Art. 20 Abs. 1-2",
    "priority": "hoch"
  },
  "gap_check": {
    "question": "...",
    "if_yes": "...",
    "if_no": "...",
    "if_partial": "..."
  },
  "remediation": { ... },
  "risk": { ... },
  "control": { ... },
  "evidence": { ... },
  "iso27001_mapping": [ ... ],
  "iso27001_2022_controls": [ ... ]
}
```

## Lizenz Ihrer Beitraege

Mit einem Pull Request stimmen Sie zu, dass:

- Beitraege zum **Code** unter AGPLv3 lizenziert werden,
- Beitraege zum **Datenmodell** (`bam_database.json`) unter
  CC BY-SA 4.0 lizenziert werden.

Bitte entfernen Sie keine bestehenden Copyright-/Attribution-Hinweise.

## Pull Requests

1. Fork erstellen
2. Branch fuer Ihre Aenderung anlegen
3. Aenderungen an `bam_database.json` mit `python3 -m json.tool
   bam_database.json` auf gueltiges JSON pruefen
4. Pull Request mit kurzer Beschreibung erstellen

Fragen? Issue eroeffnen oder info@brain-media.de.
