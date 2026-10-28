# Lakehouse Quality Report (synthetic demo)

| Dataset | Rows | Score | Tier | Failed checks |
|---|---|---|---|---|
| trials | 243 | 0.4 | Bronze | completeness:enrollment, uniqueness:trial_id, range:enrollment[0,100000] |
| biosamples | 600 | 0.833 | Silver | none |
| imaging | 400 | 0.5 | Bronze | reference:trial_id, range:quality_score[0.0,1.0] |
| grants | 120 | 1.0 | Gold | none |

Monthly-volume anomalies flagged: 1.