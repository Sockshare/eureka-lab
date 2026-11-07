"""Real-Math Simulation Evaluator, Live Formula Substitution & Custom Question Mapper for all 16 Unique Concepts."""

from __future__ import annotations

import math
import re
from typing import Any

from eureka_lab.catalog import FEATURED_QUESTIONS, LABS, LABS_BY_ID, LEGACY_ID_ALIASES


def resolve_lab_id(lab_id: str) -> str:
    if lab_id in LABS_BY_ID:
        return lab_id
    if lab_id in LEGACY_ID_ALIASES:
        return LEGACY_ID_ALIASES[lab_id]
    raise KeyError(f"Unknown lab_id: {lab_id}")


def default_params_for_lab(lab_id: str) -> dict[str, float]:
    cid = resolve_lab_id(lab_id)
    lab = LABS_BY_ID[cid]
    return {p["id"]: float(p["default"]) for p in lab["parameters"]}


def merge_params(lab_id: str, user_params: dict[str, Any] | None = None) -> dict[str, float]:
    cid = resolve_lab_id(lab_id)
    base = default_params_for_lab(cid)
    if not user_params:
        return base
    spec_by_id = {p["id"]: p for p in LABS_BY_ID[cid]["parameters"]}
    for k, v in user_params.items():
        if k in spec_by_id:
            try:
                val = float(v)
                p = spec_by_id[k]
                val = max(float(p["min"]), min(float(p["max"]), val))
                base[k] = val
            except (TypeError, ValueError):
                pass
    return base


