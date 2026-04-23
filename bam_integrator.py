# ==============================================================================
# BAM Integrator v1.1 - Gap Analysis Edition
# Full Data: https://www.brain-media.de/kaas.html
# ==============================================================================
import json
import os

def run_integrator():
    print("--- Brain-Media BAM Integrator (Audit Mode) ---\n")
    
    if not os.path.exists('bam-example.json'):
        print("Fehler: bam-example.json nicht gefunden.")
        return

    with open('bam-example.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    report = f"""
################################################################################
AUDIT-REPORT: {data.get('id')}
Regulierung: {data.get('regulation')} ({data.get('article')})
################################################################################

1. ANFORDERUNG:
   {data.get('requirement')}

2. >>> DIAGNOSE (Gap-Check):
   {data.get('gap_check', 'Keine Diagnose-Daten im Objekt vorhanden.')}

3. >>> BEHEBUNG (Remediation):
   {data.get('remediation', 'Kontaktieren Sie KaaS für Umsetzungsdetails.')}

4. RISIKO & PRIORITÄT:
   Risiko-Score: {data.get('risk', {}).get('score')}/10
   Maßnahme: {data.get('control', {}).get('measure')}
   Priorität: {data.get('control', {}).get('priority')}

5. NACHWEIS FÜR AUDITOR:
   Typ: {data.get('evidence', {}).get('type')}
--------------------------------------------------------------------------------
Full Compliance Content available at: https://www.brain-media.de/kaas.html
"""
    print(report)

if __name__ == "__main__":
    run_integrator()
