"""Configuration, settings persistence, and progress storage for Eureka Lab."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PORT = int(os.environ.get("EUREKA_PORT", "8096"))
DEFAULT_HOST = os.environ.get("EUREKA_HOST", "0.0.0.0")


def data_dir() -> Path:
    custom = os.environ.get("EUREKA_DATA_DIR")
    p = Path(custom) if custom else (ROOT_DIR / "data")
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_path() -> Path:
    return data_dir() / "settings.json"


def progress_path() -> Path:
    return data_dir() / "progress.json"


class LabSettings(BaseModel):
    default_tier: str = Field(default="high_school", description="eli7 | high_school | engineer")
    sound_enabled: bool = Field(default=False)
    high_contrast: bool = Field(default=False)
    show_fps: bool = Field(default=True)
    ai_provider: str = Field(default="builtin", description="builtin | ollama | gemini")
    ollama_url: str = Field(default="http://127.0.0.1:11434")
    ollama_model: str = Field(default="llama3.2")
    gemini_api_key: str = Field(default="")

    def effective_provider(self) -> str:
        if self.ai_provider == "gemini" and (self.gemini_api_key or os.environ.get("GEMINI_API_KEY")):
            return "gemini"
        if self.ai_provider == "ollama":
            return "ollama"
        return "builtin"

    def effective_model(self) -> str:
        prov = self.effective_provider()
        if prov == "gemini":
            return "gemini-2.5-flash"
        if prov == "ollama":
            return self.ollama_model
        return "eureka-symbolic-v1"


def load_settings() -> LabSettings:
    p = config_path()
    if p.exists():
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            return LabSettings(**raw)
        except Exception:
            pass
    s = LabSettings()
    save_settings(s)
    return s


def save_settings(settings: LabSettings) -> LabSettings:
    p = config_path()
    p.write_text(json.dumps(settings.model_dump(), indent=2), encoding="utf-8")
    return settings


def default_progress() -> dict[str, Any]:
    return {
        "xp": 150,
        "solved_quests": {},
        "questions_asked": [],
        "snapshots": [],
        "updated_at": time.time(),
    }


def load_progress() -> dict[str, Any]:
    p = progress_path()
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                base = default_progress()
                base.update(data)
                return base
        except Exception:
            pass
    prog = default_progress()
    save_progress(prog)
    return prog


def save_progress(prog: dict[str, Any]) -> dict[str, Any]:
    prog["updated_at"] = time.time()
    progress_path().write_text(json.dumps(prog, indent=2), encoding="utf-8")
    return prog


def record_quest_solved(lab_id: str, badge_name: str, xp_reward: int, telemetry: dict[str, Any] | None = None) -> dict[str, Any]:
    prog = load_progress()
    solved = prog.setdefault("solved_quests", {})
    already = lab_id in solved
    if not already:
        solved[lab_id] = {
            "lab_id": lab_id,
            "badge_name": badge_name,
            "xp_reward": xp_reward,
            "solved_at": time.time(),
            "telemetry": telemetry or {},
        }
        prog["xp"] = int(prog.get("xp", 0)) + int(xp_reward)
        save_progress(prog)
    return {
        "newly_solved": not already,
        "total_xp": prog["xp"],
        "solved_count": len(solved),
        "solved_quests": solved,
    }


def record_snapshot(lab_id: str, title: str, params: dict[str, Any], notes: str = "") -> dict[str, Any]:
    prog = load_progress()
    snaps = prog.setdefault("snapshots", [])
    snap = {
        "id": f"snap-{int(time.time() * 1000)}",
        "lab_id": lab_id,
        "title": title.strip() or f"Experiment on {lab_id}",
        "params": params,
        "notes": notes.strip(),
        "created_at": time.time(),
    }
    snaps.insert(0, snap)
    prog["snapshots"] = snaps[:30]
    prog["xp"] = int(prog.get("xp", 0)) + 25
    save_progress(prog)
    return snap
