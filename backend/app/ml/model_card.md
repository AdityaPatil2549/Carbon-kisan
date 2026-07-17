# CarbonKisan Carbon Estimator — Model Card

**Model version:** xgb_v1
**Task:** Regression — predict `co2e_tonnes` sequestered given practice, land area, and district features.

## Training data
10,000 synthetically generated rows (`app/ml/generate_synthetic.py`), parameterised by:
- Base sequestration rates from a peer-reviewed meta-analysis (Frontiers Sustainable Food Systems, 2023)
- District soil/rainfall modifiers from `data/maharashtra_districts.csv` — **currently placeholder values**, not yet joined to real ICRISAT/FAO sourced data. See that file's header for the correction note.

## Features
`practice_encoded`, `area_ha`, `soil_modifier`, `rainfall_encoded`, `season_months`

## Evaluation
Run `python app/ml/train.py` to regenerate these numbers. Target: held-out test RMSE < 0.15 tonnes CO2e.

## Known limitations
1. Training data is synthetic, not field-measured — this is disclosed, not hidden.
2. District soil modifiers are placeholder values pending real dataset integration (§ data/maharashtra_districts.csv).
3. No real-world verification loop exists yet — Phase 2 of the PRD roadmap adds satellite-based practice verification.
4. Model has only been validated for the 4 practice types and 36 Maharashtra districts in scope — do not extrapolate to other states or practices without retraining.

## Intended use
Estimate generation for marketplace listing price-setting. **Not** intended as a regulatory-grade MRV (Measurement, Reporting, Verification) certification in its current form — see PRD §12.4 for the compliance framing required in any user-facing copy.
