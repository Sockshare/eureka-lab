"""End-to-end Headless Chromium Playwright UI tests & Screenshot Generator for Eureka Lab (16 Unique Simulations)."""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOT_DIR = ROOT / "docs" / "screenshots"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@pytest.fixture(scope="module")
def live_server_url() -> str:
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "server.py"), "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    base_url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            r = httpx.get(f"{base_url}/api/health", timeout=1.0)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(0.15)
    else:
        proc.terminate()
        raise RuntimeError("Eureka Lab test server failed to start")

    yield base_url
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()


def test_full_observatory_ui_16_unique_simulations_and_capture_screenshots(live_server_url: str) -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    console_errors: list[str] = []
    page_errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1520, "height": 980})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        page.goto(live_server_url, wait_until="networkidle")
        page.wait_for_selector(".lab-tab", timeout=10000)
        assert page.locator(".lab-tab").count() == 16

        # Verify in browser JS that all 16 concepts map to 16 distinct engine instances & constructor classes
        js_verification = page.evaluate(
            """() => {
                const sims = window.EurekaSimulations || {};
                const keys = Object.keys(sims);
                const ctorNames = new Set(keys.map(k => sims[k] && sims[k].constructor && sims[k].constructor.name));
                const tabEngines = new Set(Array.from(document.querySelectorAll('.lab-tab')).map(el => el.dataset.engineId));
                return {
                    simCount: keys.length,
                    uniqueConstructors: ctorNames.size,
                    uniqueTabEngines: tabEngines.size,
                };
            }"""
        )
        assert js_verification["simCount"] == 16
        assert js_verification["uniqueConstructors"] == 16
        assert js_verification["uniqueTabEngines"] == 16

        # 1. Orbital Mechanics & Slingshot
        page.wait_for_timeout(400)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "01_orbital_mechanics_lab.png"), full_page=True)

        # Solve Quest on Lab 1 via "⚡ Tune to Solve" and verify badge updates
        page.click("#quest-solve-btn")
        page.wait_for_timeout(220)
        assert "Solved" in page.locator("#quest-status-badge").inner_text()

        # 2. Geometric Optics Prism & Lenses
        page.click('.lab-tab[data-lab-id="geometric-optics"]')
        page.click('.tier-tab[data-tier="engineer"]')
        page.wait_for_timeout(400)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "02_geometric_optics_prism.png"), full_page=True)

        # 3. Quantum Wavepacket & Barrier Tunneling
        page.click('.lab-tab[data-lab-id="quantum-tunneling"]')
        page.click('.tier-tab[data-tier="high_school"]')
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "03_quantum_tunneling.png"), full_page=True)

        # 4. General Relativity Black Hole Lensing
        page.click('.lab-tab[data-lab-id="relativistic-lensing"]')
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "04_relativistic_lensing.png"), full_page=True)

        # 5. Structural Truss Bridge Stress & Buckling
        page.click('.lab-tab[data-lab-id="structural-truss"]')
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "05_structural_truss_bridge.png"), full_page=True)

        # 6. Driven AC RLC Circuit, Phasor & Bode Plot
        page.click('.lab-tab[data-lab-id="rlc-circuit-resonance"]')
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "06_rlc_circuit_resonance.png"), full_page=True)

        # 7. Fourier Epicycles Drawing Machine
        page.click('.lab-tab[data-lab-id="fourier-epicycles"]')
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=str(SCREENSHOT_DIR / "07_fourier_epicycles.png"), full_page=True)

        # Cycle through remaining labs to verify zero runtime errors across all 16
        for rem_id in (
            "airfoil-wind-tunnel",
            "double-pendulum-chaos",
            "electromagnetic-fields",
            "thermodynamics-gas",
            "fluid-vortex-tunnel",
            "wave-interference",
            "ant-colony-swarm",
            "epidemic-seir",
            "neural-backprop",
        ):
            page.click(f'.lab-tab[data-lab-id="{rem_id}"]')
            page.wait_for_timeout(140)

        # Test Custom Question Mapper Omnibar
        page.fill("#question-input", "How does a glass prism split white laser light into a full rainbow spectrum?")
        page.click("#ask-btn")
        page.wait_for_timeout(350)
        assert not page.locator("#custom-question-banner").evaluate("el => el.classList.contains('hidden')")

        browser.close()

    assert console_errors == [], f"Unexpected browser console errors: {console_errors}"
    assert page_errors == [], f"Unexpected page errors: {page_errors}"
