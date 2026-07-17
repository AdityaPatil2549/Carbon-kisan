"""
Trains the XGBoost carbon estimator and fits a SHAP TreeExplainer.

Acceptance thresholds (PRD §8.7) — this script will WARN, not fail,
if these aren't met, because a hackathon build shouldn't hard-crash
on a threshold miss. Read the warning before you demo, though.

Run: python app/ml/train.py
Requires: data/train.csv (run generate_synthetic.py first)
"""
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import root_mean_squared_error  # scikit-learn 1.6+: `squared=False` param was removed
import xgboost as xgb
import shap

FEATURES = ["practice_encoded", "area_ha", "soil_modifier", "rainfall_encoded", "season_months"]
TARGET = "co2e_tonnes"
RMSE_THRESHOLD = 0.15


def train():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "train.csv"))
    X, y = df[FEATURES], df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    model = xgb.XGBRegressor(
        objective="reg:squarederror",
        max_depth=6,
        n_estimators=200,
        learning_rate=0.05,
        random_state=42,
    )

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
    print(f"5-fold CV RMSE: {-cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    test_rmse = root_mean_squared_error(y_test, preds)
    print(f"Held-out test RMSE: {test_rmse:.4f} (threshold: {RMSE_THRESHOLD})")

    if test_rmse >= RMSE_THRESHOLD:
        print(f"WARNING: RMSE {test_rmse:.4f} exceeds the {RMSE_THRESHOLD} tonne acceptance "
              f"threshold from PRD §8.7. Investigate feature engineering or hyperparameters "
              f"before you present this model to judges.")

    explainer = shap.TreeExplainer(model)

    # Sanity check from PRD §8.7: practice_type and soil_modifier must be
    # the top 2 SHAP features across the validation set, or the model has
    # learned something spurious, not the real relationship.
    shap_values = explainer.shap_values(X_test)
    mean_abs_shap = pd.Series(abs(shap_values).mean(axis=0), index=FEATURES).sort_values(ascending=False)
    print("\nMean |SHAP| by feature (top 2 should be practice_encoded and soil_modifier):")
    print(mean_abs_shap)
    if set(mean_abs_shap.index[:2]) != {"practice_encoded", "soil_modifier"}:
        print("WARNING: top-2 SHAP features are not {practice_encoded, soil_modifier} — "
              "the model may have learned a spurious relationship. Investigate before shipping.")

    with open(os.path.join(BASE_DIR, "app", "ml", "model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(BASE_DIR, "app", "ml", "explainer.pkl"), "wb") as f:
        pickle.dump(explainer, f)

    print("\nSaved model.pkl and explainer.pkl to app/ml/")


if __name__ == "__main__":
    train()
