# ==============================================================================
# BAM Integrator v1.2 - Gap Analysis Edition
# Schema: Brain-Media Audit Model v1.1
# Full Data: https://www.brain-media.de/kaas.html
# ==============================================================================
import json
import os
import sys
 
KAAS_URL = "https://www.brain-media.de/kaas.html"
 
def load_database(path='bam_database.json'):
    if not os.path.exists(path):
        print(f"Fehler: {path} nicht gefunden.")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
 
def format_steps(steps):
    if not steps:
        return "   Keine Schritte vorhanden – vollständige Remediation in KaaS."
    return "\n".join(f"   {i+1}. {s}" for i, s in enumerate(steps))
 
def format_crossrefs(refs):
    if not refs:
        return "   Keine Cross-Referenzen"
    return "   " + ", ".join(refs)
 
def print_object_report(obj):
    bam_id    = obj.get('bam_id', obj.get('id', 'N/A'))
    reg       = obj.get('regulation', 'N/A')
    article   = obj.get('article', 'N/A')
    cross     = obj.get('cross_refs', [])
 
    req       = obj.get('requirement', {})
    req_text  = req.get('text', req) if isinstance(req, dict) else req
    req_nut   = req.get('nutzen', '') if isinstance(req, dict) else ''
 
    gap       = obj.get('gap_check', {})
    gap_q     = gap.get('question', '– Nur in KaaS verfügbar –') if isinstance(gap, dict) else gap
    gap_no    = gap.get('if_no', '') if isinstance(gap, dict) else ''
    gap_part  = gap.get('if_partial', '') if isinstance(gap, dict) else ''
 
    rem       = obj.get('remediation', {})
    rem_sum   = rem.get('summary', '– Nur in KaaS verfügbar –') if isinstance(rem, dict) else rem
    rem_steps = rem.get('steps', []) if isinstance(rem, dict) else []
    rem_eff   = rem.get('effort', '') if isinstance(rem, dict) else ''
    rem_dead  = rem.get('deadline', '') if isinstance(rem, dict) else ''
 
    risk      = obj.get('risk', {})
    ctrl      = obj.get('control', {})
    evid      = obj.get('evidence', {})
 
    print("=" * 78)
    print(f"  BAM AUDIT REPORT: {bam_id}")
    print(f"  Regulierung: {reg}  |  Artikel: {article}  |  Status: {obj.get('status','–')}")
    print("=" * 78)
 
    print("\n── 1. REQUIREMENT ──────────────────────────────────────────────────────────")
    print(f"   {req_text}")
    if req_nut:
        print(f"   → Ihr Nutzen: {req_nut}")
 
    print("\n── 2. GAP-CHECK (Diagnose) ──────────────────────────────────────────────────")
    print(f"   Frage: {gap_q}")
    if gap_no:
        print(f"   → Bei NEIN:      {gap_no}")
    if gap_part:
        print(f"   → Bei TEILWEISE: {gap_part}")
 
    print("\n── 3. REMEDIATION (Behebung) ────────────────────────────────────────────────")
    print(f"   {rem_sum}")
    if rem_steps:
        print(format_steps(rem_steps))
    if rem_eff:
        print(f"   Aufwand: {rem_eff}  |  Frist: {rem_dead}")
 
    print("\n── 4. RISK ──────────────────────────────────────────────────────────────────")
    print(f"   Score: {risk.get('score','–')}/9  |  Likelihood: {risk.get('likelihood','–')}  |  Impact: {risk.get('impact','–')}")
    if risk.get('description'):
        print(f"   {risk.get('description')}")
 
    print("\n── 5. CONTROL ───────────────────────────────────────────────────────────────")
    print(f"   Maßnahme:     {ctrl.get('measure','–')}")
    print(f"   Priorität:    {ctrl.get('priority','–')}  |  Aufwand: {ctrl.get('effort','–')}")
    print(f"   Verantwortl.: {ctrl.get('responsible','–')}")
    if ctrl.get('notes'):
        print(f"   Hinweis:      {ctrl.get('notes')}")
 
    print("\n── 6. EVIDENCE (Audit-Nachweis) ─────────────────────────────────────────────")
    print(f"   Typ:      {evid.get('type','–')}")
    print(f"   Format:   {evid.get('format','–')}")
    print(f"   Template: {evid.get('template','–')}")
 
    if cross:
        print("\n── CROSS-COMPLIANCE (Collect Once, Comply Many) ────────────────────────────")
        print(format_crossrefs(cross))
 
    print(f"\n   Full Content: {KAAS_URL}")
    print("-" * 78 + "\n")
 
