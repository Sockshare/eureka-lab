#!/usr/bin/env python3
"""Eureka Lab setup, physics engine & diagnostics self-check script.

    python scripts/selfcheck.py
"""

from __future__ import annotations

import importlib
import os
import site
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_VENV_SP = ROOT / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if _VENV_SP.is_dir() and str(_VENV_SP) not in sys.path:
    site.addsitedir(str(_VENV_SP))

OK, BAD, WARN = "✅", "❌", "⚠️ "


def line(status: str, text: str, fix: str = "") -> None:
    print(f"{status} {text}")
    if fix:
        print(f"      → {fix}")


def main() -> int:
    problems = 0
    print("\nEureka Lab — Setup & Physics Engine Diagnostics Check\n" + "-" * 56)

    # 1. Python version
    v = sys.version_info
    if v >= (3, 10):
        line(OK, f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        problems += 1
        line(BAD, f"Python {v.major}.{v.minor} is too old (need 3.10+)", "Install Python 3.10 or newer.")

    # 2. Virtualenv check
    in_venv = (sys.prefix != getattr(sys, "base_prefix", sys.prefix)) or _VENV_SP.is_dir()
    line(
        OK if in_venv else WARN,
        "Virtual environment (.venv) detected" if in_venv else "Not inside .venv",
        "" if in_venv else "Run:  source .venv/bin/activate",
    )

    # 3. Required packages
    missing = []
    for mod in ("fastapi", "uvicorn", "httpx", "PIL", "pydantic", "multipart", "pytest", "playwright"):
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        problems += 1
        line(BAD, f"Missing packages: {', '.join(missing)}", "Run:  .venv/bin/pip install -r requirements.txt")
    else:
        line(OK, "All required packages installed (fastapi, uvicorn, httpx, pillow, pydantic, python-multipart, pytest, playwright)")

    # 4. App imports & 16 Interactive Laboratories 1-to-1 check
    try:
        from eureka_lab import __version__
        from eureka_lab.catalog import LABS
        from eureka_lab.config import config_path, load_settings
        from eureka_lab.engine import evaluate_lab_math, map_and_explain_question

        assert len(LABS) == 16, f"Expected 16 labs, found {len(LABS)}"
        engine_ids = {lab["engine_id"] for lab in LABS}
        assert len(engine_ids) == 16, f"Expected 16 unique engine_ids, found {len(engine_ids)}"
        for lab in LABS:
            res = evaluate_lab_math(lab["id"])
            assert res["live_substitution"], f"Missing live formula for {lab['id']}"
            assert set(lab["tiers"].keys()) == {"eli7", "high_school", "engineer"}

        ask_res = map_and_explain_question("How does a glass prism split white laser light into a full rainbow spectrum?")
        assert ask_res["matched_lab_id"] == "geometric-optics"
        line(OK, f"Eureka Lab v{__version__} loaded ({len(LABS)} unique 1-to-1 laboratories & 3-tier explanation engine verified)")
    except Exception as exc:
        problems += 1
        line(BAD, f"Failed to verify Eureka Lab modules: {exc}")
        return 1

    # 5. Settings check
    s = load_settings()
    line(OK, f"Settings file: {config_path()} (provider={s.effective_provider()}, model={s.effective_model()})")

    # 6. Port 8096 status
    port = int(os.environ.get("EUREKA_PORT", "8096"))
    with socket.socket() as sock:
        busy = sock.connect_ex(("127.0.0.1", port)) == 0
    line(
        OK if not busy else WARN,
        f"Port {port} is free" if not busy else f"Port {port} is currently active / serving Eureka Lab",
    )

    print("-" * 56)
    if problems:
        print(f"{problems} issue(s) need attention.\n")
        return 1
    print("All systems nominal! Start with:  ./run.sh  or  python3 server.py\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
