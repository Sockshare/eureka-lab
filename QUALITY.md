# Eureka Lab — Engineering Quality & Verification Report (`QUALITY.md`)

## 1. Architecture & Mathematical Fidelity Summary

| Subsystem | Implementation | Verification |
| :--- | :--- | :--- |
| **Entrypoints & Port** | `server.py` (with `_VENV_SP` auto-injection), `app.py`, `./run.sh` on default port **`8096`** (`EUREKA_PORT`) | `tests/smoke/test_api_smoke.py` & live `/api/health` |
| **8 Real-Math Simulations** | Symplectic Velocity-Verlet, Kutta-Joukowski Potential Flow, Stigmergic ACO Chemotaxis, Spatial SEIR, RK4 Double Pendulum, Helmholtz/Mach Wave Tank, Lande Breeder Evolution, 60 FPS Backprop MLP | `tests/unit/test_engine_and_catalog.py` |
| **3-Tier Adaptive Explanation Engine** | Toggleable `eli7` ("Explain to a 7-Year-Old"), `high_school` ("High School Honors"), and `engineer` ("Engineer & Equations") with Live Formula Substitution | `tests/ui/test_playwright_ui.py` |
| **What-If Challenge Quests** | Real-time goal evaluation across all 8 labs with XP rewards, progress bars, and 1-click demonstration tuning | `test_quest_solutions_across_all_8_labs` |
| **Headless Chromium E2E Gate** | Playwright `1.49.1` verifying `0` console errors, `0` uncaught page errors, and capturing 7 high-DPI screenshots in `docs/screenshots/` | `tests/ui/test_playwright_ui.py` |

## 2. Verification Commands

```bash
.venv/bin/python scripts/selfcheck.py
.venv/bin/pytest -v
curl -s http://127.0.0.1:8096/api/health
```
