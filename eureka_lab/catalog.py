"""Catalog of the 16 Unique Real-Math Laboratories (Strict 1-to-1 Concept-to-Engine Mapping)."""

from __future__ import annotations

from typing import Any

CATEGORIES: list[str] = [
    "Astrophysics",
    "Fluid & Aero",
    "Quantum & Optics",
    "Electromagnetism & Circuits",
    "Chaos & Math",
    "Complex Systems & AI",
]

LABS: list[dict[str, Any]] = [
    # =========================================================================
    # 1. orbital-mechanics — N-Body Gravitational Dynamics & Slingshot
    # =========================================================================
    {
        "id": "orbital-mechanics",
        "engine_id": "orbital-mechanics",
        "engine_class": "OrbitalMechanicsEngine",
        "number": 1,
        "title": "N-Body Gravitational Dynamics & Slingshot",
        "short_title": "Orbital & Slingshot",
        "category": "Astrophysics",
        "icon": "🪐",
        "accent_color": "#38bdf8",
        "tagline": "Multi-body RK4 / symplectic gravity integrator with glowing stellar corona, Lagrange contours, Roche tidal disruption bursts, and interactive slingshot launch.",
        "keywords": [
            "orbit", "gravity", "satellite", "planet", "comet", "slingshot", "kepler", "newton",
            "lagrange", "escape velocity", "moon", "spacecraft", "ellipse", "trajectory",
            "hohmann", "periapsis", "apoapsis", "solar system", "roche", "voyager",
        ],
        "canvas_hint": "Click & drag anywhere on space canvas to launch a new spacecraft vector; approach the gas giant inside the Roche limit to trigger tidal disruption!",
        "parameters": [
            {
                "id": "star_mass",
                "label": "Central Star Mass (M)",
                "symbol": "M",
                "unit": "M☉",
                "min": 0.4,
                "max": 3.5,
                "step": 0.05,
                "default": 1.0,
                "description": "Mass of the primary star in solar-mass units; scales gravitational parameter μ = G·M.",
            },
            {
                "id": "launch_speed",
                "label": "Injection Velocity (v₀)",
                "symbol": "v₀",
                "unit": "km/s",
                "min": 12.0,
                "max": 60.0,
                "step": 0.5,
                "default": 29.8,
                "description": "Tangential speed of the primary spacecraft at injection radius r₀.",
            },
            {
                "id": "orbital_radius",
                "label": "Injection Radius (r₀)",
                "symbol": "r₀",
                "unit": "AU",
                "min": 0.45,
                "max": 2.2,
                "step": 0.05,
                "default": 1.0,
                "description": "Initial distance from the central star in Astronomical Units (AU).",
            },
            {
                "id": "jupiter_mass",
                "label": "Perturber Giant Mass (m_p)",
                "symbol": "m_p",
                "unit": "M_J",
                "min": 0.0,
                "max": 8.0,
                "step": 0.25,
                "default": 1.5,
                "description": "Mass of the outer gas-giant planet used for gravity-assist slingshots and Lagrange wells.",
            },
            {
                "id": "time_warp",
                "label": "Integrator Time Warp",
                "symbol": "Δt",
                "unit": "×",
                "min": 0.25,
                "max": 4.0,
                "step": 0.25,
                "default": 1.25,
                "description": "Sub-stepped 4th-order Runge-Kutta / symplectic simulation speed multiplier.",
            },
        ],
        "presets": [
            {
                "id": "circular-earth",
                "name": "Circular Kepler Orbit (e ≈ 0.00)",
                "description": "Balanced centripetal and gravitational pull at 1.0 AU (v₀ = 29.8 km/s).",
                "params": {"star_mass": 1.0, "launch_speed": 29.8, "orbital_radius": 1.0, "jupiter_mass": 0.5, "time_warp": 1.25},
            },
            {
                "id": "hohmann-transfer",
                "name": "Hohmann Transfer Ellipse",
                "description": "Prograde delta-v burn raising apoapsis toward the outer gas giant orbit.",
                "params": {"star_mass": 1.0, "launch_speed": 36.2, "orbital_radius": 0.85, "jupiter_mass": 2.0, "time_warp": 1.5},
            },
            {
                "id": "comet-slingshot",
                "name": "Voyager Gravity Slingshot",
                "description": "High-eccentricity trajectory stealing orbital momentum from the outer giant.",
                "params": {"star_mass": 1.2, "launch_speed": 41.5, "orbital_radius": 0.70, "jupiter_mass": 4.5, "time_warp": 1.75},
            },
            {
                "id": "hyperbolic-escape",
                "name": "Hyperbolic Escape (v > v_esc)",
                "description": "Exceeds local escape velocity √(2GM/r) so specific energy ε > 0.",
                "params": {"star_mass": 0.9, "launch_speed": 46.0, "orbital_radius": 1.0, "jupiter_mass": 1.0, "time_warp": 1.25},
            },
        ],
        "formula": {
            "name": "Vis-Viva & Specific Orbital Energy Equation",
            "symbolic": "v² = G·M·(2/r₀ − 1/a)    |    e = |r₀·v₀²/(G·M) − 1|",
            "variables": "M = central star mass, r₀ = orbital radius, v₀ = tangential speed, a = semi-major axis, e = orbital eccentricity",
        },
        "tiers": {
            "eli7": {
                "headline": "Falling So Fast You Keep Missing the Star!",
                "body": (
                    "Imagine throwing a glowing snowball from a super-tall mountain. Toss it gently and gravity pulls it "
                    "down. Throw it so fast that as it falls, the round planet curves away underneath it at the exact "
                    "same rate — it keeps falling forever without hitting the ground! That is an **orbit**.\n\n"
                    "When a spacecraft flies close behind a giant planet, the planet's gravity tugs it forward like a "
                    "skateboarder grabbing the back of a moving bus — a **gravity slingshot**!"
                ),
                "try_this": "Click & drag on the space canvas to sling a new probe toward the orange gas giant and watch its speed jump!",
            },
            "high_school": {
                "headline": "Centripetal Balance, Kepler's Laws & Gravity Assists",
                "body": (
                    "Every satellite obeys Newton's Universal Gravitation $F_g = G M m / r^2$. Setting gravitational pull "
                    "equal to centripetal force $m v_{\\text{circ}}^2 / r_0$ yields circular orbit velocity $v_{\\text{circ}} = \\sqrt{GM/r_0}$.\n\n"
                    "• **Circular ($v_0 = v_{\\text{circ}}$)**: Eccentricity $e = 0$, constant altitude.\n"
                    "• **Elliptical ($v_{\\text{circ}} < v_0 < \\sqrt{2}v_{\\text{circ}}$)**: Swings between periapsis and apoapsis.\n"
                    "• **Hyperbolic Escape ($v_0 \\ge \\sqrt{2}v_{\\text{circ}}$)**: Total mechanical energy $E \\ge 0$."
                ),
                "try_this": "Raise Injection Velocity from 29.8 km/s to 42.1 km/s and watch eccentricity e climb from 0.00 to 1.00!",
            },
            "engineer": {
                "headline": "Symplectic N-Body Integration, Roche Limit & Laplace-Runge-Lenz Invariant",
                "body": (
                    "We integrate the restricted N-body equations $\\ddot{\\mathbf{r}}_i = -G \\sum_{j \\ne i} m_j (\\mathbf{r}_i - \\mathbf{r}_j)/\\|\\mathbf{r}_i - \\mathbf{r}_j\\|^3$ "
                    "with high-order sub-stepping to preserve the symplectic phase-space volume.\n\n"
                    "$$\\varepsilon = \\frac{v^2}{2} - \\frac{\\mu}{r} = -\\frac{\\mu}{2a}, \\quad "
                    "\\mathbf{e} = \\frac{\\mathbf{v} \\times (\\mathbf{r} \\times \\mathbf{v})}{\\mu} - \\frac{\\mathbf{r}}{r}$$\n\n"
                    "Effective potential contours in the co-rotating frame reveal Lagrange points $L_1..L_5$ and the tidal Roche limit $d_R \\approx 2.44 R_p (\\rho_M/\\rho_m)^{1/3}$."
                ),
                "try_this": "Verify the live Vis-Viva readout: when r₀·v₀²/(G·M) = 1, the Laplace-Runge-Lenz eccentricity e → 0.000.",
            },
        },
        "quest": {
            "id": "quest-orbital-circular",
            "title": "Circular Orbit Master (e < 0.05)",
            "prompt": "Place the primary spacecraft into a nearly circular Keplerian orbit with eccentricity e < 0.05.",
            "hint": "Match v₀ to √(G·M / r₀) — for M = 1.0 M☉ and r₀ = 1.0 AU, v_circ is ~29.8 km/s!",
            "target_metric": "eccentricity < 0.05",
            "badge_name": "Kepler Navigator",
            "xp": 150,
            "solve_params": {"star_mass": 1.0, "launch_speed": 29.8, "orbital_radius": 1.0, "jupiter_mass": 0.5, "time_warp": 1.25},
        },
    },

    # =========================================================================
    # 2. airfoil-wind-tunnel — Aerodynamic Airfoil & Kutta-Joukowski Lift
    # =========================================================================
    {
        "id": "airfoil-wind-tunnel",
        "engine_id": "airfoil-wind-tunnel",
        "engine_class": "AirfoilWindTunnelEngine",
        "number": 2,
        "title": "Aerodynamic Airfoil & Kutta-Joukowski Lift",
        "short_title": "Airfoil Wind Tunnel",
        "category": "Fluid & Aero",
        "icon": "✈️",
        "accent_color": "#22d3ee",
        "tagline": "Interactive NACA cambered wing in a high-density smoke streamline & velocity-vector wind tunnel with pressure heatmaps and post-stall vortex shedding.",
        "keywords": [
            "airplane", "wing", "lift", "drag", "airfoil", "bernoulli", "magnus", "curveball",
            "baseball", "wind tunnel", "aerodynamics", "stall", "angle of attack", "kutta",
            "flight", "fly", "pitch", "spin", "camber", "boundary layer",
        ],
        "canvas_hint": "Drag vertically on the wind tunnel to pitch Angle of Attack α live, or click to inject a neon smoke tracer pulse!",
        "parameters": [
            {
                "id": "angle_of_attack",
                "label": "Angle of Attack (α)",
                "symbol": "α",
                "unit": "°",
                "min": -10.0,
                "max": 24.0,
                "step": 0.5,
                "default": 7.5,
                "description": "Pitch angle between the NACA airfoil chord line and oncoming freestream airflow.",
            },
            {
                "id": "wind_speed",
                "label": "Freestream Airspeed (U∞)",
                "symbol": "U∞",
                "unit": "m/s",
                "min": 10.0,
                "max": 85.0,
                "step": 1.0,
                "default": 42.0,
                "description": "Oncoming wind tunnel freestream velocity.",
            },
            {
                "id": "spin_rpm",
                "label": "Circulation / Spin Rate (Ω)",
                "symbol": "Ω",
                "unit": "RPM",
                "min": -3000.0,
                "max": 3000.0,
                "step": 100.0,
                "default": 600.0,
                "description": "Vortex circulation boost / Magnus rotor spin generating Kutta-Joukowski lift.",
            },
            {
                "id": "air_density",
                "label": "Air Density (ρ)",
                "symbol": "ρ",
                "unit": "kg/m³",
                "min": 0.4,
                "max": 1.8,
                "step": 0.05,
                "default": 1.225,
                "description": "Fluid density (1.225 kg/m³ at sea level; lower at high cruise altitude).",
            },
            {
                "id": "camber",
                "label": "NACA Airfoil Camber",
                "symbol": "f/c",
                "unit": "%",
                "min": 0.0,
                "max": 12.0,
                "step": 0.5,
                "default": 4.5,
                "description": "Mean-line curvature of the wing profile (0% symmetric, 4–8% high-lift cambered wing).",
            },
        ],
        "presets": [
            {
                "id": "cruise-wing",
                "name": "Efficient Cruise Flight (α = 6°)",
                "description": "Attached laminar streamlines with peak Lift-to-Drag ratio (L/D > 14).",
                "params": {"angle_of_attack": 6.0, "wind_speed": 48.0, "spin_rpm": 0.0, "air_density": 1.225, "camber": 4.5},
            },
            {
                "id": "stall-regime",
                "name": "Deep Aerodynamic Stall (α = 19°)",
                "description": "Adverse pressure gradient detaches the upper boundary layer into a turbulent wake!",
                "params": {"angle_of_attack": 19.0, "wind_speed": 52.0, "spin_rpm": 0.0, "air_density": 1.225, "camber": 5.0},
            },
            {
                "id": "baseball-curveball",
                "name": "Magnus Curveball Circulation (2400 RPM)",
                "description": "High circulation Γ deflects wake downward and creates strong lateral Magnus force.",
                "params": {"angle_of_attack": 2.0, "wind_speed": 42.0, "spin_rpm": 2400.0, "air_density": 1.225, "camber": 0.0},
            },
            {
                "id": "high-lift-takeoff",
                "name": "Takeoff Flaps Deployed (Camber 9.5%)",
                "description": "High camber and α = 12° maximize C_L just below critical stall angle.",
                "params": {"angle_of_attack": 12.0, "wind_speed": 38.0, "spin_rpm": 400.0, "air_density": 1.225, "camber": 9.5},
            },
        ],
        "formula": {
            "name": "Kutta-Joukowski Lift Theorem & Dynamic Pressure",
            "symbolic": "L' = ρ · U∞ · Γ    |    L = ½ · ρ · U∞² · S · C_L(α, f/c)",
            "variables": "ρ = air density, U∞ = freestream speed, Γ = vortex circulation, α = angle of attack, C_L = lift coefficient",
        },
        "tiers": {
            "eli7": {
                "headline": "How Airplane Wings Scoop the Air & Curveballs Swerve!",
                "body": (
                    "Even though air is invisible, it is made of trillions of tiny bouncing molecules. A curved airplane "
                    "wing tilted slightly upward forces air over the top to speed up and bend downward off the trailing "
                    "edge. Because the wing throws air **down**, the air pushes the wing **up**!\n\n"
                    "Wait—if you tilt the wing up *too* steeply, the air can't hug the top curve anymore and breaks into "
                    "swirling whirlpools. That's called an **aerodynamic stall**!"
                ),
                "try_this": "Drag up and down on the wind tunnel canvas to tilt the wing past 16° and watch the smooth smoke lines burst into swirling stall vortices!",
            },
            "high_school": {
                "headline": "Bernoulli Pressure Gradient, Circulation & Boundary-Layer Stall",
                "body": (
                    "By Bernoulli's Principle ($P + \\frac{1}{2}\\rho v^2 = \\text{const}$), faster flow over the upper camber "
                    "creates a low-pressure suction zone above the wing and high pressure below.\n\n"
                    "• **Thin Airfoil Regime ($|\\alpha| < 15^\\circ$)**: Lift coefficient grows linearly as $C_L \\approx 2\\pi(\\alpha + 2 f/c)$.\n"
                    "• **Critical Stall ($\\alpha > 16^\\circ$)**: Viscosity and an adverse pressure gradient cause the boundary layer to detach, collapsing lift and spiking pressure drag $C_D$."
                ),
                "try_this": "Watch the Lift-Polar mini-scope in the corner as you sweep Angle of Attack α from -5° through +22°.",
            },
            "engineer": {
                "headline": "Kutta-Joukowski Circulation Γ, Thin-Airfoil Theory & Drag Polar",
                "body": (
                    "By the **Kutta condition**, sharp trailing-edge geometry enforces finite velocity, generating bound vortex "
                    "circulation $\\Gamma = \\oint \\mathbf{u}\\cdot d\\mathbf{l}$. Lift per unit span follows Kutta-Joukowski:\n\n"
                    "$$L' = \\rho_\\infty U_\\infty \\Gamma, \\quad C_L = 2\\pi\\left(\\alpha + \\frac{2f}{c}\\right) + \\Delta C_{L,\\text{Magnus}}, \\quad "
                    "C_D = C_{D0} + \\frac{C_L^2}{\\pi \\, AR \\, e}$$\n\n"
                    "Beyond $\\alpha_{\\text{crit}} \\approx 16^\\circ$, boundary-layer separation sheds alternating vortices into the wake."
                ),
                "try_this": "Tune α to 18.5° or raise circulation to achieve C_L ≥ 1.35 and inspect the live C_L(α) polar curve.",
            },
        },
        "quest": {
            "id": "quest-airfoil-stall",
            "title": "High-Lift / Stall Boundary Explorer (α ≥ 16° or C_L ≥ 1.35)",
            "prompt": "Push the wing into deep aerodynamic stall (α ≥ 16°) OR achieve extreme lift coefficient C_L ≥ 1.35.",
            "hint": "Increase Angle of Attack α above 16° or combine high camber (8%+) with α = 12°!",
            "target_metric": "α ≥ 16° or C_L ≥ 1.35",
            "badge_name": "Wind Tunnel Ace",
            "xp": 150,
            "solve_params": {"angle_of_attack": 18.5, "wind_speed": 52.0, "spin_rpm": 1200.0, "air_density": 1.225, "camber": 5.5},
        },
    },

    # =========================================================================
    # 3. double-pendulum-chaos — Chaotic Double Pendulum & Butterfly Divergence
    # =========================================================================
    {
        "id": "double-pendulum-chaos",
        "engine_id": "double-pendulum-chaos",
        "engine_class": "DoublePendulumChaosEngine",
        "number": 3,
        "title": "Chaotic Double Pendulum & Butterfly Divergence",
        "short_title": "Double Pendulum Chaos",
        "category": "Chaos & Math",
        "icon": "🦋",
        "accent_color": "#f59e0b",
        "tagline": "Simultaneous ensemble of 5 microscopically perturbed double pendulums (Δθ₀ = 10⁻⁴ rad) with glowing rainbow ribbons and live (θ₁, θ₂) strange attractor.",
        "keywords": [
            "chaos", "double pendulum", "butterfly effect", "lyapunov", "phase space", "attractor",
            "nonlinear", "lagrangian", "pendulum", "unpredictable", "weather", "sensitivity",
        ],
        "canvas_hint": "Click & drag on the left pendulum stage to set initial angles (θ₁, θ₂) and release the 5-pendulum rainbow ensemble!",
        "parameters": [
            {
                "id": "initial_angle_1",
                "label": "Upper Arm Angle (θ₁)",
                "symbol": "θ₁",
                "unit": "°",
                "min": 15.0,
                "max": 178.0,
                "step": 1.0,
                "default": 138.0,
                "description": "Initial release angle of the primary upper pendulum arm from vertical.",
            },
            {
                "id": "initial_angle_2",
                "label": "Lower Arm Angle (θ₂)",
                "symbol": "θ₂",
                "unit": "°",
                "min": 15.0,
                "max": 178.0,
                "step": 1.0,
                "default": 146.0,
                "description": "Initial release angle of the coupled lower pendulum arm.",
            },
            {
                "id": "mass_ratio",
                "label": "Bob Mass Ratio (m₂/m₁)",
                "symbol": "m₂/m₁",
                "unit": "×",
                "min": 0.2,
                "max": 3.0,
                "step": 0.1,
                "default": 1.0,
                "description": "Ratio of lower bob mass m₂ to upper bob mass m₁; controls inertial coupling.",
            },
            {
                "id": "gravity_g",
                "label": "Gravitational Accel (g)",
                "symbol": "g",
                "unit": "m/s²",
                "min": 1.6,
                "max": 24.8,
                "step": 0.2,
                "default": 9.81,
                "description": "Local gravity (1.62 Moon, 9.81 Earth, 24.79 Jupiter).",
            },
            {
                "id": "delta_theta_deg",
                "label": "Ensemble Perturbation (Δθ₀)",
                "symbol": "Δθ₀",
                "unit": "°",
                "min": 0.001,
                "max": 0.5,
                "step": 0.001,
                "default": 0.005,
                "description": "Angular separation between each of the 5 simultaneous ensemble pendulums at t = 0.",
            },
        ],
        "presets": [
            {
                "id": "butterfly-ensemble",
                "name": "Butterfly Divergence Ensemble (138°, 146°)",
                "description": "5 nearly identical pendulums swing as one for ~4 seconds before exploding into a rainbow fan!",
                "params": {"initial_angle_1": 138.0, "initial_angle_2": 146.0, "mass_ratio": 1.0, "gravity_g": 9.81, "delta_theta_deg": 0.005},
            },
            {
                "id": "kam-quasiperiodic",
                "name": "Low-Energy KAM Torus (28°, 24°)",
                "description": "Small angles stay locked in smooth Lissajous quasi-periodic orbits with λ ≈ 0.",
                "params": {"initial_angle_1": 28.0, "initial_angle_2": 24.0, "mass_ratio": 1.0, "gravity_g": 9.81, "delta_theta_deg": 0.010},
            },
            {
                "id": "extreme-inversion",
                "name": "Inverted Apex Chaos (172°, 168°)",
                "description": "Maximum gravitational potential energy drives rapid backflips and λ > 2.1 s⁻¹.",
                "params": {"initial_angle_1": 172.0, "initial_angle_2": 168.0, "mass_ratio": 1.4, "gravity_g": 9.81, "delta_theta_deg": 0.002},
            },
            {
                "id": "jupiter-whiplash",
                "name": "Jupiter Gravity Whiplash (g = 24.8 m/s²)",
                "description": "High-gravity regime accelerates whip-like momentum transfer between m₁ and m₂.",
                "params": {"initial_angle_1": 145.0, "initial_angle_2": 135.0, "mass_ratio": 1.8, "gravity_g": 24.8, "delta_theta_deg": 0.005},
            },
        ],
        "formula": {
            "name": "Euler-Lagrange Coupled Equations & Lyapunov Exponent",
            "symbolic": "|Δθ(t)| ≈ |Δθ₀| · e^(λ·t)    |    L = T(θ₁, θ₂, θ̇₁, θ̇₂) − V(θ₁, θ₂)",
            "variables": "θ₁, θ₂ = arm angles, Δθ₀ = initial perturbation, λ = maximal Lyapunov exponent (s⁻¹)",
        },
        "tiers": {
            "eli7": {
                "headline": "Why 5 Identical Swings Suddenly Split Into a Rainbow!",
                "body": (
                    "We launch **5 glowing pendulums** on top of each other, separated by less than the width of a human "
                    "hair ($0.005^\\circ$). At first, all 5 move together like a single pendulum.\n\n"
                    "Then—**BOOM!** Because the bottom arm pulls and kicks the top arm, that microscopic difference doubles "
                    "every fraction of a second until all 5 rainbow pendulums are flipping in totally different directions! "
                    "That is the famous **Butterfly Effect**."
                ),
                "try_this": "Click 'Butterfly Divergence Ensemble' and count how many seconds the 5 rainbow pendulums stay together before fanning out!",
            },
            "high_school": {
                "headline": "Deterministic Chaos, Phase Space & Predictability Horizons",
                "body": (
                    "Even though Newton's equations have **zero randomness**, nonlinear coupling between $\\theta_1$ and $\\theta_2$ "
                    "amplifies tiny initial uncertainties exponentially:\n\n"
                    "$$|\\Delta \\theta(t)| \\approx |\\Delta \\theta_0| e^{\\lambda t}$$\n\n"
                    "• **Low Energy ($\\lambda \\approx 0$)**: The right-hand $(\\theta_1, \\theta_2)$ phase portrait traces a neat, bounded loop.\n"
                    "• **Chaotic Regime ($\\lambda > 1.5\\text{ s}^{-1}$)**: Trajectories fill an intricate fractal region and diverge past $45^\\circ$ within seconds."
                ),
                "try_this": "Compare 'Low-Energy KAM Torus' (neat loop in phase space) vs 'Inverted Apex Chaos' (wild ergodic web)!",
            },
            "engineer": {
                "headline": "RK4 Integration of the Coupled Euler-Lagrange System",
                "body": (
                    "From Lagrangian $\\mathcal{L} = T - V$, the exact angular accelerations for lengths $L_1=L_2=L$ and mass ratio $\\mu = m_2/m_1$ are:\n\n"
                    "$$\\ddot{\\theta}_1 = \\frac{-g(2m_1+m_2)\\sin\\theta_1 - m_2 g \\sin(\\theta_1-2\\theta_2) - 2\\sin(\\theta_1-\\theta_2)m_2(\\dot{\\theta}_2^2 L + \\dot{\\theta}_1^2 L \\cos(\\theta_1-\\theta_2))}{L(2m_1+m_2-m_2\\cos(2\\theta_1-2\\theta_2))}$$\n\n"
                    "We integrate all 5 ensemble state vectors $(\\theta_1, \\theta_2, \\omega_1, \\omega_2)_k$ via 4th-order **Runge-Kutta (RK4)** and track $\\ln|\\Delta\\theta(t)/\\Delta\\theta_0|$ in the live mini-scope."
                ),
                "try_this": "Raise both release angles above 150° to push Lyapunov exponent λ ≥ 1.5 s⁻¹.",
            },
        },
        "quest": {
            "id": "quest-chaos-lyapunov",
            "title": "Butterfly Chaos Unleashed (λ ≥ 1.50 s⁻¹)",
            "prompt": "Inject enough gravitational potential energy so the maximal Lyapunov exponent reaches λ ≥ 1.50 s⁻¹.",
            "hint": "Raise Upper Arm Angle θ₁ and Lower Arm Angle θ₂ above 150°!",
            "target_metric": "λ ≥ 1.50 s⁻¹",
            "badge_name": "Chaos Lorenz Master",
            "xp": 150,
            "solve_params": {"initial_angle_1": 158.0, "initial_angle_2": 154.0, "mass_ratio": 1.2, "gravity_g": 9.81, "delta_theta_deg": 0.002},
        },
    },

    # =========================================================================
    # 4. geometric-optics — Optical Bench: Lenses, Prisms & Chromatic Dispersion
    # =========================================================================
    {
        "id": "geometric-optics",
        "engine_id": "geometric-optics",
        "engine_class": "GeometricOpticsEngine",
        "number": 4,
        "title": "Optical Bench: Lenses, Prisms & Chromatic Dispersion",
        "short_title": "Optics & Prism Bench",
        "category": "Quantum & Optics",
        "icon": "🌈",
        "accent_color": "#c084fc",
        "tagline": "Interactive ray-tracing optical bench with draggable biconvex/biconcave glass lenses, mirrors, and a dispersive flint-glass prism splitting white light via Cauchy's equation.",
        "keywords": [
            "optics", "lens", "prism", "rainbow", "refraction", "snell", "dispersion", "light",
            "laser", "focal length", "mirror", "index of refraction", "spectrum", "wavelength", "cauchy",
        ],
        "canvas_hint": "Drag the glass lens or flint prism directly on the optical bench to steer focal convergence and rainbow dispersion!",
        "parameters": [
            {
                "id": "beam_angle",
                "label": "Incident Laser Angle (θ_i)",
                "symbol": "θ_i",
                "unit": "°",
                "min": -25.0,
                "max": 25.0,
                "step": 0.5,
                "default": 6.0,
                "description": "Incidence angle of the collimated multi-ray white laser bundle.",
            },
            {
                "id": "lens_power",
                "label": "Lens Optical Power (D)",
                "symbol": "D",
                "unit": "dpt",
                "min": -6.0,
                "max": 8.0,
                "step": 0.25,
                "default": 3.5,
                "description": "Focal power 1/f (>0 converging biconvex lens, <0 diverging biconcave lens).",
            },
            {
                "id": "refractive_index",
                "label": "Crown/Flint Base Index (n₀)",
                "symbol": "n₀",
                "unit": "",
                "min": 1.33,
                "max": 1.95,
                "step": 0.01,
                "default": 1.62,
                "description": "Baseline refractive index n(589 nm) of the optical glass elements.",
            },
            {
                "id": "cauchy_dispersion",
                "label": "Chromatic Dispersion (B)",
                "symbol": "B",
                "unit": "×10⁴ nm²",
                "min": 0.2,
                "max": 3.5,
                "step": 0.1,
                "default": 1.8,
                "description": "Cauchy coefficient B in n(λ) = n₀ + B/λ² controlling red-to-violet rainbow spread.",
            },
            {
                "id": "prism_apex",
                "label": "Prism Apex Angle (α_p)",
                "symbol": "α_p",
                "unit": "°",
                "min": 30.0,
                "max": 72.0,
                "step": 1.0,
                "default": 60.0,
                "description": "Apex angle of the dispersive triangular prism on the optical bench.",
            },
        ],
        "presets": [
            {
                "id": "newton-rainbow-prism",
                "name": "Newton's Dispersive Flint Prism",
                "description": "Splits collimated white light into a vivid 380–700 nm spectral fan.",
                "params": {"beam_angle": 8.0, "lens_power": 2.5, "refractive_index": 1.68, "cauchy_dispersion": 2.6, "prism_apex": 60.0},
            },
            {
                "id": "biconvex-focus",
                "name": "Sharp Biconvex Focal Convergence",
                "description": "High-power converging lens brings parallel rays to a tight principal focus F.",
                "params": {"beam_angle": 0.0, "lens_power": 6.5, "refractive_index": 1.55, "cauchy_dispersion": 0.8, "prism_apex": 45.0},
            },
            {
                "id": "biconcave-diverging",
                "name": "Diverging Biconcave Beam Expander",
                "description": "Negative diopter lens spreads rays outward from a virtual focal point.",
                "params": {"beam_angle": 3.0, "lens_power": -4.5, "refractive_index": 1.58, "cauchy_dispersion": 1.5, "prism_apex": 55.0},
            },
            {
                "id": "total-internal-disp",
                "name": "Dense Diamond High-Dispersion (n=1.90)",
                "description": "Extreme refractive bending and wide angular spectral separation Δδ.",
                "params": {"beam_angle": 12.0, "lens_power": 3.5, "refractive_index": 1.90, "cauchy_dispersion": 3.2, "prism_apex": 64.0},
            },
        ],
        "formula": {
            "name": "Snell's Law, Thin-Lens Maker's Equation & Cauchy Dispersion",
            "symbolic": "n₁·sin(θ₁) = n(λ)·sin(θ₂)    |    n(λ) = n₀ + B/λ²    |    1/f = (n₀ − 1)(1/R₁ − 1/R₂)",
            "variables": "n(λ) = wavelength-dependent refractive index, λ ∈ [380, 700] nm, D = 1/f optical power, α_p = prism apex",
        },
        "tiers": {
            "eli7": {
                "headline": "Why a Glass Triangle Unlocks the Secret Rainbow Inside White Light!",
                "body": (
                    "White light from a flashlight looks plain, but it is actually every color of the rainbow traveling "
                    "together! When light enters glass, it slows down and bends.\n\n"
                    "Violet light has tiny, fast waves that get slowed down and bent **more** by glass than long, lazy red "
                    "waves. So when white light passes through a **glass prism**, violet bends sharply while red bends gently, "
                    "fanning out into a glowing rainbow!"
                ),
                "try_this": "Drag the prism and lens around the optical bench, then slide Chromatic Dispersion (B) up to widen the rainbow fan!",
            },
            "high_school": {
                "headline": "Snell's Law of Refraction, Focal Length & Chromatic Aberration",
                "body": (
                    "At every glass-air boundary, rays bend according to **Snell's Law**: $n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2$.\n\n"
                    "• **Converging vs. Diverging Lenses**: A biconvex lens ($D > 0$) bends rays toward the optical axis to meet at focal distance $f = 1/D$.\n"
                    "• **Material Dispersion**: Because refractive index decreases with wavelength ($n_{\\text{violet}} > n_{\\text{red}}$), a prism of apex angle $\\alpha_p$ deflects violet through a larger minimum deviation angle $\\delta(\\lambda)$ than red."
                ),
                "try_this": "Switch Lens Power (D) from +6.0 dpt (biconvex focus) to -4.5 dpt (biconcave spread) and trace the virtual focus!",
            },
            "engineer": {
                "headline": "Exact Vector Snell Ray-Tracing & Cauchy Spectral Dispersion",
                "body": (
                    "For incident unit ray $\\hat{\\mathbf{i}}$ and surface normal $\\hat{\\mathbf{n}}$ with ratio $\\eta = n_1/n_2(\\lambda)$, "
                    "transmitted ray vector $\\hat{\\mathbf{t}}$ is computed via vector Snell's Law:\n\n"
                    "$$\\hat{\\mathbf{t}} = \\eta\\,\\hat{\\mathbf{i}} + \\left(\\eta c_1 - \\sqrt{1 - \\eta^2(1 - c_1^2)}\\right)\\hat{\\mathbf{n}}, \\quad "
                    "n(\\lambda) = n_0 + \\frac{B}{\\lambda^2}$$\n\n"
                    "Angular spectral dispersion across the visible band ($\\lambda_{\\text{V}}=400\\text{ nm}$ to $\\lambda_{\\text{R}}=700\\text{ nm}$) is $\\Delta \\delta = \\delta(\\lambda_{\\text{V}}) - \\delta(\\lambda_{\\text{R}})$."
                ),
                "try_this": "Raise Refractive Index n₀ ≥ 1.65 and Cauchy Dispersion B ≥ 2.4 to achieve angular dispersion Δδ ≥ 5.0°!",
            },
        },
        "quest": {
            "id": "quest-optics-dispersion",
            "title": "Spectral Prism Master (Angular Spread Δδ ≥ 5.0°)",
            "prompt": "Configure the prism refractive index, apex angle, and Cauchy dispersion to split the rainbow spectrum by Δδ ≥ 5.0°.",
            "hint": "Increase Chromatic Dispersion B ≥ 2.4 and Refractive Index n₀ ≥ 1.66!",
            "target_metric": "Δδ ≥ 5.0°",
            "badge_name": "Newtonian Optician",
            "xp": 150,
            "solve_params": {"beam_angle": 8.0, "lens_power": 3.5, "refractive_index": 1.72, "cauchy_dispersion": 2.8, "prism_apex": 62.0},
        },
    },

    # =========================================================================
    # 5. electromagnetic-fields — Electrostatics, Dipoles & Lorentz Cyclotron
    # =========================================================================
    {
        "id": "electromagnetic-fields",
        "engine_id": "electromagnetic-fields",
        "engine_class": "ElectromagneticFieldsEngine",
        "number": 5,
        "title": "Electrostatics, Dipoles & Lorentz Cyclotron",
        "short_title": "EM Fields & Cyclotron",
        "category": "Electromagnetism & Circuits",
        "icon": "⚡",
        "accent_color": "#38bdf8",
        "tagline": "Interactive 2D electric field lines, equipotential voltage contours, draggable point charges, and relativistic Lorentz force cyclotron particle spirals.",
        "keywords": [
            "electric field", "magnetic field", "charge", "coulomb", "dipole", "voltage",
            "equipotential", "lorentz", "cyclotron", "electron", "proton", "electromagnetism", "gauss",
        ],
        "canvas_hint": "Drag the +q₁ and −q₂ point charges anywhere on the field grid, or click empty space to fire a test particle into the magnetic field!",
        "parameters": [
            {
                "id": "charge_q1",
                "label": "Primary Charge (q₁)",
                "symbol": "q₁",
                "unit": "μC",
                "min": -5.0,
                "max": 5.0,
                "step": 0.25,
                "default": 3.0,
                "description": "Charge magnitude and polarity of draggable source pole 1.",
            },
            {
                "id": "charge_q2",
                "label": "Secondary Charge (q₂)",
                "symbol": "q₂",
                "unit": "μC",
                "min": -5.0,
                "max": 5.0,
                "step": 0.25,
                "default": -3.0,
                "description": "Charge magnitude and polarity of draggable pole 2 (opposite sign = electric dipole).",
            },
            {
                "id": "magnetic_b",
                "label": "Perpendicular B-Field (B_z)",
                "symbol": "B_z",
                "unit": "T",
                "min": -2.5,
                "max": 2.5,
                "step": 0.1,
                "default": 0.8,
                "description": "Out-of-plane magnetic flux density B_z curling moving charges via q(v × B).",
            },
            {
                "id": "dipole_sep",
                "label": "Pole Separation (d)",
                "symbol": "d",
                "unit": "cm",
                "min": 4.0,
                "max": 24.0,
                "step": 0.5,
                "default": 12.0,
                "description": "Distance between the two primary electrostatic charges.",
            },
            {
                "id": "beam_energy",
                "label": "Injected Ion Speed (v₀)",
                "symbol": "v₀",
                "unit": "km/s",
                "min": 10.0,
                "max": 120.0,
                "step": 2.0,
                "default": 48.0,
                "description": "Initial injection velocity of positively charged test ions entering the chamber.",
            },
        ],
        "presets": [
            {
                "id": "classic-dipole",
                "name": "Symmetric Electric Dipole (+3 / −3 μC)",
                "description": "Classic Maxwellian field lines arcing from +q to −q with orthogonal equipotentials.",
                "params": {"charge_q1": 3.5, "charge_q2": -3.5, "magnetic_b": 0.3, "dipole_sep": 13.0, "beam_energy": 45.0},
            },
            {
                "id": "cyclotron-spiral",
                "name": "High-Field Lorentz Cyclotron (B_z = 2.0 T)",
                "description": "Strong perpendicular magnetic field locks ions into tight Larmor gyroradius orbits!",
                "params": {"charge_q1": 1.0, "charge_q2": -1.0, "magnetic_b": 2.0, "dipole_sep": 16.0, "beam_energy": 36.0},
            },
            {
                "id": "repulsive-monopoles",
                "name": "Repulsive Dual Positives (+4 / +4 μC)",
                "description": "Saddle point stagnation zone at the midpoint where E = 0.",
                "params": {"charge_q1": 4.0, "charge_q2": 4.0, "magnetic_b": 0.5, "dipole_sep": 12.0, "beam_energy": 55.0},
            },
            {
                "id": "exb-drift",
                "name": "Crossed-Field E × B Drift Trap",
                "description": "Balanced electric dipole and magnetic field produce trochoidal guiding-center drift.",
                "params": {"charge_q1": 4.5, "charge_q2": -4.5, "magnetic_b": 1.5, "dipole_sep": 14.0, "beam_energy": 52.0},
            },
        ],
        "formula": {
            "name": "Coulomb Superposition & Lorentz Force Law",
            "symbolic": "F = q·(E + v × B)    |    E(r) = ∑ k_e·q_i·(r − r_i)/|r − r_i|³    |    r_L = m·v/(|q|·|B|)",
            "variables": "q₁, q₂ = point charges, B_z = magnetic field, v₀ = particle speed, r_L = Larmor cyclotron radius",
        },
        "tiers": {
            "eli7": {
                "headline": "Invisible Push-and-Pull Force Fields & Spinning Particle Rollercoasters!",
                "body": (
                    "Positive (+) and negative (−) charges fill the space around them with an invisible web called an "
                    "**electric field**. Opposite charges pull together like magnets, while matching charges push apart!\n\n"
                    "When we turn on a **magnetic field ($B$)** pointing out of the screen, flying charged particles feel "
                    "a sideways tug that makes them loop-the-loop in glowing spirals called **cyclotron orbits**!"
                ),
                "try_this": "Drag the red (+q₁) and blue (−q₂) charges around the canvas and watch the glowing field web bend in real time!",
            },
            "high_school": {
                "headline": "Coulomb's Law, Equipotential Contours & Cyclotron Gyroradius",
                "body": (
                    "The electric field at any point is the vector sum $\\mathbf{E} = \\sum k_e q_i \\hat{\\mathbf{r}}_i / r_i^2$, "
                    "while voltage $V = \\sum k_e q_i / r_i$ forms **equipotential contours** that are always perpendicular to $\\mathbf{E}$.\n\n"
                    "• **Lorentz Force**: A particle of charge $q$ moving at velocity $\\mathbf{v}$ experiences $\\mathbf{F} = q(\\mathbf{E} + \\mathbf{v} \\times \\mathbf{B})$.\n"
                    "• **Cyclotron Radius**: Because $\\mathbf{v} \\times \\mathbf{B}$ is perpendicular to $\\mathbf{v}$, magnetic force does zero work and bends ions into circles of radius $r_L = mv/(qB)$."
                ),
                "try_this": "Increase Perpendicular B-Field (B_z) toward 2.0 T and watch the particle trajectories curl into tight Larmor circles!",
            },
            "engineer": {
                "headline": "Boris Pusher Integration, Dipole Moment & Guiding-Center Drift",
                "body": (
                    "Electrostatic scalar potential $\\Phi(\\mathbf{r}) = \\frac{1}{4\\pi\\varepsilon_0}\\sum_i \\frac{q_i}{\\|\\mathbf{r}-\\mathbf{r}_i\\|}$ "
                    "satisfies Poisson's equation $\\nabla^2 \\Phi = -\\rho/\\varepsilon_0$ with dipole moment $\\mathbf{p} = q\\mathbf{d}$.\n\n"
                    "$$m\\frac{d\\mathbf{v}}{dt} = q\\left(-\\nabla\\Phi + \\mathbf{v}\\times B_z\\hat{\\mathbf{z}}\\right), \\quad "
                    "\\omega_c = \\frac{|q B_z|}{m}, \\quad \\mathbf{v}_{E\\times B} = \\frac{\\mathbf{E}\\times\\mathbf{B}}{B^2}$$\n\n"
                    "Particles are integrated using an energy-conserving **Boris-style symplectic step**."
                ),
                "try_this": "Raise |B_z| ≥ 1.6 T to tighten the cyclotron gyroradius r_L ≤ 4.5 cm and complete the quest!",
            },
        },
        "quest": {
            "id": "quest-em-cyclotron",
            "title": "Cyclotron Magnetic Confinement (r_L ≤ 4.5 cm)",
            "prompt": "Tune the magnetic flux density B_z and ion speed v₀ to confine charged particles into a tight Larmor gyroradius r_L ≤ 4.5 cm.",
            "hint": "Increase Perpendicular B-Field |B_z| to ≥ 1.6 T and moderate Ion Speed v₀ ≤ 45 km/s!",
            "target_metric": "r_L ≤ 4.5 cm",
            "badge_name": "Maxwell Lorentz Pioneer",
            "xp": 150,
            "solve_params": {"charge_q1": 3.0, "charge_q2": -3.0, "magnetic_b": 2.0, "dipole_sep": 12.0, "beam_energy": 36.0},
        },
    },

    # =========================================================================
    # 6. quantum-tunneling — Quantum Wavepacket & Barrier Tunneling
    # =========================================================================
    {
        "id": "quantum-tunneling",
        "engine_id": "quantum-tunneling",
        "engine_class": "QuantumTunnelingEngine",
        "number": 6,
        "title": "Quantum Wavepacket & Barrier Tunneling",
        "short_title": "Quantum Tunneling",
        "category": "Quantum & Optics",
        "icon": "⚛️",
        "accent_color": "#a78bfa",
        "tagline": "Real-time Time-Dependent Schrödinger Equation (TDSE) solver showing a phase-colored Gaussian wavepacket ψ(x,t) tunneling through a potential barrier.",
        "keywords": [
            "quantum", "schrodinger", "tunneling", "wavefunction", "wavepacket", "barrier",
            "probability", "heisenberg", "planck", "de broglie", "superposition", "alpha decay", "qubit",
        ],
        "canvas_hint": "Click anywhere on the quantum axis to re-launch the wavepacket, or drag the potential barrier V₀ directly!",
        "parameters": [
            {
                "id": "packet_energy",
                "label": "Wavepacket Energy (E)",
                "symbol": "E",
                "unit": "eV",
                "min": 1.0,
                "max": 12.0,
                "step": 0.2,
                "default": 5.2,
                "description": "Mean kinetic energy E = ℏ²k₀²/(2m) of the incident Gaussian electron wavepacket.",
            },
            {
                "id": "barrier_height",
                "label": "Barrier Potential (V₀)",
                "symbol": "V₀",
                "unit": "eV",
                "min": 0.5,
                "max": 14.0,
                "step": 0.2,
                "default": 6.8,
                "description": "Height of the rectangular potential barrier V(x) in electron-volts.",
            },
            {
                "id": "barrier_width",
                "label": "Barrier Thickness (a)",
                "symbol": "a",
                "unit": "nm",
                "min": 0.2,
                "max": 2.5,
                "step": 0.05,
                "default": 0.65,
                "description": "Spatial width of the potential barrier; exponential WKB decay depends strongly on a.",
            },
            {
                "id": "packet_sigma",
                "label": "Position Spread (σ_x)",
                "symbol": "σ_x",
                "unit": "nm",
                "min": 0.3,
                "max": 1.8,
                "step": 0.05,
                "default": 0.75,
                "description": "Spatial width of initial Gaussian packet; narrower σ_x means wider momentum spread σ_p = ℏ/(2σ_x).",
            },
            {
                "id": "effective_mass",
                "label": "Effective Mass (m*/m_e)",
                "symbol": "m*",
                "unit": "m_e",
                "min": 0.2,
                "max": 2.0,
                "step": 0.05,
                "default": 0.6,
                "description": "Particle effective mass relative to a free electron.",
            },
        ],
        "presets": [
            {
                "id": "sub-barrier-tunneling",
                "name": "Sub-Barrier Quantum Tunneling (E < V₀)",
                "description": "Classically forbidden (E=5.2 eV < V₀=6.8 eV), yet ~25% of probability |ψ|² leaks through!",
                "params": {"packet_energy": 5.2, "barrier_height": 6.8, "barrier_width": 0.55, "packet_sigma": 0.75, "effective_mass": 0.5},
            },
            {
                "id": "thin-barrier-high-t",
                "name": "Ultra-Thin STM Tunnel Junction (a = 0.30 nm)",
                "description": "Scanning Tunneling Microscope regime where thin barrier permits T > 45%.",
                "params": {"packet_energy": 5.8, "barrier_height": 6.4, "barrier_width": 0.30, "packet_sigma": 0.80, "effective_mass": 0.45},
            },
            {
                "id": "thick-wall-reflection",
                "name": "Thick Opaque Barrier (a = 2.0 nm)",
                "description": "Evanescent wave e^(-κx) decays to near zero before reaching the right side.",
                "params": {"packet_energy": 4.0, "barrier_height": 9.5, "barrier_width": 2.00, "packet_sigma": 0.70, "effective_mass": 1.0},
            },
            {
                "id": "over-barrier-ramsauer",
                "name": "Over-Barrier Resonance (E > V₀)",
                "description": "Even when E > V₀, quantum impedance mismatch causes partial wave reflection!",
                "params": {"packet_energy": 9.5, "barrier_height": 5.5, "barrier_width": 0.85, "packet_sigma": 0.75, "effective_mass": 0.6},
            },
        ],
        "formula": {
            "name": "Time-Dependent Schrödinger Equation & WKB Tunneling Transmission",
            "symbolic": "iℏ ∂ψ/∂t = [−(ℏ²/2m)∂²/∂x² + V(x)]ψ    |    T ≈ [1 + V₀²·sinh²(κa)/(4E(V₀−E))]⁻¹",
            "variables": "ψ(x,t) = complex wavefunction, E = particle energy, V₀ = barrier height, a = barrier width, T = transmission probability",
        },
        "tiers": {
            "eli7": {
                "headline": "How a Quantum Particle Walks Straight Through a Solid Wall!",
                "body": (
                    "If you roll a tennis ball at a brick wall, it always bounces back. Join the **quantum world**, where "
                    "tiny electrons aren't hard little balls—they are **waves of possibility** ($\\psi$)!\n\n"
                    "When an electron wave hits a thin energy wall that is taller than its energy, the wave doesn't stop "
                    "instantly—it fades softly *inside* the wall. If the wall is thin enough, part of the wave pokes out "
                    "the other side, meaning the electron **teleports (tunnels) right through the wall**!"
                ),
                "try_this": "Slide Barrier Thickness (a) down to 0.30 nm and watch a huge glowing piece of the wave leak through the golden barrier!",
            },
            "high_school": {
                "headline": "De Broglie Matter Waves, Born Probability $|\\psi|^2$ & Evanescent Decay",
                "body": (
                    "By Max Born's rule, the height of $|\\psi(x,t)|^2$ gives the probability density of finding the electron at position $x$, "
                    "and total probability is always conserved ($T + R = 100\\%$). Inside a barrier where $E < V_0$, kinetic energy would be negative, "
                    "so the oscillating wave becomes an **exponentially decaying evanescent wave** $\\psi(x) \\propto e^{-\\kappa x}$.\n\n"
                    "• **Real ($\\text{Re}\\,\\psi$, cyan)** and **Imaginary ($\\text{Im}\\,\\psi$, magenta)** parts spiral in complex phase.\n"
                    "• **Tunneling Transmission ($T$)**: Grows exponentially as barrier width $a$ or effective mass $m^*$ decreases."
                ),
                "try_this": "Observe the live T (Transmitted) vs R (Reflected) gauges in the top-right probability conservation scope!",
            },
            "engineer": {
                "headline": "Unitary Split-Step / Crank-Nicolson FDTD Solver & Exact Barrier Scattering",
                "body": (
                    "We evolve $\\psi(x,t) = \\psi_R(x,t) + i\\,\\psi_I(x,t)$ on a staggered leapfrog grid conserving the $L^2$ norm $\\int |\\psi|^2 dx = 1$:\n\n"
                    "$$\\psi_R^{n+1/2} = \\psi_R^{n-1/2} + \\frac{\\Delta t}{\\hbar}\\hat{H}\\psi_I^n, \\quad "
                    "\\psi_I^{n+1} = \\psi_I^n - \\frac{\\Delta t}{\\hbar}\\hat{H}\\psi_R^{n+1/2}$$\n\n"
                    "For rectangular barrier $V_0 > E$ with decay constant $\\kappa = \\sqrt{2m^*(V_0-E)}/\\hbar$, exact transmission is "
                    "$T = \\left[1 + \\frac{V_0^2 \\sinh^2(\\kappa a)}{4E(V_0 - E)}\\right]^{-1}$."
                ),
                "try_this": "Achieve Quantum Tunneling Transmission T ≥ 20% while keeping E < V₀ (sub-barrier regime) to complete the quest!",
            },
        },
        "quest": {
            "id": "quest-quantum-tunnel",
            "title": "Forbidden Barrier Tunneling (T ≥ 20%)",
            "prompt": "Achieve a quantum transmission probability T ≥ 20% through the potential barrier.",
            "hint": "Use a thin barrier (a ≤ 0.50 nm) and bring Wavepacket Energy E close to Barrier Potential V₀!",
            "target_metric": "Transmission T ≥ 20%",
            "badge_name": "Schrödinger Wave Master",
            "xp": 150,
            "solve_params": {"packet_energy": 5.8, "barrier_height": 6.4, "barrier_width": 0.35, "packet_sigma": 0.80, "effective_mass": 0.45},
        },
    },

    # =========================================================================
    # 7. thermodynamics-gas — Kinetic Theory of Gases, Piston & Maxwell-Boltzmann
    # =========================================================================
    {
        "id": "thermodynamics-gas",
        "engine_id": "thermodynamics-gas",
        "engine_class": "ThermodynamicsGasEngine",
        "number": 7,
        "title": "Kinetic Theory of Gases, Piston & Maxwell-Boltzmann",
        "short_title": "Kinetic Gas & Piston",
        "category": "Fluid & Aero",
        "icon": "🔥",
        "accent_color": "#fb923c",
        "tagline": "220+ elastic hard-sphere molecules inside an interactive compression piston with wall heat bath, pressure impulse gauges (PV = Nk_BT), and live Maxwell-Boltzmann speed histogram.",
        "keywords": [
            "thermodynamics", "gas", "pressure", "temperature", "piston", "maxwell", "boltzmann",
            "ideal gas", "entropy", "heat", "molecules", "kinetic theory", "adiabatic", "boyle",
        ],
        "canvas_hint": "Drag the vertical compression piston left/right on the canvas to compress the gas adiabatically and watch temperature & pressure spike!",
        "parameters": [
            {
                "id": "temperature_k",
                "label": "Heat Bath Temperature (T)",
                "symbol": "T",
                "unit": "K",
                "min": 100.0,
                "max": 1200.0,
                "step": 20.0,
                "default": 350.0,
                "description": "Thermal reservoir temperature scaling root-mean-square molecular speed v_rms = √(3k_BT/m).",
            },
            {
                "id": "piston_volume",
                "label": "Chamber Volume Fraction (V)",
                "symbol": "V/V₀",
                "unit": "%",
                "min": 35.0,
                "max": 100.0,
                "step": 1.0,
                "default": 75.0,
                "description": "Position of the movable compression piston as a percentage of full chamber volume.",
            },
            {
                "id": "particle_count",
                "label": "Molecule Count (N)",
                "symbol": "N",
                "unit": "mol.",
                "min": 60,
                "max": 260,
                "step": 10,
                "default": 160,
                "description": "Number of elastic hard-sphere gas particles colliding in the chamber.",
            },
            {
                "id": "molecular_mass",
                "label": "Molar Mass (M_mol)",
                "symbol": "M",
                "unit": "g/mol",
                "min": 4.0,
                "max": 44.0,
                "step": 2.0,
                "default": 28.0,
                "description": "Molecular weight (4 = Helium, 28 = Nitrogen N₂, 44 = CO₂); lighter molecules move faster at fixed T.",
            },
            {
                "id": "adiabatic_gamma",
                "label": "Heat Capacity Ratio (γ)",
                "symbol": "γ",
                "unit": "",
                "min": 1.2,
                "max": 1.67,
                "step": 0.01,
                "default": 1.40,
                "description": "Adiabatic index C_P/C_V (1.67 monatomic He, 1.40 diatomic air).",
            },
        ],
        "presets": [
            {
                "id": "stp-nitrogen",
                "name": "Room-Temperature Nitrogen (300 K)",
                "description": "Balanced thermal equilibrium with classic bell-skewed Maxwell-Boltzmann curve.",
                "params": {"temperature_k": 300.0, "piston_volume": 80.0, "particle_count": 160, "molecular_mass": 28.0, "adiabatic_gamma": 1.40},
            },
            {
                "id": "adiabatic-crush",
                "name": "High-Pressure Piston Compression (V = 40%)",
                "description": "Halving volume doubles collision frequency and spikes wall pressure P = Nk_BT/V!",
                "params": {"temperature_k": 780.0, "piston_volume": 40.0, "particle_count": 220, "molecular_mass": 28.0, "adiabatic_gamma": 1.40},
            },
            {
                "id": "helium-hypervelocity",
                "name": "Hot Helium Plasma (M = 4 g/mol, 960 K)",
                "description": "Light helium atoms zip at >2,400 m/s, shifting the Maxwell-Boltzmann tail far right.",
                "params": {"temperature_k": 960.0, "piston_volume": 65.0, "particle_count": 180, "molecular_mass": 4.0, "adiabatic_gamma": 1.67},
            },
            {
                "id": "cryogenic-co2",
                "name": "Cryogenic Heavy CO₂ (140 K, M = 44 g/mol)",
                "description": "Cold, heavy molecules cluster into a narrow low-velocity Maxwell peak.",
                "params": {"temperature_k": 140.0, "piston_volume": 90.0, "particle_count": 140, "molecular_mass": 44.0, "adiabatic_gamma": 1.30},
            },
        ],
        "formula": {
            "name": "Ideal Gas Law & Maxwell-Boltzmann Speed Distribution",
            "symbolic": "P·V = N·k_B·T    |    v_rms = √(3·R·T / M)    |    f(v) = 4π(m/2πk_BT)^(3/2) · v² · e^(−mv²/2k_BT)",
            "variables": "P = wall pressure, V = chamber volume, T = absolute temperature (K), M = molar mass, v_rms = root-mean-square speed",
        },
        "tiers": {
            "eli7": {
                "headline": "Why Pumping a Bike Tire Makes It Feel Warm & Pressurized!",
                "body": (
                    "Temperature is just a measure of how fast tiny gas molecules are jiggling and zooming around! "
                    "**Pressure** is the drumbeat of billions of molecules slamming into the container walls.\n\n"
                    "When you push the **piston** inward to squeeze the gas into a smaller space, the molecules have less "
                    "room and bounce off the moving piston faster—making both the **pressure** and **temperature** shoot up!"
                ),
                "try_this": "Grab the glowing piston handle on the canvas and slide it left to squeeze the molecules into a tiny hot chamber!",
            },
            "high_school": {
                "headline": "Ideal Gas Law $PV = nRT$, Root-Mean-Square Speed & Maxwell-Boltzmann Curve",
                "body": (
                    "Microscopic momentum transfer during elastic wall collisions produces macroscopic pressure $P = \\frac{1}{3}\\frac{N}{V}m\\langle v^2\\rangle$.\n\n"
                    "• **Average Kinetic Energy**: $\\langle K \\rangle = \\frac{3}{2}k_B T$, yielding $v_{\\text{rms}} = \\sqrt{3RT/M}$.\n"
                    "• **Speed Histogram**: Even at one fixed temperature $T$, molecules don't all move at the same speed—elastic particle-particle collisions continually reshape their speeds into the **Maxwell-Boltzmann distribution** $f(v)$ shown on the right!"
                ),
                "try_this": "Keep Temperature at 600 K and slide Molar Mass from 44 (CO₂) down to 4 (Helium) to watch v_rms nearly triple!",
            },
            "engineer": {
                "headline": "Hard-Sphere Impulse Virial, Adiabatic Compression $PV^\\gamma$ & Statistical Mechanics",
                "body": (
                    "Pairwise elastic hard-sphere collisions conserve momentum $\\mathbf{p}_i + \\mathbf{p}_j$ and kinetic energy, "
                    "relaxing any initial distribution toward the canonical Boltzmann state:\n\n"
                    "$$f(v) = 4\\pi \\left(\\frac{m}{2\\pi k_B T}\\right)^{3/2} v^2 \\exp\\left(-\\frac{m v^2}{2 k_B T}\\right), \\quad "
                    "v_p = \\sqrt{\\frac{2RT}{M}} < \\langle v \\rangle = \\sqrt{\\frac{8RT}{\\pi M}} < v_{\\text{rms}} = \\sqrt{\\frac{3RT}{M}}$$\n\n"
                    "The right-hand scope overlays the theoretical $f(v)$ curve (amber) against the live empirical particle speed histogram (cyan)."
                ),
                "try_this": "Compress the piston and heat the gas to achieve Chamber Pressure P ≥ 3.50 atm to complete the quest!",
            },
        },
        "quest": {
            "id": "quest-thermo-pressure",
            "title": "High-Pressure Thermal Reactor (P ≥ 3.50 atm)",
            "prompt": "Compress the piston volume V and raise temperature T + molecule count N so chamber pressure reaches P ≥ 3.50 atm.",
            "hint": "Lower Chamber Volume V ≤ 45%, raise Temperature T ≥ 750 K, and increase N ≥ 200!",
            "target_metric": "Pressure P ≥ 3.50 atm",
            "badge_name": "Boltzmann Statistical Master",
            "xp": 150,
            "solve_params": {"temperature_k": 820.0, "piston_volume": 42.0, "particle_count": 220, "molecular_mass": 20.0, "adiabatic_gamma": 1.40},
        },
    },

    # =========================================================================
    # 8. fluid-vortex-tunnel — Navier-Stokes Fluid Dynamics & Kármán Vortex Street
    # =========================================================================
    {
        "id": "fluid-vortex-tunnel",
        "engine_id": "fluid-vortex-tunnel",
        "engine_class": "FluidVortexTunnelEngine",
        "number": 8,
        "title": "Navier-Stokes Fluid Dynamics & Kármán Vortex Street",
        "short_title": "Navier-Stokes Vortex",
        "category": "Fluid & Aero",
        "icon": "🌊",
        "accent_color": "#2dd4bf",
        "tagline": "Real-time Eulerian incompressible Navier-Stokes grid solver with vorticity confinement, neon multi-dye injection, and swirling Kármán vortex streets.",
        "keywords": [
            "fluid", "navier stokes", "vortex", "karman", "turbulence", "reynolds", "viscosity",
            "curl", "vorticity", "smoke", "dye", "eulerian", "strouhal", "wake", "cfd",
        ],
        "canvas_hint": "Drag the cylindrical obstacle inside the fluid channel or swirl your mouse through the flow to inject vorticity!",
        "parameters": [
            {
                "id": "reynolds_number",
                "label": "Reynolds Number (Re)",
                "symbol": "Re",
                "unit": "",
                "min": 15.0,
                "max": 600.0,
                "step": 5.0,
                "default": 180.0,
                "description": "Ratio of inertial to viscous forces Re = U·D/ν; vortex shedding begins above Re ≈ 47.",
            },
            {
                "id": "inflow_velocity",
                "label": "Channel Inflow Speed (U₀)",
                "symbol": "U₀",
                "unit": "m/s",
                "min": 0.5,
                "max": 5.0,
                "step": 0.1,
                "default": 2.4,
                "description": "Left-to-right inflow jet velocity driving the Eulerian fluid grid.",
            },
            {
                "id": "obstacle_diameter",
                "label": "Cylinder Diameter (D)",
                "symbol": "D",
                "unit": "cm",
                "min": 4.0,
                "max": 18.0,
                "step": 0.5,
                "default": 9.0,
                "description": "Characteristic diameter of the bluff obstacle in the channel.",
            },
            {
                "id": "vorticity_confinement",
                "label": "Vorticity Confinement (ε_ω)",
                "symbol": "ε_ω",
                "unit": "",
                "min": 0.5,
                "max": 6.0,
                "step": 0.25,
                "default": 3.2,
                "description": "Numerical curl-restoring gain that preserves crisp, curling vortex filaments.",
            },
            {
                "id": "dye_injection",
                "label": "Neon Dye Contrast",
                "symbol": "C_dye",
                "unit": "×",
                "min": 0.5,
                "max": 2.5,
                "step": 0.1,
                "default": 1.5,
                "description": "Intensity of the multi-band cyan/magenta/gold passive scalar dye ribbons.",
            },
        ],
        "presets": [
            {
                "id": "karman-street",
                "name": "Classic Kármán Vortex Street (Re = 180)",
                "description": "Alternating clockwise and counter-clockwise eddies shed at Strouhal number St ≈ 0.19.",
                "params": {"reynolds_number": 180.0, "inflow_velocity": 2.4, "obstacle_diameter": 9.0, "vorticity_confinement": 3.2, "dye_injection": 1.6},
            },
            {
                "id": "creeping-stokes",
                "name": "Laminar Creeping Flow (Re = 22)",
                "description": "High viscosity suppresses shedding into a symmetric attached recirculation pair.",
                "params": {"reynolds_number": 22.0, "inflow_velocity": 1.1, "obstacle_diameter": 8.0, "vorticity_confinement": 0.8, "dye_injection": 1.3},
            },
            {
                "id": "turbulent-wake",
                "name": "High-Re Turbulent Eddy Cascade (Re = 480)",
                "description": "Rapid high-frequency vortex shedding and intense curl filaments.",
                "params": {"reynolds_number": 480.0, "inflow_velocity": 3.8, "obstacle_diameter": 10.5, "vorticity_confinement": 5.0, "dye_injection": 2.0},
            },
            {
                "id": "slender-high-freq",
                "name": "Slender Cylinder High-Pitch Shedding",
                "description": "Small obstacle diameter D = 5 cm in fast flow raises shedding frequency f_s = St·U/D.",
                "params": {"reynolds_number": 260.0, "inflow_velocity": 4.2, "obstacle_diameter": 5.0, "vorticity_confinement": 3.8, "dye_injection": 1.7},
            },
        ],
        "formula": {
            "name": "Incompressible Navier-Stokes & Strouhal Vortex Shedding Law",
            "symbolic": "∂u/∂t + (u·∇)u = −(1/ρ)∇p + ν∇²u    |    ∇·u = 0    |    St = f_s·D/U₀ ≈ 0.198(1 − 19.7/Re)",
            "variables": "u = velocity field, ω = ∇×u vorticity curl, Re = Reynolds number, St = Strouhal number, f_s = shedding frequency",
        },
        "tiers": {
            "eli7": {
                "headline": "Why Flags Flutter in the Wind & Rivers Swirl Around Rocks!",
                "body": (
                    "Even when wind blows completely steady, a flagpole or bridge cable makes the air behind it dance! "
                    "As fluid flows past a round obstacle, it curls into a whirlpool on the top side, lets it go, and then "
                    "curls into an opposite whirlpool on the bottom side.\n\n"
                    "This left-right-left-right parade of glowing neon swirls is called a **Kármán Vortex Street**—and it's "
                    "why flags flap and telephone wires 'sing' in the wind!"
                ),
                "try_this": "Drag the round obstacle up and down or swirl your mouse through the neon dye streams to stir up giant whirlpools!",
            },
            "high_school": {
                "headline": "Reynolds Number $Re$, Viscosity vs. Inertia & Strouhal Frequency",
                "body": (
                    "Fluid behavior is governed by the dimensionless **Reynolds Number** $Re = \\frac{U_0 D}{\\nu}$, comparing "
                    "fluid inertia to viscous friction.\n\n"
                    "• **Laminar Flow ($Re < 47$)**: Viscosity smooths out disturbances; streamlines wrap smoothly around the cylinder.\n"
                    "• **Periodic Vortex Street ($50 < Re < 500$)**: The wake oscillates at the **Strouhal shedding frequency** "
                    "$f_s = \\text{St} \\cdot U_0 / D$, where $\\text{St} \\approx 0.20$."
                ),
                "try_this": "Lower Reynolds Number to 22 (smooth laminar wake), then slide it up to 300 to trigger alternating vortex shedding!",
            },
            "engineer": {
                "headline": "Chorin Pressure-Poisson Projection, Semi-Lagrangian Advection & Vorticity",
                "body": (
                    "On an Eulerian grid, we solve the incompressible Navier-Stokes system via operator splitting:\n\n"
                    "$$\\mathbf{u}^* = \\text{Advect}(\\mathbf{u}^n, \\Delta t) + \\Delta t\\,\\nu\\nabla^2\\mathbf{u}^n + \\Delta t\\,\\varepsilon_\\omega (\\hat{\\mathbf{N}}\\times\\boldsymbol{\\omega}), \\quad "
                    "\\nabla^2 p = \\frac{\\rho}{\\Delta t}\\nabla\\cdot\\mathbf{u}^*, \\quad "
                    "\\mathbf{u}^{n+1} = \\mathbf{u}^* - \\frac{\\Delta t}{\\rho}\\nabla p$$\n\n"
                    "Empirical Roshko-Strouhal relation $\\text{St}(Re) = 0.198(1 - 19.7/Re)$ predicts vortex shedding frequency $f_s$."
                ),
                "try_this": "Push Reynolds Number Re ≥ 220 and Inflow Speed U₀ ≥ 3.0 m/s so shedding frequency f_s ≥ 6.0 Hz!",
            },
        },
        "quest": {
            "id": "quest-fluid-vortex",
            "title": "Kármán Vortex Resonator (f_s ≥ 6.0 Hz & Re ≥ 150)",
            "prompt": "Tune Reynolds Number Re ≥ 150, Inflow Speed U₀, and Cylinder Diameter D so vortex shedding frequency reaches f_s ≥ 6.0 Hz.",
            "hint": "Raise Inflow Speed U₀ ≥ 3.2 m/s, Reynolds Number Re ≥ 220, and keep Cylinder Diameter D ≤ 9.0 cm!",
            "target_metric": "f_s ≥ 6.0 Hz (Re ≥ 150)",
            "badge_name": "Navier-Stokes Virtuoso",
            "xp": 150,
            "solve_params": {"reynolds_number": 280.0, "inflow_velocity": 3.6, "obstacle_diameter": 8.0, "vorticity_confinement": 4.0, "dye_injection": 1.8},
        },
    },

    # =========================================================================
    # 9. wave-interference — 2D Acoustic Ripple Tank, Double-Slit & Mach Cone
    # =========================================================================
    {
        "id": "wave-interference",
        "engine_id": "wave-interference",
        "engine_class": "WaveInterferenceEngine",
        "number": 9,
        "title": "2D Acoustic Ripple Tank, Double-Slit & Mach Cone",
        "short_title": "Wave & Mach Ripple Tank",
        "category": "Quantum & Optics",
        "icon": "🔊",
        "accent_color": "#a78bfa",
        "tagline": "2D acoustic/optical ripple tank with coherent Young double-slit interference, supersonic Mach shock cones, and live far-field fringe intensity profile.",
        "keywords": [
            "wave", "sound", "interference", "diffraction", "doppler", "mach", "sonic boom",
            "double slit", "frequency", "wavelength", "ripple tank", "phase", "acoustics",
        ],
        "canvas_hint": "Click anywhere in the ripple tank to drop a pulsed wave source, or toggle the Web Audio Synthesizer to hear Doppler pitch shift!",
        "parameters": [
            {
                "id": "frequency_hz",
                "label": "Source Frequency (f₀)",
                "symbol": "f₀",
                "unit": "Hz",
                "min": 110.0,
                "max": 660.0,
                "step": 10.0,
                "default": 260.0,
                "description": "Base emission frequency controlling wavelength λ = c / f₀.",
            },
            {
                "id": "source_separation",
                "label": "Slit / Source Separation (d/λ)",
                "symbol": "d/λ",
                "unit": "λ",
                "min": 0.0,
                "max": 6.0,
                "step": 0.25,
                "default": 2.5,
                "description": "Distance between the two coherent emitters in wavelengths (0 = single moving Doppler source).",
            },
            {
                "id": "source_velocity",
                "label": "Source Mach Number (M = v_s/c)",
                "symbol": "M",
                "unit": "Mach",
                "min": 0.0,
                "max": 1.6,
                "step": 0.05,
                "default": 0.35,
                "description": "Emitter speed relative to wave speed c (M > 1.0 forms a supersonic Mach shock cone).",
            },
            {
                "id": "phase_diff",
                "label": "Phase Offset (Δφ)",
                "symbol": "Δφ",
                "unit": "°",
                "min": 0.0,
                "max": 180.0,
                "step": 15.0,
                "default": 0.0,
                "description": "Phase angle between Source 1 and Source 2 (steers interference fringes!).",
            },
            {
                "id": "harmonics_count",
                "label": "Fourier Harmonics (K)",
                "symbol": "K",
                "unit": "modes",
                "min": 1,
                "max": 7,
                "step": 1,
                "default": 2,
                "description": "Number of odd Fourier harmonics superposed on the far-field detector scope.",
            },
        ],
        "presets": [
            {
                "id": "young-double-slit",
                "name": "Young's Double-Slit Interference (d = 3λ)",
                "description": "Hyperbolic constructive/destructive nodal lanes and far-field I(θ) fringes.",
                "params": {"frequency_hz": 280.0, "source_separation": 3.0, "source_velocity": 0.0, "phase_diff": 0.0, "harmonics_count": 2},
            },
            {
                "id": "doppler-ambulance",
                "name": "Subsonic Doppler Siren (Mach 0.65)",
                "description": "Wavefronts compress ahead (higher pitch f₊) and stretch behind (lower pitch f₋).",
                "params": {"frequency_hz": 320.0, "source_separation": 0.0, "source_velocity": 0.65, "phase_diff": 0.0, "harmonics_count": 1},
            },
            {
                "id": "supersonic-mach-cone",
                "name": "Supersonic Sonic Boom (Mach 1.30)",
                "description": "Emitter outruns its own waves, forming a V-shaped Mach cone θ_M = arcsin(1/M)!",
                "params": {"frequency_hz": 300.0, "source_separation": 0.0, "source_velocity": 1.30, "phase_diff": 0.0, "harmonics_count": 3},
            },
            {
                "id": "phased-array-beam",
                "name": "Phased-Array Beam Steering (Δφ = 90°)",
                "description": "Shifting relative phase Δφ steers the main constructive lobe without moving the antennas!",
                "params": {"frequency_hz": 340.0, "source_separation": 2.5, "source_velocity": 0.0, "phase_diff": 90.0, "harmonics_count": 5},
            },
        ],
        "formula": {
            "name": "Wave Superposition, Doppler Shift & Mach Cone Angle",
            "symbolic": "f_obs = f₀ / (1 ∓ v_s/c)    |    sin(θ_Mach) = c / v_s = 1 / M    |    I(θ) = I₀ cos²(π·d·sinθ/λ + Δφ/2)",
            "variables": "f₀ = source frequency, v_s = source velocity, c = wave speed, M = Mach number, d = source separation",
        },
        "tiers": {
            "eli7": {
                "headline": "Why Sirens Change Pitch & Supersonic Jets Make a Sonic Boom!",
                "body": (
                    "Drop two pebbles in a pond and their ripples cross: where two wave crests meet, they add into a "
                    "**super-tall wave**; where a crest meets a trough, they **cancel out to flat water**!\n\n"
                    "Now imagine a jet flying faster than its own sound ripples (**Mach > 1**). All the sound circles pile "
                    "up into a glowing V-shaped wake called a **Mach Cone**—and when that cone sweeps past your ears, you "
                    "hear a **Sonic Boom**!"
                ),
                "try_this": "Click 'Supersonic Sonic Boom (Mach 1.30)' to see the glowing V-shaped Mach cone form behind the racing source!",
            },
            "high_school": {
                "headline": "Constructive/Destructive Interference, Path Difference & Doppler Shift",
                "body": (
                    "For two coherent sources separated by $d$, path difference $\\Delta r = |r_1 - r_2|$ determines fringe intensity:\n"
                    "• **Constructive ($\\Delta r = m\\lambda$)**: Bright antinodal hyperbolas.\n"
                    "• **Destructive ($\\Delta r = (m + \\frac{1}{2})\\lambda$)**: Quiet nodal lines.\n"
                    "• **Doppler Shift**: A moving source at Mach $M = v_s/c$ shifts forward frequency to $f_+ = f_0/(1 - M)$."
                ),
                "try_this": "Slide Phase Offset (Δφ) from 0° to 180° and watch the central bright fringe flip into a dark nodal line!",
            },
            "engineer": {
                "headline": "Helmholtz Huygens Superposition, Phased Arrays & Mach Caustics",
                "body": (
                    "The complex acoustic pressure field from $N$ moving harmonic monopole sources is:\n\n"
                    "$$p(\\mathbf{r}, t) = \\text{Re}\\sum_{m=1}^{N} \\frac{A_m}{\\sqrt{\\|\\mathbf{r}-\\mathbf{r}_m(t_{\\text{ret}})\\|}} e^{i(k\\|\\mathbf{r}-\\mathbf{r}_m\\| - \\omega_0 t + \\phi_m)}$$\n\n"
                    "For $M = v_s/c > 1$, the envelope of retarded spherical wavefronts forms a conical caustic of half-angle $\\theta_M = \\arcsin(1/M)$."
                ),
                "try_this": "Set Source Mach Number M ≥ 0.85 or Fourier Harmonics K ≥ 4 to complete the quest!",
            },
        },
        "quest": {
            "id": "quest-wave-mach",
            "title": "Transonic / Supersonic Wave Master (Mach ≥ 0.85 or K ≥ 4)",
            "prompt": "Accelerate the emitter into the transonic/supersonic regime (Mach ≥ 0.85) OR synthesize K ≥ 4 harmonic modes.",
            "hint": "Slide Source Mach Number (M) above 0.85 or set Fourier Harmonics K ≥ 4!",
            "target_metric": "Mach ≥ 0.85 or K ≥ 4",
            "badge_name": "Mach Wave Architect",
            "xp": 150,
            "solve_params": {"frequency_hz": 300.0, "source_separation": 0.0, "source_velocity": 1.25, "phase_diff": 0.0, "harmonics_count": 5},
        },
    },

    # =========================================================================
    # 10. structural-truss — Structural Truss Bridge Stress, Load & Buckling Lab
    # =========================================================================
    {
        "id": "structural-truss",
        "engine_id": "structural-truss",
        "engine_class": "StructuralTrussEngine",
        "number": 10,
        "title": "Structural Truss Bridge Stress, Load & Buckling Lab",
        "short_title": "Truss Bridge Stress",
        "category": "Fluid & Aero",
        "icon": "🌉",
        "accent_color": "#f43f5e",
        "tagline": "Interactive civil engineering Warren/Pratt truss bridge finite-element solver with moving heavy vehicle load, tension/compression axial stress heatmaps, and Euler buckling.",
        "keywords": [
            "bridge", "truss", "stress", "strain", "buckling", "structural", "civil engineering",
            "tension", "compression", "hooke", "youngs modulus", "load", "seismic", "beam", "statics",
        ],
        "canvas_hint": "Drag the heavy truck load across the bridge deck or pull down on any truss joint node to test structural deflection!",
        "parameters": [
            {
                "id": "vehicle_load",
                "label": "Vehicle Live Load (F_load)",
                "symbol": "F",
                "unit": "kN",
                "min": 50.0,
                "max": 600.0,
                "step": 10.0,
                "default": 220.0,
                "description": "Downward gravitational force exerted by the moving heavy freight vehicle.",
            },
            {
                "id": "youngs_modulus",
                "label": "Steel Stiffness Modulus (E)",
                "symbol": "E",
                "unit": "GPa",
                "min": 70.0,
                "max": 280.0,
                "step": 5.0,
                "default": 200.0,
                "description": "Elastic modulus of truss members (70 GPa Aluminum, 200 GPa Structural Steel, 280 GPa Carbon Composite).",
            },
            {
                "id": "truss_depth",
                "label": "Truss Arch Height (H)",
                "symbol": "H",
                "unit": "m",
                "min": 3.0,
                "max": 12.0,
                "step": 0.5,
                "default": 7.5,
                "description": "Vertical depth of the Warren truss superstructure; taller trusses reduce chord axial stress.",
            },
            {
                "id": "beam_area",
                "label": "Member Cross-Section (A)",
                "symbol": "A",
                "unit": "cm²",
                "min": 15.0,
                "max": 90.0,
                "step": 2.5,
                "default": 45.0,
                "description": "Cross-sectional steel area of each truss girder.",
            },
            {
                "id": "seismic_amp",
                "label": "Seismic Ground Excitation",
                "symbol": "a_g",
                "unit": "g",
                "min": 0.0,
                "max": 0.60,
                "step": 0.02,
                "default": 0.04,
                "description": "Horizontal and vertical earthquake ground acceleration shaking the bridge piers.",
            },
        ],
        "presets": [
            {
                "id": "safe-highway-bridge",
                "name": "Safe AASHTO Steel Bridge (SF > 2.2)",
                "description": "Balanced Warren truss where top chords carry compression (red) and bottom chords carry tension (cyan).",
                "params": {"vehicle_load": 200.0, "youngs_modulus": 210.0, "truss_depth": 8.5, "beam_area": 55.0, "seismic_amp": 0.02},
            },
            {
                "id": "overloaded-buckling",
                "name": "Critical Euler Buckling Overload (560 kN)",
                "description": "Heavy load on shallow slender truss exceeds yield limit (SF < 1.0) and buckles top members!",
                "params": {"vehicle_load": 560.0, "youngs_modulus": 120.0, "truss_depth": 4.0, "beam_area": 20.0, "seismic_amp": 0.15},
            },
            {
                "id": "seismic-earthquake",
                "name": "0.45g Seismic Resonance Test",
                "description": "Strong ground shaking excites structural vibration modes across all truss bays.",
                "params": {"vehicle_load": 320.0, "youngs_modulus": 200.0, "truss_depth": 7.0, "beam_area": 45.0, "seismic_amp": 0.45},
            },
            {
                "id": "ultra-stiff-arch",
                "name": "Deep High-Strength Truss (SF > 3.5)",
                "description": "Deep 11 m truss with 80 cm² composite girders minimizes mid-span deflection δ_max.",
                "params": {"vehicle_load": 180.0, "youngs_modulus": 260.0, "truss_depth": 11.0, "beam_area": 80.0, "seismic_amp": 0.00},
            },
        ],
        "formula": {
            "name": "Direct Stiffness Truss Equilibrium, Axial Stress & Euler Buckling",
            "symbolic": "K · u = F_ext    |    σ_axial = E · (L − L₀)/L₀    |    P_cr = π²·E·I / L₀²    |    SF = σ_yield / σ_max",
            "variables": "K = global stiffness matrix, σ_axial = member stress (MPa), E = Young's modulus, P_cr = Euler buckling load, SF = safety factor",
        },
        "tiers": {
            "eli7": {
                "headline": "Why Bridges Are Built Out of Triangles Instead of Squares!",
                "body": (
                    "Try making a square out of four straws—if you push on the top, it squishes flat right away! Now make a "
                    "**triangle** out of three straws: it cannot change its shape unless a straw stretches or bends!\n\n"
                    "When a heavy truck drives across our **truss bridge**, the top bars get squeezed together (**Compression**, "
                    "glowing red) while the bottom bars get pulled tight (**Tension**, glowing blue). If the truck is way too "
                    "heavy, a squeezed bar suddenly pops sideways—that's called **buckling**!"
                ),
                "try_this": "Click 'Critical Euler Buckling Overload' to see the top red bridge bars bend and buckle under the giant truck!",
            },
            "high_school": {
                "headline": "Hooke's Law, Tension vs. Compression & Structural Factor of Safety",
                "body": (
                    "Each steel member acts like a stiff spring obeying **Hooke's Law** in stress-strain form: $\\sigma = F/A = E \\cdot \\varepsilon$, "
                    "where strain $\\varepsilon = \\Delta L / L_0$.\n\n"
                    "• **Top Chord (Compression, $\\sigma < 0$)**: Resists inward bending moment $M \\approx F_{\\text{load}} L_{\\text{span}} / 4$, so axial force scales inversely with truss height $H$.\n"
                    "• **Factor of Safety ($\\text{SF} = \\sigma_{\\text{yield}} / \\sigma_{\\max}$)**: Civil codes require $\\text{SF} \\ge 2.0$ so the bridge never yields or buckles."
                ),
                "try_this": "Increase Truss Arch Height (H) from 4 m to 11 m and watch maximum member stress drop in half!",
            },
            "engineer": {
                "headline": "2D Bar-Element Stiffness Matrix $[K]\\{u\\}=\\{F\\}$ & Euler Column Buckling",
                "body": (
                    "Each pin-jointed truss element $e$ of length $L_e$, area $A$, and direction cosines $(c, s)$ contributes local stiffness:\n\n"
                    "$$\\mathbf{k}_e = \\frac{E A}{L_e}\\begin{bmatrix} c^2 & cs & -c^2 & -cs \\\\ cs & s^2 & -cs & -s^2 \\\\ -c^2 & -cs & c^2 & cs \\\\ -cs & -s^2 & cs & s^2 \\end{bmatrix}, \\quad "
                    "\\sigma_{\\max} \\approx \\frac{F_{\\text{load}} L_{\\text{span}}}{4 H A}(1 + 2.2 a_g)$$\n\n"
                    "Compression members fail by **Euler buckling** when $|F_e| > P_{\\text{cr}} = \\pi^2 E I / L_e^2$."
                ),
                "try_this": "Reinforce the bridge so Factor of Safety SF ≥ 2.40 under at least 220 kN of vehicle load!",
            },
        },
        "quest": {
            "id": "quest-truss-safety",
            "title": "Chief Bridge Engineer (Safety Factor SF ≥ 2.40)",
            "prompt": "Reinforce the truss height H, cross-sectional area A, and stiffness E to achieve a structural Safety Factor SF ≥ 2.40.",
            "hint": "Increase Truss Arch Height H ≥ 9.0 m and Member Cross-Section A ≥ 65 cm² with low seismic shaking!",
            "target_metric": "Safety Factor SF ≥ 2.40",
            "badge_name": "Structural Statics Master",
            "xp": 150,
            "solve_params": {"vehicle_load": 200.0, "youngs_modulus": 240.0, "truss_depth": 10.0, "beam_area": 75.0, "seismic_amp": 0.02},
        },
    },

    # =========================================================================
    # 11. rlc-circuit-resonance — Driven AC RLC Circuit, Phasor Diagram & Bode Plot
    # =========================================================================
    {
        "id": "rlc-circuit-resonance",
        "engine_id": "rlc-circuit-resonance",
        "engine_class": "RlcCircuitResonanceEngine",
        "number": 11,
        "title": "Driven AC RLC Circuit, Phasor Diagram & Bode Plot",
        "short_title": "RLC Resonance & Bode",
        "category": "Electromagnetism & Circuits",
        "icon": "🎛️",
        "accent_color": "#10b981",
        "tagline": "Interactive AC series RLC laboratory with animated electron drift schematic, 4-channel storage oscilloscope, rotating complex impedance phasors, and Bode resonance curve.",
        "keywords": [
            "circuit", "rlc", "resonance", "inductor", "capacitor", "resistor", "impedance",
            "phasor", "bode plot", "ac", "voltage", "current", "ohm", "kirchhoff", "oscilloscope", "radio",
        ],
        "canvas_hint": "Drag the frequency marker directly on the Bode resonance plot to sweep driving frequency f across ω₀ = 1/√(LC)!",
        "parameters": [
            {
                "id": "drive_freq_hz",
                "label": "AC Driving Frequency (f)",
                "symbol": "f",
                "unit": "Hz",
                "min": 40.0,
                "max": 400.0,
                "step": 2.0,
                "default": 159.0,
                "description": "Frequency of the sinusoidal AC voltage generator V(t) = V₀ sin(2πft).",
            },
            {
                "id": "resistance_ohm",
                "label": "Series Resistance (R)",
                "symbol": "R",
                "unit": "Ω",
                "min": 5.0,
                "max": 120.0,
                "step": 1.0,
                "default": 18.0,
                "description": "Ohmic resistance dissipating heat; lower R yields a sharper, taller Q-factor resonance peak.",
            },
            {
                "id": "inductance_mh",
                "label": "Coil Inductance (L)",
                "symbol": "L",
                "unit": "mH",
                "min": 10.0,
                "max": 120.0,
                "step": 2.0,
                "default": 50.0,
                "description": "Magnetic inductance L producing inductive reactance X_L = 2πfL (voltage leads current by +90°).",
            },
            {
                "id": "capacitance_uf",
                "label": "Capacitance (C)",
                "symbol": "C",
                "unit": "μF",
                "min": 4.0,
                "max": 60.0,
                "step": 1.0,
                "default": 20.0,
                "description": "Capacitor value producing capacitive reactance X_C = 1/(2πfC) (voltage lags current by −90°).",
            },
            {
                "id": "source_voltage",
                "label": "Peak AC Source Voltage (V₀)",
                "symbol": "V₀",
                "unit": "V",
                "min": 5.0,
                "max": 50.0,
                "step": 1.0,
                "default": 24.0,
                "description": "Peak amplitude of the driving AC voltage source.",
            },
        ],
        "presets": [
            {
                "id": "exact-resonance",
                "name": "Exact LC Resonance Lock (f = f₀ = 159 Hz)",
                "description": "X_L = X_C cancel completely! Impedance drops to Z = R, phase φ = 0°, and current peaks.",
                "params": {"drive_freq_hz": 159.0, "resistance_ohm": 14.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
            },
            {
                "id": "capacitive-low-freq",
                "name": "Capacitive Regime (f = 70 Hz < f₀)",
                "description": "At low frequency, capacitor blocks current (X_C > X_L) so current leads voltage (φ < 0°).",
                "params": {"drive_freq_hz": 70.0, "resistance_ohm": 22.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
            },
            {
                "id": "inductive-high-freq",
                "name": "Inductive Regime (f = 310 Hz > f₀)",
                "description": "At high frequency, inductor chokes current (X_L > X_C) so current lags voltage (φ > 0°).",
                "params": {"drive_freq_hz": 310.0, "resistance_ohm": 22.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
            },
            {
                "id": "high-q-radio-tuner",
                "name": "High-Q Radio Tank Selectivity (R = 6 Ω)",
                "description": "Ultra-low damping creates a needle-sharp Bode resonance peak with voltage magnification V_C > Q·V₀!",
                "params": {"drive_freq_hz": 159.0, "resistance_ohm": 6.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
            },
        ],
        "formula": {
            "name": "Complex AC Impedance, Phasor Phase & Resonance Frequency",
            "symbolic": "Z = R + j(ωL − 1/ωC)    |    f₀ = 1/(2π√(LC))    |    I₀ = V₀ / √(R² + (X_L − X_C)²)    |    tan(φ) = (X_L − X_C)/R",
            "variables": "R = resistance, X_L = ωL inductive reactance, X_C = 1/(ωC) capacitive reactance, f₀ = resonance frequency, Q = quality factor",
        },
        "tiers": {
            "eli7": {
                "headline": "How a Radio Tuner Picks Out Just One Station From the Air!",
                "body": (
                    "Inside every radio is an electric swing set made of a **coil ($L$)** that stores magnetic energy and a "
                    "**capacitor ($C$)** that stores electric charge. Energy sloshes back and forth between them at one "
                    "special rhythm called the **resonant frequency ($f_0$)**!\n\n"
                    "When you push the circuit at *that exact frequency*, the coil and capacitor cancel each other's pushback "
                    "out completely, and electric current surges to a massive peak!"
                ),
                "try_this": "Drag the glowing dot on the Bode graph to the very top of the mountain peak where X_L and X_C cancel out!",
            },
            "high_school": {
                "headline": "Reactance Cancellation ($X_L = X_C$), Phase Shift & Ohm's Law for AC",
                "body": (
                    "In an AC circuit driven at angular frequency $\\omega = 2\\pi f$, inductors oppose rapid current changes "
                    "($X_L = \\omega L$) while capacitors oppose slow DC changes ($X_C = 1/(\\omega C)$).\n\n"
                    "• **Total Impedance**: $Z = \\sqrt{R^2 + (X_L - X_C)^2}$ and peak current $I_0 = V_0 / Z$.\n"
                    "• **Resonance ($f_0 = \\frac{1}{2\\pi\\sqrt{LC}}$)**: Because $V_L$ leads current by $+90^\\circ$ and $V_C$ lags by $-90^\\circ$, at $f = f_0$ they are $180^\\circ$ out of phase and cancel to zero net reactive drop!"
                ),
                "try_this": "Look at the rotating Phasor Diagram: at f = 159 Hz (L=50 mH, C=20 μF), the green V_L arrow and pink V_C arrow have equal length and cancel!",
            },
            "engineer": {
                "headline": "Complex Phasor Analysis, Transfer Function $H(j\\omega)$ & Quality Factor $Q$",
                "body": (
                    "In the Laplace/Fourier domain $s = j\\omega$, complex impedance is $\\tilde{Z}(j\\omega) = R + j\\left(\\omega L - \\frac{1}{\\omega C}\\right) = |Z|e^{j\\phi}$:\n\n"
                    "$$I(t) = \\frac{V_0}{|Z|}\\sin(\\omega t - \\phi), \\quad \\phi = \\arctan\\left(\\frac{\\omega L - 1/(\\omega C)}{R}\\right), \\quad "
                    "Q = \\frac{1}{R}\\sqrt{\\frac{L}{C}}$$\n\n"
                    "At resonance $\\omega_0 = 1/\\sqrt{LC}$, reactive voltages experience magnification $|V_L| = |V_C| = Q \\cdot V_0$."
                ),
                "try_this": "Tune the circuit to resonance (|φ| ≤ 8°) with Quality Factor Q ≥ 2.5 to complete the quest!",
            },
        },
        "quest": {
            "id": "quest-rlc-resonance",
            "title": "Resonance Lock & Power Factor Unity (|φ| ≤ 8° & Q ≥ 2.5)",
            "prompt": "Tune driving frequency f to match the LC resonant frequency f₀ so phase shift |φ| ≤ 8° with Quality Factor Q ≥ 2.5.",
            "hint": "For L = 50 mH and C = 20 μF, set f = 159 Hz and Resistance R ≤ 18 Ω!",
            "target_metric": "|φ| ≤ 8° and Q ≥ 2.5",
            "badge_name": "Tesla Phasor Engineer",
            "xp": 150,
            "solve_params": {"drive_freq_hz": 159.0, "resistance_ohm": 12.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
        },
    },

    # =========================================================================
    # 12. relativistic-lensing — General Relativity Spacetime Grid & Gravitational Lensing
    # =========================================================================
    {
        "id": "relativistic-lensing",
        "engine_id": "relativistic-lensing",
        "engine_class": "RelativisticLensingEngine",
        "number": 12,
        "title": "General Relativity Spacetime Grid & Gravitational Lensing",
        "short_title": "Black Hole Lensing",
        "category": "Astrophysics",
        "icon": "🕳️",
        "accent_color": "#f43f5e",
        "tagline": "3D-projected Flamm's paraboloid spacetime curvature mesh around a Schwarzschild black hole bending photon geodesics, photon sphere orbits, and Einstein rings.",
        "keywords": [
            "black hole", "relativity", "einstein", "spacetime", "gravitational lensing", "schwarzschild",
            "event horizon", "photon sphere", "geodesic", "redshift", "gravity", "curvature", "interstellar",
        ],
        "canvas_hint": "Drag the photon emitter beam vertically on the canvas to sweep impact parameter b across the Photon Sphere (r = 1.5 r_s)!",
        "parameters": [
            {
                "id": "bh_mass",
                "label": "Black Hole Mass (M_BH)",
                "symbol": "M",
                "unit": "M☉",
                "min": 2.0,
                "max": 25.0,
                "step": 0.5,
                "default": 10.0,
                "description": "Mass of the Schwarzschild black hole; sets event horizon radius r_s = 2GM/c².",
            },
            {
                "id": "impact_param",
                "label": "Photon Impact Parameter (b/r_s)",
                "symbol": "b/r_s",
                "unit": "r_s",
                "min": 1.2,
                "max": 6.5,
                "step": 0.05,
                "default": 2.85,
                "description": "Perpendicular aiming distance of the primary light ray in units of r_s (critical capture at b_c = 2.60 r_s).",
            },
            {
                "id": "beam_spread",
                "label": "Photon Bundle Width",
                "symbol": "Δb",
                "unit": "r_s",
                "min": 0.0,
                "max": 4.0,
                "step": 0.1,
                "default": 2.2,
                "description": "Spread of parallel incoming light rays showing multi-ray gravitational lensing and Einstein ring formation.",
            },
            {
                "id": "grid_tilt",
                "label": "3D Flamm Funnel Tilt",
                "symbol": "θ_view",
                "unit": "°",
                "min": 15.0,
                "max": 65.0,
                "step": 1.0,
                "default": 42.0,
                "description": "3D projection tilt angle of the warped Flamm's paraboloid spacetime embedding mesh.",
            },
            {
                "id": "accretion_spin",
                "label": "Relativistic Doppler Disk Glow",
                "symbol": "a*",
                "unit": "",
                "min": 0.0,
                "max": 0.98,
                "step": 0.02,
                "default": 0.65,
                "description": "Accretion disk relativistic beaming & frame-dragging intensity.",
            },
        ],
        "presets": [
            {
                "id": "einstein-lensing",
                "name": "Einstein Gravitational Lensing Bundle",
                "description": "Parallel starlight rays bend around the spacetime funnel, focusing on the far side.",
                "params": {"bh_mass": 10.0, "impact_param": 2.95, "beam_spread": 2.6, "grid_tilt": 44.0, "accretion_spin": 0.65},
            },
            {
                "id": "photon-sphere-skimming",
                "name": "Critical Photon Sphere Orbit (b ≈ 2.60 r_s)",
                "description": "Light skims r_ph = 1.5 r_s, whipping nearly a full loop around the black hole before escaping!",
                "params": {"bh_mass": 12.0, "impact_param": 2.62, "beam_spread": 0.8, "grid_tilt": 40.0, "accretion_spin": 0.80},
            },
            {
                "id": "event-horizon-capture",
                "name": "Event Horizon Plunge (b < 2.60 r_s)",
                "description": "Rays aimed inside the critical impact parameter spiral across r = r_s and never return.",
                "params": {"bh_mass": 15.0, "impact_param": 1.85, "beam_spread": 1.6, "grid_tilt": 48.0, "accretion_spin": 0.75},
            },
            {
                "id": "weak-field-solar",
                "name": "Weak-Field Eddington Deflection (b = 5.5 r_s)",
                "description": "Distant grazing ray bends by Einstein's angle Δφ = 4GM/(c²b) — twice Newton's prediction!",
                "params": {"bh_mass": 6.0, "impact_param": 5.50, "beam_spread": 1.2, "grid_tilt": 32.0, "accretion_spin": 0.30},
            },
        ],
        "formula": {
            "name": "Schwarzschild Metric, Null Geodesics & Einstein Deflection Angle",
            "symbolic": "r_s = 2GM/c²    |    (du/dφ)² = 1/b² − u²(1 − r_s·u)    |    Δφ ≈ 4GM/(c²·b) = 2·r_s/b",
            "variables": "r_s = Schwarzschild event horizon, r_ph = 1.5 r_s photon sphere, b = impact parameter, u = 1/r, Δφ = deflection angle",
        },
        "tiers": {
            "eli7": {
                "headline": "How a Black Hole Warps Space Like a Heavy Bowling Ball on a Trampoline!",
                "body": (
                    "Albert Einstein discovered that gravity isn't an invisible rope—instead, heavy things **bend the fabric "
                    "of space and time** like a bowling ball sinking into a stretchy trampoline!\n\n"
                    "Even though light has zero weight, it follows the curves of space. When starlight flies past a **Black "
                    "Hole**, the deep funnel bends the light beam like a giant cosmic magnifying glass (**Gravitational Lensing**). "
                    "If light gets closer than the **Event Horizon**, not even light can climb back out!"
                ),
                "try_this": "Drag vertically on the canvas to aim the golden laser bundle right at the glowing orange Photon Sphere ring!",
            },
            "high_school": {
                "headline": "Schwarzschild Radius $r_s$, Photon Sphere $1.5 r_s$ & Gravitational Redshift",
                "body": (
                    "A non-rotating black hole of mass $M$ has an **Event Horizon** at the Schwarzschild radius $r_s = 2GM/c^2 \\approx 2.95(M/M_\\odot)\\text{ km}$.\n\n"
                    "• **Einstein Deflection**: For impact parameter $b$, general relativity predicts $\\Delta\\phi \\approx \\frac{4GM}{c^2 b} = \\frac{2 r_s}{b}$ (twice the Newtonian value because both time and space curve).\n"
                    "• **Photon Sphere ($r_{\\text{ph}} = 1.5 r_s$, $b_c = \\frac{3\\sqrt{3}}{2}r_s \\approx 2.60 r_s$)**: Unstable circular orbit where light can orbit the black hole!"
                ),
                "try_this": "Slide Photon Impact Parameter (b/r_s) down toward 2.62 r_s and watch the light ray whip >90° around the black hole!",
            },
            "engineer": {
                "headline": "Binet Null Geodesic Equation & Flamm's Paraboloid Embedding",
                "body": (
                    "In Schwarzschild coordinates $(t, r, \\theta, \\phi)$ with $u = 1/r$, equatorial null geodesics ($ds^2 = 0$) obey Binet's nonlinear ODE:\n\n"
                    "$$\\frac{d^2 u}{d\\phi^2} + u = \\frac{3}{2} r_s u^2, \\quad "
                    "z_{\\text{Flamm}}(r) = 2\\sqrt{r_s(r - r_s)}, \\quad "
                    "z_{\\text{grav}} = \\frac{1}{\\sqrt{1 - r_s/r}} - 1$$\n\n"
                    "The effective potential $V_{\\text{eff}}(r) = (1 - r_s/r)/r^2$ peaks at $r_{\\text{ph}} = 1.5 r_s$ with critical capture parameter $b_{\\text{crit}} = \\frac{3\\sqrt{3}}{2}r_s$."
                ),
                "try_this": "Skim the photon sphere so gravitational deflection Δφ ≥ 45° without falling into the horizon!",
            },
        },
        "quest": {
            "id": "quest-relativity-lens",
            "title": "Relativistic Strong-Field Lensing (Deflection Δφ ≥ 45°)",
            "prompt": "Aim the photon beam close to the critical photon sphere so strong-field gravitational deflection reaches Δφ ≥ 45°.",
            "hint": "Set Photon Impact Parameter (b/r_s) between 2.60 and 2.95 r_s with Black Hole Mass ≥ 10 M☉!",
            "target_metric": "Deflection Δφ ≥ 45°",
            "badge_name": "Schwarzschild Geodesic Master",
            "xp": 150,
            "solve_params": {"bh_mass": 12.0, "impact_param": 2.68, "beam_spread": 1.8, "grid_tilt": 42.0, "accretion_spin": 0.75},
        },
    },

    # =========================================================================
    # 13. fourier-epicycles — Discrete Fourier Transform Epicycle Drawing Machine
    # =========================================================================
    {
        "id": "fourier-epicycles",
        "engine_id": "fourier-epicycles",
        "engine_class": "FourierEpicyclesEngine",
        "number": 13,
        "title": "Discrete Fourier Transform Epicycle Drawing Machine",
        "short_title": "Fourier Epicycles",
        "category": "Chaos & Math",
        "icon": "🌀",
        "accent_color": "#ec4899",
        "tagline": "Complex Discrete Fourier Transform (DFT) visualizer where chains of rotating harmonic phasor circles trace closed contours alongside a live frequency spectrum.",
        "keywords": [
            "fourier", "epicycle", "dft", "fft", "harmonics", "frequency", "spectrum", "sine",
            "cosine", "signal processing", "phasor", "wave", "drawing", "compression", "math",
        ],
        "canvas_hint": "Draw your own custom closed shape right on the canvas with your mouse and watch the Fourier epicycle gears compute its exact DFT and trace it!",
        "parameters": [
            {
                "id": "epicycle_count",
                "label": "Active Epicycle Harmonics (M)",
                "symbol": "M",
                "unit": "circles",
                "min": 2,
                "max": 64,
                "step": 1,
                "default": 28,
                "description": "Number of largest-amplitude DFT complex harmonics retained in the tip-to-tail gear chain.",
            },
            {
                "id": "shape_preset",
                "label": "Target Contour Shape",
                "symbol": "f(t)",
                "unit": "id",
                "min": 1,
                "max": 4,
                "step": 1,
                "default": 1,
                "description": "1 = Starship Rocket, 2 = Parametric Heart, 3 = 8-Point Starburst, 4 = Square-Wave Step Box.",
            },
            {
                "id": "cycle_speed",
                "label": "Fundamental Angular Speed (ω₀)",
                "symbol": "ω₀",
                "unit": "×",
                "min": 0.25,
                "max": 3.0,
                "step": 0.05,
                "default": 1.0,
                "description": "Rotation rate of the fundamental n = 1 harmonic circle.",
            },
            {
                "id": "trail_persistence",
                "label": "Contour Trail Length",
                "symbol": "τ_trail",
                "unit": "%",
                "min": 25.0,
                "max": 100.0,
                "step": 5.0,
                "default": 90.0,
                "description": "Percentage of the full 2π period kept illuminated in the neon drawing trace.",
            },
            {
                "id": "harmonic_filter",
                "label": "High-Frequency Boost",
                "symbol": "α_hf",
                "unit": "×",
                "min": 0.5,
                "max": 1.5,
                "step": 0.05,
                "default": 1.0,
                "description": "Scales higher-order harmonic amplitudes to exaggerate or smooth sharp corners (Gibbs phenomenon).",
            },
        ],
        "presets": [
            {
                "id": "starship-contour",
                "name": "Starship Silhouette (M = 36 Epicycles)",
                "description": "36 rotating complex phasors reconstruct fins, nosecone, and fuselage with >98% energy!",
                "params": {"epicycle_count": 36, "shape_preset": 1, "cycle_speed": 1.0, "trail_persistence": 95.0, "harmonic_filter": 1.0},
            },
            {
                "id": "low-rank-ellipse",
                "name": "3-Circle Low-Pass Filter (M = 3)",
                "description": "Truncating the Fourier series to 3 circles smooths away all sharp corners into a soft blob.",
                "params": {"epicycle_count": 3, "shape_preset": 1, "cycle_speed": 1.0, "trail_persistence": 95.0, "harmonic_filter": 1.0},
            },
            {
                "id": "parametric-heart",
                "name": "Parametric Cardioid Heart (M = 24)",
                "description": "Smooth algebraic curve converges rapidly with only a handful of low-order harmonics.",
                "params": {"epicycle_count": 24, "shape_preset": 2, "cycle_speed": 1.1, "trail_persistence": 95.0, "harmonic_filter": 1.0},
            },
            {
                "id": "square-gibbs",
                "name": "Square Box & Gibbs Ringing (M = 48)",
                "description": "Sharp 90° corners require high frequencies 1/n and show classic Gibbs overshoot ears.",
                "params": {"epicycle_count": 48, "shape_preset": 4, "cycle_speed": 0.9, "trail_persistence": 95.0, "harmonic_filter": 1.15},
            },
        ],
        "formula": {
            "name": "Complex Discrete Fourier Transform (DFT) & Parseval Reconstruction",
            "symbolic": "c_k = (1/N) ∑ z_n · e^(−i·2πkn/N)    |    z(t) ≈ ∑_{k=1}^M |c_k| · e^(i(ω_k·t + φ_k))",
            "variables": "z(t) = x(t) + i·y(t) complex contour, c_k = complex Fourier coefficient, M = active epicycles, E_M/E_tot = Parseval energy",
        },
        "tiers": {
            "eli7": {
                "headline": "How Spinning Wheels Inside Wheels Can Draw Almost Any Picture!",
                "body": (
                    "Imagine attaching a smaller spinning wheel to the rim of a big wheel, and a tiny wheel to the rim of "
                    "that one, with a glowing neon pen on the very last tip. Every wheel spins at a steady speed in a perfect "
                    "circle.\n\n"
                    "French mathematician **Joseph Fourier** proved something magical: if you pick the right wheel sizes and "
                    "starting angles, a chain of spinning circles (**epicycles**) can draw a rocket ship, a heart, or even "
                    "your own signature!"
                ),
                "try_this": "Slide Active Epicycle Harmonics (M) down to 2 (blurry oval), then slide it up to 40 to watch the sharp corners snap into focus—or draw your own shape on the canvas!",
            },
            "high_school": {
                "headline": "Complex Phasors $e^{i\\omega t}$, Harmonic Decomposition & Low-Pass Filtering",
                "body": (
                    "By **Euler's Formula** $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$, every term $c_k e^{i k \\omega_0 t}$ "
                    "is a vector of radius $|c_k|$ rotating at integer frequency $k\\omega_0$ in the 2D complex plane.\n\n"
                    "• **Low Frequencies ($k = \\pm 1, \\pm 2$)**: Capture the coarse overall size and orientation of the shape.\n"
                    "• **High Frequencies ($|k| \\gg 1$)**: Carve out fine details and sharp corners. Dropping high frequencies is how **JPEG images and MP3 audio** compress data!"
                ),
                "try_this": "Check the right-hand Amplitude Spectrum |c_k| bar chart to see which harmonic frequencies carry the most energy!",
            },
            "engineer": {
                "headline": "Orthogonal $L^2(\\mathbb{T})$ Basis, DFT Coefficients & Parseval's Theorem",
                "body": (
                    "Given $N$ sampled contour vertices $z_n = x_n + i y_n \\in \\mathbb{C}$, the exact Discrete Fourier Transform coefficients are:\n\n"
                    "$$c_k = \\frac{1}{N}\\sum_{n=0}^{N-1} z_n e^{-i 2\\pi k n / N}, \\quad "
                    "z_M(t) = \\sum_{m=1}^{M} c_{k_m} e^{i k_m \\omega_0 t}$$\n\n"
                    "By **Parseval's Identity**, sorting terms by descending magnitude $|c_{k_1}| \\ge |c_{k_2}| \\ge \\dots$ maximizes reconstructed contour energy $E_M / E_{\\text{total}} = \\sum_{m=1}^M |c_{k_m}|^2 / \\sum_{\\text{all}} |c_k|^2$."
                ),
                "try_this": "Retain enough harmonics M so Parseval Reconstruction Fidelity reaches ≥ 96.5%!",
            },
        },
        "quest": {
            "id": "quest-fourier-fidelity",
            "title": "Parseval Reconstruction Master (Fidelity ≥ 96.5%)",
            "prompt": "Configure the Fourier epicycle series to reconstruct the target contour with ≥ 96.5% spectral energy fidelity.",
            "hint": "Increase Active Epicycle Harmonics (M) to ≥ 32 circles!",
            "target_metric": "Reconstruction ≥ 96.5%",
            "badge_name": "Fourier Harmonic Architect",
            "xp": 150,
            "solve_params": {"epicycle_count": 42, "shape_preset": 1, "cycle_speed": 1.0, "trail_persistence": 95.0, "harmonic_filter": 1.0},
        },
    },

    # =========================================================================
    # 14. ant-colony-swarm — Bio-Inspired Ant Colony Pheromone Pathfinding
    # =========================================================================
    {
        "id": "ant-colony-swarm",
        "engine_id": "ant-colony-swarm",
        "engine_class": "AntColonySwarmEngine",
        "number": 14,
        "title": "Bio-Inspired Ant Colony Pheromone Pathfinding",
        "short_title": "Ant Colony Swarm",
        "category": "Complex Systems & AI",
        "icon": "🐜",
        "accent_color": "#34d399",
        "tagline": "300+ autonomous foraging agents depositing and following evaporating home/food chemical pheromone gradients (∇c) around obstacles to discover shortest paths.",
        "keywords": [
            "ant", "ants", "swarm", "pheromone", "shortest path", "stigmergy", "colony",
            "emergent", "foraging", "dijkstra", "optimization", "aco", "insects", "biology",
        ],
        "canvas_hint": "Click & drag on the terrain to paint or move stone obstacles and watch the ant highway dynamically reroute around them!",
        "parameters": [
            {
                "id": "ant_count",
                "label": "Forager Population (N)",
                "symbol": "N",
                "unit": "ants",
                "min": 50,
                "max": 320,
                "step": 10,
                "default": 180,
                "description": "Number of autonomous ant agents simultaneously exploring and reinforcing trails.",
            },
            {
                "id": "evaporation_rate",
                "label": "Pheromone Evaporation (ρ)",
                "symbol": "ρ",
                "unit": "%/s",
                "min": 0.5,
                "max": 12.0,
                "step": 0.5,
                "default": 3.5,
                "description": "Decay rate allowing long detours to fade away.",
            },
            {
                "id": "pheromone_strength",
                "label": "Chemotaxis Sensitivity (α_p)",
                "symbol": "α_p",
                "unit": "×",
                "min": 0.5,
                "max": 5.0,
                "step": 0.25,
                "default": 2.8,
                "description": "Non-linear exponent governing how strongly ants lock onto existing chemical trails.",
            },
            {
                "id": "exploration_noise",
                "label": "Random Exploration Jitter (ε)",
                "symbol": "ε",
                "unit": "rad",
                "min": 0.05,
                "max": 0.90,
                "step": 0.05,
                "default": 0.22,
                "description": "Angular exploration noise enabling discovery of new shortcuts.",
            },
            {
                "id": "obstacle_preset",
                "label": "Terrain Obstacle Layout",
                "symbol": "Ω_obs",
                "unit": "mode",
                "min": 0,
                "max": 2,
                "step": 1,
                "default": 1,
                "description": "0 = Open Plains, 1 = Central Boulder Split, 2 = Double-Bridge Maze.",
            },
        ],
        "presets": [
            {
                "id": "optimal-colony",
                "name": "Shortest-Path Highway Lock",
                "description": "Balanced evaporation (3.5%/s) and high sensitivity rapidly lock onto the shortest branch.",
                "params": {"ant_count": 220, "evaporation_rate": 3.5, "pheromone_strength": 3.8, "exploration_noise": 0.16, "obstacle_preset": 1},
            },
            {
                "id": "random-scouts",
                "name": "Pure Random Walk (Low Sensitivity)",
                "description": "High exploration noise and weak pheromone gain prevent highway formation.",
                "params": {"ant_count": 140, "evaporation_rate": 9.0, "pheromone_strength": 0.7, "exploration_noise": 0.75, "obstacle_preset": 1},
            },
            {
                "id": "double-bridge-maze",
                "name": "Dorigo Double-Bridge Experiment",
                "description": "Classic 2-wall maze where the shorter corridor wins via positive feedback.",
                "params": {"ant_count": 260, "evaporation_rate": 4.0, "pheromone_strength": 4.0, "exploration_noise": 0.18, "obstacle_preset": 2},
            },
            {
                "id": "frozen-lock-in",
                "name": "Zero-Evaporation Suboptimal Lock-In",
                "description": "Without evaporation (ρ = 0.5%/s), early meandering trails never fade away.",
                "params": {"ant_count": 180, "evaporation_rate": 0.5, "pheromone_strength": 4.5, "exploration_noise": 0.10, "obstacle_preset": 2},
            },
        ],
        "formula": {
            "name": "Reaction-Diffusion Pheromone Field & Dorigo ACO Choice Rule",
            "symbolic": "∂c/∂t = D·∇²c − ρ·c + ∑ S_i(x,t)    |    P_k = (τ_k)^α_p / ∑ (τ_j)^α_p",
            "variables": "c(x,t) = pheromone concentration, ρ = evaporation rate, α_p = trail sensitivity, N = ant population",
        },
        "tiers": {
            "eli7": {
                "headline": "How Blind Ants Build Invisible Smell Highways!",
                "body": (
                    "No single ant has a map or a boss telling it where to go. Instead, when an ant finds yummy food, it "
                    "walks home leaving tiny drops of smelly perfume called **pheromones**.\n\n"
                    "Ants taking the **short path** get back and forth much faster than ants taking the **long path**, so "
                    "the short path gets twice as much perfume before the smell evaporates! Soon the whole colony marches "
                    "along the shortest highway!"
                ),
                "try_this": "Click & drag on the canvas to drop a new rock barrier right across the green trail and watch the ants find a new shortcut!",
            },
            "high_school": {
                "headline": "Stigmergy, Positive Feedback Loops & Evaporation Pruning",
                "body": (
                    "**Stigmergy** is indirect coordination through the environment: each ant samples chemical intensity "
                    "$c(\\mathbf{x})$ with its left/center/right antennae and turns toward $\\nabla c$.\n\n"
                    "• **Positive Feedback ($\\alpha_p$)**: Short loops accumulate round-trip deposits faster ($f \\propto 1/L$).\n"
                    "• **Evaporation ($\\rho$)**: Exponential decay $c(t) = c_0 e^{-\\rho t}$ erases obsolete long detours."
                ),
                "try_this": "Compare 'Pure Random Walk' vs 'Shortest-Path Highway Lock' and watch the Trail Efficiency meter climb!",
            },
            "engineer": {
                "headline": "Coupled PDE-Agent Chemotaxis & Ant Colony Optimization (ACO)",
                "body": (
                    "Two scalar fields $c_{\\text{home}}(\\mathbf{x}, t)$ and $c_{\\text{food}}(\\mathbf{x}, t)$ evolve via discrete reaction-diffusion:\n\n"
                    "$$\\frac{\\partial c}{\\partial t} = D \\nabla^2 c - \\rho c + \\sum_{i=1}^{N} q_i \\delta(\\mathbf{x} - \\mathbf{x}_i(t)), \\quad "
                    "d\\theta_i = \\alpha_p \\,\\text{atan2}(\\nabla_\\perp c, \\nabla_\\parallel c)\\,dt + \\varepsilon\\,dW_t$$\n\n"
                    "By Dorigo's ACO theorem, path selection probability $P_A = \\tau_A^{\\alpha_p}/(\\tau_A^{\\alpha_p}+\\tau_B^{\\alpha_p}) \\to 1$ for $L_A < L_B$."
                ),
                "try_this": "Tune N, ρ, and α_p to achieve Trail Convergence Efficiency η ≥ 65%!",
            },
        },
        "quest": {
            "id": "quest-ants-highway",
            "title": "Swarm Highway Architect (Efficiency η ≥ 65%)",
            "prompt": "Balance pheromone sensitivity α_p, evaporation ρ, and ant count N so shortest-path trail efficiency reaches η ≥ 65%.",
            "hint": "Set Ant Count N ≥ 180, Pheromone Sensitivity α_p ≥ 3.5, and Exploration Jitter ε ≤ 0.20!",
            "target_metric": "trail_efficiency ≥ 65%",
            "badge_name": "Stigmergy Master",
            "xp": 150,
            "solve_params": {"ant_count": 220, "evaporation_rate": 4.0, "pheromone_strength": 4.2, "exploration_noise": 0.12, "obstacle_preset": 1},
        },
    },

    # =========================================================================
    # 15. epidemic-seir — Spatial SEIR Contagion Network & Herd Immunity
    # =========================================================================
    {
        "id": "epidemic-seir",
        "engine_id": "epidemic-seir",
        "engine_class": "EpidemicSeirEngine",
        "number": 15,
        "title": "Spatial SEIR Contagion Network & Herd Immunity",
        "short_title": "SEIR Epidemic & Herd",
        "category": "Complex Systems & AI",
        "icon": "🧬",
        "accent_color": "#f43f5e",
        "tagline": "Stochastic spatial agent population with Susceptible, Exposed, Infectious, Recovered & Vaccinated compartments, transmission arcs, and live stacked SEIR curve.",
        "keywords": [
            "epidemic", "virus", "pandemic", "sir", "seir", "vaccine", "herd immunity", "contagion",
            "reproduction number", "r0", "quarantine", "infection", "disease", "outbreak", "flatten the curve",
        ],
        "canvas_hint": "Click inside the city arena to introduce an infectious index case, or adjust Vaccination Rate to erect a herd-immunity shield!",
        "parameters": [
            {
                "id": "transmission_prob",
                "label": "Transmission Rate (β)",
                "symbol": "β",
                "unit": "/contact",
                "min": 0.08,
                "max": 0.95,
                "step": 0.02,
                "default": 0.52,
                "description": "Probability of viral transmission per close spatial contact.",
            },
            {
                "id": "recovery_rate",
                "label": "Recovery Rate (γ)",
                "symbol": "γ",
                "unit": "/day",
                "min": 0.05,
                "max": 0.50,
                "step": 0.01,
                "default": 0.16,
                "description": "Inverse of infectious duration (I → R transition rate).",
            },
            {
                "id": "vaccination_rate",
                "label": "Pre-Existing Vaccination (V%)",
                "symbol": "v",
                "unit": "%",
                "min": 0.0,
                "max": 90.0,
                "step": 2.0,
                "default": 15.0,
                "description": "Percentage of population immunized prior to outbreak (emerald shield nodes).",
            },
            {
                "id": "social_distancing",
                "label": "Mobility Reduction (d%)",
                "symbol": "d",
                "unit": "%",
                "min": 0.0,
                "max": 85.0,
                "step": 5.0,
                "default": 20.0,
                "description": "Reduction in agent movement speed and contact radius.",
            },
            {
                "id": "incubation_days",
                "label": "Exposed Latency Period (1/σ)",
                "symbol": "τ_inc",
                "unit": "days",
                "min": 1.0,
                "max": 10.0,
                "step": 0.5,
                "default": 3.0,
                "description": "Latent Exposed (E) duration before an agent becomes actively infectious (I).",
            },
        ],
        "presets": [
            {
                "id": "unmitigated-wave",
                "name": "Unmitigated Superspreader Wave (R_t ≈ 3.2)",
                "description": "Low vaccination and high mobility trigger an explosive red infection spike.",
                "params": {"transmission_prob": 0.62, "recovery_rate": 0.15, "vaccination_rate": 5.0, "social_distancing": 5.0, "incubation_days": 2.5},
            },
            {
                "id": "herd-immunity-shield",
                "name": "Herd Immunity Threshold (68% Vaccinated)",
                "description": "Vaccinated green nodes block transmission chains so R_t drops below 1.0!",
                "params": {"transmission_prob": 0.36, "recovery_rate": 0.18, "vaccination_rate": 68.0, "social_distancing": 30.0, "incubation_days": 3.0},
            },
            {
                "id": "flatten-the-curve",
                "name": "Flatten the Curve (Social Distancing 65%)",
                "description": "Reduced contact mobility keeps peak hospitalizations below capacity.",
                "params": {"transmission_prob": 0.46, "recovery_rate": 0.18, "vaccination_rate": 25.0, "social_distancing": 65.0, "incubation_days": 3.5},
            },
            {
                "id": "stealth-incubation",
                "name": "Long Incubation Stealth Virus (8 Days)",
                "description": "Agents travel widely in the yellow Exposed state before symptoms appear.",
                "params": {"transmission_prob": 0.54, "recovery_rate": 0.14, "vaccination_rate": 15.0, "social_distancing": 15.0, "incubation_days": 8.0},
            },
        ],
        "formula": {
            "name": "Kermack-McKendrick SEIR ODEs & Herd Immunity Threshold",
            "symbolic": "R₀ = β / γ    |    R_t = R₀ · (1 − d) · (1 − v)    |    v_herd = 1 − 1/R₀",
            "variables": "β = transmission rate, γ = recovery rate, d = distancing fraction, v = vaccinated fraction, R_t = effective reproduction number",
        },
        "tiers": {
            "eli7": {
                "headline": "How Vaccines Act Like Firebreaks in a Forest!",
                "body": (
                    "Imagine a room full of dominoes: flick one red domino and the whole room topples! A contagious virus "
                    "spreads the same way when people bump into each other.\n\n"
                    "**Vaccination** turns people into sturdy green shield blocks that can't be knocked over. Once enough "
                    "green shields are scattered around the city, the virus hits a dead end everywhere it turns—protecting "
                    "even the unshielded dots! That's **Herd Immunity**."
                ),
                "try_this": "Click 'Herd Immunity Threshold (68% Vaccinated)' and watch the red sparks fizzle out against the green shield dots!",
            },
            "high_school": {
                "headline": "Basic ($R_0$) vs. Effective ($R_t$) Reproduction Number & Epidemic Peak",
                "body": (
                    "The fate of an outbreak hinges on the **Effective Reproduction Number** $R_t = R_0 (1 - d)(1 - v)$, "
                    "where $R_0 = \\beta / \\gamma$.\n\n"
                    "• **$R_t > 1$ (Supercritical)**: Each case infects more than 1 new person; $I(t)$ grows exponentially.\n"
                    "• **$R_t < 1$ (Subcritical Containment)**: Chains die out geometrically; the critical **Herd Immunity Threshold** is $v_c = 1 - 1/R_0$."
                ),
                "try_this": "Watch the stacked SEIR chart on the right as you raise Vaccination above v_c = 1 − 1/R₀!",
            },
            "engineer": {
                "headline": "Compartmental SEIR Dynamical System & Bifurcation at $R_t = 1$",
                "body": (
                    "The mean-field compartmental ODEs governing Susceptible ($S$), Exposed ($E$), Infectious ($I$), and Recovered/Vaccinated ($R$) fractions are:\n\n"
                    "$$\\frac{dS}{dt} = -\\beta(1-d)\\frac{S I}{N}, \\quad "
                    "\\frac{dE}{dt} = \\beta(1-d)\\frac{S I}{N} - \\sigma E, \\quad "
                    "\\frac{dI}{dt} = \\sigma E - \\gamma I, \\quad "
                    "\\frac{dR}{dt} = \\gamma I$$\n\n"
                    "Infection peaks when $\\frac{dI}{dt} = 0$, corresponding to $S/N = 1 / [R_0(1-d)]$."
                ),
                "try_this": "Bring the Effective Reproduction Number down to R_t < 1.00 to contain the outbreak and complete the quest!",
            },
        },
        "quest": {
            "id": "quest-epidemic-contain",
            "title": "Epidemic Containment Commander (R_t < 1.00)",
            "prompt": "Combine vaccination (v%) and mobility reduction (d%) to drive the Effective Reproduction Number below R_t < 1.00.",
            "hint": "Increase Vaccination Rate to ≥ 60% and Mobility Reduction to ≥ 35%!",
            "target_metric": "R_t < 1.00",
            "badge_name": "Epidemiology Guardian",
            "xp": 150,
            "solve_params": {"transmission_prob": 0.34, "recovery_rate": 0.20, "vaccination_rate": 66.0, "social_distancing": 40.0, "incubation_days": 3.0},
        },
    },

    # =========================================================================
    # 16. neural-backprop — Deep Neural Network Decision Boundary & Gradient Flow
    # =========================================================================
    {
        "id": "neural-backprop",
        "engine_id": "neural-backprop",
        "engine_class": "NeuralBackpropEngine",
        "number": 16,
        "title": "Deep Neural Network Decision Boundary & Gradient Flow",
        "short_title": "Neural Net Backprop",
        "category": "Complex Systems & AI",
        "icon": "🧠",
        "accent_color": "#ec4899",
        "tagline": "Live in-browser multi-layer perceptron training via backpropagation on 2D XOR/ring/spiral manifolds with 2D probability heatmap, animated synapse weights, and loss curve.",
        "keywords": [
            "neural network", "ai", "machine learning", "deep learning", "backpropagation", "gradient descent",
            "neuron", "activation", "relu", "tanh", "sigmoid", "decision boundary", "xor", "classification",
        ],
        "canvas_hint": "Click anywhere on the 2D decision heatmap to add custom training data points (hold Shift+Click for Pink Class 0)!",
        "parameters": [
            {
                "id": "hidden_neurons",
                "label": "Hidden Layer Neurons (H)",
                "symbol": "H",
                "unit": "neurons",
                "min": 2,
                "max": 16,
                "step": 1,
                "default": 8,
                "description": "Width of the hidden representation layer (2 → H → 1 architecture).",
            },
            {
                "id": "learning_rate",
                "label": "SGD Learning Rate (η)",
                "symbol": "η",
                "unit": "",
                "min": 0.02,
                "max": 0.50,
                "step": 0.02,
                "default": 0.18,
                "description": "Gradient descent step size multiplying −∇L(W).",
            },
            {
                "id": "dataset_type",
                "label": "2D Manifold Dataset",
                "symbol": "𝒟",
                "unit": "mode",
                "min": 1,
                "max": 3,
                "step": 1,
                "default": 2,
                "description": "1 = Nonlinear XOR Quadrants, 2 = Concentric Rings, 3 = Interleaved Twin Spirals.",
            },
            {
                "id": "activation_fn",
                "label": "Activation Function (σ)",
                "symbol": "σ",
                "unit": "fn",
                "min": 1,
                "max": 3,
                "step": 1,
                "default": 1,
                "description": "1 = Smooth tanh(z), 2 = Piecewise-Linear ReLU(z), 3 = Logistic Sigmoid(z).",
            },
            {
                "id": "regularization",
                "label": "L2 Weight Decay (λ)",
                "symbol": "λ",
                "unit": "",
                "min": 0.000,
                "max": 0.030,
                "step": 0.002,
                "default": 0.004,
                "description": "Tikhonov L2 penalty λ‖W‖² preventing extreme weight saturation.",
            },
        ],
        "presets": [
            {
                "id": "concentric-rings",
                "name": "Concentric Rings Classifier (H = 8)",
                "description": "8 tanh hidden neurons wrap a closed nonlinear boundary around the inner class.",
                "params": {"hidden_neurons": 8, "learning_rate": 0.22, "dataset_type": 2, "activation_fn": 1, "regularization": 0.002},
            },
            {
                "id": "classic-xor",
                "name": "Minsky-Papert XOR Solution (ReLU)",
                "description": "Solves the famous non-linearly separable XOR problem with crisp ReLU folds.",
                "params": {"hidden_neurons": 8, "learning_rate": 0.24, "dataset_type": 1, "activation_fn": 2, "regularization": 0.002},
            },
            {
                "id": "twin-spirals-deep",
                "name": "Twin Interleaved Spirals (H = 14)",
                "description": "High-capacity hidden layer carves a winding spiral decision channel.",
                "params": {"hidden_neurons": 14, "learning_rate": 0.28, "dataset_type": 3, "activation_fn": 1, "regularization": 0.001},
            },
            {
                "id": "underfit-bottleneck",
                "name": "Underfitting Bottleneck (H = 2 Neurons)",
                "description": "With only 2 hidden neurons, the network lacks enough hyperplane folds to enclose a ring!",
                "params": {"hidden_neurons": 2, "learning_rate": 0.12, "dataset_type": 2, "activation_fn": 3, "regularization": 0.020},
            },
        ],
        "formula": {
            "name": "MLP Forward Pass, Binary Cross-Entropy & Backpropagation",
            "symbolic": "ŷ = s(W₂ · σ(W₁·x + b₁) + b₂)    |    W ← (1 − η·λ)W − η · ∂L_BCE / ∂W",
            "variables": "H = hidden neurons, η = learning rate, σ = activation function, λ = L2 regularization, L_BCE = cross-entropy loss",
        },
        "tiers": {
            "eli7": {
                "headline": "How a Computer Brain Learns by Folding Colored Paper!",
                "body": (
                    "Imagine blue dots and pink dots mixed together in a ring on a sheet of paper. With a single straight "
                    "ruler, you can **never** draw one straight line that separates the inside ring from the outside ring!\n\n"
                    "Each **Hidden Neuron** in a Neural Network is like making one crease in the paper. With 8 or 12 neurons, "
                    "the network folds the space into a circle or spiral, nudging its lines every frame (**Gradient Descent**) "
                    "whenever it guesses a dot's color wrong!"
                ),
                "try_this": "Compare 'Underfitting Bottleneck (H=2)' where the network gets stuck with 2 lines vs 'Concentric Rings (H=8)'!",
            },
            "high_school": {
                "headline": "Non-Linear Separability, Activation Functions & Gradient Descent",
                "body": (
                    "A single linear perceptron $z = w_1 x_1 + w_2 x_2 + b$ can only slice the 2D plane with a **straight line**. "
                    "To solve XOR, rings, or spirals, we stack $H$ hidden neurons with a nonlinear **activation function** $\\sigma(z)$.\n\n"
                    "• **Why Nonlinearity Matters**: Without $\\sigma(z)$, multiplying matrices $W_2(W_1 \\mathbf{x})$ collapses into another straight line!\n"
                    "• **Backpropagation**: On every step, the network measures its prediction error ($\\mathcal{L}_{\\text{BCE}}$) and shifts every synapse along $-\\eta \\nabla \\mathcal{L}$."
                ),
                "try_this": "Switch Activation Function (σ) between 1 (smooth curved tanh) and 2 (sharp polygon ReLU edges)!",
            },
            "engineer": {
                "headline": "Universal Approximation, Chain-Rule Backprop & Tikhonov Regularization",
                "body": (
                    "For input $\\mathbf{x} \\in \\mathbb{R}^2$, hidden pre-activations $\\mathbf{z}_1 = \\mathbf{W}_1 \\mathbf{x} + \\mathbf{b}_1 \\in \\mathbb{R}^H$, "
                    "$\\mathbf{h} = \\sigma(\\mathbf{z}_1)$, and output $\\hat{y} = \\text{sigmoid}(\\mathbf{w}_2^\\top \\mathbf{h} + b_2)$, we minimize regularized Binary Cross-Entropy:\n\n"
                    "$$\\mathcal{L}(\\Theta) = -\\frac{1}{N}\\sum_{i=1}^{N} \\Big[y_i \\ln \\hat{y}_i + (1-y_i)\\ln(1-\\hat{y}_i)\\Big] + \\frac{\\lambda}{2}\\left(\\|\\mathbf{W}_1\\|_F^2 + \\|\\mathbf{w}_2\\|_2^2\\right)$$\n\n"
                    "Output residual $\\delta_2 = \\hat{y} - y$ propagates backward to $\\boldsymbol{\\delta}_1 = (\\mathbf{w}_2 \\delta_2) \\odot \\sigma'(\\mathbf{z}_1)$ at 60 FPS."
                ),
                "try_this": "Configure H ≥ 10 and η ≥ 0.20 so Classification Accuracy climbs above 92%!",
            },
        },
        "quest": {
            "id": "quest-nn-accuracy",
            "title": "Universal Approximator (Classification Accuracy ≥ 92%)",
            "prompt": "Configure hidden capacity H, learning rate η, and activation σ to achieve ≥ 92% classification accuracy on the active dataset.",
            "hint": "Use Hidden Neurons H ≥ 10, Learning Rate η ≥ 0.22, and low L2 Regularization λ ≤ 0.004!",
            "target_metric": "accuracy ≥ 92%",
            "badge_name": "Backprop Architect",
            "xp": 150,
            "solve_params": {"hidden_neurons": 12, "learning_rate": 0.28, "dataset_type": 2, "activation_fn": 1, "regularization": 0.002},
        },
    },
]

LABS_BY_ID: dict[str, dict[str, Any]] = {lab["id"]: lab for lab in LABS}

# Backward-compatible aliases so any old bookmark/query still resolves cleanly
LEGACY_ID_ALIASES: dict[str, str] = {
    "aerodynamics-wind-tunnel": "airfoil-wind-tunnel",
    "epidemic-contagion-sir": "epidemic-seir",
    "wave-interference-doppler": "wave-interference",
    "neural-network-playground": "neural-backprop",
}


FEATURED_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "q-slingshot",
        "question": "How did Voyager use Jupiter's gravity as a slingshot to reach outer space?",
        "lab_id": "orbital-mechanics",
        "category": "Astrophysics",
        "recommended_params": {"star_mass": 1.1, "launch_speed": 39.5, "orbital_radius": 0.75, "jupiter_mass": 4.5, "time_warp": 1.5},
    },
    {
        "id": "q-curveball",
        "question": "How does a spinning baseball curveball swerve or an airplane wing stall?",
        "lab_id": "airfoil-wind-tunnel",
        "category": "Fluid & Aero",
        "recommended_params": {"angle_of_attack": 2.0, "wind_speed": 42.0, "spin_rpm": 2400.0, "air_density": 1.225, "camber": 0.0},
    },
    {
        "id": "q-butterfly",
        "question": "Why does a 0.001° difference make a double pendulum completely unpredictable?",
        "lab_id": "double-pendulum-chaos",
        "category": "Chaos & Math",
        "recommended_params": {"initial_angle_1": 138.0, "initial_angle_2": 146.0, "mass_ratio": 1.0, "gravity_g": 9.81, "delta_theta_deg": 0.002},
    },
    {
        "id": "q-prism-rainbow",
        "question": "How does a glass prism split white laser light into a full rainbow spectrum?",
        "lab_id": "geometric-optics",
        "category": "Quantum & Optics",
        "recommended_params": {"beam_angle": 8.0, "lens_power": 2.5, "refractive_index": 1.70, "cauchy_dispersion": 2.8, "prism_apex": 60.0},
    },
    {
        "id": "q-cyclotron",
        "question": "Why do charged particles spiral in circles inside a magnetic field?",
        "lab_id": "electromagnetic-fields",
        "category": "Electromagnetism & Circuits",
        "recommended_params": {"charge_q1": 2.5, "charge_q2": -2.5, "magnetic_b": 2.0, "dipole_sep": 14.0, "beam_energy": 38.0},
    },
    {
        "id": "q-quantum-tunnel",
        "question": "How can a quantum electron tunnel straight through a solid energy barrier?",
        "lab_id": "quantum-tunneling",
        "category": "Quantum & Optics",
        "recommended_params": {"packet_energy": 5.6, "barrier_height": 6.5, "barrier_width": 0.35, "packet_sigma": 0.75, "effective_mass": 0.45},
    },
    {
        "id": "q-piston-gas",
        "question": "Why does compressing gas with a piston spike its pressure and Maxwell speed curve?",
        "lab_id": "thermodynamics-gas",
        "category": "Fluid & Aero",
        "recommended_params": {"temperature_k": 760.0, "piston_volume": 42.0, "particle_count": 210, "molecular_mass": 20.0, "adiabatic_gamma": 1.40},
    },
    {
        "id": "q-karman-vortex",
        "question": "What creates a swirling Kármán vortex street behind an obstacle in a fluid?",
        "lab_id": "fluid-vortex-tunnel",
        "category": "Fluid & Aero",
        "recommended_params": {"reynolds_number": 240.0, "inflow_velocity": 3.2, "obstacle_diameter": 8.5, "vorticity_confinement": 3.8, "dye_injection": 1.8},
    },
    {
        "id": "q-sonic-boom",
        "question": "What happens when a supersonic jet flies faster than the speed of sound (Mach > 1)?",
        "lab_id": "wave-interference",
        "category": "Quantum & Optics",
        "recommended_params": {"frequency_hz": 300.0, "source_separation": 0.0, "source_velocity": 1.25, "phase_diff": 0.0, "harmonics_count": 4},
    },
    {
        "id": "q-truss-bridge",
        "question": "How do triangles in a steel truss bridge carry heavy loads without buckling?",
        "lab_id": "structural-truss",
        "category": "Fluid & Aero",
        "recommended_params": {"vehicle_load": 240.0, "youngs_modulus": 220.0, "truss_depth": 9.5, "beam_area": 70.0, "seismic_amp": 0.04},
    },
    {
        "id": "q-rlc-resonance",
        "question": "How does an AC RLC circuit lock onto resonance when inductive and capacitive reactance cancel?",
        "lab_id": "rlc-circuit-resonance",
        "category": "Electromagnetism & Circuits",
        "recommended_params": {"drive_freq_hz": 159.0, "resistance_ohm": 12.0, "inductance_mh": 50.0, "capacitance_uf": 20.0, "source_voltage": 24.0},
    },
    {
        "id": "q-black-hole-lens",
        "question": "How does a black hole warp spacetime to bend starlight into an Einstein ring?",
        "lab_id": "relativistic-lensing",
        "category": "Astrophysics",
        "recommended_params": {"bh_mass": 12.0, "impact_param": 2.68, "beam_spread": 2.2, "grid_tilt": 42.0, "accretion_spin": 0.75},
    },
    {
        "id": "q-fourier-epicycles",
        "question": "How can a chain of spinning Fourier epicycle circles draw any complex shape?",
        "lab_id": "fourier-epicycles",
        "category": "Chaos & Math",
        "recommended_params": {"epicycle_count": 40, "shape_preset": 1, "cycle_speed": 1.0, "trail_persistence": 95.0, "harmonic_filter": 1.0},
    },
    {
        "id": "q-ants",
        "question": "How do blind ants find the shortest path around an obstacle without a leader?",
        "lab_id": "ant-colony-swarm",
        "category": "Complex Systems & AI",
        "recommended_params": {"ant_count": 200, "evaporation_rate": 3.5, "pheromone_strength": 3.8, "exploration_noise": 0.16, "obstacle_preset": 1},
    },
    {
        "id": "q-herd-immunity",
        "question": "What happens if we vaccinate 65% of a city before a contagious virus arrives?",
        "lab_id": "epidemic-seir",
        "category": "Complex Systems & AI",
        "recommended_params": {"transmission_prob": 0.36, "recovery_rate": 0.18, "vaccination_rate": 66.0, "social_distancing": 30.0, "incubation_days": 3.0},
    },
    {
        "id": "q-neural-xor",
        "question": "How do hidden neurons let a neural network classify concentric rings or spirals?",
        "lab_id": "neural-backprop",
        "category": "Complex Systems & AI",
        "recommended_params": {"hidden_neurons": 12, "learning_rate": 0.26, "dataset_type": 2, "activation_fn": 1, "regularization": 0.002},
    },
]
