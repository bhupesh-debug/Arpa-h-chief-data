"""Stdlib unittest suite for the executive data-leadership demos."""
import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ai_governance import score_case, tier_of, route_case  # noqa: E402
from lakehouse import (check_completeness, check_reference, check_uniqueness,  # noqa: E402
                       evaluate_all, promote, score_checks)
from ato_tracker import system_scores  # noqa: E402


def case(**kw):
    base = {"id": "T", "name": "t", "data_sensitivity": "public", "autonomy": "advisory",
            "population_impact": "none", "model_opacity": "interpretable", "deployment": "internal"}
    base.update(kw)
    return base


class TestAIGovernance(unittest.TestCase):
    def test_minimal_case_scores_zero_low(self):
        s, floor = score_case(case())
        self.assertEqual(s, 0.0)
        self.assertEqual(tier_of(s), "Low")
        self.assertFalse(floor)

    def test_tier_boundaries(self):
        self.assertEqual(tier_of(34.9), "Low")
        self.assertEqual(tier_of(35.0), "Moderate")
        self.assertEqual(tier_of(59.9), "Moderate")
        self.assertEqual(tier_of(60.0), "High")
        self.assertEqual(tier_of(79.9), "High")
        self.assertEqual(tier_of(80.0), "Critical")

    def test_restricted_autonomous_floor(self):
        s, floor = score_case(case(data_sensitivity="restricted", autonomy="autonomous"))
        self.assertTrue(floor)
        self.assertGreaterEqual(s, 60.0)
        self.assertEqual(tier_of(s), "High")

    def test_routing_consistent_for_all_use_cases(self):
        with open(ROOT / "data/synthetic/ai_use_cases.csv") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 14)
        for r in rows:
            rt = route_case(r)
            self.assertEqual(rt["tier"], tier_of(rt["score"]))
            self.assertIn(rt["tier"], ("Low", "Moderate", "High", "Critical"))

    def test_critical_route_requires_director_approval(self):
        rt = route_case(case(data_sensitivity="restricted", autonomy="autonomous",
                             population_impact="public", model_opacity="black-box",
                             deployment="public-facing"))
        self.assertEqual(rt["tier"], "Critical")
        self.assertIn("Director-level approval", rt["reviews"])


class TestLakehouse(unittest.TestCase):
    def test_completeness_counts_missing(self):
        rows = [{"v": "1"}, {"v": ""}, {"v": "3"}]
        c = check_completeness(rows, "v")
        self.assertEqual(c["missing"], 1)
        self.assertEqual(c["status"], "fail")  # 33% missing > 2% threshold

    def test_reference_counts_broken(self):
        rows = [{"t": "T0001"}, {"t": "T9999"}]
        c = check_reference(rows, "t", {"T0001"})
        self.assertEqual(c["broken"], 1)
        self.assertEqual(c["status"], "fail")

    def test_promotion_tiers(self):
        self.assertEqual(promote(1.0, [{"check": "uniqueness:x", "status": "pass"}]), "Gold")
        self.assertEqual(promote(0.833, [{"check": "completeness:x", "status": "warn"}]), "Silver")
        self.assertEqual(promote(0.5, [{"check": "reference:x", "status": "fail"}]), "Bronze")
        # Referential failure caps at Bronze even with a high score
        self.assertEqual(promote(0.95, [{"check": "reference:x", "status": "fail"}]), "Bronze")

    def test_live_tiers_cover_gold_silver_bronze(self):
        res = evaluate_all()
        tiers = {v["tier"] for v in res.values()}
        self.assertEqual(tiers, {"Gold", "Silver", "Bronze"})
        self.assertEqual(res["grants"]["tier"], "Gold")
        self.assertEqual(res["trials"]["tier"], "Bronze")


class TestATO(unittest.TestCase):
    def test_live_veto(self):
        # Identity Platform scores >= 0.90 but carries one open critical POA&M:
        # the veto must block authorization despite the high score.
        s = system_scores()["SYS-04"]
        self.assertGreaterEqual(s["score"], 0.90)
        self.assertGreaterEqual(s["open_critical_poams"], 1)
        self.assertEqual(s["recommendation"], "Not authorized")

    def test_authorized_systems_have_no_open_critical(self):
        for v in system_scores().values():
            if v["recommendation"] == "Authorized":
                self.assertEqual(v["open_critical_poams"], 0)
                self.assertGreaterEqual(v["score"], 0.90)

    def test_dataset_counts(self):
        for name, expected in [("systems.csv", 8), ("controls.csv", 30), ("control_assessments.csv", 240)]:
            with open(ROOT / "data/synthetic" / name) as f:
                self.assertEqual(len(list(csv.DictReader(f))), expected)

    def test_no_real_agency_data_in_datasets(self):
        for f in Path(ROOT / "data/synthetic").glob("*.csv"):
            text = f.read_text()
            self.assertNotIn("ARPA-H", text, msg=f"{f.name} must not reference the real agency")
            self.assertNotIn("arpa-h.gov", text)


if __name__ == "__main__":
    unittest.main()