def print_summary(objects, reg_filter=None):
    total = len(objects)
    by_status = {}
    by_reg = {}
    by_prio = {}
 
    for o in objects:
        s = o.get('status', 'unbekannt')
        r = o.get('regulation', 'unbekannt')
        risk = o.get('risk', {})
        score = risk.get('score', 0)
 
        by_status[s] = by_status.get(s, 0) + 1
        by_reg[r] = by_reg.get(r, 0) + 1
 
        ctrl_prio = o.get('control', {}).get('priority', 'unbekannt')
        by_prio[ctrl_prio] = by_prio.get(ctrl_prio, 0) + 1
 
    print("=" * 78)
    title = f"  BAM DATENBANK ÜBERSICHT"
    if reg_filter:
        title += f" – Filter: {reg_filter}"
    print(title)
    print("=" * 78)
    print(f"\n  Gesamt BAM-Objekte: {total}")
 
    print("\n  Nach Regulierung:")
    for r, c in sorted(by_reg.items()):
        print(f"    {r:<15} {c} Objekte")
 
    print("\n  Nach Status:")
    for s, c in sorted(by_status.items()):
        print(f"    {s:<20} {c}")
 
    print("\n  Nach Priorität (Control):")
    for p in ['sofort', 'kurzfristig', 'mittelfristig', 'langfristig']:
        if p in by_prio:
            print(f"    {p:<20} {by_prio[p]}")
 
    sofort = [o for o in objects if o.get('control', {}).get('priority') == 'sofort']
    if sofort:
        print(f"\n  ⚠ SOFORT-Maßnahmen ({len(sofort)}):")
        for o in sofort:
            bam_id = o.get('bam_id', o.get('id', 'N/A'))
            ctrl   = o.get('control', {}).get('measure', '–')
            print(f"    [{bam_id}] {ctrl}")
 
    print(f"\n  Full Compliance Content: {KAAS_URL}")
    print("-" * 78 + "\n")
 
def run_integrator():
    print("\n--- Brain-Media BAM Integrator v1.2 (Gap Analysis Edition) ---\n")
 
    db = load_database()
    objects = db.get('objects', [])
 
    # Args: optional filter by regulation or bam_id
    args = sys.argv[1:]
    reg_filter = None
    id_filter  = None
 
    for arg in args:
        if arg.upper() in ['NIS-2', 'DORA', 'CRA', 'EU AI ACT', 'CROSS']:
            reg_filter = arg
        elif arg.startswith('--id='):
            id_filter = arg.split('=')[1]
        elif arg == '--summary':
            print_summary(objects)
            return
        elif arg == '--help':
            print("Verwendung:")
            print("  python bam_integrator.py              → Alle Objekte")
            print("  python bam_integrator.py NIS-2        → Nur NIS-2")
            print("  python bam_integrator.py DORA         → Nur DORA")
            print("  python bam_integrator.py --id=NIS2-021j-MFA → Einzelnes Objekt")
            print("  python bam_integrator.py --summary    → Übersicht")
            return
 
    # Filter
    if id_filter:
        objects = [o for o in objects if o.get('bam_id', o.get('id')) == id_filter]
    elif reg_filter:
        objects = [o for o in objects if o.get('regulation', '').upper() == reg_filter.upper()]
 
    if not objects:
        print(f"Keine BAM-Objekte gefunden für Filter: {reg_filter or id_filter}")
        return
 
    # Summary first
    print_summary(objects, reg_filter)
 
    # Individual reports
    for obj in objects:
        print_object_report(obj)
 
if __name__ == "__main__":
    run_integrator()