def evaluate_lab_math(
    lab_id: str,
    user_params: dict[str, Any] | None = None,
    telemetry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute exact physical quantities, live substituted equation string, and quest completion for all 16 concepts."""
    cid = resolve_lab_id(lab_id)
    lab = LABS_BY_ID[cid]
    p = merge_params(cid, user_params)
    tel = telemetry or {}

    if cid == "orbital-mechanics":
        gm_base = 886.85 * p["star_mass"]
        r0 = max(0.2, p["orbital_radius"])
        v0 = p["launch_speed"]
        v_circ = math.sqrt(gm_base / r0)
        v_esc = math.sqrt(2.0 * gm_base / r0)
        ratio = (r0 * (v0**2)) / gm_base
        ecc = abs(ratio - 1.0)
        if tel.get("canvas_eccentricity") is not None:
            try:
                ecc = min(ecc, float(tel["canvas_eccentricity"]))
            except (TypeError, ValueError):
                pass
        if ratio < 1.99:
            semi_major_a = 1.0 / max(0.02, (2.0 / r0 - (v0**2) / gm_base))
            period_yr = math.sqrt((abs(semi_major_a) ** 3) / max(0.1, p["star_mass"]))
            regime = "Circular Kepler Orbit" if ecc < 0.05 else "Bound Elliptical Orbit"
        else:
            semi_major_a = -1.0 / max(0.02, ((v0**2) / gm_base - 2.0 / r0))
            period_yr = float("inf")
            regime = "Hyperbolic Escape (v₀ ≥ v_esc)"

        live_sub = (
            f"v_circ = √(G·{p['star_mass']:.2f}M☉ / {r0:.2f}AU) = {v_circ:.1f} km/s   |   "
            f"e = |({r0:.2f} · {v0:.1f}²) / (886.9 · {p['star_mass']:.2f}) − 1| = {ecc:.3f}"
        )
        quest_solved = ecc < 0.05
        quest_progress = max(0.0, min(100.0, (1.0 - max(0.0, ecc - 0.04) / 0.45) * 100.0))
        metrics = [
            {"label": "Eccentricity (e)", "value": f"{ecc:.3f}", "unit": "", "status": "good" if ecc < 0.05 else "info"},
            {"label": "Circular Speed (v_c)", "value": f"{v_circ:.1f}", "unit": "km/s", "status": "info"},
            {"label": "Escape Speed (v_esc)", "value": f"{v_esc:.1f}", "unit": "km/s", "status": "warn" if v0 >= v_esc else "info"},
            {"label": "Orbital Period (T)", "value": "∞ (Escape)" if math.isinf(period_yr) else f"{period_yr:.2f}", "unit": "yr", "status": "info"},
            {"label": "Regime", "value": regime, "unit": "", "status": "good" if ecc < 0.05 else "info"},
        ]

    elif cid == "airfoil-wind-tunnel":
        alpha_deg = p["angle_of_attack"]
        alpha_rad = math.radians(alpha_deg)
        u_inf = p["wind_speed"]
        rho = p["air_density"]
        rpm = p["spin_rpm"]
        camber_frac = p["camber"] / 100.0
        q_dyn = 0.5 * rho * (u_inf**2)

        cl_attached = 2.0 * math.pi * (alpha_rad + 2.0 * camber_frac)
        cl_magnus = 0.28 * (rpm / 2000.0)
        stalled = alpha_deg >= 16.0 or alpha_deg <= -14.0
        if not stalled:
            cl = cl_attached + cl_magnus
            cd = 0.018 + (cl**2) / (math.pi * 7.2 * 0.85) + 0.015 * abs(rpm / 2000.0)
            flow_regime = "Attached Laminar / Vortex Lift"
        else:
            stall_excess = abs(alpha_deg) - 15.0
            cl = (0.85 * math.copysign(1.0, alpha_deg) * max(0.25, 1.0 - 0.055 * stall_excess)) + cl_magnus
            cd = 0.08 + 1.15 * (math.sin(alpha_rad) ** 2) + 0.02 * abs(rpm / 2000.0)
            flow_regime = "POST-STALL FLOW SEPARATION"

        wing_area = 1.5
        lift_n = q_dyn * wing_area * cl
        drag_n = q_dyn * wing_area * cd
        l_over_d = cl / max(0.005, cd)

        live_sub = (
            f"q = ½·({rho:.3f})·({u_inf:.0f})² = {q_dyn:.0f} Pa   |   "
            f"C_L(α={alpha_deg:.1f}°, Ω={rpm:.0f}) = {cl:.2f}   ⇒   L = {lift_n:.0f} N, D = {drag_n:.0f} N"
        )
        quest_solved = bool(alpha_deg >= 16.0 or abs(cl) >= 1.35)
        quest_progress = max(
            min(100.0, (alpha_deg / 16.0) * 100.0),
            min(100.0, (abs(cl) / 1.35) * 100.0),
        )
        metrics = [
            {"label": "Lift Coeff (C_L)", "value": f"{cl:.2f}", "unit": "", "status": "good" if abs(cl) >= 1.35 else "info"},
            {"label": "Drag Coeff (C_D)", "value": f"{cd:.3f}", "unit": "", "status": "warn" if stalled else "info"},
            {"label": "Lift / Drag (L/D)", "value": f"{l_over_d:.1f}", "unit": "×", "status": "good" if l_over_d > 12 else "info"},
            {"label": "Lift Force (L)", "value": f"{lift_n:.0f}", "unit": "N", "status": "info"},
            {"label": "Boundary Layer", "value": flow_regime, "unit": "", "status": "warn" if stalled else "good"},
        ]

    elif cid == "double-pendulum-chaos":
        th1 = p["initial_angle_1"]
        th2 = p["initial_angle_2"]
        m_ratio = p["mass_ratio"]
        g = p["gravity_g"]
        d_theta = p["delta_theta_deg"]

        e_norm = ((1.0 - math.cos(math.radians(th1))) + m_ratio * (1.0 - math.cos(math.radians(th2)))) / (2.0 * (1.0 + m_ratio))
        omega_0 = math.sqrt(g / 1.0)
        if e_norm < 0.22:
            lyapunov = 0.08 * omega_0 * (e_norm / 0.22)
            regime = "Quasi-Periodic KAM Torus"
        else:
            lyapunov = (0.18 + 2.35 * ((e_norm - 0.22) / 0.78) ** 1.25) * (omega_0 / 3.13)
            regime = "Deterministic Chaos (Butterfly Regime)"

        t_horizon = math.log(45.0 / max(1e-5, d_theta)) / max(0.05, lyapunov)

        live_sub = (
            f"E/E_max = {e_norm * 100:.1f}%   |   λ ≈ {lyapunov:.2f} s⁻¹   |   "
            f"|Δθ(t)| ≈ {d_theta:.3f}° · exp({lyapunov:.2f}·t)   ⇒   T_horizon ≈ {t_horizon:.1f} s"
        )
        quest_solved = lyapunov >= 1.5 or bool(tel.get("divergence_deg", 0) >= 45.0)
        quest_progress = max(0.0, min(100.0, (lyapunov / 1.5) * 100.0))
        metrics = [
            {"label": "Lyapunov Exp (λ)", "value": f"{lyapunov:.2f}", "unit": "s⁻¹", "status": "good" if lyapunov >= 1.5 else "info"},
            {"label": "Predictability Horizon", "value": f"{t_horizon:.1f}", "unit": "s", "status": "info"},
            {"label": "Potential Energy", "value": f"{e_norm * 100:.1f}", "unit": "% max", "status": "info"},
            {"label": "Initial Δθ₀", "value": f"{d_theta:.3f}", "unit": "°", "status": "info"},
            {"label": "Phase Regime", "value": regime, "unit": "", "status": "good" if lyapunov >= 1.5 else "info"},
        ]

    elif cid == "geometric-optics":
        theta_i = p["beam_angle"]
        d_power = p["lens_power"]
        n0 = p["refractive_index"]
        b_cauchy = p["cauchy_dispersion"]  # in 10^4 nm^2
        apex_deg = p["prism_apex"]

        # Cauchy index at red (700 nm) and violet (400 nm)
        n_red = n0 + (b_cauchy * 1e4) / (700.0**2)
        n_violet = n0 + (b_cauchy * 1e4) / (400.0**2)
        dn = n_violet - n_red

        # Prism deviation approximation + exact thin-prism / minimum deviation scaling
        apex_rad = math.radians(apex_deg)
        sin_half_r = min(0.99, n_red * math.sin(apex_rad * 0.5))
        sin_half_v = min(0.99, n_violet * math.sin(apex_rad * 0.5))
        dev_red_deg = math.degrees(2.0 * math.asin(sin_half_r) - apex_rad)
        dev_violet_deg = math.degrees(2.0 * math.asin(sin_half_v) - apex_rad)
        angular_spread_deg = max(0.1, dev_violet_deg - dev_red_deg)
        focal_cm = 100.0 / d_power if abs(d_power) > 0.05 else float("inf")
        crit_angle_deg = math.degrees(math.asin(1.0 / n0))

        live_sub = (
            f"n(400nm) = {n_violet:.3f}, n(700nm) = {n_red:.3f} (Δn = {dn:.3f})   |   "
            f"δ_V − δ_R = {dev_violet_deg:.1f}° − {dev_red_deg:.1f}° = {angular_spread_deg:.2f}°"
        )
        quest_solved = angular_spread_deg >= 5.0
        quest_progress = max(0.0, min(100.0, (angular_spread_deg / 5.0) * 100.0))
        metrics = [
            {"label": "Spectral Spread (Δδ)", "value": f"{angular_spread_deg:.2f}", "unit": "°", "status": "good" if angular_spread_deg >= 5.0 else "info"},
            {"label": "Violet Index (n_V)", "value": f"{n_violet:.3f}", "unit": "", "status": "info"},
            {"label": "Red Index (n_R)", "value": f"{n_red:.3f}", "unit": "", "status": "info"},
            {"label": "Focal Length (f)", "value": "∞" if math.isinf(focal_cm) else f"{focal_cm:+.1f}", "unit": "cm", "status": "info"},
            {"label": "Critical Angle (θ_c)", "value": f"{crit_angle_deg:.1f}", "unit": "°", "status": "info"},
        ]

    elif cid == "electromagnetic-fields":
        q1 = p["charge_q1"]
        q2 = p["charge_q2"]
        bz = p["magnetic_b"]
        sep_cm = p["dipole_sep"]
        v0_kms = p["beam_energy"]

        # Midpoint electric field (kV/m scaled) & dipole moment
        r_half_m = max(0.01, (sep_cm * 0.01) * 0.5)
        k_e = 8.988e3  # scaled for μC -> kV/m
        e_mid = k_e * abs(q1 - q2) / (r_half_m**2) * 1e-3  # MV/m
        dipole_p = abs(q1 - q2) * 0.5 * sep_cm  # μC·cm

        # Effective Larmor cyclotron radius in cm for test ion
        if abs(bz) > 0.04:
            r_larmor_cm = (v0_kms * 0.22) / abs(bz)
            f_cyc_mhz = 15.2 * abs(bz)
            regime = "Tight Cyclotron Confinement" if r_larmor_cm <= 4.5 else "Magnetized Gyromotion"
        else:
            r_larmor_cm = 99.9
            f_cyc_mhz = 0.0
            regime = "Pure Electrostatic Trajectory"

        live_sub = (
            f"|E_mid| = {e_mid:.2f} MV/m   |   B_z = {bz:+.2f} T, v₀ = {v0_kms:.0f} km/s   ⇒   "
            f"Larmor Radius r_L = m·v₀/(|q·B|) = {r_larmor_cm:.2f} cm"
        )
        quest_solved = r_larmor_cm <= 4.5
        quest_progress = max(0.0, min(100.0, (4.5 / max(2.5, r_larmor_cm)) * 100.0)) if r_larmor_cm > 4.5 else 100.0
        metrics = [
            {"label": "Larmor Radius (r_L)", "value": f"{r_larmor_cm:.2f}", "unit": "cm", "status": "good" if r_larmor_cm <= 4.5 else "info"},
            {"label": "Cyclotron Freq (f_c)", "value": f"{f_cyc_mhz:.1f}", "unit": "MHz", "status": "info"},
            {"label": "Midpoint Field |E|", "value": f"{e_mid:.2f}", "unit": "MV/m", "status": "info"},
            {"label": "Dipole Moment (p)", "value": f"{dipole_p:.1f}", "unit": "μC·cm", "status": "info"},
            {"label": "Lorentz Regime", "value": regime, "unit": "", "status": "good" if r_larmor_cm <= 4.5 else "info"},
        ]

    elif cid == "quantum-tunneling":
        e_ev = p["packet_energy"]
        v0_ev = p["barrier_height"]
        a_nm = p["barrier_width"]
        sigma_nm = p["packet_sigma"]
        m_eff = p["effective_mass"]

        # Exact quantum rectangular barrier transmission coefficient
        # 2*m_e / hbar^2 ≈ 26.25 eV^-1 nm^-2
        c_factor = 26.25 * m_eff
        if abs(e_ev - v0_ev) < 1e-3:
            trans = 1.0 / (1.0 + 0.25 * c_factor * v0_ev * (a_nm**2))
            regime = "Critical Barrier Grazing (E ≈ V₀)"
        elif e_ev < v0_ev:
            kappa = math.sqrt(c_factor * (v0_ev - e_ev))
            ka = min(18.0, kappa * a_nm)
            denom = 1.0 + (v0_ev**2 * (math.sinh(ka) ** 2)) / max(1e-4, 4.0 * e_ev * (v0_ev - e_ev))
            trans = 1.0 / denom
            regime = "Quantum Evanescent Tunneling (E < V₀)"
        else:
            k2 = math.sqrt(c_factor * (e_ev - v0_ev))
            denom = 1.0 + (v0_ev**2 * (math.sin(k2 * a_nm) ** 2)) / max(1e-4, 4.0 * e_ev * (e_ev - v0_ev))
            trans = 1.0 / denom
            regime = "Over-Barrier Ramsauer Scattering (E > V₀)"

        if tel.get("canvas_transmission") is not None:
            try:
                trans = max(trans, float(tel["canvas_transmission"]))
            except (TypeError, ValueError):
                pass

        trans_pct = trans * 100.0
        refl_pct = 100.0 - trans_pct
        lambda_db_nm = 1.226 / math.sqrt(max(0.1, e_ev * m_eff))

        live_sub = (
            f"E = {e_ev:.1f} eV, V₀ = {v0_ev:.1f} eV, a = {a_nm:.2f} nm   |   "
            f"λ_dB = {lambda_db_nm:.2f} nm   ⇒   Transmission T = {trans_pct:.1f}%, Reflection R = {refl_pct:.1f}%"
        )
        quest_solved = trans_pct >= 20.0
        quest_progress = max(0.0, min(100.0, (trans_pct / 20.0) * 100.0))
        metrics = [
            {"label": "Transmission (T)", "value": f"{trans_pct:.1f}", "unit": "%", "status": "good" if trans_pct >= 20.0 else "info"},
            {"label": "Reflection (R)", "value": f"{refl_pct:.1f}", "unit": "%", "status": "info"},
            {"label": "de Broglie (λ_dB)", "value": f"{lambda_db_nm:.2f}", "unit": "nm", "status": "info"},
            {"label": "Unitarity (T+R)", "value": "100.0", "unit": "%", "status": "good"},
            {"label": "Scattering Mode", "value": regime, "unit": "", "status": "good" if trans_pct >= 20.0 else "info"},
        ]

    elif cid == "thermodynamics-gas":
        temp_k = p["temperature_k"]
        vol_pct = p["piston_volume"]
        n_part = int(p["particle_count"])
        m_mol = p["molecular_mass"]
        gamma = p["adiabatic_gamma"]

        r_gas = 8.3145  # J/(mol*K)
        m_kg = m_mol * 1e-3
        v_rms = math.sqrt(3.0 * r_gas * temp_k / m_kg)
        v_mp = math.sqrt(2.0 * r_gas * temp_k / m_kg)
        # Pressure in atm scaled to STP reference (N=160, T=300 K, V=80% -> 1.00 atm)
        pressure_atm = (n_part / 160.0) * (temp_k / 300.0) / (vol_pct / 80.0)
        internal_u_kj = 1.5 * (n_part / 100.0) * (temp_k / 300.0) / max(0.2, gamma - 1.0)

        live_sub = (
            f"P = N·k_B·T / V = ({n_part}/160)·({temp_k:.0f}K/300K)/({vol_pct:.0f}%/80%) = {pressure_atm:.2f} atm   |   "
            f"v_rms = √(3RT/M) = {v_rms:.0f} m/s"
        )
        quest_solved = pressure_atm >= 3.50
        quest_progress = max(0.0, min(100.0, (pressure_atm / 3.50) * 100.0))
        metrics = [
            {"label": "Chamber Pressure (P)", "value": f"{pressure_atm:.2f}", "unit": "atm", "status": "good" if pressure_atm >= 3.50 else "info"},
            {"label": "RMS Speed (v_rms)", "value": f"{v_rms:.0f}", "unit": "m/s", "status": "info"},
            {"label": "Peak Speed (v_mp)", "value": f"{v_mp:.0f}", "unit": "m/s", "status": "info"},
            {"label": "Internal Energy (U)", "value": f"{internal_u_kj:.2f}", "unit": "kJ", "status": "info"},
            {"label": "Gas State", "value": "High-Pressure Compressed" if pressure_atm >= 3.50 else "Sub-Critical Thermal Gas", "unit": "", "status": "good" if pressure_atm >= 3.50 else "info"},
        ]

    elif cid == "fluid-vortex-tunnel":
        re_num = p["reynolds_number"]
        u0 = p["inflow_velocity"]
        diam_cm = p["obstacle_diameter"]
        vort_conf = p["vorticity_confinement"]

        diam_m = diam_cm * 0.01
        if re_num < 47.0:
            strouhal = 0.0
            f_shed = 0.0
            wake_state = "Attached Symmetric Twin-Eddy (Re < 47)"
        else:
            strouhal = 0.198 * (1.0 - 19.7 / re_num)
            f_shed = strouhal * u0 / max(0.01, diam_m)
            wake_state = "Kármán Vortex Street Shedding" if re_num < 350 else "Turbulent Vortex Wake Cascade"

        peak_vort = (u0 / diam_m) * (0.45 + 0.18 * vort_conf) * math.sqrt(re_num / 100.0)

        live_sub = (
            f"Re = {re_num:.0f}   |   St = 0.198·(1 − 19.7/{re_num:.0f}) = {strouhal:.3f}   ⇒   "
            f"f_shed = St·U₀/D = {strouhal:.3f}·{u0:.1f}/{diam_m:.2f}m = {f_shed:.2f} Hz"
        )
        quest_solved = bool(re_num >= 150.0 and f_shed >= 6.0)
        quest_progress = min(100.0, 0.5 * min(100.0, (re_num / 150.0) * 100.0) + 0.5 * min(100.0, (f_shed / 6.0) * 100.0))
        metrics = [
            {"label": "Shedding Freq (f_s)", "value": f"{f_shed:.2f}", "unit": "Hz", "status": "good" if f_shed >= 6.0 else "info"},
            {"label": "Strouhal Number (St)", "value": f"{strouhal:.3f}", "unit": "", "status": "info"},
            {"label": "Reynolds Number (Re)", "value": f"{re_num:.0f}", "unit": "", "status": "good" if re_num >= 150 else "info"},
            {"label": "Peak Curl |∇×u|", "value": f"{peak_vort:.1f}", "unit": "s⁻¹", "status": "info"},
            {"label": "Wake Topology", "value": wake_state, "unit": "", "status": "good" if quest_solved else "info"},
        ]

    elif cid == "wave-interference":
        f0 = p["frequency_hz"]
        sep_lambda = p["source_separation"]
        mach = p["source_velocity"]
        harmonics = int(p["harmonics_count"])

        c_sound = 343.0
        wavelength_m = c_sound / f0
        if mach < 0.98:
            f_front = f0 / (1.0 - mach)
            mach_cone_str = "Subsonic (No Shock Cone)"
        else:
            f_front = f0 * 12.0
            cone_deg = math.degrees(math.asin(1.0 / max(1.0, mach)))
            mach_cone_str = f"Mach Cone θ_M = {cone_deg:.1f}°"
        f_back = f0 / (1.0 + mach)
        antinodes = int(2 * math.floor(sep_lambda) + 1) if sep_lambda > 0 else 1

        live_sub = (
            f"λ = c/f₀ = 343/{f0:.0f} = {wavelength_m:.2f} m   |   "
            f"f_front = {f0:.0f}/|1 − {mach:.2f}| = {f_front:.0f} Hz,  f_back = {f_back:.0f} Hz   |   K = {harmonics} modes"
        )
        quest_solved = bool(mach >= 0.85 or harmonics >= 4)
        quest_progress = max(min(100.0, (mach / 0.85) * 100.0), min(100.0, (harmonics / 4.0) * 100.0))
        metrics = [
            {"label": "Forward Pitch (f_+)", "value": f"{f_front:.0f}", "unit": "Hz", "status": "good" if mach >= 0.85 else "info"},
            {"label": "Rearward Pitch (f_−)", "value": f"{f_back:.0f}", "unit": "Hz", "status": "info"},
            {"label": "Wavelength (λ)", "value": f"{wavelength_m:.2f}", "unit": "m", "status": "info"},
            {"label": "Constructive Maxima", "value": f"{antinodes}", "unit": "fringes", "status": "info"},
            {"label": "Wavefront Regime", "value": mach_cone_str, "unit": "", "status": "good" if mach >= 0.85 else "info"},
        ]

    elif cid == "structural-truss":
        load_kn = p["vehicle_load"]
        e_gpa = p["youngs_modulus"]
        height_m = p["truss_depth"]
        area_cm2 = p["beam_area"]
        seismic_g = p["seismic_amp"]

        span_m = 36.0
        # Mid-span bending moment M = F * L / 4 amplified by dynamic seismic factor
        dyn_factor = 1.0 + 2.2 * seismic_g
        chord_force_kn = (load_kn * span_m / (4.0 * max(1.0, height_m))) * dyn_factor
        # Axial stress in MPa: 1 kN / cm^2 = 10 MPa
        max_stress_mpa = (chord_force_kn / max(5.0, area_cm2)) * 10.0
        yield_strength_mpa = 250.0 * (e_gpa / 200.0) ** 0.35
        safety_factor = yield_strength_mpa / max(1.0, max_stress_mpa)
        deflection_mm = (load_kn * (span_m**3) * dyn_factor) / (48.0 * e_gpa * (height_m**2) * area_cm2) * 18.0
        buckled = safety_factor < 1.0

        live_sub = (
            f"F_chord = ({load_kn:.0f}kN · 36m)/(4 · {height_m:.1f}m) = {chord_force_kn:.0f} kN   |   "
            f"σ_max = {max_stress_mpa:.1f} MPa   ⇒   Safety Factor SF = {safety_factor:.2f}"
        )
        quest_solved = safety_factor >= 2.40
        quest_progress = max(0.0, min(100.0, (safety_factor / 2.40) * 100.0))
        metrics = [
            {"label": "Safety Factor (SF)", "value": f"{safety_factor:.2f}", "unit": "×", "status": "good" if safety_factor >= 2.40 else ("warn" if buckled else "info")},
            {"label": "Peak Axial Stress", "value": f"{max_stress_mpa:.1f}", "unit": "MPa", "status": "warn" if buckled else "info"},
            {"label": "Midspan Deflection", "value": f"{deflection_mm:.1f}", "unit": "mm", "status": "info"},
            {"label": "Chord Force (F_c)", "value": f"{chord_force_kn:.0f}", "unit": "kN", "status": "info"},
            {"label": "Structural Integrity", "value": "BUCKLING FAILURE (SF < 1)" if buckled else ("AASHTO Certified" if safety_factor >= 2.40 else "Elastic Load Bearing"), "unit": "", "status": "warn" if buckled else ("good" if safety_factor >= 2.40 else "info")},
        ]

    elif cid == "rlc-circuit-resonance":
        freq = p["drive_freq_hz"]
        r_ohm = p["resistance_ohm"]
        l_mh = p["inductance_mh"]
        c_uf = p["capacitance_uf"]
        v0 = p["source_voltage"]

        l_h = l_mh * 1e-3
        c_f = c_uf * 1e-6
        omega = 2.0 * math.pi * freq
        f0_res = 1.0 / (2.0 * math.pi * math.sqrt(l_h * c_f))
        xl = omega * l_h
        xc = 1.0 / max(1e-6, omega * c_f)
        z_mag = math.sqrt(r_ohm**2 + (xl - xc) ** 2)
        i_peak = v0 / z_mag
        phase_deg = math.degrees(math.atan2(xl - xc, r_ohm))
        q_factor = (1.0 / r_ohm) * math.sqrt(l_h / c_f)

        live_sub = (
            f"X_L = {xl:.1f} Ω, X_C = {xc:.1f} Ω, |Z| = {z_mag:.1f} Ω   |   "
            f"f₀ = {f0_res:.1f} Hz   ⇒   I₀ = {i_peak:.2f} A, φ = {phase_deg:+.1f}°, Q = {q_factor:.2f}"
        )
        quest_solved = bool(abs(phase_deg) <= 8.0 and q_factor >= 2.5)
        phase_score = max(0.0, min(100.0, (1.0 - max(0.0, abs(phase_deg) - 6.0) / 60.0) * 100.0))
        q_score = min(100.0, (q_factor / 2.5) * 100.0)
        quest_progress = 0.6 * phase_score + 0.4 * q_score
        metrics = [
            {"label": "Phase Angle (φ)", "value": f"{phase_deg:+.1f}", "unit": "°", "status": "good" if abs(phase_deg) <= 8.0 else "info"},
            {"label": "Impedance |Z|", "value": f"{z_mag:.1f}", "unit": "Ω", "status": "info"},
            {"label": "Peak Current (I₀)", "value": f"{i_peak:.2f}", "unit": "A", "status": "good" if abs(phase_deg) <= 8.0 else "info"},
            {"label": "Resonant Freq (f₀)", "value": f"{f0_res:.1f}", "unit": "Hz", "status": "info"},
            {"label": "Quality Factor (Q)", "value": f"{q_factor:.2f}", "unit": "", "status": "good" if q_factor >= 2.5 else "info"},
        ]

    elif cid == "relativistic-lensing":
        m_bh = p["bh_mass"]
        b_ratio = p["impact_param"]
        rs_km = 2.953 * m_bh  # Schwarzschild radius in km
        b_crit = 1.5 * math.sqrt(3.0)  # ~2.598 r_s

        if b_ratio <= b_crit:
            defl_deg = 360.0
            captured = True
            grav_z = float("inf")
            regime = "EVENT HORIZON CAPTURE (b ≤ 2.60 r_s)"
        else:
            captured = False
            # Strong-field Darwin logarithmic divergence near b_crit + weak-field 2*r_s/b
            weak_rad = 2.0 / b_ratio
            strong_boost = 0.85 * math.log(max(1.005, (b_ratio + b_crit) / (b_ratio - b_crit)))
            defl_deg = min(340.0, math.degrees(weak_rad + strong_boost * (b_crit / b_ratio) ** 2))
            r_closest = max(1.51, b_ratio * 0.88)
            grav_z = 1.0 / math.sqrt(max(0.02, 1.0 - 1.0 / r_closest)) - 1.0
            regime = "Strong-Field Photon Sphere Skim" if defl_deg >= 45.0 else "Weak-Field Einstein Lensing"

        live_sub = (
            f"r_s = 2GM/c² = {rs_km:.1f} km   |   r_ph = 1.5·r_s = {1.5 * rs_km:.1f} km   |   "
            f"b = {b_ratio:.2f}·r_s   ⇒   Deflection Δφ = {'CAPTURED' if captured else f'{defl_deg:.1f}°'}"
        )
        quest_solved = bool(not captured and defl_deg >= 45.0)
        quest_progress = 100.0 if quest_solved else (35.0 if captured else max(0.0, min(100.0, (defl_deg / 45.0) * 100.0)))
        metrics = [
            {"label": "Deflection (Δφ)", "value": "Captured" if captured else f"{defl_deg:.1f}", "unit": "" if captured else "°", "status": "good" if quest_solved else ("warn" if captured else "info")},
            {"label": "Horizon Radius (r_s)", "value": f"{rs_km:.1f}", "unit": "km", "status": "info"},
            {"label": "Photon Sphere (r_ph)", "value": f"{1.5 * rs_km:.1f}", "unit": "km", "status": "info"},
            {"label": "Redshift (z_grav)", "value": "∞" if captured else f"{grav_z:.3f}", "unit": "", "status": "info"},
            {"label": "Geodesic Fate", "value": regime, "unit": "", "status": "good" if quest_solved else ("warn" if captured else "info")},
        ]

    elif cid == "fourier-epicycles":
        m_circles = int(p["epicycle_count"])
        shape_id = int(p["shape_preset"])
        speed = p["cycle_speed"]
        hf_boost = p["harmonic_filter"]

        shape_names = {1: "Starship Rocket", 2: "Cardioid Heart", 3: "8-Point Starburst", 4: "Square Step Box"}
        # Parseval energy fraction captured by top M complex harmonics
        decay_rate = {1: 0.115, 2: 0.16, 3: 0.095, 4: 0.088}.get(shape_id, 0.11)
        fidelity_pct = min(99.8, 100.0 * (1.0 - math.exp(-decay_rate * m_circles - 0.18)))
        rms_err_px = max(0.4, 42.0 * math.exp(-0.085 * m_circles))
        compression_ratio = 128.0 / max(1, m_circles)

        live_sub = (
            f"z_M(t) = ∑_{{k=1}}^{{{m_circles}}} c_k · e^(i·ω_k·t)   |   "
            f"Parseval Energy E_M/E_tot = {fidelity_pct:.2f}%   |   RMS Error = {rms_err_px:.1f} px"
        )
        quest_solved = fidelity_pct >= 96.5
        quest_progress = max(0.0, min(100.0, ((fidelity_pct - 40.0) / (96.5 - 40.0)) * 100.0))
        metrics = [
            {"label": "Parseval Fidelity", "value": f"{fidelity_pct:.2f}", "unit": "%", "status": "good" if fidelity_pct >= 96.5 else "info"},
            {"label": "Active Epicycles (M)", "value": f"{m_circles}", "unit": "phasors", "status": "info"},
            {"label": "Contour RMS Error", "value": f"{rms_err_px:.1f}", "unit": "px", "status": "good" if rms_err_px < 4.0 else "info"},
            {"label": "DFT Compression", "value": f"{compression_ratio:.1f}", "unit": ": 1", "status": "info"},
            {"label": "Target Manifold", "value": shape_names.get(shape_id, "Starship"), "unit": "", "status": "info"},
        ]

    elif cid == "ant-colony-swarm":
        n_ants = int(p["ant_count"])
        evap = p["evaporation_rate"]
        alpha_p = p["pheromone_strength"]
        noise = p["exploration_noise"]
        obs = int(p["obstacle_preset"])

        signal_to_noise = (alpha_p * math.sqrt(n_ants / 100.0)) / (0.6 + 1.8 * noise + 0.04 * abs(evap - 4.0))
        obstacle_penalty = 1.0 - 0.06 * obs
        computed_eff = max(12.0, min(96.0, 100.0 * (1.0 - math.exp(-0.52 * signal_to_noise)) * obstacle_penalty))
        if tel.get("canvas_efficiency") is not None:
            try:
                computed_eff = max(computed_eff, float(tel["canvas_efficiency"]))
            except (TypeError, ValueError):
                pass
        flux_rate = (n_ants * (computed_eff / 100.0)) / (2.2 + 0.35 * obs)

        live_sub = (
            f"P_short = τ_s^{alpha_p:.2f} / (τ_s^{alpha_p:.2f} + τ_l^{alpha_p:.2f})   |   "
            f"N={n_ants}, ρ={evap:.1f}%/s, ε={noise:.2f} rad   ⇒   Efficiency η = {computed_eff:.1f}%"
        )
        quest_solved = computed_eff >= 65.0
        quest_progress = max(0.0, min(100.0, (computed_eff / 65.0) * 100.0))
        metrics = [
            {"label": "Trail Efficiency (η)", "value": f"{computed_eff:.1f}", "unit": "%", "status": "good" if computed_eff >= 65.0 else "info"},
            {"label": "Harvest Flux (J)", "value": f"{flux_rate:.1f}", "unit": "food/min", "status": "info"},
            {"label": "Pheromone Gain (α_p)", "value": f"{alpha_p:.2f}", "unit": "×", "status": "info"},
            {"label": "Half-Life (t_½)", "value": f"{math.log(2) / max(0.005, evap / 100.0):.1f}", "unit": "s", "status": "info"},
            {"label": "Colony State", "value": "Shortest-Path Highway Locked" if computed_eff >= 65.0 else "Foraging / Exploring", "unit": "", "status": "good" if computed_eff >= 65.0 else "info"},
        ]

    elif cid == "epidemic-seir":
        beta = p["transmission_prob"]
        gamma = p["recovery_rate"]
        vacc = p["vaccination_rate"] / 100.0
        dist = p["social_distancing"] / 100.0

        r0 = beta / max(0.01, gamma)
        r_t = r0 * (1.0 - dist) * (1.0 - vacc)
        if tel.get("canvas_rt") is not None:
            try:
                r_t = min(r_t, float(tel["canvas_rt"]))
            except (TypeError, ValueError):
                pass
        herd_thresh_pct = max(0.0, (1.0 - 1.0 / max(1.0, r0)) * 100.0)
        if r_t > 1.0:
            s_eff = 1.0 - vacc
            i_peak_pct = max(1.0, min(92.0, (s_eff - (1.0 + math.log(r_t)) / r0) * 100.0))
            epidemic_state = "Exponential Growth (R_t > 1)"
        else:
            i_peak_pct = max(0.5, 3.5 * r_t)
            epidemic_state = "Contained / Herd Immunity (R_t < 1)"

        live_sub = (
            f"R₀ = β/γ = {beta:.2f}/{gamma:.2f} = {r0:.2f}   |   "
            f"R_t = {r0:.2f} · (1 − {dist:.2f}) · (1 − {vacc:.2f}) = {r_t:.2f}"
        )
        quest_solved = r_t < 1.0
        quest_progress = max(0.0, min(100.0, (1.0 / max(0.95, r_t)) * 100.0)) if r_t >= 1.0 else 100.0
        metrics = [
            {"label": "Effective R_t", "value": f"{r_t:.2f}", "unit": "", "status": "good" if r_t < 1.0 else "warn"},
            {"label": "Basic R₀ (β/γ)", "value": f"{r0:.2f}", "unit": "", "status": "info"},
            {"label": "Herd Threshold (v_c)", "value": f"{herd_thresh_pct:.1f}", "unit": "%", "status": "info"},
            {"label": "Peak Infected (I_max)", "value": f"{i_peak_pct:.1f}", "unit": "%", "status": "good" if i_peak_pct < 10 else "warn"},
            {"label": "Outbreak Status", "value": epidemic_state, "unit": "", "status": "good" if r_t < 1.0 else "warn"},
        ]

    elif cid == "neural-backprop":
        h = int(p["hidden_neurons"])
        lr = p["learning_rate"]
        dtype = int(p["dataset_type"])
        act = int(p["activation_fn"])
        reg = p["regularization"]

        dataset_names = {1: "Nonlinear XOR", 2: "Concentric Rings", 3: "Twin Spirals"}
        act_names = {1: "tanh(z)", 2: "ReLU(z)", 3: "Sigmoid(z)"}
        min_neurons_needed = {1: 4, 2: 5, 3: 10}[dtype]
        capacity_ratio = h / float(min_neurons_needed)
        lr_factor = min(1.0, lr / 0.14)
        reg_penalty = max(0.0, (reg - 0.012) * 850.0)
        act_bonus = 3.0 if (dtype == 3 and act == 1) or (dtype == 1 and act == 2) else 0.0

        est_acc = max(52.0, min(99.2, 54.0 + 41.5 * (1.0 - math.exp(-1.35 * capacity_ratio * lr_factor)) + act_bonus - reg_penalty))
        if tel.get("canvas_accuracy") is not None:
            try:
                est_acc = max(est_acc, float(tel["canvas_accuracy"]))
            except (TypeError, ValueError):
                pass
        bce_loss = max(0.025, 0.72 * (1.0 - (est_acc - 50.0) / 51.0))
        param_count = 2 * h + h + h + 1

        live_sub = (
            f"Params |Θ| = 2·{h} + {h} + {h} + 1 = {param_count} weights   |   "
            f"σ={act_names.get(act, 'tanh')}, η={lr:.2f}, λ={reg:.3f}   ⇒   Loss L_BCE = {bce_loss:.3f}, Acc = {est_acc:.1f}%"
        )
        quest_solved = est_acc >= 92.0
        quest_progress = max(0.0, min(100.0, (est_acc / 92.0) * 100.0))
        metrics = [
            {"label": "Classification Acc", "value": f"{est_acc:.1f}", "unit": "%", "status": "good" if est_acc >= 92.0 else "info"},
            {"label": "Cross-Entropy Loss", "value": f"{bce_loss:.3f}", "unit": "nats", "status": "good" if bce_loss < 0.18 else "info"},
            {"label": "Trainable Weights", "value": f"{param_count}", "unit": "params", "status": "info"},
            {"label": "Dataset Topology", "value": dataset_names.get(dtype, "Rings"), "unit": "", "status": "info"},
            {"label": "Capacity Status", "value": "Universal Fit (≥92%)" if est_acc >= 92.0 else "Training / Underfit", "unit": "", "status": "good" if est_acc >= 92.0 else "warn"},
        ]

    return {
        "lab_id": cid,
        "engine_id": lab["engine_id"],
        "params": p,
        "formula_name": lab["formula"]["name"],
        "formula_symbolic": lab["formula"]["symbolic"],
        "live_substitution": live_sub,
        "metrics": metrics,
        "quest": {
            **lab["quest"],
            "solved": quest_solved,
            "progress_pct": round(quest_progress, 1),
        },
    }


def _score_lab_for_question(q_lower: str, lab: dict[str, Any]) -> float:
    score = 0.0
    for kw in lab["keywords"]:
        if kw in q_lower:
            score += 3.5 if " " in kw else 2.2
    words = set(re.findall(r"[a-z0-9_]+", q_lower))
    title_words = set(re.findall(r"[a-z0-9_]+", (lab["title"] + " " + lab["category"]).lower()))
    score += 1.5 * len(words & title_words)
    return score


def _tune_params_for_question(lab_id: str, q_lower: str) -> tuple[dict[str, float], str]:
    """Select smart initial parameters and a scenario label tailored to the user's question."""
    cid = resolve_lab_id(lab_id)
    p = default_params_for_lab(cid)
    scenario_label = "Interactive Custom Scenario"

    # Check if question matches a featured question for this lab first
    for fq in FEATURED_QUESTIONS:
        if fq["lab_id"] == cid and fq["question"].lower() == q_lower:
            p.update(fq["recommended_params"])
            return p, f"{LABS_BY_ID[cid]['short_title']} Featured Scenario"

    if cid == "orbital-mechanics":
        if any(w in q_lower for w in ("slingshot", "jupiter", "voyager", "assist", "comet")):
            p.update({"star_mass": 1.1, "launch_speed": 39.5, "orbital_radius": 0.75, "jupiter_mass": 4.5, "time_warp": 1.5})
            scenario_label = "Gravity-Assist Slingshot Trajectory"
        elif any(w in q_lower for w in ("escape", "leave", "hyperbolic", "fast")):
            p.update({"star_mass": 1.0, "launch_speed": 45.0, "orbital_radius": 1.0, "jupiter_mass": 1.0, "time_warp": 1.25})
            scenario_label = "Hyperbolic Escape Velocity Regime"
        else:
            p.update({"star_mass": 1.0, "launch_speed": 29.8, "orbital_radius": 1.0, "jupiter_mass": 0.5, "time_warp": 1.25})
            scenario_label = "Circular Keplerian Orbit (e ≈ 0.00)"

    elif cid == "airfoil-wind-tunnel":
        if any(w in q_lower for w in ("curveball", "baseball", "spin", "magnus", "soccer", "tennis")):
            p.update({"angle_of_attack": 2.0, "wind_speed": 42.0, "spin_rpm": 2400.0, "air_density": 1.225, "camber": 0.0})
            scenario_label = "Magnus Effect Spinning Curveball (2400 RPM)"
        elif any(w in q_lower for w in ("stall", "steep", "crash", "separate")):
            p.update({"angle_of_attack": 19.0, "wind_speed": 50.0, "spin_rpm": 0.0, "air_density": 1.225, "camber": 5.0})
            scenario_label = "Critical Post-Stall Boundary Layer Separation (α = 19°)"
        else:
            p.update({"angle_of_attack": 8.0, "wind_speed": 48.0, "spin_rpm": 300.0, "air_density": 1.225, "camber": 4.5})
            scenario_label = "High-Lift Cambered Airfoil Flow"

    elif cid == "double-pendulum-chaos":
        p.update({"initial_angle_1": 138.0, "initial_angle_2": 146.0, "mass_ratio": 1.0, "gravity_g": 9.81, "delta_theta_deg": 0.002})
        scenario_label = "Butterfly Effect 5-Pendulum Divergence (Δθ₀ = 0.002°)"

    elif cid == "geometric-optics":
        p.update({"beam_angle": 8.0, "lens_power": 2.5, "refractive_index": 1.70, "cauchy_dispersion": 2.8, "prism_apex": 60.0})
        scenario_label = "Newtonian Flint Prism Chromatic Dispersion"

    elif cid == "electromagnetic-fields":
        p.update({"charge_q1": 3.0, "charge_q2": -3.0, "magnetic_b": 2.0, "dipole_sep": 12.0, "beam_energy": 36.0})
        scenario_label = "Dipole & Lorentz Cyclotron Confinement"

    elif cid == "quantum-tunneling":
        p.update({"packet_energy": 5.8, "barrier_height": 6.4, "barrier_width": 0.35, "packet_sigma": 0.80, "effective_mass": 0.45})
        scenario_label = "Sub-Barrier Quantum Wavepacket Tunneling"

    elif cid == "thermodynamics-gas":
        p.update({"temperature_k": 780.0, "piston_volume": 42.0, "particle_count": 210, "molecular_mass": 20.0, "adiabatic_gamma": 1.40})
        scenario_label = "Adiabatic Piston Compression & Maxwell-Boltzmann Distribution"

    elif cid == "fluid-vortex-tunnel":
        p.update({"reynolds_number": 240.0, "inflow_velocity": 3.2, "obstacle_diameter": 8.5, "vorticity_confinement": 3.8, "dye_injection": 1.8})
        scenario_label = "Kármán Vortex Street Shedding (Re = 240)"

    elif cid == "wave-interference":
        if any(w in q_lower for w in ("sonic", "boom", "mach", "supersonic", "jet", "doppler", "siren")):
            mach_val = 1.25 if any(w in q_lower for w in ("sonic", "boom", "mach", "supersonic", "jet")) else 0.75
            p.update({"frequency_hz": 300.0, "source_separation": 0.0, "source_velocity": mach_val, "phase_diff": 0.0, "harmonics_count": 4})
            scenario_label = f"Doppler Wavefront Compression (Mach {mach_val:.2f})"
        else:
            p.update({"frequency_hz": 280.0, "source_separation": 3.0, "source_velocity": 0.0, "phase_diff": 0.0, "harmonics_count": 4})
            scenario_label = "Two-Source Young Interference & Harmonic Tank"

    elif cid == "structural-truss":
        p.update({"vehicle_load": 200.0, "youngs_modulus": 240.0, "truss_depth": 10.0, "beam_area": 75.0, "seismic_amp": 0.02})
        scenario_label = "Warren Truss Axial Stress & Buckling Analysis"

    elif cid == "rlc-circuit-resonance":
        p.update({"drive_freq_hz": 159.0, "resistance_ohm": 12.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0})
        scenario_label = "AC Series RLC Resonance Lock (f = f₀)"

    elif cid == "relativistic-lensing":
        p.update({"bh_mass": 12.0, "impact_param": 2.68, "beam_spread": 2.0, "grid_tilt": 42.0, "accretion_spin": 0.75})
        scenario_label = "Schwarzschild Photon Sphere & Einstein Lensing"

    elif cid == "fourier-epicycles":
        p.update({"epicycle_count": 40, "shape_preset": 1, "cycle_speed": 1.0, "trail_persistence": 95.0, "harmonic_filter": 1.0})
        scenario_label = "Complex DFT Epicycle Harmonic Reconstruction"

    elif cid == "ant-colony-swarm":
        p.update({"ant_count": 200, "evaporation_rate": 3.5, "pheromone_strength": 3.8, "exploration_noise": 0.16, "obstacle_preset": 1})
        scenario_label = "Stigmergic Double-Bridge Shortest Path"

    elif cid == "epidemic-seir":
        p.update({"transmission_prob": 0.36, "recovery_rate": 0.18, "vaccination_rate": 66.0, "social_distancing": 30.0, "incubation_days": 3.0})
        scenario_label = "Herd Immunity Containment (R_t < 1.0)"

    elif cid == "neural-backprop":
        p.update({"hidden_neurons": 12, "learning_rate": 0.26, "dataset_type": 2, "activation_fn": 1, "regularization": 0.002})
        scenario_label = "12-Neuron Concentric Ring Manifold"

    return p, scenario_label


def map_and_explain_question(question: str) -> dict[str, Any]:
    """Map any natural-language 'How does X work?' question to one of the 16 unique concepts + 3-tier explanation."""
    q_clean = (question or "").strip()
    if not q_clean:
        q_clean = "How does a glass prism split white laser light into a full rainbow spectrum?"
    q_lower = q_clean.lower()

    # Exact featured question match check first
    best_lab_id = None
    best_score = 0.0
    for fq in FEATURED_QUESTIONS:
        if fq["question"].lower() == q_lower:
            best_lab_id = fq["lab_id"]
            best_score = 15.0
            break

    if not best_lab_id:
        scored = [(lab["id"], _score_lab_for_question(q_lower, lab)) for lab in LABS]
        scored.sort(key=lambda item: item[1], reverse=True)
        best_lab_id, best_score = scored[0]

    if best_score <= 0:
        if any(w in q_lower for w in ("sky", "plane", "wind", "air", "ball")):
            best_lab_id = "airfoil-wind-tunnel"
        elif any(w in q_lower for w in ("space", "sun", "earth", "mars", "rocket")):
            best_lab_id = "orbital-mechanics"
        elif any(w in q_lower for w in ("sick", "cold", "flu", "covid", "spread", "immune")):
            best_lab_id = "epidemic-seir"
        elif any(w in q_lower for w in ("sound", "music", "echo", "hear", "note")):
            best_lab_id = "wave-interference"
        elif any(w in q_lower for w in ("brain", "computer", "chatgpt", "learn", "pattern")):
            best_lab_id = "neural-backprop"
        else:
            best_lab_id = "orbital-mechanics"

    lab = LABS_BY_ID[best_lab_id]
    recommended_params, scenario_label = _tune_params_for_question(best_lab_id, q_lower)
    math_eval = evaluate_lab_math(best_lab_id, recommended_params)

    base_tiers = lab["tiers"]
    custom_tiers = {
        "eli7": {
            "headline": f"7-Year-Old Answer: “{q_clean}”",
            "body": (
                f"**Great question!** Here is the big secret behind *{q_clean}*:\n\n"
                f"{base_tiers['eli7']['body']}\n\n"
                f"✨ **On the canvas right now:** We automatically configured **{lab['title']}** into the "
                f"**{scenario_label}** setup so you can see it happen with your own eyes!"
            ),
            "try_this": base_tiers["eli7"]["try_this"],
        },
        "high_school": {
            "headline": f"High School Physics & Mechanism: “{q_clean}”",
            "body": (
                f"To understand *{q_clean}*, we model the system in the **{lab['title']}** ({scenario_label}):\n\n"
                f"{base_tiers['high_school']['body']}\n\n"
                f"📊 **Live Computed State:** `{math_eval['live_substitution']}`"
            ),
            "try_this": base_tiers["high_school"]["try_this"],
        },
        "engineer": {
            "headline": f"Engineering & Differential Equations: “{q_clean}”",
            "body": (
                f"**Governing Formulation ({lab['formula']['name']}):**\n\n"
                f"{base_tiers['engineer']['body']}\n\n"
                f"🔬 **Real-Time Numerical Evaluation:** `{math_eval['live_substitution']}`"
            ),
            "try_this": base_tiers["engineer"]["try_this"],
        },
    }

    related = [fq["question"] for fq in FEATURED_QUESTIONS if fq["lab_id"] != best_lab_id][:4]

    return {
        "question": q_clean,
        "matched_lab_id": best_lab_id,
        "matched_lab_title": lab["title"],
        "matched_category": lab["category"],
        "scenario_label": scenario_label,
        "confidence": min(0.99, round(0.78 + 0.04 * best_score, 2)),
        "recommended_params": recommended_params,
        "tiers": custom_tiers,
        "math": math_eval,
        "follow_up_questions": related,
    }
