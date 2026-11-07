#!/usr/bin/env bash
# Eureka Lab — one-command launcher.
#
#   ./run.sh                     start on http://127.0.0.1:8096
#   EUREKA_PORT=9000 ./run.sh
#   ./run.sh --no-browser
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${EUREKA_PORT:-8096}"
cd "$HERE"

if [[ -f .env ]]; then set -a; . ./.env; set +a; fi

PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || { echo "[!] python3 not found (need 3.10+)." >&2; exit 1; }

if [[ ! -x .venv/bin/python ]]; then
  echo "[*] Creating virtual environment (.venv)..."
  if command -v uv >/dev/null 2>&1; then uv venv -q .venv
  elif [[ -x "$HOME/.local/bin/uv" ]]; then "$HOME/.local/bin/uv" venv -q .venv
  else "$PY" -m venv .venv
  fi
fi

if [[ ! -f .venv/.deps-installed ]] || [[ requirements.txt -nt .venv/.deps-installed ]]; then
  echo "[*] Installing dependencies..."
  if command -v uv >/dev/null 2>&1; then uv pip install -q -p .venv/bin/python -r requirements.txt
  elif [[ -x "$HOME/.local/bin/uv" ]]; then "$HOME/.local/bin/uv" pip install -q -p .venv/bin/python -r requirements.txt
  else .venv/bin/python -m pip install -q --upgrade pip && .venv/bin/python -m pip install -q -r requirements.txt
  fi
  touch .venv/.deps-installed
fi

if command -v lsof >/dev/null 2>&1 && lsof -t -i:"${PORT}" >/dev/null 2>&1; then
  echo "[*] Port ${PORT} busy — stopping previous instance..."
  lsof -t -i:"${PORT}" | xargs -r kill 2>/dev/null || true; sleep 1
fi

echo "[*] Eureka Lab → http://127.0.0.1:${PORT}   (Ctrl+C to stop)"
exec .venv/bin/python server.py --port "${PORT}" "$@"
