"""Generate markdown reports + standalone HTML dashboard with charts."""
import base64
import csv
import io
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from ai_governance import route_case  # noqa: E402
from lakehouse import evaluate_all  # noqa: E402
from ato_tracker import system_scores, family_scores  # noqa: E402

REP = ROOT / "reports"
REP.mkdir(exist_ok=True)


def chart_png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def bar_chart(title, labels, values, color="#1F3864"):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(labels, values, color=color)
    ax.set_title(title)
    ax.set_ylim(0, max(values) * 1.15 + 0.05)
    for i, v in enumerate(values):
        ax.text(i, v + max(values) * 0.02, str(v), ha="center", fontsize=9)
    plt.xticks(rotation=20, ha="right", fontsize=8)
    plt.tight_layout()
    return chart_png(fig)


def main():
    cases = list(csv.DictReader(open(ROOT / "data/synthetic/ai_use_cases.csv")))
    routes = [route_case(c) for c in cases]
    tiers = Counter(r["tier"] for r in routes)
    lake = evaluate_all()
    ato = system_scores()
    poams = list(csv.DictReader(open(ROOT / "data/synthetic/poams.csv")))
    open_poams = [p for p in poams if p["status"] == "open"]
    sev = Counter(p["severity"] for p in open_poams)

    # ---- Markdown reports ----
    lines = ["# AI Governance Report (synthetic demo)\n",
             "Rule-based risk scoring + approval routing for 14 fictional AI use cases.\n",
             "| ID | Use case | Score | Tier | Route (SLA) |",
             "|---|---|---|---|---|"]
    for r in routes:
        lines.append(f"| {r['id']} | {r['name']} | {r['score']} | {r['tier']} | {'; '.join(r['reviews'])} ({r['sla_days']}d) |")
    lines.append(f"\nTier distribution: {dict(tiers)}. Floor rule applied: "
                 f"{sum(1 for r in routes if r['floor_applied'])} case(s).")
    (REP / "ai_governance_report.md").write_text("\n".join(lines))

    lines = ["# Lakehouse Quality Report (synthetic demo)\n",
             "| Dataset | Rows | Score | Tier | Failed checks |",
             "|---|---|---|---|---|"]
    for k, v in lake.items():
        failed = ", ".join(c["check"] for c in v["checks"] if c["status"] == "fail") or "none"
        lines.append(f"| {k} | {v['rows']} | {v['score']} | {v['tier']} | {failed} |")
    lines.append(f"\nMonthly-volume anomalies flagged: {sum(len(v['anomalies']) for v in lake.values())}.")
    (REP / "lakehouse_report.md").write_text("\n".join(lines))

    lines = ["# ATO Tracker Report (synthetic demo)\n",
             "| System | Score | Recommendation | Open POA&Ms (critical) |",
             "|---|---|---|---|"]
    for sid, v in ato.items():
        lines.append(f"| {v['name']} | {v['score']} | {v['recommendation']} | {v['open_poams']} ({v['open_critical_poams']}) |")
    lines.append(f"\nOpen POA&Ms by severity: {dict(sev)}.")
    (REP / "ato_report.md").write_text("\n".join(lines))

    # ---- Dashboard ----
    tier_chart = bar_chart("AI use cases by risk tier", list(tiers.keys()), [tiers[k] for k in tiers])
    qual_chart = bar_chart("Dataset quality score", list(lake.keys()), [v["score"] for v in lake.values()])
    comp_chart = bar_chart("System compliance score", [v["name"] for v in ato.values()],
                           [v["score"] for v in ato.values()])
    sev_chart = bar_chart("Open POA&Ms by severity", list(sev.keys()), [sev[k] for k in sev], color="#7B2D0E")

    def table(headers, rows):
        th = "".join(f"<th>{h}</th>" for h in headers)
        tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        return f"<table><tr>{th}</tr>{tr}</table>"

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Executive Data-Leadership Dashboard — Synthetic Demo</title>
<style>body{{font-family:Arial,sans-serif;max-width:980px;margin:30px auto;padding:0 20px;color:#222}}
h1{{color:#1F3864}}h2{{color:#1F3864;border-bottom:2px solid #D9E2F3;padding-bottom:4px}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}th,td{{border:1px solid #B0B8C8;padding:6px 8px;text-align:left;font-size:14px}}
th{{background:#D9E2F3}}img{{max-width:100%}}.warn{{background:#FFF2CC;padding:10px;border-left:4px solid #BF8F00}}</style>
</head><body>
<h1>Executive Data-Leadership Dashboard</h1>
<p class="warn"><b>Portfolio demonstration on synthetic data.</b> All programs, systems, use cases,
and figures are fictional. This is NOT evidence of a C-suite/SES role, federal employment,
a security clearance, or any executive record.</p>
<h2>1. Responsible-AI governance routing</h2>
<img src="{tier_chart}">
{table(["ID","Use case","Score","Tier","Approval route","SLA"],
 [[r["id"], r["name"], r["score"], r["tier"], "; ".join(r["reviews"]), f"{r['sla_days']} days"] for r in routes])}
<h2>2. Lakehouse quality gates</h2>
<img src="{qual_chart}">
{table(["Dataset","Rows","Score","Tier"],
 [[k, v["rows"], v["score"], v["tier"]] for k, v in lake.items()])}
<h2>3. ATO / compliance posture</h2>
<img src="{comp_chart}">
{table(["System","Score","Recommendation","Open POA&Ms (critical)"],
 [[v["name"], v["score"], v["recommendation"], f"{v['open_poams']} ({v['open_critical_poams']})"] for v in ato.values()])}
<img src="{sev_chart}">
<p><b>Headline:</b> Identity Platform scores 0.95 but is <b>Not authorized</b> — one open critical
POA&amp;M vetoes authorization. That veto is the governance point: a high average must never
outvote an open critical gap.</p>
</body></html>"""
    (REP / "dashboard.html").write_text(html)
    print("reports + dashboard written:", len(html), "chars")


if __name__ == "__main__":
    main()
