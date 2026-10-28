# Executive Data Leadership — Portfolio Project

**JD:** Chief of IT and Data Technology, ARPA-H (federal health research agency).
**Honest-fit decision (read first):** this is a chief-level leadership role (10+ years, 5 years
C-suite/SES/equivalent), not a hands-on ML job. A generic model demo would read as tone-deaf
and would misrepresent the candidate. This project is therefore **executive infrastructure in
working code** — the artifacts a chief governs — built as a **portfolio demonstration of how
the candidate would approach the function**.

## Plain-language disclaimer

This is NOT evidence of having held a C-suite/SES role, federal employment, a security
clearance, or any executive record. It demonstrates approach, judgment, and working
governance mechanics. Nothing here claims otherwise.

## What is built

1. **Responsible-AI governance engine** (`src/ai_governance.py`) — transparent weighted risk
   scoring (0–100) over sensitivity / autonomy / population impact / opacity / deployment,
   4 tiers (Low / Moderate / High / Critical), approval routes with SLAs and monitoring
   cadences, and policy floors (restricted health data + autonomous operation can never score
   below High). 14 fictional use cases: Low 3, Moderate 5, High 4, Critical 2.
2. **Lakehouse quality gates** (`src/lakehouse.py`) — completeness, uniqueness, range,
   reference, and allowed-value checks; Bronze/Silver/Gold promotion (a failed
   referential-integrity check caps at Bronze). Grants Gold (1.000), biosamples Silver (0.833),
   imaging Bronze (0.500), trials Bronze (0.400). 1 monthly-volume anomaly flagged.
3. **ATO control-mapping tracker** (`src/ato_tracker.py`) — 8 fictional systems x 30 NIST
   SP 800-53 Rev. 5-style controls = 240 assessments, 115 POA&M items. Compliance score per
   system; **any open critical POA&M vetoes authorization**. 2 Authorized, 6 Not authorized —
   including Identity Platform (0.95) blocked by one open critical POA&M. That veto is the
   governance point: a high average must never outvote an open critical gap.

## Data

All data is **synthetic, seeded (seed 42), and fictional**: program names, systems, use cases,
and figures are invented for demo purposes. No real ARPA-H data, budgets, systems, or people
are represented. Injected, disclosed defects: missing enrollments, duplicate trial IDs,
negative enrollments, broken image references, out-of-range quality scores, and the planted
Identity Platform veto scenario. A test asserts no dataset CSV mentions the real agency.

## How to run

```bash
python -m src.data_gen        # regenerate synthetic data (seeded, deterministic)
python -m unittest discover -s tests   # 13 tests, stdlib unittest
python build_outputs.py       # Markdown reports + standalone dashboard.html
python build_notebooks.py     # 3 executed notebooks (stored outputs from real runs)
python build_deck.py          # 10-slide deck (python-pptx)
python build_report.py        # project report PDF
```

Python 3.12+; numpy, matplotlib, reportlab, python-pptx. No sklearn/scipy/pytest/Streamlit
in this environment — none claimed; stdlib unittest and standalone HTML instead.

## Results summary

- Tests: **13/13 pass** (tier boundaries, policy floors, routing consistency, check math,
  promotion tiers, live veto, dataset counts, no-real-agency-data assertion).
- Notebooks: 3/3 executed, every code cell carries stored outputs from actual runs.
- Deck: 10 slides, verified via python-pptx. GitHub link is a placeholder — no repo created.

## Resume fit (Step 6, from Bhupesh_Chandra_Dimri_Master_Resume.pdf)

Overall fit for THIS role: **3/10**. Data/analytics fluency is real (SQL/Python pipelines,
Power BI/Tableau dashboards, forecasting +27%, reporting accuracy 99.5%); the executive
record the JD requires is absent (no C-suite/SES roles, no engineering-org leadership, no
federal compliance, no health IT). This project narrows the demonstration gap — it does not
close the seniority gap. Appointment type and citizenship are NOT stated in the JD and must
be confirmed in writing before any application; availability while employed full-time is
[CONFIRM WITH CANDIDATE].

## Limitations

- Thresholds are policy choices for a demo, not agency policy; re-validate on real data.
- Control titles are modeled on NIST SP 800-53 Rev. 5 families, not a certified baseline.
- Anomaly flagger found 1 monthly-volume anomaly; not stress-tested with injected daily anomalies.
- No Databricks port (listed as future work), no real systems, no clearance/federal claims.
- The JD states no salary, grade, location, clearance, or appointment type — none are quoted
  anywhere in this package.
- This project is preparation and analysis, not legal or immigration advice.

## Structure

```
ml-project-arpa-h-chief-data/
├── README.md  requirements.txt  .gitignore
├── src/  data_gen.py  ai_governance.py  lakehouse.py  ato_tracker.py
├── data/synthetic/  (9 CSVs)
├── notebooks/  01_ai_governance.ipynb  02_lakehouse_quality.ipynb  03_ato_tracker.ipynb
├── tests/  test_all.py
└── reports/  ai_governance_report.md  lakehouse_report.md  ato_report.md
              dashboard.html  deck.pptx  report.pdf
```
