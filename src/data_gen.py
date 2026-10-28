"""Synthetic data generation (seeded, deterministic).

All entities are FICTIONAL. No real ARPA-H program, system, budget, or
person is represented. This module exists so the demos run on realistic
shapes of data without touching any real agency data.
"""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "synthetic"

SENS = ["public", "internal", "confidential", "restricted"]
AUTO = ["advisory", "human-in-loop", "autonomous"]
IMPACT = ["none", "internal", "participants", "public"]
OPACITY = ["interpretable", "explainable", "black-box"]
DEPLOY = ["internal", "research-facing", "public-facing"]

AI_USE_CASES = [
    # (name, purpose, sensitivity, autonomy, impact, opacity, deployment, program)
    ("TrialMatch Assistant", "Match de-identified participant profiles to trial criteria", "confidential", "advisory", "participants", "explainable", "research-facing", "Program Northlight"),
    ("GrantScan Triage", "Rank incoming research proposals for reviewer assignment", "internal", "advisory", "internal", "interpretable", "internal", "Program Northlight"),
    ("BioImage QC", "Flag low-quality microscopy images before analysis", "internal", "human-in-loop", "internal", "black-box", "research-facing", "Program Harbor"),
    ("AdverseEvent Signal Scan", "Detect safety signals in trial event narratives", "restricted", "human-in-loop", "participants", "explainable", "research-facing", "Program Harbor"),
    ("Budget Forecaster", "Forecast program spend against quarterly plans", "internal", "advisory", "internal", "interpretable", "internal", "Operations"),
    ("Public Evidence Summarizer", "Draft plain-language summaries of published findings", "public", "human-in-loop", "public", "black-box", "public-facing", "Program Beacon"),
    ("Autonomous Grant Writer", "Draft full funding announcements without human review", "internal", "autonomous", "public", "black-box", "public-facing", "Program Beacon"),
    ("Participant Chat Help", "Answer participant questions about trial logistics", "confidential", "human-in-loop", "participants", "black-box", "public-facing", "Program Harbor"),
    ("Genomic Variant Prioritizer", "Rank variants for follow-up in rare-disease cohorts", "restricted", "advisory", "participants", "black-box", "research-facing", "Program Keystone"),
    ("Autonomous Eligibility Decider", "Approve or deny trial eligibility without human review", "restricted", "autonomous", "participants", "black-box", "research-facing", "Program Keystone"),
    ("Internal Search Copilot", "Retrieval assistant over internal policy documents", "internal", "advisory", "internal", "explainable", "internal", "Operations"),
    ("Fraud Pattern Detector", "Flag anomalous invoice patterns in vendor payments", "confidential", "human-in-loop", "internal", "explainable", "internal", "Operations"),
    ("Public Chatbot Health Advice", "Answer public health questions directly", "public", "autonomous", "public", "black-box", "public-facing", "Program Beacon"),
    ("De-identification Auditor", "Verify de-identification of shared datasets", "restricted", "human-in-loop", "participants", "interpretable", "internal", "Program Keystone"),
]

SYSTEMS = [
    # (name, description, profile) profile drives seeded compliance posture
    ("Research Data Lake", "Central lakehouse for program research datasets", "strong"),
    ("Grants Portal", "Proposal intake, review, and award workflows", "mixed"),
    ("AI Model Registry", "Inventory, versioning, and approval records for AI systems", "mixed"),
    ("Identity Platform", "Workforce identity, MFA, and privileged access", "strong"),
    ("Collaboration Suite", "Document sharing and team workspaces", "weak"),
    ("Publication Repository", "Public-facing repository of published findings", "mixed"),
    ("Finance System", "Budget execution and vendor payment processing", "mixed"),
    ("Legacy File Shares", "Unstructured legacy shares pending migration", "critical"),
]

CONTROL_FAMILIES = [
    ("AC", "Access Control", ["AC-2", "AC-3", "AC-6"]),
    ("AU", "Audit and Accountability", ["AU-2", "AU-6", "AU-12"]),
    ("CM", "Configuration Management", ["CM-2", "CM-6", "CM-8"]),
    ("IA", "Identification and Authentication", ["IA-2", "IA-5", "IA-8"]),
    ("IR", "Incident Response", ["IR-4", "IR-5", "IR-8"]),
    ("SC", "System and Communications Protection", ["SC-7", "SC-13", "SC-28"]),
    ("SI", "System and Information Integrity", ["SI-2", "SI-4", "SI-10"]),
    ("RA", "Risk Assessment", ["RA-3", "RA-5", "RA-7"]),
    ("CA", "Assessment, Authorization, and Monitoring", ["CA-2", "CA-5", "CA-7"]),
    ("PM", "Program Management", ["PM-9", "PM-14", "PM-28"]),
]
# A small set of controls whose open gaps veto authorization (critical baseline).
CRITICAL_CONTROLS = {"AC-2", "IA-2", "AU-6", "IR-5", "SC-13", "SI-4", "CA-7"}


def _write(name, rows, fields):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def gen_ai_use_cases():
    rows = []
    for i, (name, purpose, s, a, imp, op, dep, prog) in enumerate(AI_USE_CASES, 1):
        rows.append({"id": f"AI-{i:02d}", "name": name, "purpose": purpose,
                     "data_sensitivity": s, "autonomy": a, "population_impact": imp,
                     "model_opacity": op, "deployment": dep, "program": prog})
    _write("ai_use_cases.csv", rows, list(rows[0].keys()))
    return len(rows)


