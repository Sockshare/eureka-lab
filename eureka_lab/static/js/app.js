/**
 * Eureka Lab — Frontend Controller for 16 Unique Concepts (1-to-1 Simulation Engines),
 * Category/Search Concept Selector, 3-Tier Adaptive Explanation Engine & Live Formula Sync.
 */
(function () {
  "use strict";

  const LOGICAL_W = 880;
  const LOGICAL_H = 480;

  const state = {
    labs: [],
    labsById: {},
    categories: [
      "Astrophysics",
      "Fluid & Aero",
      "Quantum & Optics",
      "Electromagnetism & Circuits",
      "Chaos & Math",
      "Complex Systems & AI",
    ],
    activeCategoryFilter: "ALL",
    searchQuery: "",
    featuredQuestions: [],
    activeLabId: "orbital-mechanics",
    activeTier: "high_school",
    currentParams: {},
    customTiersOverride: null,
    running: true,
    solvedQuests: {},
    xp: 150,
    snapshots: [],
    lastComputeTs: 0,
  };

  // Optimal Quest-Solving Parameter Presets for all 16 unique concepts
  const QUEST_SOLVE_PARAMS = {
    "orbital-mechanics": { star_mass: 1.0, launch_speed: 29.8, orbital_radius: 1.0, jupiter_mass: 0.5, time_warp: 1.25 },
    "airfoil-wind-tunnel": { angle_of_attack: 18.5, wind_speed: 52.0, spin_rpm: 1200.0, air_density: 1.225, camber: 5.5 },
    "double-pendulum-chaos": { initial_angle_1: 158.0, initial_angle_2: 154.0, mass_ratio: 1.2, gravity_g: 9.81, delta_theta_deg: 0.002 },
    "geometric-optics": { beam_angle: 8.0, lens_power: 3.5, refractive_index: 1.72, cauchy_dispersion: 2.8, prism_apex: 62.0 },
    "electromagnetic-fields": { charge_q1: 3.0, charge_q2: -3.0, magnetic_b: 2.0, dipole_sep: 12.0, beam_energy: 36.0 },
    "quantum-tunneling": { packet_energy: 5.8, barrier_height: 6.4, barrier_width: 0.35, packet_sigma: 0.80, effective_mass: 0.45 },
    "thermodynamics-gas": { temperature_k: 820.0, piston_volume: 42.0, particle_count: 220, molecular_mass: 20.0, adiabatic_gamma: 1.40 },
    "fluid-vortex-tunnel": { reynolds_number: 280.0, inflow_velocity: 3.6, obstacle_diameter: 8.0, vorticity_confinement: 4.0, dye_injection: 1.8 },
    "wave-interference": { frequency_hz: 300.0, source_separation: 0.0, source_velocity: 1.25, phase_diff: 0.0, harmonics_count: 5 },
    "structural-truss": { vehicle_load: 200.0, youngs_modulus: 240.0, truss_depth: 10.0, beam_area: 75.0, seismic_amp: 0.02 },
    "rlc-circuit-resonance": { drive_freq_hz: 159.0, resistance_ohm: 12.0, inductance_mh: 50.0, capacitance_uf: 20.0, source_voltage: 24.0 },
    "relativistic-lensing": { bh_mass: 12.0, impact_param: 2.68, beam_spread: 1.8, grid_tilt: 42.0, accretion_spin: 0.75 },
    "fourier-epicycles": { epicycle_count: 42, shape_preset: 1, cycle_speed: 1.0, trail_persistence: 95.0, harmonic_filter: 1.0 },
    "ant-colony-swarm": { ant_count: 220, evaporation_rate: 4.0, pheromone_strength: 4.2, exploration_noise: 0.12, obstacle_preset: 1 },
    "epidemic-seir": { transmission_prob: 0.34, recovery_rate: 0.20, vaccination_rate: 66.0, social_distancing: 40.0, incubation_days: 3.0 },
    "neural-backprop": { hidden_neurons: 12, learning_rate: 0.28, dataset_type: 2, activation_fn: 1, regularization: 0.002 },
  };

  function cleanMathTex(tex) {
    return tex
      .replace(/\\text\{([^}]+)\}/g, "$1")
      .replace(/\\mathbf\{([^}]+)\}/g, "$1")
      .replace(/\\boldsymbol\{([^}]+)\}/g, "$1")
      .replace(/\\mathcal\{L\}/g, "ℒ")
      .replace(/\\mathcal\{N\}/g, "𝒩")
      .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, "($1)/($2)")
      .replace(/\\sqrt\{([^}]+)\}/g, "√($1)")
      .replace(/\\hat\{([^}]+)\}/g, "$1̂")
      .replace(/\\bar\{([^}]+)\}/g, "$1̄")
      .replace(/\\dot\{\\theta\}/g, "θ̇")
      .replace(/\\ddot\{\\theta\}/g, "θ̈")
      .replace(/\\ddot\{\\mathbf\{r\}\}/g, "r̈")
      .replace(/\\alpha/g, "α")
      .replace(/\\beta/g, "β")
      .replace(/\\gamma/g, "γ")
      .replace(/\\Gamma/g, "Γ")
      .replace(/\\delta/g, "δ")
      .replace(/\\Delta/g, "Δ")
      .replace(/\\varepsilon/g, "ε")
      .replace(/\\eta/g, "η")
      .replace(/\\theta/g, "θ")
      .replace(/\\Theta/g, "Θ")
      .replace(/\\kappa/g, "κ")
      .replace(/\\lambda/g, "λ")
      .replace(/\\mu/g, "μ")
      .replace(/\\nu/g, "ν")
      .replace(/\\pi/g, "π")
      .replace(/\\rho/g, "ρ")
      .replace(/\\sigma/g, "σ")
      .replace(/\\tau/g, "τ")
      .replace(/\\phi/g, "φ")
      .replace(/\\Phi/g, "Φ")
      .replace(/\\psi/g, "ψ")
      .replace(/\\Psi/g, "Ψ")
      .replace(/\\omega/g, "ω")
      .replace(/\\Omega/g, "Ω")
      .replace(/\\hbar/g, "ℏ")
      .replace(/\\infty/g, "∞")
      .replace(/\\nabla/g, "∇")
      .replace(/\\partial/g, "∂")
      .replace(/\\oint/g, "∮")
      .replace(/\\sum/g, "∑")
      .replace(/\\cdot/g, "·")
      .replace(/\\times/g, "×")
      .replace(/\\odot/g, "⊙")
      .replace(/\\ge/g, "≥")
      .replace(/\\le/g, "≤")
      .replace(/\\gg/g, "≫")
      .replace(/\\ll/g, "≪")
      .replace(/\\ne/g, "≠")
      .replace(/\\approx/g, "≈")
      .replace(/\\propto/g, "∝")
      .replace(/\\pm/g, "±")
      .replace(/\\mp/g, "∓")
      .replace(/\\to/g, "→")
      .replace(/\\ln/g, "ln")
      .replace(/\\sin/g, "sin")
      .replace(/\\cos/g, "cos")
      .replace(/\\sinh/g, "sinh")
      .replace(/\\arcsin/g, "arcsin")
      .replace(/\\arctan/g, "arctan")
      .replace(/\\exp/g, "exp")
      .replace(/\\min/g, "min")
      .replace(/\\max/g, "max")
      .replace(/\\circ/g, "°")
      .replace(/\\,/g, " ")
      .replace(/\\!/g, "")
      .replace(/\\Big\[/g, "[")
      .replace(/\\Big\]/g, "]")
      .replace(/\\left/g, "")
      .replace(/\\right/g, "")
      .replace(/\^\{([^}]+)\}/g, "^($1)")
      .replace(/_\{([^}]+)\}/g, "_$1");
  }

  function formatMarkdownText(raw) {
    if (!raw) return "";
    const paragraphs = String(raw).split(/\n\n+/);
    return paragraphs
      .map((p) => {
        let html = p
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
          .replace(/\*(.+?)\*/g, "<em>$1</em>")
          .replace(/`([^`]+)`/g, "<code>$1</code>")
          .replace(/\$\$(.+?)\$\$/g, (_, m) => `<div class="math-chip">${cleanMathTex(m)}</div>`)
          .replace(/\$(.+?)\$/g, (_, m) => `<span class="math-chip">${cleanMathTex(m)}</span>`)
          .replace(/\n/g, "<br/>");
        return `<p>${html}</p>`;
      })
      .join("");
  }

  async function bootstrap() {
    const res = await fetch("/api/labs");
    const data = await res.json();
    state.labs = data.labs || [];
    state.labs.forEach((l) => {
      state.labsById[l.id] = l;
    });
    if (Array.isArray(data.categories) && data.categories.length) {
      state.categories = data.categories;
    }
    state.featuredQuestions = data.featured_questions || [];
    if (data.progress) {
      state.xp = data.progress.xp || 150;
      state.solvedQuests = data.progress.solved_quests || {};
      state.snapshots = data.progress.snapshots || [];
    }

    renderWonderRibbon();
    renderCategoryFilters();
    renderLabDock();
    renderSnapshots();
    updateTopbarStats();

    selectLab(state.labs[0]?.id || "orbital-mechanics");
    setupEventListeners();
    startAnimationLoop();
  }

  function updateTopbarStats() {
    const xpEl = document.getElementById("xp-value");
    const qEl = document.getElementById("quests-solved-count");
    if (xpEl) xpEl.textContent = String(state.xp);
    if (qEl) {
      const count = Object.keys(state.solvedQuests).length;
      qEl.textContent = `${count} / ${state.labs.length || 16}`;
    }
  }

  function renderWonderRibbon() {
    const bar = document.getElementById("featured-questions-bar");
    if (!bar) return;
    bar.innerHTML = "";
    state.featuredQuestions.forEach((fq) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "wonder-chip";
      btn.textContent = fq.question;
      btn.addEventListener("click", () => {
        const input = document.getElementById("question-input");
        if (input) input.value = fq.question;
        submitAskQuestion(fq.question);
      });
      bar.appendChild(btn);
    });
  }

  function renderCategoryFilters() {
    const bar = document.getElementById("category-filter-pills");
    if (!bar) return;
    bar.innerHTML = "";

    const allOptions = ["ALL", ...state.categories];
    allOptions.forEach((cat) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `cat-filter-btn ${state.activeCategoryFilter === cat ? "active" : ""}`;
      btn.dataset.category = cat;
      const count = cat === "ALL"
        ? state.labs.length
        : state.labs.filter((l) => l.category === cat).length;
      btn.textContent = cat === "ALL" ? `All Concepts (${count})` : `${cat} (${count})`;
      btn.addEventListener("click", () => {
        state.activeCategoryFilter = cat;
        renderCategoryFilters();
        renderLabDock();
      });
      bar.appendChild(btn);
    });
  }

  function renderLabDock() {
    const dock = document.getElementById("lab-tabs");
    if (!dock) return;
    dock.innerHTML = "";

    const q = state.searchQuery.trim().toLowerCase();
    state.labs.forEach((lab) => {
      const matchesCat = state.activeCategoryFilter === "ALL" || lab.category === state.activeCategoryFilter;
      const matchesSearch =
        !q ||
        lab.title.toLowerCase().includes(q) ||
        lab.short_title.toLowerCase().includes(q) ||
        lab.category.toLowerCase().includes(q) ||
        (lab.keywords || []).some((kw) => kw.toLowerCase().includes(q));

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `lab-tab ${lab.id === state.activeLabId ? "active" : ""} ${matchesCat && matchesSearch ? "" : "filtered-out"}`;
      btn.dataset.labId = lab.id;
      btn.dataset.engineId = lab.engine_id || lab.id;
      btn.dataset.category = lab.category;
      const isSolved = Boolean(state.solvedQuests[lab.id]);
      const numStr = String(lab.number).padStart(2, "0");
      btn.innerHTML = `
        <div class="lab-tab-top">
          <span class="lab-tab-icon">${lab.icon}</span>
          ${
            isSolved
              ? `<span class="lab-tab-quest-check" title="Quest Completed">✓ Quest</span>`
              : `<span class="lab-tab-num">#${numStr}</span>`
          }
        </div>
        <span class="lab-tab-title">${lab.short_title}</span>
        <span class="lab-tab-cat-badge">${lab.category}</span>
      `;
      btn.addEventListener("click", () => {
        state.customTiersOverride = null;
        document.getElementById("custom-question-banner")?.classList.add("hidden");
        selectLab(lab.id);
      });
      dock.appendChild(btn);
    });
  }

  function getActiveSim(labId) {
    const lab = state.labsById[labId];
    const engineKey = (lab && lab.engine_id) || labId;
    return window.EurekaSimulations[engineKey];
  }

  function selectLab(labId, overrideParams = null, keepCustomBanner = false) {
    const lab = state.labsById[labId];
    if (!lab) return;

    // Stop wave audio if switching away
    if (state.activeLabId === "wave-interference" && labId !== "wave-interference") {
      const waveSim = window.EurekaSimulations["wave-interference"];
      if (waveSim && waveSim.stopAudio) waveSim.stopAudio();
    }

    state.activeLabId = labId;
    if (!keepCustomBanner) {
      state.customTiersOverride = null;
    }

    // Initialize default or overridden parameters
    const params = {};
    lab.parameters.forEach((p) => {
      params[p.id] = overrideParams && overrideParams[p.id] !== undefined ? Number(overrideParams[p.id]) : Number(p.default);
    });
    state.currentParams = params;

    // Update Dock active state
    document.querySelectorAll(".lab-tab").forEach((el) => {
      el.classList.toggle("active", el.dataset.labId === labId);
    });

    // Update Canvas Header
    document.getElementById("active-lab-category").textContent = lab.category;
    document.getElementById("active-lab-title").textContent = lab.title;
    document.getElementById("active-lab-tagline").textContent = lab.tagline;
    document.getElementById("canvas-interaction-hint").textContent = lab.canvas_hint;
    const engBadge = document.getElementById("active-engine-badge");
    if (engBadge) {
      engBadge.textContent = `Engine: ${lab.engine_class || lab.engine_id} (1-to-1 Dedicated)`;
    }

    // Special action button (Web Audio for Wave Tank)
    const specialBtn = document.getElementById("special-action-btn");
    if (labId === "wave-interference") {
      specialBtn.classList.remove("hidden");
      specialBtn.textContent = "🔊 Web Audio Synth: OFF";
    } else {
      specialBtn.classList.add("hidden");
    }

    // Initialize Dedicated Canvas Simulation Engine
    const sim = getActiveSim(labId);
    if (sim && sim.init) {
      sim.init(state.currentParams);
    }

    renderPresets(lab);
    renderSliders(lab);
    renderExplanationTier();
    triggerComputeSync();
  }

  function renderPresets(lab) {
    const container = document.getElementById("preset-buttons");
    if (!container) return;
    container.innerHTML = "";
    (lab.presets || []).forEach((preset) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "preset-btn";
      btn.dataset.presetId = preset.id;
      btn.innerHTML = `
        <span class="preset-btn-name">${preset.name}</span>
        <span class="preset-btn-desc">${preset.description}</span>
      `;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".preset-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        applyParams(preset.params);
      });
      container.appendChild(btn);
    });
  }

  function renderSliders(lab) {
    const container = document.getElementById("parameter-sliders");
    if (!container) return;
    container.innerHTML = "";
    lab.parameters.forEach((p) => {
      const val = state.currentParams[p.id] ?? p.default;
      const item = document.createElement("div");
      item.className = "slider-item";
      item.innerHTML = `
        <div class="slider-top">
          <label class="slider-label" for="slider-${p.id}">${p.label}</label>
          <span class="slider-readout" id="readout-${p.id}">${val} ${p.unit}</span>
        </div>
        <input
          id="slider-${p.id}"
          class="slider-input"
          type="range"
          min="${p.min}"
          max="${p.max}"
          step="${p.step}"
          value="${val}"
          data-param-id="${p.id}"
          data-unit="${p.unit}"
        />
        <p class="slider-desc">${p.description}</p>
      `;
      const input = item.querySelector("input");
      input.addEventListener("input", (e) => {
        const num = Number(e.target.value);
        state.currentParams[p.id] = num;
        const readout = document.getElementById(`readout-${p.id}`);
        if (readout) readout.textContent = `${num} ${p.unit}`;
        const waveSim = window.EurekaSimulations["wave-interference"];
        if (state.activeLabId === "wave-interference" && waveSim && waveSim.audioPlaying) {
          waveSim._updateAudioNodes(state.currentParams);
        }
        triggerComputeSync();
      });
      container.appendChild(item);
    });
  }

  function applyParams(newParams) {
    const lab = state.labsById[state.activeLabId];
    if (!lab) return;
    Object.entries(newParams).forEach(([k, v]) => {
      const num = Number(v);
      state.currentParams[k] = num;
      const slider = document.getElementById(`slider-${k}`);
      if (slider) slider.value = String(num);
      const spec = lab.parameters.find((p) => p.id === k);
      const readout = document.getElementById(`readout-${k}`);
      if (readout && spec) readout.textContent = `${num} ${spec.unit}`;
    });
    const sim = getActiveSim(state.activeLabId);
    if (sim && sim.init) sim.init(state.currentParams);
    triggerComputeSync();
  }

  function renderExplanationTier() {
    const lab = state.labsById[state.activeLabId];
    if (!lab) return;
    const tiersSource = state.customTiersOverride || lab.tiers;
    const tierData = tiersSource[state.activeTier] || lab.tiers[state.activeTier];
    if (!tierData) return;

    document.querySelectorAll(".tier-tab").forEach((btn) => {
      const isAct = btn.dataset.tier === state.activeTier;
      btn.classList.toggle("active", isAct);
      btn.setAttribute("aria-selected", isAct ? "true" : "false");
    });

    document.getElementById("tier-headline").textContent = cleanMathTex(
      String(tierData.headline || "").replace(/\$/g, "")
    );
    document.getElementById("tier-body").innerHTML = formatMarkdownText(tierData.body);
    document.getElementById("tier-try-this").textContent = cleanMathTex(
      String(tierData.try_this || "").replace(/\$/g, "")
    );
  }

  async function triggerComputeSync() {
    const labId = state.activeLabId;
    const sim = getActiveSim(labId);
    const telemetry = sim && sim.getTelemetry ? sim.getTelemetry() : {};

    try {
      const res = await fetch(`/api/labs/${labId}/compute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ params: state.currentParams, telemetry }),
      });
      if (!res.ok) return;
      const data = await res.json();
      updateFormulaAndMetricsUI(data);
    } catch (_err) {
      // Ignore transient network hiccups
    }
  }

  function updateFormulaAndMetricsUI(data) {
    document.getElementById("formula-name").textContent = data.formula_name;
    document.getElementById("formula-symbolic").textContent = data.formula_symbolic;
    document.getElementById("formula-live-substitution").textContent = data.live_substitution;

    const strip = document.getElementById("metrics-strip");
    if (strip && Array.isArray(data.metrics)) {
      strip.innerHTML = data.metrics
        .map(
          (m) => `
          <div class="metric-box status-${m.status || "info"}">
            <div class="metric-label">${m.label}</div>
            <div class="metric-value">${m.value}<span class="metric-unit">${m.unit || ""}</span></div>
          </div>
        `
        )
        .join("");
    }

    if (data.quest) {
      const q = data.quest;
      const card = document.getElementById("quest-card");
      const badge = document.getElementById("quest-status-badge");
      const fill = document.getElementById("quest-progress-fill");
      document.getElementById("quest-title").textContent = q.title;
      document.getElementById("quest-prompt").textContent = q.prompt;
      document.getElementById("quest-hint").textContent = `💡 Hint: ${q.hint}`;

      const isSolved = Boolean(q.solved || state.solvedQuests[state.activeLabId]);
      card.classList.toggle("quest-solved", isSolved);
      badge.textContent = isSolved ? `🏆 Solved (+${q.xp} XP)` : `${q.progress_pct}% Toward Goal`;
      fill.style.width = `${isSolved ? 100 : q.progress_pct}%`;
    }

    if (data.progress) {
      const prevSolvedCount = Object.keys(state.solvedQuests).length;
      state.xp = data.progress.xp;
      state.solvedQuests = data.progress.solved_quests || {};
      updateTopbarStats();
      if (Object.keys(state.solvedQuests).length !== prevSolvedCount) {
        renderLabDock();
      }
    }
  }

  async function submitAskQuestion(questionText) {
    const q = (questionText || "").trim();
    if (!q) return;

    const btn = document.getElementById("ask-btn");
    const origText = btn.textContent;
    btn.textContent = "Mapping...";

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      state.customTiersOverride = data.tiers;
      if (data.progress) {
        state.xp = data.progress.xp;
        updateTopbarStats();
      }

      const banner = document.getElementById("custom-question-banner");
      document.getElementById("mapped-question-text").textContent = `“${data.question}”`;
      document.getElementById("mapped-scenario-pill").textContent = `${data.matched_lab_title} · ${data.scenario_label}`;
      banner.classList.remove("hidden");

      selectLab(data.matched_lab_id, data.recommended_params, true);
      renderExplanationTier();
    } finally {
      btn.textContent = origText;
    }
  }

  function renderSnapshots() {
    const list = document.getElementById("snapshots-list");
    const countEl = document.getElementById("snapshots-count");
    if (!list) return;
    if (countEl) countEl.textContent = `${state.snapshots.length} saved`;
    if (!state.snapshots.length) {
      list.innerHTML = `<p class="empty-note">Click "📸 Save Snapshot" to bookmark any interesting parameter configuration.</p>`;
      return;
    }
    list.innerHTML = "";
    state.snapshots.slice(0, 8).forEach((snap) => {
      const row = document.createElement("div");
      row.className = "snapshot-row";
      row.innerHTML = `
        <strong>${snap.title}</strong>
        <span class="panel-subtitle">${snap.lab_id}</span>
      `;
      row.addEventListener("click", () => {
        selectLab(snap.lab_id, snap.params);
      });
      list.appendChild(row);
    });
  }

  function setupEventListeners() {
    document.getElementById("ask-form")?.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = document.getElementById("question-input");
      submitAskQuestion(input.value);
    });

    document.getElementById("concept-search-input")?.addEventListener("input", (e) => {
      state.searchQuery = e.target.value || "";
      renderLabDock();
    });

    document.getElementById("dismiss-question-banner")?.addEventListener("click", () => {
      state.customTiersOverride = null;
      document.getElementById("custom-question-banner")?.classList.add("hidden");
      renderExplanationTier();
    });

    document.querySelectorAll(".tier-tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.activeTier = btn.dataset.tier;
        renderExplanationTier();
      });
    });

    const playPauseBtn = document.getElementById("play-pause-btn");
    playPauseBtn?.addEventListener("click", () => {
      state.running = !state.running;
      playPauseBtn.textContent = state.running ? "⏸ Pause" : "▶ Resume";
    });

    document.getElementById("reset-sim-btn")?.addEventListener("click", () => {
      const sim = getActiveSim(state.activeLabId);
      if (sim && sim.init) sim.init(state.currentParams);
    });

    const specialBtn = document.getElementById("special-action-btn");
    specialBtn?.addEventListener("click", () => {
      const sim = window.EurekaSimulations["wave-interference"];
      if (sim && sim.toggleAudio) {
        const playing = sim.toggleAudio(state.currentParams);
        specialBtn.textContent = playing ? "🔊 Web Audio Synth: ON" : "🔊 Web Audio Synth: OFF";
      }
    });

    document.getElementById("restore-defaults-btn")?.addEventListener("click", () => {
      const lab = state.labsById[state.activeLabId];
      if (!lab) return;
      const defaults = {};
      lab.parameters.forEach((p) => {
        defaults[p.id] = p.default;
      });
      applyParams(defaults);
    });

    document.getElementById("quest-solve-btn")?.addEventListener("click", () => {
      const lab = state.labsById[state.activeLabId];
      const solveParams = (lab && lab.quest && lab.quest.solve_params) || QUEST_SOLVE_PARAMS[state.activeLabId];
      if (solveParams) {
        applyParams(solveParams);
      }
    });

    document.getElementById("save-snapshot-btn")?.addEventListener("click", async () => {
      const lab = state.labsById[state.activeLabId];
      if (!lab) return;
      const res = await fetch("/api/snapshots", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lab_id: state.activeLabId,
          title: `${lab.short_title} (#${state.snapshots.length + 1})`,
          params: state.currentParams,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        state.snapshots = data.snapshots || [];
        state.xp = data.xp || state.xp;
        renderSnapshots();
        updateTopbarStats();
      }
    });

    const canvas = document.getElementById("sim-canvas");
    if (canvas) {
      const toCanvasCoords = (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = LOGICAL_W / rect.width;
        const scaleY = LOGICAL_H / rect.height;
        return {
          x: (e.clientX - rect.left) * scaleX,
          y: (e.clientY - rect.top) * scaleY,
        };
      };

      canvas.addEventListener("pointerdown", (e) => {
        const pt = toCanvasCoords(e);
        const sim = getActiveSim(state.activeLabId);
        if (sim && sim.onPointerDown) sim.onPointerDown(pt.x, pt.y, e);
      });
      canvas.addEventListener("pointermove", (e) => {
        const pt = toCanvasCoords(e);
        const sim = getActiveSim(state.activeLabId);
        if (sim && sim.onPointerMove) sim.onPointerMove(pt.x, pt.y, e);
      });
      window.addEventListener("pointerup", (e) => {
        const pt = toCanvasCoords(e);
        const sim = getActiveSim(state.activeLabId);
        if (sim && sim.onPointerUp) sim.onPointerUp(pt.x, pt.y, LOGICAL_W, LOGICAL_H);
      });
    }
  }

  function startAnimationLoop() {
    const canvas = document.getElementById("sim-canvas");
    const ctx = canvas.getContext("2d");
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = LOGICAL_W * dpr;
    canvas.height = LOGICAL_H * dpr;

    let lastTime = performance.now();

    function frame(now) {
      const dt = Math.min(0.04, (now - lastTime) / 1000);
      lastTime = now;

      ctx.save();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const sim = getActiveSim(state.activeLabId);
      if (sim) {
        if (state.running && sim.update) {
          sim.update(dt, state.currentParams);
        }
        if (sim.render) {
          sim.render(ctx, LOGICAL_W, LOGICAL_H, state.currentParams);
        }
      }

      ctx.restore();

      if (now - state.lastComputeTs > 2200) {
        state.lastComputeTs = now;
        triggerComputeSync();
      }

      requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
  }

  document.addEventListener("DOMContentLoaded", bootstrap);
})();
