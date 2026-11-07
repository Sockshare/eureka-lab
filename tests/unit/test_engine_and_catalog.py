"""Unit tests for the 16 Unique Real-Math Simulations, 1-to-1 Engine Mapping, Live Formula Evaluator & Question Mapper."""

from __future__ import annotations

import pytest

from eureka_lab.catalog import CATEGORIES, FEATURED_QUESTIONS, LABS, LABS_BY_ID
from eureka_lab.engine import default_params_for_lab, evaluate_lab_math, map_and_explain_question


def test_catalog_has_all_16_unique_concepts_and_strict_1_to_1_engines() -> None:
    assert len(LABS) == 16
    expected_ids = {
        "orbital-mechanics",
        "airfoil-wind-tunnel",
        "double-pendulum-chaos",
        "geometric-optics",
        "electromagnetic-fields",
        "quantum-tunneling",
        "thermodynamics-gas",
        "fluid-vortex-tunnel",
        "wave-interference",
        "structural-truss",
        "rlc-circuit-resonance",
        "relativistic-lensing",
        "fourier-epicycles",
        "ant-colony-swarm",
        "epidemic-seir",
        "neural-backprop",
    }
    assert set(LABS_BY_ID.keys()) == expected_ids

    # Mandatory assertion: 16 concepts == 16 distinct engine_ids & 16 distinct engine_classes (ZERO duplicates!)
    concept_ids = [lab["id"] for lab in LABS]
    engine_ids = [lab["engine_id"] for lab in LABS]
    engine_classes = [lab["engine_class"] for lab in LABS]
    assert len(set(concept_ids)) == 16
    assert len(set(engine_ids)) == 16
    assert len(set(engine_classes)) == 16
    for lab in LABS:
        assert lab["engine_id"] == lab["id"]
        assert lab["category"] in CATEGORIES
        assert len(lab["parameters"]) == 5
        assert len(lab["presets"]) >= 4
        assert set(lab["tiers"].keys()) == {"eli7", "high_school", "engineer"}
        assert "quest" in lab and lab["quest"]["xp"] > 0
        assert "solve_params" in lab["quest"]


@pytest.mark.parametrize("lab_id", list(LABS_BY_ID.keys()))
def test_evaluate_lab_math_defaults_and_live_substitution(lab_id: str) -> None:
    defaults = default_params_for_lab(lab_id)
    res = evaluate_lab_math(lab_id, defaults)
    assert res["lab_id"] == lab_id
    assert res["engine_id"] == lab_id
    assert len(res["live_substitution"]) > 15
    assert len(res["metrics"]) == 5
    assert "solved" in res["quest"]
    assert 0.0 <= res["quest"]["progress_pct"] <= 100.0


@pytest.mark.parametrize("lab_id", list(LABS_BY_ID.keys()))
def test_quest_solutions_across_all_16_labs(lab_id: str) -> None:
    solve_params = LABS_BY_ID[lab_id]["quest"]["solve_params"]
    res = evaluate_lab_math(lab_id, solve_params)
    assert res["quest"]["solved"] is True, f"Quest for {lab_id} failed to solve with solve_params={solve_params}"


def test_question_mapper_routes_all_16_featured_questions_accurately() -> None:
    assert len(FEATURED_QUESTIONS) == 16
    assert len({fq["lab_id"] for fq in FEATURED_QUESTIONS}) == 16
    for fq in FEATURED_QUESTIONS:
        mapped = map_and_explain_question(fq["question"])
        assert mapped["matched_lab_id"] == fq["lab_id"]
        assert set(mapped["tiers"].keys()) == {"eli7", "high_school", "engineer"}
        assert fq["question"] in mapped["tiers"]["eli7"]["headline"]
