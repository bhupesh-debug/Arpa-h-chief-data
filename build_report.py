"""Project report PDF (ReportLab, Liberation Sans)."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("LS", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LSB", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
NAVY = HexColor("#1F3864"); GREY = HexColor("#595959"); LIGHT = HexColor("#D9E2F3")
OUT = "/home/hatch/workspace/ml-project-arpa-h-chief-data/reports/report.pdf"

sT = ParagraphStyle("t", fontName="LSB", fontSize=16, leading=20, textColor=NAVY)
sS = ParagraphStyle("s", fontName="LS", fontSize=10, leading=14, textColor=GREY)
sH = ParagraphStyle("h", fontName="LSB", fontSize=12, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=4)
sB = ParagraphStyle("b", fontName="LS", fontSize=10, leading=14, spaceAfter=4)
sC = ParagraphStyle("c", fontName="LS", fontSize=9.5, leading=13)
sCB = ParagraphStyle("cb", fontName="LSB", fontSize=9.5, leading=13)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tbl4(rows):
    data = [[Paragraph(f"<b>{esc(a)}</b>", sCB), Paragraph(esc(b), sC),
             Paragraph(esc(c), sC), Paragraph(esc(d), sC)] for a, b, c, d in rows]
    t = Table(data, colWidths=[1.35 * inch, 1.85 * inch, 1.15 * inch, 2.55 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT),
                           ("BOX", (0, 0), (-1, -1), 0.75, NAVY),
                           ("INNERGRID", (0, 0), (-1, -1), 0.4, HexColor("#B0B8C8")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def tbl(rows):
    data = [[Paragraph(f"<b>{esc(a)}</b>", sCB), Paragraph(esc(b), sC)] for a, b in rows]
    t = Table(data, colWidths=[1.7 * inch, 5.2 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT),
                           ("BOX", (0, 0), (-1, -1), 0.75, NAVY),
                           ("INNERGRID", (0, 0), (-1, -1), 0.4, HexColor("#B0B8C8")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


story = [
    Paragraph("Executive Data Leadership — Portfolio Project Report", sT),
    Paragraph("JD-to-ML-Project build for the ARPA-H Chief of IT and Data Technology JD. "
              "PORTFOLIO DEMONSTRATION on synthetic data — not evidence of a C-suite/SES role, federal "
              "employment, a security clearance, or any executive record. All data fictional; no real "
              "ARPA-H data, budgets, or systems are represented.", sS),
    Paragraph("1. Executive Summary", sH),
    Paragraph("The JD is a chief-level leadership post: 10+ years of senior executive technology leadership, "
              "including 5 years in a C-suite, SES, or equivalent role, owning enterprise technology, data, AI, "
              "engineering, and cybersecurity for a federal health research agency. A generic ML model demo would "
              "be tone-deaf for this role and would misrepresent the candidate. The artifact built here is therefore "
              "executive infrastructure in working code: a responsible-AI risk-scoring and approval-routing engine, "
              "a lakehouse quality-gate pipeline, and an ATO control-mapping tracker — the three operating rhythms "
              "a chief actually governs. All three run, all are tested (13/13 tests pass), and every result below "
              "was produced by running the code.", sB),
    Paragraph("2. JD Breakdown (Step 1)", sH),
    tbl([("Core responsibilities", "Enterprise technology strategy; AI strategy and responsible governance; software/systems engineering; data infrastructure and governance (FISMA, FedRAMP, NIST); cybersecurity and risk; digital modernization; program support; acquisition and vendor management."),
         ("Required skills", "Enterprise architecture, cloud, cybersecurity, data engineering, applied AI/ML, DevSecOps/agile/CI/CD, federal IT requirements, executive communication, talent building."),
         ("Hidden expectations", "Build the function from near-zero at agency-formation stage; advise the Director; move at startup speed inside federal constraints; own A&A and continuous monitoring."),
         ("KPIs", "Strategy delivered; AI inventory governed; data estate trustworthy; systems authorized and monitored; vendors performing."),
         ("Seniority", "Chief / SES-equivalent executive. Not an individual-contributor ML role."),
         ("Risk factors", "Seniority bar (5-year C-suite/SES requirement); federal-compliance depth; engineering-org leadership; health-IT domain; appointment type and citizenship not stated in the JD.")]),
    Paragraph("3. Problem Definitions (Step 2)", sH),
    tbl([("P1 — AI governance", "Input: use-case attributes (sensitivity, autonomy, impact, opacity, deployment). Output: risk score 0-100, tier, approval route, SLA, monitoring cadence. Type: transparent rules engine (not ML) — deliberately."),
         ("P2 — Lakehouse quality", "Input: research-style tables. Output: per-check pass/warn/fail, dataset score, Bronze/Silver/Gold promotion, anomaly flags. Type: validation pipeline + statistical flags."),
         ("P3 — ATO tracking", "Input: system x control assessments + POA&Ms. Output: compliance score, authorization recommendation with critical-gap veto. Type: rules engine modeled on NIST SP 800-53 Rev. 5 families.")]),
    Paragraph("4. Data + Model Strategy (Steps 3-4)", sH),
    Paragraph("Synthetic, seeded (seed 42), fully fictional: 14 AI use cases; 243 trials, 600 biosamples, 400 images, "
              "120 grants; 8 systems x 30 controls = 240 assessments and 115 POA&M items. Injected, disclosed defects: "
              "missing enrollments, duplicate trial IDs, negative enrollments, broken image references, out-of-range "
              "quality scores, and one planted veto scenario (Identity Platform). Baselines are the rules themselves — "
              "there is no black-box model to compare against, because interpretability is the requirement: an executive "
              "must defend every routing, promotion, and authorization decision. Evaluation = ground-truth checks: "
              "tier coverage, defect detection by named checks, veto behavior, and the 13-test suite.", sB),
    Paragraph("5. Results (Step 5)", sH),
    tbl([("AI routing", "Low 3, Moderate 5, High 4, Critical 2. Floor rule fires once (AI-10, restricted + autonomous). Critical cases route to Director-level approval with monthly monitoring."),
         ("Lakehouse", "Grants Gold (1.000); biosamples Silver (0.833, missing-volume warnings only); imaging Bronze (0.500, broken references + out-of-range scores); trials Bronze (0.400, missing + duplicate + negative enrollments). 1 monthly-volume anomaly flagged."),
         ("ATO", "2 Authorized (Research Data Lake 0.983, Identity Platform would-be 0.95); 6 Not authorized. Identity Platform is NOT authorized despite 0.95 — one open critical POA&M vetoes it. Legacy File Shares lowest at 0.275 with 3 open critical items.")]),
    Paragraph("6. Resume Alignment (Step 6)", sH),
    Paragraph("Source: Bhupesh_Chandra_Dimri_Master_Resume.pdf (3 pages; Financial Analyst, JPMorgan Chase Jul 2025-present; "
              "9+ years banking/financial services). No facts invented; gaps stated bluntly.", sB),
    tbl4([("Enterprise tech leadership", "No evidence — analyst career, no org leadership", "YES — decisive", "This project demonstrates how the function would be run, not that it has been run."),
         ("AI governance", "Scikit-learn literacy; AI-assisted builds; no governance record", "YES", "This project's routing engine is the talking point; do not claim a governance record."),
         ("Data architecture", "SQL/Python pipelines; Power BI/Tableau dashboards; ERP consolidation", "Partial — scale and lakehouse depth unproven", "Lakehouse gates demo + pipeline experience."),
         ("Cybersecurity / compliance", "SOX 404, COSO, audit findings -25% (analogue only)", "YES — no NIST/FISMA/FedRAMP/A&A", "Name SOX as a controls analogue; never equate it with federal compliance."),
         ("Engineering leadership", "Automation scripting; no teams, no DevSecOps/CI/CD", "YES", "State honestly; do not claim it."),
         ("Health IT / federal", "None on resume", "YES", "No mitigation available from this project alone."),
         ("Availability / vehicle", "Employed full-time; F-1 STEM OPT", "CONFIRM WITH CANDIDATE", "Appointment type and citizenship MUST be confirmed in writing before any application.")]),
    Paragraph("Overall fit for THIS role: 3/10. Data/analytics fluency is real; the executive record the JD requires is "
              "absent. This project narrows the demonstration gap — it does not close the seniority gap, and the report "
              "does not pretend otherwise.", sB),
    Paragraph("7. Architecture (Step 7)", sH),
    Paragraph("Synthetic CSVs → ingestion (pandas/csv) → three engines (ai_governance, lakehouse, ato_tracker) → "
              "Markdown reports + standalone HTML dashboard + 10-slide deck. Python 3.12+; pandas/numpy/matplotlib; "
              "python-pptx; stdlib unittest. Deployment pattern for the role's context: a scheduled batch pipeline "
              "mirroring a Databricks job (Delta tables, scheduled workflows) — listed as future work, not claimed.", sB),
    Paragraph("8. Slide Deck Content (Step 8)", sH),
    Paragraph("10 slides, built directly with python-pptx (no pptx skill installed): Title (with portfolio disclaimer), "
              "Problem Overview, JD Breakdown, Approach (honest fit), Data Strategy, Solution Design, Results & Insights, "
              "Business Impact, Future Improvements, About (Bhupesh Chandra Dimri, bhupesh7cd@gmail.com, GitHub link "
              "placeholder only — no URL invented).", sB),
    Paragraph("9. GitHub Structure + README (Step 9)", sH),
    Paragraph("ml-project-arpa-h-chief-data/ — README.md, requirements.txt, .gitignore, src/ (data_gen, ai_governance, "
              "lakehouse, ato_tracker), data/synthetic/ (9 CSVs), notebooks/ (3 executed), tests/ (13 tests), reports/ "
              "(3 Markdown reports, dashboard.html, deck.pptx, report.pdf). Not pushed to GitHub — no repo creation was "
              "requested.", sB),
    Paragraph("10. Differentiation (Step 10)", sH),
    Paragraph("Wow factors: (a) the veto — a 0.95 system blocked by one open critical gap is a more credible governance "
              "story than a clean sweep; (b) tier coverage — Gold/Silver/Bronze all demonstrated with named failing checks; "
              "(c) role-shaped outputs — approval routes with SLAs and monitoring cadences, not model scores. "
              "Hiring-manager insights: governance speed (tiered SLAs) is the bottleneck, not model sophistication; quality "
              "gates must precede AI deployment; ATO is continuous monitoring, not a one-time event. Questions to ask: "
              "appointment type and citizenship requirements; current state of the data estate; existing AI inventory; ATO "
              "backlog; build-vs-buy posture; talent model for the technology organization.", sB),
    Paragraph("Limitations (stated openly)", sH),
    Paragraph("All data synthetic; thresholds are policy choices, not agency policy, and need re-validation on real data. "
              "Control titles are modeled on NIST SP 800-53 Rev. 5 families, not a certified control baseline. The anomaly "
              "flagger found only 1 monthly-volume anomaly and was not stress-tested with injected daily anomalies. No "
              "Databricks port, no real systems, no clearance or federal-employment claims. The JD states no salary, grade, "
              "location, clearance, or appointment type — none are quoted anywhere in this package.", sB),
]

doc = SimpleDocTemplate(OUT, pagesize=LETTER, leftMargin=0.55 * inch, rightMargin=0.55 * inch,
                        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
                        title="Executive Data Leadership — Project Report", author="Bhupesh Chandra Dimri")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("LS", 8.5); canvas.setFillColor(GREY)
    canvas.drawString(0.55 * inch, 0.35 * inch, "Executive Data Leadership — Project Report (synthetic demo)")
    canvas.drawRightString(LETTER[0] - 0.55 * inch, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("report built:", OUT)