def gen_research_tables(seed=42):
    rng = random.Random(seed)
    trials = []
    for i in range(1, 241):
        trials.append({"trial_id": f"T{i:04d}",
                       "title": f"Synthetic trial {i}",
                       "phase": rng.choice(["I", "II", "III", "IV"]),
                       "enrollment": rng.randint(20, 1200),
                       "start_date": f"202{rng.randint(0, 5)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                       "sponsor_program": rng.choice(["Program Northlight", "Program Harbor", "Program Beacon", "Program Keystone"]),
                       "status": rng.choice(["recruiting", "active", "completed"])})
    # Injected defects: 6 missing enrollments, 3 duplicate ids, 2 negative enrollments
    for j in [5, 40, 90, 130, 180, 220]:
        trials[j]["enrollment"] = ""
    trials.append(dict(trials[10])); trials.append(dict(trials[50])); trials.append(dict(trials[99]))
    trials[200]["enrollment"] = -15; trials[210]["enrollment"] = -3
    _write("trials.csv", trials, list(trials[0].keys()))

    samples = []
    for i in range(1, 601):
        tid = f"T{rng.randint(1, 240):04d}"
        samples.append({"sample_id": f"S{i:05d}", "trial_id": tid,
                        "sample_type": rng.choice(["blood", "tissue", "saliva", "plasma"]),
                        "collected_date": f"202{rng.randint(2, 5)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                        "volume_ml": round(rng.uniform(0.5, 25.0), 1) if i not in (55, 300) else ""})
    _write("biosamples.csv", samples, list(samples[0].keys()))

    images = []
    for i in range(1, 401):
        tid = f"T{rng.randint(1, 240):04d}"
        if i in (44, 145, 246, 347):  # broken references (injected)
            tid = f"T8{i:03d}"
        images.append({"image_id": f"IMG{i:05d}", "trial_id": tid,
                       "modality": rng.choice(["microscopy", "MRI", "CT", "histology"]),
                       "quality_score": round(rng.uniform(0.3, 1.0), 2),
                       "acquired_date": f"202{rng.randint(2, 5)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"})
    images[77]["quality_score"] = 1.45  # out-of-range (injected)
    images[301]["quality_score"] = -0.2
    _write("imaging.csv", images, list(images[0].keys()))

    grants = []
    for i in range(1, 121):
        grants.append({"grant_id": f"G{i:04d}",
                       "program": rng.choice(["Program Northlight", "Program Harbor", "Program Beacon", "Program Keystone"]),
                       "amount_usd": rng.randint(50000, 4000000),
                       "award_year": rng.randint(2022, 2026),
                       "status": rng.choice(["active", "closed", "pending"])})
    _write("grants.csv", grants, list(grants[0].keys()))
    return {"trials": len(trials), "biosamples": len(samples), "imaging": len(images), "grants": len(grants)}


def gen_ato(seed=42):
    rng = random.Random(seed)
    systems = [{"system_id": f"SYS-{i:02d}", "name": n, "description": d, "profile": p}
               for i, (n, d, p) in enumerate(SYSTEMS, 1)]
    _write("systems.csv", systems, ["system_id", "name", "description", "profile"])
    controls = []
    for fam, fam_name, ids in CONTROL_FAMILIES:
        for cid in ids:
            controls.append({"control_id": cid, "family": fam, "family_name": fam_name,
                             "title": f"{cid} control (modeled on NIST SP 800-53 Rev. 5)"})
    _write("controls.csv", controls, ["control_id", "family", "family_name", "title"])
    profile_weights = {
        "strong": [("implemented", 0.90), ("partially", 0.08), ("not implemented", 0.02)],
        "mixed": [("implemented", 0.55), ("partially", 0.30), ("planned", 0.05), ("not implemented", 0.10)],
        "weak": [("implemented", 0.30), ("partially", 0.35), ("planned", 0.10), ("not implemented", 0.25)],
        "critical": [("implemented", 0.15), ("partially", 0.25), ("planned", 0.10), ("not implemented", 0.50)],
    }
    assessments, poams = [], []
    for s in systems:
        w = profile_weights[s["profile"]]
        for c in controls:
            r = rng.random(); acc = 0.0; status = w[-1][0]
            for st, p in w:
                acc += p
                if r < acc:
                    status = st; break
            # Force the critical system to fail critical controls (ground truth: vetoed)
            if s["name"] == "Legacy File Shares" and c["control_id"] in CRITICAL_CONTROLS:
                status = "not implemented"
            # Planted veto scenario: strong system blocked by ONE open critical gap
            if s["name"] == "Identity Platform" and c["control_id"] == "IR-5":
                status = "not implemented"
            if s["name"] == "Research Data Lake" and c["control_id"] in CRITICAL_CONTROLS:
                status = "implemented"
            assessments.append({"system_id": s["system_id"], "control_id": c["control_id"], "status": status})
            if status in ("partially", "not implemented", "planned"):
                sev = "critical" if c["control_id"] in CRITICAL_CONTROLS and status == "not implemented" else ("high" if status == "not implemented" else "medium")
                poam_status = "open" if rng.random() < 0.8 else "closed"
                if s["name"] == "Identity Platform" and c["control_id"] == "IR-5":
                    poam_status = "open"  # planted veto scenario
                poams.append({"poam_id": f"POAM-{len(poams)+1:04d}", "system_id": s["system_id"],
                              "control_id": c["control_id"], "severity": sev,
                              "status": poam_status,
                              "due_days": rng.choice([30, 60, 90, 180])})
    _write("control_assessments.csv", assessments, ["system_id", "control_id", "status"])
    _write("poams.csv", poams, ["poam_id", "system_id", "control_id", "severity", "status", "due_days"])
    return {"systems": len(systems), "controls": len(controls),
            "assessments": len(assessments), "poams": len(poams)}


def main():
    print("ai_use_cases:", gen_ai_use_cases())
    print("research:", gen_research_tables())
    print("ato:", gen_ato())


if __name__ == "__main__":
    main()
