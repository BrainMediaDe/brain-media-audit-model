"""
Brain-Media Audit Model (BAM) Core - bam_rag.py

Copyright (c) 2026 Dr. Holger Reibold / Brain-Media.de
https://brain-media.de

Dieses Programm ist freie Software: Sie können es unter den
Bedingungen der GNU Affero General Public License, wie von der
Free Software Foundation veroeffentlicht, weitergeben und/oder
modifizieren, entweder gemaess Version 3 der Lizenz oder (nach
Ihrer Option) jeder spaeteren Version. Siehe LICENSE-Datei.

Teil von "Brain-Media Audit Model (BAM) Core"
https://github.com/BrainMediaDe/brain-media-audit-model
"""

import json
import sys
from openai import OpenAI

# ── Konfiguration ──────────────────────────────────────────────────
LM_STUDIO_URL = "http://localhost:1234/v1"
BAM_JSON_PATH = "bam_database.json"
MAX_OBJECTS   = 8   # wie viele BAM-Objekte als Kontext mitgegeben werden

# ── Verbindung zu LM Studio ────────────────────────────────────────
client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")

# ── BAM-Datenbank laden ────────────────────────────────────────────
def load_bam(path=BAM_JSON_PATH):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("objects", [])

# ── Relevante BAM-Objekte suchen ───────────────────────────────────
def find_relevant(query: str, objects: list, max_n: int = MAX_OBJECTS) -> list:
    """
    Einfache Keyword-Suche – findet BAM-Objekte die zur Frage passen.
    Für produktiven Einsatz: durch Embeddings ersetzen.
    """
    query_lower = query.lower()
    keywords = [w for w in query_lower.split() if len(w) > 3]

    scored = []
    for obj in objects:
        score = 0
        searchable = json.dumps(obj, ensure_ascii=False).lower()
        for kw in keywords:
            if kw in searchable:
                score += 1
        # Boost für direkte Regulierungserwähnungen
        for reg in ["nis-2", "nis2", "dora", "cra", "eu ai act", "iso 27001"]:
            if reg in query_lower and reg.replace("-","") in searchable:
                score += 3
        if score > 0:
            scored.append((score, obj))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [obj for _, obj in scored[:max_n]]

# ── BAM-Objekte als Kontext formatieren ───────────────────────────
def format_context(objects: list) -> str:
    if not objects:
        return "Keine passenden BAM-Objekte gefunden."

    lines = []
    for obj in objects:
        r = obj.get("requirement", {})
        g = obj.get("gap_check", {})
        rem = obj.get("remediation", {})
        risk = obj.get("risk", {})
        lines.append(f"""
--- BAM-Objekt: {obj['bam_id']} ({obj['regulation']} · {obj.get('article','')}) ---
Anforderung: {r.get('text','')}
Gap-Check:   {g.get('question','')}
Remediation: {rem.get('summary','')}
Schritte:    {' | '.join(rem.get('steps',[])[:3])}
Risiko:      Score {risk.get('score','')}/9 – {risk.get('description','')}
Bußgeld:     bis {risk.get('regulatory_fine',{}).get('max_eur','?'):,} EUR
""")
    return "\n".join(lines)

# ── System-Prompt ──────────────────────────────────────────────────
SYSTEM_PROMPT = """Du bist ein Compliance-Experte für NIS-2, DORA, CRA, EU AI Act und ISO 27001.
Du arbeitest ausschließlich auf Basis des Brain-Media Audit Model (BAM) – einem validierten, maschinenlesbaren Compliance-Datenmodell.

Regeln:
- Antworte NUR auf Basis der bereitgestellten BAM-Objekte
- Zitiere konkrete Artikel und BAM-IDs wenn möglich
- Nenne Bußgeldrahmen und Fristen wenn relevant
- Sage klar wenn ein Thema nicht in den BAM-Daten abgedeckt ist
- Antworte auf Deutsch, präzise und strukturiert
- Keine Erfindungen – nur was in den BAM-Daten steht"""

# ── Chat-Funktion ──────────────────────────────────────────────────
def ask(question: str, objects: list, history: list) -> str:
    relevant = find_relevant(question, objects)
    context  = format_context(relevant)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Konversations-History (letzte 4 Runden)
    messages.extend(history[-8:])

    # Aktuelle Frage + BAM-Kontext
    messages.append({
        "role": "user",
        "content": f"""Frage: {question}

Relevante BAM-Objekte als Kontext:
{context}

Beantworte die Frage auf Basis dieser BAM-Daten."""
    })

    response = client.chat.completions.create(
        model="local-model",  # LM Studio ignoriert diesen Wert
        messages=messages,
        temperature=0.2,      # Niedrig für präzise Compliance-Antworten
        max_tokens=1024,
    )

    answer = response.choices[0].message.content
    # History aktualisieren
    history.append({"role": "user",      "content": question})
    history.append({"role": "assistant", "content": answer})
    return answer

# ── Interaktive Shell ──────────────────────────────────────────────
def main():
    print("=" * 60)
    print("BAM RAG – Brain-Media Audit Model × LM Studio")
    print("=" * 60)

    # BAM laden
    try:
        objects = load_bam()
        print(f"✓ BAM geladen: {len(objects)} Objekte")
    except FileNotFoundError:
        print(f"✗ {BAM_JSON_PATH} nicht gefunden.")
        print("  Stelle sicher dass du das Skript im api/-Ordner ausführst.")
        sys.exit(1)

    # LM Studio prüfen
    try:
        models = client.models.list()
        print(f"✓ LM Studio verbunden")
    except Exception as e:
        print(f"✗ LM Studio nicht erreichbar: {e}")
        print("  Stelle sicher dass LM Studio läuft und der Server gestartet ist.")
        sys.exit(1)

    print("\nBeispiel-Fragen:")
    print("  Was muss ich für NIS-2 Art. 21 umsetzen?")
    print("  Welche DORA-Anforderungen gelten für Backups?")
    print("  Was kostet es wenn ich MFA nicht einführe?")
    print("\n'exit' zum Beenden\n")

    history = []
    while True:
        try:
            question = input("Frage: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBeende.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            break

        print("\nDenke nach…\n")
        try:
            answer = ask(question, objects, history)
            print(f"Antwort:\n{answer}\n")
            print("-" * 60)
        except Exception as e:
            print(f"Fehler: {e}\n")

if __name__ == "__main__":
    main()
