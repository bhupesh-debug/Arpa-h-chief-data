"""Responsible-AI risk scoring + approval routing (transparent rules, no ML).

Score = weighted points, normalized to 0-100. Tiers:
  <35 Low | 35-59 Moderate | 60-79 High | >=80 Critical.
Policy floors: restricted health data + autonomous operation, or
restricted data + public-facing deployment, can never score below High.
"""
SENS = {"public": 0, "internal": 10, "confidential": 20, "restricted": 30}
AUTO = {"advisory": 0, "human-in-loop": 10, "autonomous": 25}
IMPACT = {"none": 0, "internal": 5, "participants": 15, "public": 25}
OPACITY = {"interpretable": 0, "explainable": 5, "black-box": 15}
DEPLOY = {"internal": 0, "research-facing": 5, "public-facing": 10}
MAX_POINTS = 105.0

ROUTES = {
    "Low": {"reviews": ["Program owner sign-off"], "sla_days": 5, "monitoring": "Annual review"},
    "Moderate": {"reviews": ["AI review board"], "sla_days": 15, "monitoring": "Semi-annual review"},
    "High": {"reviews": ["AI review board", "Privacy review", "Security review"], "sla_days": 30,
             "monitoring": "Quarterly review + drift log"},
    "Critical": {"reviews": ["AI review board", "Privacy review", "Security review", "Director-level approval"],
                 "sla_days": 45, "monitoring": "Monthly review + continuous monitoring"},
}


def score_case(c):
    pts = (SENS[c["data_sensitivity"]] + AUTO[c["autonomy"]] + IMPACT[c["population_impact"]]
           + OPACITY[c["model_opacity"]] + DEPLOY[c["deployment"]])
    score = round(pts * 100.0 / MAX_POINTS, 1)
    floor = False
    if c["data_sensitivity"] == "restricted" and (c["autonomy"] == "autonomous" or c["deployment"] == "public-facing"):
        score = max(score, 60.0); floor = True
    return score, floor


def tier_of(score):
    if score < 35: return "Low"
    if score < 60: return "Moderate"
    if score < 80: return "High"
    return "Critical"


def route_case(c):
    score, floor = score_case(c)
    tier = tier_of(score)
    r = dict(ROUTES[tier])
    return {"id": c["id"], "name": c["name"], "score": score, "tier": tier,
            "floor_applied": floor, "reviews": r["reviews"],
            "sla_days": r["sla_days"], "monitoring": r["monitoring"]}
