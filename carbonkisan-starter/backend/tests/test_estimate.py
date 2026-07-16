"""
Sanity tests for the estimate response shape and the "manual validation"
cases required by PRD §8.7 — 10 hand-crafted checks against literature-
derived expected ranges. This file ships with 4 as a starting template;
extend to the full 10 before your Day 4 judge-hardening pass.

These tests assume model.pkl/explainer.pkl already exist
(run app/ml/generate_synthetic.py then app/ml/train.py first) and that
a `districts` table with seed data exists in your Supabase project —
they are integration tests, not pure unit tests, by design, because the
estimate function is meaningless without real district feature lookups.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_shap_breakdown_sums_close_to_total(monkeypatch):
    """
    The SHAP breakdown components should sum to something in the
    neighbourhood of the total co2e_tonnes prediction (SHAP values are
    additive with the model's expected_value baseline by construction —
    this test guards against the breakdown silently drifting out of
    sync with the underlying prediction after a refactor).
    """
    # Requires live model + Supabase connection — run manually against
    # a configured environment, this is a template to extend, not a
    # CI-safe unit test as written.
    pass


def test_no_till_cover_crop_higher_than_no_till_alone():
    """
    Sanity check from literature (PRD §8.5): combined no-till + cover
    crop must always estimate higher than no-till alone, for identical
    area/district/season inputs. If this ever fails, the model has
    learned something inconsistent with the base rates it was trained on.
    """
    pass  # extend with a live call to carbon_estimator.estimate() for both practices


def test_area_scaling_is_monotonic():
    """Doubling area_ha should roughly double co2e_tonnes, holding everything else constant."""
    pass  # extend with two live calls at area_ha=1 and area_ha=2


def test_unknown_district_raises_value_error():
    pass  # extend: assert carbon_estimator.estimate(..., district_code="XX_FAKE", ...) raises ValueError
