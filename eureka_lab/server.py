"""FastAPI backend server for Eureka Lab (port 8096)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from eureka_lab import __app_name__, __version__
from eureka_lab.catalog import CATEGORIES, FEATURED_QUESTIONS, LABS, LABS_BY_ID
from eureka_lab.config import (
    DEFAULT_PORT,
    LabSettings,
    load_progress,
    load_settings,
    record_quest_solved,
    record_snapshot,
    save_progress,
    save_settings,
)
from eureka_lab.engine import evaluate_lab_math, map_and_explain_question, resolve_lab_id

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="Eureka Lab — 16 Unique Real-Math Physics & Science Simulation Laboratories",
    version=__version__,
    description="16 distinct concepts backed 1-to-1 by 16 dedicated interactive HTML5 Canvas physics/science simulation engines + 3-tier explanation engine.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def _no_cache_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
    response = await call_next(request)
    if request.url.path.startswith("/api/") or request.url.path in ("/", "/static/js/app.js", "/static/js/simulations.js", "/static/css/styles.css"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


class ComputeRequest(BaseModel):
    params: dict[str, Any] = Field(default_factory=dict)
    telemetry: dict[str, Any] = Field(default_factory=dict)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class SnapshotRequest(BaseModel):
    lab_id: str
    title: str = ""
    params: dict[str, Any] = Field(default_factory=dict)
    notes: str = ""


@app.get("/api/health")
def api_health() -> dict[str, Any]:
    s = load_settings()
    prog = load_progress()
    unique_engines = {lab["engine_id"] for lab in LABS}
    return {
        "status": "ok",
        "ok": True,
        "app": "eureka-lab",
        "name": __app_name__,
        "version": __version__,
        "port": DEFAULT_PORT,
        "labs_count": len(LABS),
        "unique_engines_count": len(unique_engines),
        "one_to_one_mapping": len(LABS) == len(unique_engines),
        "solved_quests": len(prog.get("solved_quests", {})),
        "xp": prog.get("xp", 150),
        "provider": s.effective_provider(),
    }


@app.get("/api/labs")
def api_list_labs() -> dict[str, Any]:
    prog = load_progress()
    solved = prog.get("solved_quests", {})
    labs_out = []
    for lab in LABS:
        math_default = evaluate_lab_math(lab["id"])
        labs_out.append({
            **lab,
            "default_math": math_default,
            "quest_solved": lab["id"] in solved,
        })
    return {
        "labs": labs_out,
        "categories": CATEGORIES,
        "featured_questions": FEATURED_QUESTIONS,
        "progress": prog,
    }


@app.get("/api/labs/{lab_id}")
def api_get_lab(lab_id: str) -> dict[str, Any]:
    try:
        cid = resolve_lab_id(lab_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown lab '{lab_id}'")
    lab = LABS_BY_ID[cid]
    prog = load_progress()
    solved = prog.get("solved_quests", {})
    math_default = evaluate_lab_math(cid)
    return {
        **lab,
        "default_math": math_default,
        "quest_solved": cid in solved,
    }


@app.post("/api/labs/{lab_id}/compute")
def api_compute_lab(lab_id: str, req: ComputeRequest) -> dict[str, Any]:
    try:
        cid = resolve_lab_id(lab_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown lab '{lab_id}'")
    lab = LABS_BY_ID[cid]
    result = evaluate_lab_math(cid, req.params, req.telemetry)
    quest_award = None
    if result["quest"]["solved"]:
        quest_award = record_quest_solved(
            lab_id=cid,
            badge_name=lab["quest"]["badge_name"],
            xp_reward=int(lab["quest"]["xp"]),
            telemetry=req.telemetry,
        )
    prog = load_progress()
    result["quest_award"] = quest_award
    result["progress"] = {
        "xp": prog.get("xp", 150),
        "solved_count": len(prog.get("solved_quests", {})),
        "solved_quests": prog.get("solved_quests", {}),
    }
    return result


@app.post("/api/quests/{lab_id}/complete")
def api_complete_quest(lab_id: str, req: ComputeRequest | None = None) -> dict[str, Any]:
    try:
        cid = resolve_lab_id(lab_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown lab '{lab_id}'")
    lab = LABS_BY_ID[cid]
    award = record_quest_solved(
        lab_id=cid,
        badge_name=lab["quest"]["badge_name"],
        xp_reward=int(lab["quest"]["xp"]),
        telemetry=(req.telemetry if req else {}),
    )
    return {"ok": True, **award}


@app.post("/api/ask")
def api_ask_question(req: AskRequest) -> dict[str, Any]:
    result = map_and_explain_question(req.question)
    prog = load_progress()
    asked = prog.setdefault("questions_asked", [])
    asked.insert(
        0,
        {
            "question": result["question"],
            "matched_lab_id": result["matched_lab_id"],
            "scenario_label": result["scenario_label"],
            "asked_at": time.time(),
        },
    )
    prog["questions_asked"] = asked[:25]
    prog["xp"] = int(prog.get("xp", 150)) + 20
    save_progress(prog)
    result["progress"] = {
        "xp": prog["xp"],
        "solved_count": len(prog.get("solved_quests", {})),
    }
    return result


@app.get("/api/questions/featured")
def api_featured_questions() -> dict[str, Any]:
    return {"questions": FEATURED_QUESTIONS}


@app.get("/api/progress")
def api_get_progress() -> dict[str, Any]:
    prog = load_progress()
    return {
        **prog,
        "total_labs": len(LABS),
        "solved_count": len(prog.get("solved_quests", {})),
    }


@app.post("/api/snapshots")
def api_save_snapshot(req: SnapshotRequest) -> dict[str, Any]:
    try:
        cid = resolve_lab_id(req.lab_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown lab '{req.lab_id}'")
    snap = record_snapshot(cid, req.title, req.params, req.notes)
    prog = load_progress()
    return {"snapshot": snap, "snapshots": prog.get("snapshots", []), "xp": prog.get("xp", 150)}


@app.get("/api/settings")
def api_get_settings() -> dict[str, Any]:
    s = load_settings()
    data = s.model_dump()
    data["has_gemini_key"] = bool(s.gemini_api_key)
    data["gemini_api_key"] = ""
    return data


@app.post("/api/settings")
def api_update_settings(payload: dict[str, Any]) -> dict[str, Any]:
    current = load_settings().model_dump()
    for k, v in payload.items():
        if k in current and v is not None:
            if k == "gemini_api_key" and v == "":
                continue
            current[k] = v
    updated = save_settings(LabSettings(**current))
    out = updated.model_dump()
    out["has_gemini_key"] = bool(updated.gemini_api_key)
    out["gemini_api_key"] = ""
    return out


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index() -> Any:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return JSONResponse({"error": "Frontend assets missing"}, status_code=500)
    return FileResponse(str(index_file))
