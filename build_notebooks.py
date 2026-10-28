"""Build 3 notebooks with outputs captured from ACTUAL runs (no fabricated outputs)."""
import io
import json
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
NB = ROOT / "notebooks"
NB.mkdir(exist_ok=True)


def run_capture(code, ns):
    # Execute as if running from the notebooks/ directory (matching the cell paths).
    buf = io.StringIO()
    prev = os.getcwd()
    os.chdir(NB)
    try:
        with redirect_stdout(buf):
            exec(compile(code, "<cell>", "exec"), ns)
    finally:
        os.chdir(prev)
    return buf.getvalue()


def nb(cells):
    ns = {}
    out = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                     "language_info": {"name": "python"}},
           "nbformat": 4, "nbformat_minor": 5}
    for kind, src in cells:
        if kind == "md":
            out["cells"].append({"cell_type": "markdown", "metadata": {}, "source": src.splitlines(True)})
        else:
            text = run_capture(src, ns)
            out["cells"].append({"cell_type": "code", "execution_count": 1, "metadata": {},
                                 "outputs": ([{"output_type": "stream", "name": "stdout",
                                               "text": text.splitlines(True)}] if text.strip() else []),
                                 "source": src.splitlines(True)})
    return out


COMMON = "import sys; sys.path.insert(0, '../src')\n"

n1 = nb([
    ("md", "# 01 — Responsible-AI Governance Routing\nRule-based risk scoring (no ML) for 14 fictional AI use cases. Scores are transparent by design: an executive must be able to defend every routing decision."),
    ("code", COMMON + """import csv
from ai_governance import route_case
cases = list(csv.DictReader(open('../data/synthetic/ai_use_cases.csv')))
routes = [route_case(c) for c in cases]
for r in routes:
    print(f"{r['id']} | {r['name'][:38]:38} | {r['score']:5} | {r['tier']:8} | {'; '.join(r['reviews'])}")
"""),
    ("code", COMMON + """from collections import Counter
print('Tier distribution:', dict(Counter(r['tier'] for r in routes)))
print('Floor rule applied to:', [r['id'] for r in routes if r['floor_applied']])
print('Critical cases:', [r['name'] for r in routes if r['tier'] == 'Critical'])
"""),
])
(NB / "01_ai_governance.ipynb").write_text(json.dumps(n1, indent=1))

n2 = nb([
    ("md", "# 02 — Lakehouse Quality Gates\nIngestion validation, quality checks, and promotion tiers (Bronze/Silver/Gold) on four fictional health-research-style datasets. A failed referential-integrity check caps a dataset at Bronze."),
    ("code", COMMON + """from lakehouse import evaluate_all
res = evaluate_all()
for k, v in res.items():
    print(f"{k:12} rows={v['rows']:4} score={v['score']:.3f} tier={v['tier']}")
    for c in v['checks']:
        print(f"    {c['check']:32} {c['status']}")
    print(f"    monthly-volume anomalies: {len(v['anomalies'])}")
"""),
])
(NB / "02_lakehouse_quality.ipynb").write_text(json.dumps(n2, indent=1))

n3 = nb([
    ("md", "# 03 — ATO / Control-Mapping Tracker\nNIST-style control mapping with compliance scoring and the critical-POA&M veto: any open critical POA&M blocks authorization regardless of score."),
    ("code", COMMON + """from ato_tracker import system_scores, family_scores
for sid, v in system_scores().items():
    print(f"{sid} | {v['name'][:26]:26} | score={v['score']:.3f} | {v['recommendation']:16} | open POA&Ms={v['open_poams']} (critical {v['open_critical_poams']})")
print()
print('Identity Platform (SYS-04) family scores:', family_scores('SYS-04'))
"""),
])
(NB / "03_ato_tracker.ipynb").write_text(json.dumps(n3, indent=1))
print("notebooks written")
