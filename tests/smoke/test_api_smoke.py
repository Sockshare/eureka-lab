"""FastAPI smoke tests for Eureka Lab REST API endpoints (16 Unique Simulations)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from eureka_lab.server import app

client = TestClient(app)


def test_api_health() -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["app"] == "eureka-lab"
    assert data["labs_count"] == 16
    assert data["unique_engines_count"] == 16
    assert data["one_to_one_mapping"] is True


def test_api_labs_and_compute_all_16() -> None:
    res = client.get("/api/labs")
    assert res.status_code == 200
    payload = res.json()
    assert len(payload["labs"]) == 16
    assert len({lab["engine_id"] for lab in payload["labs"]}) == 16

    for lab in payload["labs"]:
        lid = lab["id"]
        c_res = client.post(f"/api/labs/{lid}/compute", json={"params": {}, "telemetry": {}})
        assert c_res.status_code == 200
        c_data = c_res.json()
        assert c_data["lab_id"] == lid
        assert c_data["engine_id"] == lid
        assert len(c_data["metrics"]) == 5


def test_api_ask_question_and_snapshot() -> None:
    ask_res = client.post(
        "/api/ask",
        json={"question": "How does a glass prism split white laser light into a full rainbow spectrum?"},
    )
    assert ask_res.status_code == 200
    ask_data = ask_res.json()
    assert ask_data["matched_lab_id"] == "geometric-optics"
    assert "eli7" in ask_data["tiers"]

    snap_res = client.post(
        "/api/snapshots",
        json={
            "lab_id": "orbital-mechanics",
            "title": "Test Hohmann Orbit",
            "params": {"star_mass": 1.0, "launch_speed": 35.0},
        },
    )
    assert snap_res.status_code == 200
    assert snap_res.json()["snapshot"]["lab_id"] == "orbital-mechanics"
