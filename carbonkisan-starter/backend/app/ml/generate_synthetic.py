"""
Generates synthetic training data for the carbon estimator.

Methodology (defensible and disclosed — this is what goes in the
model card and what you say when a judge asks "where's your data
from?"): base sequestration rates are drawn from a peer-reviewed
meta-analysis (Frontiers Sustainable Food Systems, 2023). District
soil/rainfall modifiers come from data/maharashtra_districts.csv
(currently placeholder values pending real ICRISAT/FAO sourcing —
see that file's header comment). Gaussian noise simulates natural
field variance around the literature mean.

Run: python app/ml/generate_synthetic.py
"""
import numpy as np
import pandas as pd

np.random.seed(42)

BASE_RATES = {
    "no_till": 0.73,
    "cover_crop": 1.31,
    "no_till_cover_crop": 1.43,
    "agroforestry": 0.67,
}
PRACTICE_ENCODING = {"no_till": 0, "cover_crop": 1, "no_till_cover_crop": 2, "agroforestry": 3}
RAINFALL_ENCODING = {"low": 0, "medium": 1, "high": 2}

N_SAMPLES = 10_000


def generate(districts_csv: str = "data/maharashtra_districts.csv", out_csv: str = "data/train.csv"):
    districts = pd.read_csv(districts_csv)

    rows = []
    for _ in range(N_SAMPLES):
        district = districts.sample(1).iloc[0]
        practice = np.random.choice(list(BASE_RATES.keys()))
        area_ha = round(float(np.random.uniform(0.5, 10.0)), 2)
        season_months = int(np.random.choice([6, 12]))

        co2e = (
            BASE_RATES[practice]
            * area_ha
            * district["soil_modifier"]
            * (season_months / 12)
            + np.random.normal(0, 0.1)
        )
        co2e = max(co2e, 0.01)  # sequestration cannot be negative in this simplified model

        rows.append({
            "practice_encoded": PRACTICE_ENCODING[practice],
            "area_ha": area_ha,
            "soil_modifier": district["soil_modifier"],
            "rainfall_encoded": RAINFALL_ENCODING[district["rainfall_zone"]],
            "season_months": season_months,
            "co2e_tonnes": round(co2e, 3),
        })

    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"Generated {len(df)} synthetic rows -> {out_csv}")
    print(df.describe())


if __name__ == "__main__":
    generate()
