"""ATO / control-mapping tracker (modeled on NIST SP 800-53 Rev. 5 families).

Score weights: implemented 1.0, partially 0.5, planned 0.25, not implemented 0.0.
Recommendation:
  Authorized:      score >= 0.90 and no open critical POA&M.
  Conditional:     score >= 0.75 and no open critical POA&M.
  Not authorized:  otherwise (including ANY open critical POA&M — the veto).
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "synthetic"
WEIGHTS = {"implemented": 1.0, "partially": 0.5, "planned": 0.25, "not implemented": 0.0}
CRITICAL_CONTROLS = {"AC-2", "IA-2", "AU-6", "IR-5", "SC-13", "SI-4", "CA-7"}


def _load(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def system_scores():
    systems = _load("systems.csv")
    assessments = _load("control_assessments.csv")
    poams = _load("poams.csv")
    out = {}
    for s in systems:
        sid = s["system_id"]
        rows = [a for a in assessments if a["system_id"] == sid]
        score = round(sum(WEIGHTS[a["status"]] for a in rows) / max(len(rows), 1), 3)
        open_crit = [p for p in poams if p["system_id"] == sid and p["status"] == "open"
                     and p["severity"] == "critical"]
        open_all = [p for p in poams if p["system_id"] == sid and p["status"] == "open"]
        if open_crit:
            rec = "Not authorized"
        elif score >= 0.90:
            rec = "Authorized"
        elif score >= 0.75:
            rec = "Conditional"
        else:
            rec = "Not authorized"
        out[sid] = {"name": s["name"], "score": score, "recommendation": rec,
                    "open_critical_poams": len(open_crit), "open_poams": len(open_all),
                    "controls_assessed": len(rows)}
    return out


def family_scores(system_id):
    controls = {c["control_id"]: c["family"] for c in _load("controls.csv")}
    rows = [a for a in _load("control_assessments.csv") if a["system_id"] == system_id]
    fams = {}
    for a in rows:
        fams.setdefault(controls[a["control_id"]], []).append(WEIGHTS[a["status"]])
    return {f: round(sum(v) / len(v), 3) for f, v in sorted(fams.items())}
