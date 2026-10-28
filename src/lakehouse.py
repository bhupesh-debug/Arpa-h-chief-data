"""Lakehouse quality gates: ingestion validation, quality checks, anomaly flags.

Promotion rule (bronze -> silver -> gold):
  Gold: score >= 0.90 and zero failed checks.
  Silver: score >= 0.75 and no failed check on a key column.
  Bronze: otherwise. A dataset with a failed referential-integrity check
  can never promote above Bronze.
"""
import csv
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "synthetic"


def load(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def check_completeness(rows, col):
    missing = sum(1 for r in rows if r.get(col, "") in ("", None))
    rate = missing / max(len(rows), 1)
    status = "pass" if rate == 0 else ("warn" if rate <= 0.02 else "fail")
    return {"check": f"completeness:{col}", "missing": missing, "rate": round(rate, 4), "status": status}


def check_uniqueness(rows, col):
    vals = [r[col] for r in rows if r.get(col, "") != ""]
    dup = len(vals) - len(set(vals))
    status = "pass" if dup == 0 else "fail"
    return {"check": f"uniqueness:{col}", "duplicates": dup, "status": status}


def check_range(rows, col, lo, hi):
    bad = sum(1 for r in rows if (v := _num(r.get(col, ""))) is not None and not (lo <= v <= hi))
    status = "pass" if bad == 0 else "fail"
    return {"check": f"range:{col}[{lo},{hi}]", "out_of_range": bad, "status": status}


def check_reference(rows, col, valid_ids):
    bad = sum(1 for r in rows if r.get(col, "") not in valid_ids)
    status = "pass" if bad == 0 else "fail"
    return {"check": f"reference:{col}", "broken": bad, "status": status}


def check_allowed_values(rows, col, allowed):
    bad = sum(1 for r in rows if r.get(col, "") not in allowed)
    status = "pass" if bad == 0 else "fail"
    return {"check": f"allowed:{col}", "invalid": bad, "status": status}


def score_checks(checks):
    pts = {"pass": 1.0, "warn": 0.5, "fail": 0.0}
    return round(sum(pts[c["status"]] for c in checks) / max(len(checks), 1), 3)


def promote(score, checks):
    ref_fail = any(c["check"].startswith("reference:") and c["status"] == "fail" for c in checks)
    if ref_fail:
        return "Bronze"
    if score >= 0.90 and all(c["status"] != "fail" for c in checks):
        return "Gold"
    if score >= 0.75:
        return "Silver"
    return "Bronze"


def monthly_volume_anomalies(rows, date_col):
    counts = Counter(r[date_col][:7] for r in rows if r.get(date_col, ""))
    if len(counts) < 4:
        return []
    vals = list(counts.values())
    mu, sd = statistics.mean(vals), (statistics.pstdev(vals) or 1.0)
    return [{"month": m, "count": n, "z": round((n - mu) / sd, 2)}
            for m, n in sorted(counts.items()) if abs((n - mu) / sd) > 3]


def evaluate_all():
    trials = load("trials.csv")
    samples = load("biosamples.csv")
    images = load("imaging.csv")
    grants = load("grants.csv")
    trial_ids = {r["trial_id"] for r in trials}
    out = {}
    t_checks = [check_completeness(trials, "enrollment"), check_uniqueness(trials, "trial_id"),
                check_range(trials, "enrollment", 0, 100000),
                check_allowed_values(trials, "phase", {"I", "II", "III", "IV"}),
                check_allowed_values(trials, "status", {"recruiting", "active", "completed"})]
    out["trials"] = {"rows": len(trials), "checks": t_checks, "score": score_checks(t_checks),
                     "tier": promote(score_checks(t_checks), t_checks),
                     "anomalies": monthly_volume_anomalies(trials, "start_date")}
    s_checks = [check_completeness(samples, "volume_ml"), check_uniqueness(samples, "sample_id"),
                check_reference(samples, "trial_id", trial_ids)]
    out["biosamples"] = {"rows": len(samples), "checks": s_checks, "score": score_checks(s_checks),
                         "tier": promote(score_checks(s_checks), s_checks),
                         "anomalies": monthly_volume_anomalies(samples, "collected_date")}
    i_checks = [check_reference(images, "trial_id", trial_ids), check_uniqueness(images, "image_id"),
                check_range(images, "quality_score", 0.0, 1.0),
                check_allowed_values(images, "modality", {"microscopy", "MRI", "CT", "histology"})]
    out["imaging"] = {"rows": len(images), "checks": i_checks, "score": score_checks(i_checks),
                      "tier": promote(score_checks(i_checks), i_checks),
                      "anomalies": monthly_volume_anomalies(images, "acquired_date")}
    g_checks = [check_uniqueness(grants, "grant_id"), check_range(grants, "amount_usd", 0, 10**9),
                check_completeness(grants, "amount_usd"),
                check_allowed_values(grants, "status", {"active", "closed", "pending"})]
    out["grants"] = {"rows": len(grants), "checks": g_checks, "score": score_checks(g_checks),
                     "tier": promote(score_checks(g_checks), g_checks), "anomalies": []}
    return out
