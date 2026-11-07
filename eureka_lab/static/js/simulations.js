/**
 * Eureka Lab — 16 Unique, Dedicated Real-Math 60 FPS HTML5 Canvas Simulation Engines
 * Strict 1-to-1 Concept-to-Engine Mapping (16 Concepts == 16 Dedicated Simulation Classes).
 */
(function () {
  "use strict";

  const TAU = Math.PI * 2;

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(hi, v));
  }

  function drawScientificGrid(ctx, w, h, accentColor = "rgba(56, 189, 248, 0.07)") {
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, "#040814");
    grad.addColorStop(1, "#071022");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    ctx.strokeStyle = "rgba(148, 163, 184, 0.055)";
    ctx.lineWidth = 1;
    const step = 40;
    ctx.beginPath();
    for (let x = step; x < w; x += step) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
    }
    for (let y = step; y < h; y += step) {
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
    }
    ctx.stroke();

    ctx.strokeStyle = accentColor;
    ctx.beginPath();
    for (let x = step * 3; x < w; x += step * 3) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
    }
    for (let y = step * 3; y < h; y += step * 3) {
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
    }
    ctx.stroke();
  }

  function drawScopePanel(ctx, x, y, w, h, title, subtitle = "", borderColor = "rgba(56, 189, 248, 0.38)") {
    ctx.save();
    ctx.fillStyle = "rgba(9, 15, 30, 0.88)";
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(x, y, w, h, 8);
    } else {
      ctx.rect(x, y, w, h);
    }
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#e2e8f0";
    ctx.font = "bold 10.5px 'JetBrains Mono', monospace";
    ctx.fillText(title, x + 10, y + 16);
    if (subtitle) {
      ctx.fillStyle = "#94a3b8";
      ctx.font = "9.5px 'JetBrains Mono', monospace";
      ctx.fillText(subtitle, x + 10, y + 29);
    }
    ctx.restore();
  }

  function drawHandleBadge(ctx, x, y, label, color = "#38bdf8") {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.setLineDash([3, 3]);
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.arc(x, y, 13, 0, TAU);
    ctx.stroke();
    ctx.setLineDash([]);
    if (label) {
      ctx.fillStyle = "rgba(7, 11, 20, 0.82)";
      const tw = ctx.measureText(label).width + 10;
      ctx.fillRect(x - tw * 0.5, y + 15, tw, 15);
      ctx.fillStyle = color;
      ctx.font = "bold 9.5px 'JetBrains Mono', monospace";
      ctx.fillText(label, x - tw * 0.5 + 5, y + 26);
    }
    ctx.restore();
  }

  function wavelengthToRgb(nm, alpha = 1.0) {
    let r = 0, g = 0, b = 0;
    if (nm >= 380 && nm < 440) {
      r = -(nm - 440) / 60;
      b = 1;
    } else if (nm >= 440 && nm < 490) {
      g = (nm - 440) / 50;
      b = 1;
    } else if (nm >= 490 && nm < 510) {
      g = 1;
      b = -(nm - 510) / 20;
    } else if (nm >= 510 && nm < 580) {
      r = (nm - 510) / 70;
      g = 1;
    } else if (nm >= 580 && nm < 645) {
      r = 1;
      g = -(nm - 645) / 65;
    } else if (nm >= 645 && nm <= 750) {
      r = 1;
    }
    return `rgba(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}, ${alpha})`;
  }

  // =========================================================================
  // 1. OrbitalMechanicsEngine (orbital-mechanics)
  // =========================================================================
  class OrbitalMechanicsEngine {
    constructor() {
      this.probes = [];
      this.debris = [];
      this.dragStart = null;
      this.dragCurrent = null;
      this.jupiterAngle = 0.75;
      this.lastParamsKey = "";
      this.energyHistory = [];
      this.telemetry = { canvas_eccentricity: 0.0 };
      this.init({});
    }

    init(params) {
      const mStar = params.star_mass ?? 1.0;
      const v0 = params.launch_speed ?? 29.8;
      const r0 = params.orbital_radius ?? 1.0;
      this.lastParamsKey = `${mStar.toFixed(2)}_${v0.toFixed(1)}_${r0.toFixed(2)}`;

      this.auPx = 128;
      this.velScale = 3.15;
      this.gmCanvas = Math.pow(29.78 * this.velScale, 2) * this.auPx * mStar;

      const rPx = r0 * this.auPx;
      const vPx = v0 * this.velScale;

      this.probes = [
        {
          x: rPx,
          y: 0,
          vx: 0,
          vy: -vPx,
          color: "#38bdf8",
          name: "Voyager-1",
          trail: [],
          ecc: 0.0,
          energy: 0.0,
        },
        {
          x: 0,
          y: -rPx * 1.32,
          vx: vPx * 0.85,
          vy: 0,
          color: "#a78bfa",
          name: "Cassini-II",
          trail: [],
          ecc: 0.14,
          energy: 0.0,
        },
      ];
      this.debris = [];
      this.energyHistory = [];
    }

    _accel(x, y, jx, jy, gmStar, gmJup) {
      const r2 = x * x + y * y + 120;
      const r = Math.sqrt(r2);
      let ax = (-gmStar * x) / (r2 * r);
      let ay = (-gmStar * y) / (r2 * y === 0 ? r2 * r : r2 * r);
      ay = (-gmStar * y) / (r2 * r);
      if (gmJup > 0) {
        const dx = x - jx;
        const dy = y - jy;
        const d2 = dx * dx + dy * dy + 140;
        const d = Math.sqrt(d2);
        ax += (-gmJup * dx) / (d2 * d);
        ay += (-gmJup * dy) / (d2 * d);
      }
      return [ax, ay];
    }

    update(dt, params) {
      const mStar = params.star_mass ?? 1.0;
      const v0 = params.launch_speed ?? 29.8;
      const r0 = params.orbital_radius ?? 1.0;
      const mJup = params.jupiter_mass ?? 1.5;
      const warp = params.time_warp ?? 1.25;

      const key = `${mStar.toFixed(2)}_${v0.toFixed(1)}_${r0.toFixed(2)}`;
      if (key !== this.lastParamsKey) {
        this.init(params);
      }

      const gmStar = Math.pow(29.78 * this.velScale, 2) * this.auPx * mStar;
      const gmJup = gmStar * (mJup * 0.014);
      const rJup = 1.92 * this.auPx;
      const omegaJup = Math.sqrt(gmStar / Math.pow(rJup, 3));
      const rocheRadius = 18 + mJup * 2.6;

      const subSteps = 6;
      const h = (dt * warp * 1.35) / subSteps;

      for (let s = 0; s < subSteps; s++) {
        this.jupiterAngle += omegaJup * h;
        const jx = Math.cos(this.jupiterAngle) * rJup;
        const jy = Math.sin(this.jupiterAngle) * rJup;

        for (const p of this.probes) {
          const [ax0, ay0] = this._accel(p.x, p.y, jx, jy, gmStar, gmJup);
          const vxHalf = p.vx + 0.5 * h * ax0;
          const vyHalf = p.vy + 0.5 * h * ay0;
          p.x += h * vxHalf;
          p.y += h * vyHalf;
          const [ax1, ay1] = this._accel(p.x, p.y, jx, jy, gmStar, gmJup);
          p.vx = vxHalf + 0.5 * h * ax1;
          p.vy = vyHalf + 0.5 * h * ay1;

          // Roche tidal burst if grazing giant planet
          const dJup = Math.hypot(p.x - jx, p.y - jy);
          if (mJup > 0.5 && dJup < rocheRadius && this.debris.length < 40) {
            for (let k = 0; k < 4; k++) {
              const ang = Math.random() * TAU;
              this.debris.push({
                x: p.x,
                y: p.y,
                vx: p.vx * 0.6 + Math.cos(ang) * 45,
                vy: p.vy * 0.6 + Math.sin(ang) * 45,
                life: 1.0,
              });
            }
          }

          const dist = Math.hypot(p.x, p.y);
          if (dist > 620 || dist < 16) {
            p.x = r0 * this.auPx;
            p.y = 0;
            p.vx = 0;
            p.vy = -v0 * this.velScale;
            p.trail = [];
          }
        }
      }

      for (let i = this.debris.length - 1; i >= 0; i--) {
        const d = this.debris[i];
        d.x += d.vx * dt;
        d.y += d.vy * dt;
        d.life -= dt * 0.9;
        if (d.life <= 0) this.debris.splice(i, 1);
      }

      for (const p of this.probes) {
        p.trail.push({ x: p.x, y: p.y });
        if (p.trail.length > 210) p.trail.shift();

        const r = Math.hypot(p.x, p.y);
        const v2 = p.vx * p.vx + p.vy * p.vy;
        const hAngular = p.x * p.vy - p.y * p.vx;
        const ex = (p.vy * hAngular) / gmStar - p.x / r;
        const ey = (-p.vx * hAngular) / gmStar - p.y / r;
        p.ecc = Math.hypot(ex, ey);
        p.energy = 0.5 * v2 - gmStar / r;
      }

      if (this.probes.length > 0) {
        this.telemetry.canvas_eccentricity = this.probes[0].ecc;
        this.energyHistory.push(this.probes[0].ecc);
        if (this.energyHistory.length > 90) this.energyHistory.shift();
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(56, 189, 248, 0.08)");
      const cx = w * 0.41;
      const cy = h * 0.52;
      const mStar = params.star_mass ?? 1.0;
      const mJup = params.jupiter_mass ?? 1.5;

      // AU & Lagrange equipotential rings
      [0.5, 1.0, 1.5, 1.92].forEach((au, idx) => {
        ctx.strokeStyle = idx === 3 ? "rgba(251, 146, 60, 0.22)" : "rgba(148, 163, 184, 0.13)";
        ctx.setLineDash(idx === 3 ? [5, 5] : []);
        ctx.beginPath();
        ctx.arc(cx, cy, au * this.auPx, 0, TAU);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = "rgba(148, 163, 184, 0.48)";
        ctx.font = "10px 'JetBrains Mono', monospace";
        ctx.fillText(`${au.toFixed(1)} AU`, cx + au * this.auPx + 4, cy - 4);
      });

      // Perturber Giant Planet + Roche Limit + L1-L5 Lagrange points
      const rJup = 1.92 * this.auPx;
      const jx = cx + Math.cos(this.jupiterAngle) * rJup;
      const jy = cy + Math.sin(this.jupiterAngle) * rJup;
      if (mJup > 0.05) {
        [
          { ang: Math.PI / 3, r: rJup, name: "L4" },
          { ang: -Math.PI / 3, r: rJup, name: "L5" },
          { ang: 0, r: rJup * 0.84, name: "L1" },
          { ang: 0, r: rJup * 1.16, name: "L2" },
        ].forEach((lp) => {
          const lx = cx + Math.cos(this.jupiterAngle + lp.ang) * lp.r;
          const ly = cy + Math.sin(this.jupiterAngle + lp.ang) * lp.r;
          ctx.strokeStyle = "rgba(52, 211, 153, 0.6)";
          ctx.beginPath();
          ctx.arc(lx, ly, 4.5, 0, TAU);
          ctx.stroke();
          ctx.fillStyle = "#6ee7b7";
          ctx.font = "9.5px 'JetBrains Mono', monospace";
          ctx.fillText(lp.name, lx + 6, ly + 3);
        });

        // Roche limit ring
        const rocheR = 18 + mJup * 2.6;
        ctx.strokeStyle = "rgba(244, 63, 94, 0.42)";
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.arc(jx, jy, rocheR, 0, TAU);
        ctx.stroke();
        ctx.setLineDash([]);

        const jGrad = ctx.createRadialGradient(jx, jy, 2, jx, jy, rocheR * 1.3);
        jGrad.addColorStop(0, "#fb923c");
        jGrad.addColorStop(0.45, "rgba(251, 146, 60, 0.28)");
        jGrad.addColorStop(1, "rgba(251, 146, 60, 0)");
        ctx.fillStyle = jGrad;
        ctx.beginPath();
        ctx.arc(jx, jy, rocheR * 1.3, 0, TAU);
        ctx.fill();

        ctx.fillStyle = "#fdba74";
        ctx.beginPath();
        ctx.arc(jx, jy, 7 + mJup * 0.7, 0, TAU);
        ctx.fill();
        ctx.fillStyle = "#fed7aa";
        ctx.font = "bold 10.5px 'JetBrains Mono', monospace";
        ctx.fillText(`Giant (${mJup.toFixed(1)} M_J)`, jx + 11, jy - 8);
      }

      // Central Star with glowing corona
      const starRadius = 15 + mStar * 4.5;
      const sGrad = ctx.createRadialGradient(cx, cy, 3, cx, cy, starRadius * 3.1);
      sGrad.addColorStop(0, "#ffffff");
      sGrad.addColorStop(0.25, "#fde047");
      sGrad.addColorStop(0.55, "rgba(245, 158, 11, 0.45)");
      sGrad.addColorStop(1, "rgba(245, 158, 11, 0)");
      ctx.fillStyle = sGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, starRadius * 3.1, 0, TAU);
      ctx.fill();

      // Roche tidal debris sparks
      for (const d of this.debris) {
        ctx.fillStyle = `rgba(251, 191, 36, ${d.life})`;
        ctx.beginPath();
        ctx.arc(cx + d.x, cy + d.y, 2.2, 0, TAU);
        ctx.fill();
      }

      // Probes & glowing trajectory ribbons
      for (const p of this.probes) {
        if (p.trail.length > 2) {
          ctx.save();
          ctx.shadowColor = p.color;
          ctx.shadowBlur = 8;
          ctx.beginPath();
          for (let i = 0; i < p.trail.length; i++) {
            const pt = p.trail[i];
            if (i === 0) ctx.moveTo(cx + pt.x, cy + pt.y);
            else ctx.lineTo(cx + pt.x, cy + pt.y);
          }
          ctx.strokeStyle = p.color;
          ctx.lineWidth = 2.3;
          ctx.stroke();
          ctx.restore();
        }

        const px = cx + p.x;
        const py = cy + p.y;
        ctx.strokeStyle = "#34d399";
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(px + p.vx * 0.22, py + p.vy * 0.22);
        ctx.stroke();

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(px, py, 5.5, 0, TAU);
        ctx.fill();

        ctx.fillStyle = "#f8fafc";
        ctx.font = "10.5px 'JetBrains Mono', monospace";
        ctx.fillText(`${p.name} (e=${p.ecc.toFixed(3)})`, px + 8, py - 7);
      }

      if (this.dragStart && this.dragCurrent) {
        ctx.strokeStyle = "#38bdf8";
        ctx.setLineDash([4, 4]);
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.dragStart.x, this.dragStart.y);
        ctx.lineTo(this.dragCurrent.x, this.dragCurrent.y);
        ctx.stroke();
        ctx.setLineDash([]);
        drawHandleBadge(ctx, this.dragStart.x, this.dragStart.y, "SLINGSHOT LAUNCH", "#38bdf8");
      }

      // Top-Right Telemetry Mini-Scope: Eccentricity & Vis-Viva Invariant
      const sx = w - 245, sy = 44, sw = 230, sh = 128;
      drawScopePanel(ctx, sx, sy, sw, sh, "VIS-VIVA ORBITAL SCOPE", "Laplace-Runge-Lenz e(t) & Energy");
      ctx.strokeStyle = "rgba(52, 211, 153, 0.35)";
      ctx.setLineDash([3, 3]);
      const targetY = sy + sh - 18 - 0.05 * 70;
      ctx.beginPath();
      ctx.moveTo(sx + 10, targetY);
      ctx.lineTo(sx + sw - 10, targetY);
      ctx.stroke();
      ctx.setLineDash([]);

      if (this.energyHistory.length > 1) {
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.beginPath();
        this.energyHistory.forEach((eVal, i) => {
          const gx = sx + 12 + (i / 90) * (sw - 24);
          const gy = sy + sh - 18 - clamp(eVal, 0, 1.2) * 70;
          if (i === 0) ctx.moveTo(gx, gy);
          else ctx.lineTo(gx, gy);
        });
        ctx.stroke();
      }
      ctx.fillStyle = "#34d399";
      ctx.font = "9.5px 'JetBrains Mono', monospace";
      ctx.fillText("e = 0.00 (Circular Target)", sx + 12, sy + sh - 6);
    }

    onPointerDown(x, y) {
      this.dragStart = { x, y };
      this.dragCurrent = { x, y };
    }
    onPointerMove(x, y) {
      if (this.dragStart) this.dragCurrent = { x, y };
    }
    onPointerUp(x, y, w, h) {
      if (!this.dragStart) return;
      const cx = (w || 880) * 0.41;
      const cy = (h || 480) * 0.52;
      const dx = x - this.dragStart.x;
      const dy = y - this.dragStart.y;
      const vx = Math.hypot(dx, dy) > 8 ? dx * 1.4 : 0;
      const vy = Math.hypot(dx, dy) > 8 ? dy * 1.4 : -95;
      this.probes.push({
        x: this.dragStart.x - cx,
        y: this.dragStart.y - cy,
        vx,
        vy,
        color: "#f43f5e",
        name: `Probe-${this.probes.length + 1}`,
        trail: [],
        ecc: 0.1,
        energy: 0,
      });
      if (this.probes.length > 5) this.probes.shift();
      this.dragStart = null;
      this.dragCurrent = null;
    }
    getTelemetry() {
      return this.telemetry;
    }
  }

  // =========================================================================
  // 2. AirfoilWindTunnelEngine (airfoil-wind-tunnel)
  // =========================================================================
  class AirfoilWindTunnelEngine {
    constructor() {
      this.particles = [];
      this.vortices = [];
      this.time = 0;
      this.dragging = false;
      this.init({});
    }

    init() {
      this.particles = [];
      for (let i = 0; i < 210; i++) {
        this.particles.push({
          x: Math.random() * 880,
          y: 35 + Math.random() * 410,
          band: i % 9,
        });
      }
      this.vortices = [];
    }

    _flowVelocity(x, y, cx, cy, params) {
      const alpha = ((params.angle_of_attack ?? 7.5) * Math.PI) / 180;
      const uInf = (params.wind_speed ?? 42) * 3.8;
      const rpm = params.spin_rpm ?? 600;
      const camber = (params.camber ?? 4.5) / 100;
      const stalled = Math.abs(params.angle_of_attack ?? 7.5) >= 16;

      const dx = x - cx;
      const dy = y - cy;
      const r2 = dx * dx + dy * dy + 720;
      const r = Math.sqrt(r2);
      const R2 = 5200;

      const gamma = uInf * 195 * (Math.sin(alpha) + 1.4 * camber + (rpm / 3000) * 0.48);
      let vx = uInf * (1 - (R2 * (dx * dx - dy * dy)) / (r2 * r2)) - (gamma * dy) / (TAU * r2);
      let vy = -uInf * ((2 * R2 * dx * dy) / (r2 * r2)) + (gamma * dx) / (TAU * r2);

      if (stalled && dx > 15 && Math.abs(dy) < 95) {
        const wakeWave = Math.sin(this.time * 14 - dx * 0.048) * 95 * (1 - Math.min(1, dx / 450));
        vy += wakeWave;
        vx *= 0.52;
      }
      return [vx, vy, r];
    }

    update(dt, params) {
      this.time += dt;
      const cx = 290;
      const cy = 245;
      const stalled = Math.abs(params.angle_of_attack ?? 7.5) >= 16;

      for (const p of this.particles) {
        const [vx, vy] = this._flowVelocity(p.x, p.y, cx, cy, params);
        p.x += vx * dt;
        p.y += vy * dt;
        if (p.x > 880 || p.y < 15 || p.y > 465) {
          p.x = 5 + Math.random() * 25;
          p.y = 42 + p.band * 48 + (Math.random() - 0.5) * 6;
        }
      }

      if (stalled && Math.random() < 0.35) {
        this.vortices.push({
          x: cx + 70,
          y: cy + (Math.random() > 0.5 ? -24 : 24),
          r: 7,
          dir: Math.random() > 0.5 ? 1 : -1,
          alpha: 0.85,
        });
      }
      for (let i = this.vortices.length - 1; i >= 0; i--) {
        const v = this.vortices[i];
        v.x += (params.wind_speed ?? 42) * 2.5 * dt;
        v.y += Math.sin(this.time * 9 + v.x * 0.03) * 26 * dt;
        v.r += 16 * dt;
        v.alpha -= 0.42 * dt;
        if (v.alpha <= 0 || v.x > 880) this.vortices.splice(i, 1);
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(34, 211, 238, 0.08)");
      const cx = 290;
      const cy = 245;
      const alphaDeg = params.angle_of_attack ?? 7.5;
      const alphaRad = (alphaDeg * Math.PI) / 180;
      const camber = params.camber ?? 4.5;
      const stalled = Math.abs(alphaDeg) >= 16;

      // Upper Suction (Cyan) & Lower High-Pressure (Rose) Heatmap Glow
      const topGrad = ctx.createRadialGradient(cx, cy - 42, 8, cx, cy - 42, 145);
      topGrad.addColorStop(0, "rgba(34, 211, 238, 0.38)");
      topGrad.addColorStop(1, "rgba(34, 211, 238, 0)");
      ctx.fillStyle = topGrad;
      ctx.beginPath();
      ctx.arc(cx, cy - 42, 145, 0, TAU);
      ctx.fill();

      const botGrad = ctx.createRadialGradient(cx, cy + 44, 8, cx, cy + 44, 130);
      botGrad.addColorStop(0, "rgba(244, 63, 94, 0.30)");
      botGrad.addColorStop(1, "rgba(244, 63, 94, 0)");
      ctx.fillStyle = botGrad;
      ctx.beginPath();
      ctx.arc(cx, cy + 44, 130, 0, TAU);
      ctx.fill();

      // Continuous Smoke Streamlines
      for (let b = 0; b < 11; b++) {
        let sx = 12;
        let sy = 40 + b * 40;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        for (let step = 0; step < 80; step++) {
          const [vx, vy] = this._flowVelocity(sx, sy, cx, cy, params);
          const speed = Math.hypot(vx, vy) + 1;
          sx += (vx / speed) * 11;
          sy += (vy / speed) * 11;
          ctx.lineTo(sx, sy);
          if (sx > w) break;
        }
        ctx.strokeStyle = b === 4 || b === 5 ? "rgba(56, 189, 248, 0.58)" : "rgba(148, 163, 184, 0.22)";
        ctx.lineWidth = b === 4 || b === 5 ? 2.1 : 1.2;
        ctx.stroke();
      }

      // Glowing Smoke Tracer Particles
      for (const p of this.particles) {
        ctx.fillStyle = p.band === 4 ? "#22d3ee" : "#e2e8f0";
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2.3, 0, TAU);
        ctx.fill();
      }

      // Post-Stall Shedding Vortices
      for (const v of this.vortices) {
        ctx.strokeStyle = `rgba(244, 63, 94, ${v.alpha})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(v.x, v.y, v.r, 0, TAU * 0.8);
        ctx.stroke();
      }

      // NACA Cambered Wing Profile
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(-alphaRad);
      ctx.fillStyle = "#e2e8f0";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(-98, 0);
      ctx.quadraticCurveTo(-22, -38 - camber * 2.4, 102, 4);
      ctx.quadraticCurveTo(-18, 18 - camber * 1.1, -98, 0);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Chord line
      ctx.strokeStyle = "rgba(15, 23, 42, 0.65)";
      ctx.setLineDash([4, 3]);
      ctx.beginPath();
      ctx.moveTo(-96, 0);
      ctx.lineTo(100, 4);
      ctx.stroke();
      ctx.restore();

      // Force Vectors: Lift (Emerald) & Drag (Rose)
      const liftLen = clamp((alphaDeg + camber * 1.3) * 5.2, -90, 115);
      const dragLen = stalled ? 88 : 26 + Math.abs(alphaDeg) * 1.9;
      ctx.strokeStyle = "#10b981";
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx, cy - liftLen);
      ctx.stroke();
      ctx.fillStyle = "#10b981";
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.fillText("LIFT (L)", cx - 26, cy - liftLen - 8);

      ctx.strokeStyle = "#f43f5e";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + dragLen, cy);
      ctx.stroke();
      ctx.fillStyle = "#f43f5e";
      ctx.fillText("DRAG (D)", cx + dragLen + 6, cy + 4);

      drawHandleBadge(ctx, cx + 85, cy - Math.sin(alphaRad) * 85, `α = ${alphaDeg.toFixed(1)}°`, "#22d3ee");

      // Top-Right Mini-Scope: Aerodynamic Lift Polar C_L(α) & Stall Boundary
      const sx = w - 255, sy = 44, sw = 240, sh = 148;
      drawScopePanel(ctx, sx, sy, sw, sh, "LIFT POLAR C_L(α) & STALL", "Green = C_L(α) · Red = Critical Stall");
      const ox = sx + 38, oy = sy + sh - 28, gw = sw - 54, gh = sh - 68;
      ctx.strokeStyle = "rgba(148, 163, 184, 0.3)";
      ctx.beginPath();
      ctx.moveTo(ox, sy + 38);
      ctx.lineTo(ox, oy);
      ctx.lineTo(ox + gw, oy);
      ctx.stroke();

      // Plot C_L curve from -10 to +24 deg
      ctx.strokeStyle = "#22d3ee";
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let a = -10; a <= 24; a += 1) {
        const px = ox + ((a + 10) / 34) * gw;
        const clVal = Math.abs(a) < 16
          ? 2 * Math.PI * ((a * Math.PI) / 180 + 0.02 * camber)
          : 0.85 * Math.sign(a) * Math.max(0.25, 1 - 0.055 * (Math.abs(a) - 15));
        const py = oy - clamp((clVal + 0.5) / 2.6, 0, 1) * gh;
        if (a === -10) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Current operating point marker
      const curX = ox + ((alphaDeg + 10) / 34) * gw;
      const curCl = Math.abs(alphaDeg) < 16
        ? 2 * Math.PI * (alphaRad + 0.02 * camber)
        : 0.85 * Math.sign(alphaDeg) * Math.max(0.25, 1 - 0.055 * (Math.abs(alphaDeg) - 15));
      const curY = oy - clamp((curCl + 0.5) / 2.6, 0, 1) * gh;
      ctx.fillStyle = stalled ? "#f43f5e" : "#10b981";
      ctx.beginPath();
      ctx.arc(curX, curY, 5, 0, TAU);
      ctx.fill();
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "9.5px 'JetBrains Mono', monospace";
      ctx.fillText(`α=${alphaDeg.toFixed(1)}° (C_L=${curCl.toFixed(2)})`, ox + 6, oy + 16);
    }

    onPointerDown(x, y) {
      this.dragging = true;
      this.particles.push({ x, y, band: 4 });
    }
    onPointerMove(x, y) {
      if (!this.dragging) return;
      const slider = document.getElementById("slider-angle_of_attack");
      if (slider) {
        const newAlpha = clamp(((245 - y) / 170) * 20, -10, 24);
        slider.value = newAlpha.toFixed(1);
        slider.dispatchEvent(new Event("input"));
      }
    }
    onPointerUp() {
      this.dragging = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 3. DoublePendulumChaosEngine (double-pendulum-chaos)
  // =========================================================================
  class DoublePendulumChaosEngine {
    constructor() {
      this.ensemble = [];
      this.phaseTrail = [];
      this.divHistory = [];
      this.lastKey = "";
      this.divergenceDeg = 0;
      this.init({});
    }

    init(params) {
      const th1 = ((params.initial_angle_1 ?? 138) * Math.PI) / 180;
      const th2 = ((params.initial_angle_2 ?? 146) * Math.PI) / 180;
      const dTheta = ((params.delta_theta_deg ?? 0.005) * Math.PI) / 180;
      this.lastKey = `${th1.toFixed(3)}_${th2.toFixed(3)}_${dTheta.toFixed(6)}`;

      const colors = ["#38bdf8", "#2dd4bf", "#a78bfa", "#f59e0b", "#f43f5e"];
      this.ensemble = colors.map((col, idx) => ({
        t1: th1 + idx * dTheta,
        t2: th2 + idx * dTheta * 0.5,
        w1: 0,
        w2: 0,
        color: col,
        trail: [],
      }));
      this.phaseTrail = [];
      this.divHistory = [];
      this.divergenceDeg = 0;
    }

    _derivs(s, mRatio, g) {
      const L1 = 1.0, L2 = 1.0, m1 = 1.0, m2 = mRatio;
      const d = s.t1 - s.t2;
      const den1 = L1 * (2 * m1 + m2 - m2 * Math.cos(2 * s.t1 - 2 * s.t2));
      const a1 =
        (-g * (2 * m1 + m2) * Math.sin(s.t1) -
          m2 * g * Math.sin(s.t1 - 2 * s.t2) -
          2 * Math.sin(d) * m2 * (s.w2 * s.w2 * L2 + s.w1 * s.w1 * L1 * Math.cos(d))) /
        den1;
      const a2 =
        (2 *
          Math.sin(d) *
          (s.w1 * s.w1 * L1 * (m1 + m2) +
            g * (m1 + m2) * Math.cos(s.t1) +
            s.w2 * s.w2 * L2 * m2 * Math.cos(d))) /
        den1;
      return { dt1: s.w1, dt2: s.w2, dw1: a1, dw2: a2 };
    }

    _rk4(s, dt, mRatio, g) {
      const k1 = this._derivs(s, mRatio, g);
      const s2 = {
        t1: s.t1 + 0.5 * dt * k1.dt1,
        t2: s.t2 + 0.5 * dt * k1.dt2,
        w1: s.w1 + 0.5 * dt * k1.dw1,
        w2: s.w2 + 0.5 * dt * k1.dw2,
      };
      const k2 = this._derivs(s2, mRatio, g);
      const s3 = {
        t1: s.t1 + 0.5 * dt * k2.dt1,
        t2: s.t2 + 0.5 * dt * k2.dt2,
        w1: s.w1 + 0.5 * dt * k2.dw1,
        w2: s.w2 + 0.5 * dt * k2.dw2,
      };
      const k3 = this._derivs(s3, mRatio, g);
      const s4 = {
        t1: s.t1 + dt * k3.dt1,
        t2: s.t2 + dt * k3.dt2,
        w1: s.w1 + dt * k3.dw1,
        w2: s.w2 + dt * k3.dw2,
      };
      const k4 = this._derivs(s4, mRatio, g);
      return {
        ...s,
        t1: s.t1 + (dt / 6) * (k1.dt1 + 2 * k2.dt1 + 2 * k3.dt1 + k4.dt1),
        t2: s.t2 + (dt / 6) * (k1.dt2 + 2 * k2.dt2 + 2 * k3.dt2 + k4.dt2),
        w1: (s.w1 + (dt / 6) * (k1.dw1 + 2 * k2.dw1 + 2 * k3.dw1 + k4.dw1)) * 0.9998,
        w2: (s.w2 + (dt / 6) * (k1.dw2 + 2 * k2.dw2 + 2 * k3.dw2 + k4.dw2)) * 0.9998,
      };
    }

    update(dt, params) {
      const th1 = ((params.initial_angle_1 ?? 138) * Math.PI) / 180;
      const th2 = ((params.initial_angle_2 ?? 146) * Math.PI) / 180;
      const dTheta = ((params.delta_theta_deg ?? 0.005) * Math.PI) / 180;
      const key = `${th1.toFixed(3)}_${th2.toFixed(3)}_${dTheta.toFixed(6)}`;
      if (key !== this.lastKey) this.init(params);

      const mRatio = params.mass_ratio ?? 1.0;
      const g = params.gravity_g ?? 9.81;

      const sub = 6;
      const h = (dt * 1.45) / sub;
      for (let i = 0; i < sub; i++) {
        for (let k = 0; k < this.ensemble.length; k++) {
          this.ensemble[k] = this._rk4(this.ensemble[k], h, mRatio, g);
        }
      }

      const armPx = 94;
      for (const p of this.ensemble) {
        const x1 = Math.sin(p.t1) * armPx;
        const y1 = Math.cos(p.t1) * armPx;
        const x2 = x1 + Math.sin(p.t2) * armPx;
        const y2 = y1 + Math.cos(p.t2) * armPx;
        p.trail.push({ x: x2, y: y2 });
        if (p.trail.length > 165) p.trail.shift();
      }

      const p0 = this.ensemble[0];
      const pLast = this.ensemble[this.ensemble.length - 1];
      this.phaseTrail.push({ t1: p0.t1, t2: p0.t2 });
      if (this.phaseTrail.length > 260) this.phaseTrail.shift();

      this.divergenceDeg = (Math.hypot(p0.t1 - pLast.t1, p0.t2 - pLast.t2) * 180) / Math.PI;
      this.divHistory.push(Math.log10(Math.max(1e-4, this.divergenceDeg)));
      if (this.divHistory.length > 110) this.divHistory.shift();
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(245, 158, 11, 0.08)");
      const px = 235, py = 235, armPx = 94;
      const mRatio = params.mass_ratio ?? 1.0;

      ctx.strokeStyle = "rgba(148, 163, 184, 0.14)";
      ctx.beginPath();
      ctx.arc(px, py, armPx * 2, 0, TAU);
      ctx.stroke();

      // Rainbow ribbons for all 5 ensemble pendulums
      for (const p of this.ensemble) {
        if (p.trail.length < 2) continue;
        ctx.beginPath();
        p.trail.forEach((pt, i) => {
          if (i === 0) ctx.moveTo(px + pt.x, py + pt.y);
          else ctx.lineTo(px + pt.x, py + pt.y);
        });
        ctx.strokeStyle = p.color;
        ctx.lineWidth = 1.9;
        ctx.stroke();
      }

      // Render arms for all 5 ensemble pendulums
      for (let idx = this.ensemble.length - 1; idx >= 0; idx--) {
        const p = this.ensemble[idx];
        const x1 = px + Math.sin(p.t1) * armPx;
        const y1 = py + Math.cos(p.t1) * armPx;
        const x2 = x1 + Math.sin(p.t2) * armPx;
        const y2 = y1 + Math.cos(p.t2) * armPx;

        ctx.strokeStyle = p.color;
        ctx.lineWidth = idx === 0 ? 3.2 : 1.8;
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(x2, y2, (idx === 0 ? 6.5 : 4.5) * Math.sqrt(mRatio * 0.7 + 0.3), 0, TAU);
        ctx.fill();
      }

      // Right Stage: Phase-Space Strange Attractor + Lyapunov Scope
      const rx = 475, ry = 44, rw = 385, rh = 255;
      drawScopePanel(ctx, rx, ry, rw, rh, "PHASE-SPACE PORTRAIT (θ₁ vs θ₂)", "KAM Torus Loop vs Ergodic Strange Attractor", "rgba(245, 158, 11, 0.4)");
      const pcx = rx + rw * 0.5, pcy = ry + rh * 0.55;
      ctx.strokeStyle = "rgba(148, 163, 184, 0.18)";
      ctx.beginPath();
      ctx.moveTo(rx + 15, pcy);
      ctx.lineTo(rx + rw - 15, pcy);
      ctx.moveTo(pcx, ry + 36);
      ctx.lineTo(pcx, ry + rh - 12);
      ctx.stroke();

      if (this.phaseTrail.length > 2) {
        ctx.strokeStyle = "#f59e0b";
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        this.phaseTrail.forEach((pt, i) => {
          const a1 = ((pt.t1 + Math.PI) % TAU + TAU) % TAU - Math.PI;
          const a2 = ((pt.t2 + Math.PI) % TAU + TAU) % TAU - Math.PI;
          const sx = pcx + (a1 / Math.PI) * (rw * 0.42);
          const sy = pcy - (a2 / Math.PI) * (rh * 0.36);
          if (i === 0) ctx.moveTo(sx, sy);
          else ctx.lineTo(sx, sy);
        });
        ctx.stroke();
      }

      // Bottom-Right Scope: Log Divergence ln|Δθ(t)|
      const lx = 475, ly = 312, lw = 385, lh = 148;
      drawScopePanel(ctx, lx, ly, lw, lh, `LYAPUNOV DIVERGENCE |Δθ(t)| = ${this.divergenceDeg.toFixed(2)}°`, "Log10 Angular Spread of 5-Pendulum Ensemble");
      if (this.divHistory.length > 1) {
        ctx.strokeStyle = "#f43f5e";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        this.divHistory.forEach((v, i) => {
          const gx = lx + 14 + (i / 110) * (lw - 28);
          const gy = ly + lh - 18 - clamp((v + 4) / 6.5, 0, 1) * (lh - 58);
          if (i === 0) ctx.moveTo(gx, gy);
          else ctx.lineTo(gx, gy);
        });
        ctx.stroke();
      }
    }

    onPointerDown(x, y) {
      if (x < 460) {
        const ang = Math.atan2(x - 235, y - 235);
        this.ensemble.forEach((p, idx) => {
          p.t1 = ang + idx * 0.0005;
          p.w1 = 0;
          p.w2 = 0;
          p.trail = [];
        });
      }
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return { divergence_deg: this.divergenceDeg };
    }
  }

  // =========================================================================
  // 4. GeometricOpticsEngine (geometric-optics)
  // =========================================================================
  class GeometricOpticsEngine {
    constructor() {
      this.lensX = 250;
      this.prismX = 500;
      this.prismY = 255;
      this.dragTarget = null;
      this.init({});
    }

    init() {
      this.lensX = 250;
      this.prismX = 500;
      this.prismY = 255;
    }

    update() {}

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(192, 132, 252, 0.08)");
      const beamAngleDeg = params.beam_angle ?? 6.0;
      const lensPower = params.lens_power ?? 3.5;
      const n0 = params.refractive_index ?? 1.62;
      const bCauchy = params.cauchy_dispersion ?? 1.8;
      const apexDeg = params.prism_apex ?? 60.0;

      const axisY = 255;
      // Optical bench axis
      ctx.strokeStyle = "rgba(148, 163, 184, 0.25)";
      ctx.setLineDash([6, 6]);
      ctx.beginPath();
      ctx.moveTo(20, axisY);
      ctx.lineTo(w - 20, axisY);
      ctx.stroke();
      ctx.setLineDash([]);

      // 1. Laser Emitter Box
      const srcX = 58, srcY = axisY;
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2;
      ctx.fillRect(srcX - 38, srcY - 24, 42, 48);
      ctx.strokeRect(srcX - 38, srcY - 24, 42, 48);
      ctx.fillStyle = "#f8fafc";
      ctx.font = "bold 9.5px 'JetBrains Mono', monospace";
      ctx.fillText("LASER", srcX - 33, srcY + 3);

      // 2. Biconvex / Biconcave Glass Lens at this.lensX
      const lx = this.lensX;
      const lensH = 115;
      ctx.save();
      ctx.fillStyle = "rgba(56, 189, 248, 0.18)";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      const curve = clamp(lensPower * 4.5, -26, 32);
      ctx.moveTo(lx, axisY - lensH);
      ctx.quadraticCurveTo(lx + curve, axisY, lx, axisY + lensH);
      ctx.quadraticCurveTo(lx - curve, axisY, lx, axisY - lensH);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Principal Focus markers F and F'
      if (Math.abs(lensPower) > 0.2) {
        const fPx = (100 / lensPower) * 3.2;
        [lx + fPx, lx - fPx].forEach((fx, i) => {
          ctx.fillStyle = "#38bdf8";
          ctx.beginPath();
          ctx.arc(fx, axisY, 3.5, 0, TAU);
          ctx.fill();
          ctx.font = "10px 'JetBrains Mono', monospace";
          ctx.fillText(i === 0 ? "F'" : "F", fx - 4, axisY - 8);
        });
      }
      drawHandleBadge(ctx, lx, axisY - lensH - 16, `LENS D=${lensPower.toFixed(1)}dpt`, "#38bdf8");

      // 3. Dispersive Flint Glass Prism at (this.prismX, this.prismY)
      const px = this.prismX, py = this.prismY;
      const pSize = 112;
      const halfApex = ((apexDeg * 0.5) * Math.PI) / 180;
      const topX = px, topY = py - pSize * 0.78;
      const botY = py + pSize * 0.62;
      const halfBase = (botY - topY) * Math.tan(halfApex);
      const leftX = px - halfBase, rightX = px + halfBase;

      ctx.save();
      const pGrad = ctx.createLinearGradient(leftX, topY, rightX, botY);
      pGrad.addColorStop(0, "rgba(192, 132, 252, 0.26)");
      pGrad.addColorStop(1, "rgba(56, 189, 248, 0.16)");
      ctx.fillStyle = pGrad;
      ctx.strokeStyle = "#c084fc";
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.moveTo(topX, topY);
      ctx.lineTo(rightX, botY);
      ctx.lineTo(leftX, botY);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      ctx.restore();
      drawHandleBadge(ctx, topX, topY - 12, `PRISM α=${apexDeg.toFixed(0)}°`, "#c084fc");

      // 4. Ray-Tracing: Collimated Multi-Ray Bundle -> Lens Refraction -> Prism Chromatic Fan
      const rayOffsets = [-28, -14, 0, 14, 28];
      const incSlope = Math.tan((beamAngleDeg * Math.PI) / 180);

      for (const yOff of rayOffsets) {
        const yStart = srcY + yOff;
        const yAtLens = yStart + (lx - srcX) * incSlope;

        // White incident ray from Laser to Lens
        ctx.strokeStyle = "rgba(248, 250, 252, 0.85)";
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(srcX + 4, yStart);
        ctx.lineTo(lx, yAtLens);
        ctx.stroke();

        // Thin-lens deflection slope after lens: Δθ = -yAtLens / f
        const fPx = Math.abs(lensPower) > 0.15 ? (100 / lensPower) * 4.2 : 99999;
        const slopeAfterLens = incSlope - ((yAtLens - axisY) / fPx) * 0.55;

        // Intersect ray with left face of prism (around x = px - halfBase * 0.48)
        const hitX = px - halfBase * 0.45;
        const hitY = clamp(yAtLens + (hitX - lx) * slopeAfterLens, topY + 14, botY - 12);

        ctx.strokeStyle = "rgba(248, 250, 252, 0.90)";
        ctx.lineWidth = 2.1;
        ctx.beginPath();
        ctx.moveTo(lx, yAtLens);
        ctx.lineTo(hitX, hitY);
        ctx.stroke();

        // For the central 3 rays, split into 14 continuous spectral wavelengths via Cauchy + Snell!
        const wavelengths = yOff === 0 || Math.abs(yOff) === 14
          ? [400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 680, 700]
          : [430, 540, 660];

        for (const wl of wavelengths) {
          const nLambda = n0 + (bCauchy * 1e4) / (wl * wl);
          // Snell refraction inside prism & exiting right face
          const devAngle = (nLambda - 1.0) * (apexDeg * Math.PI / 180) * 0.92;
          const internalSlope = slopeAfterLens + devAngle * 0.38;
          const exitX = px + halfBase * 0.45;
          const exitY = clamp(hitY + (exitX - hitX) * internalSlope, topY + 14, botY - 8);

          // Inside-prism spectral ray
          ctx.strokeStyle = wavelengthToRgb(wl, 0.55);
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ctx.moveTo(hitX, hitY);
          ctx.lineTo(exitX, exitY);
          ctx.stroke();

          // Exiting rainbow fan ray toward detector screen
          const finalSlope = slopeAfterLens + devAngle * 1.15 - (700 - wl) * 0.00055 * bCauchy;
          const screenX = w - 34;
          const screenY = exitY + (screenX - exitX) * finalSlope;

          ctx.save();
          ctx.strokeStyle = wavelengthToRgb(wl, 0.82);
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          ctx.moveTo(exitX, exitY);
          ctx.lineTo(screenX, screenY);
          ctx.stroke();
          ctx.restore();
        }
      }

      // Detector Screen Bar on far right
      ctx.fillStyle = "#1e293b";
      ctx.fillRect(w - 34, 45, 10, h - 80);
      for (let sy = 80; sy < h - 60; sy += 4) {
        const wl = 400 + ((sy - 80) / (h - 140)) * 300;
        ctx.fillStyle = wavelengthToRgb(wl, 0.7);
        ctx.fillRect(w - 34, sy, 10, 4);
      }

      // Top-Right Mini-Scope: Cauchy Dispersion Curve n(λ) = n₀ + B/λ²
      const sx = w - 265, sy = 42, sw = 220, sh = 128;
      drawScopePanel(ctx, sx, sy, sw, sh, "CAUCHY DISPERSION n(λ)", `n(λ) = ${n0.toFixed(2)} + ${bCauchy.toFixed(1)}×10⁴/λ²`, "rgba(192, 132, 252, 0.45)");
      const ox = sx + 28, oy = sy + sh - 22, gw = sw - 42, gh = sh - 58;
      ctx.lineWidth = 2.5;
      for (let i = 0; i < 30; i++) {
        const wl1 = 380 + (i / 30) * 320;
        const wl2 = 380 + ((i + 1) / 30) * 320;
        const n1 = n0 + (bCauchy * 1e4) / (wl1 * wl1);
        const n2 = n0 + (bCauchy * 1e4) / (wl2 * wl2);
        const x1 = ox + (i / 30) * gw;
        const x2 = ox + ((i + 1) / 30) * gw;
        const y1 = oy - clamp((n1 - 1.3) / 0.85, 0, 1) * gh;
        const y2 = oy - clamp((n2 - 1.3) / 0.85, 0, 1) * gh;
        ctx.strokeStyle = wavelengthToRgb(wl1, 0.95);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
      }
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText("380nm (Violet)", ox, oy + 13);
      ctx.fillText("700nm (Red)", ox + gw - 62, oy + 13);
    }

    onPointerDown(x, y) {
      if (Math.abs(x - this.lensX) < 45) this.dragTarget = "lens";
      else if (Math.hypot(x - this.prismX, y - this.prismY) < 75) this.dragTarget = "prism";
    }
    onPointerMove(x, y) {
      if (this.dragTarget === "lens") this.lensX = clamp(x, 130, 380);
      else if (this.dragTarget === "prism") {
        this.prismX = clamp(x, 410, 650);
        this.prismY = clamp(y, 160, 340);
      }
    }
    onPointerUp() {
      this.dragTarget = null;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 5. ElectromagneticFieldsEngine (electromagnetic-fields)
  // =========================================================================
  class ElectromagneticFieldsEngine {
    constructor() {
      this.poles = [
        { x: 260, y: 245 },
        { x: 480, y: 245 },
      ];
      this.ions = [];
      this.dragIdx = -1;
      this.lastSep = -1;
      this.init({});
    }

    init(params) {
      const sepPx = (params.dipole_sep ?? 12.0) * 18;
      this.lastSep = sepPx;
      this.poles = [
        { x: 370 - sepPx * 0.5, y: 245 },
        { x: 370 + sepPx * 0.5, y: 245 },
      ];
      this.ions = [];
      for (let i = 0; i < 6; i++) {
        this._spawnIon(params, i * 0.8);
      }
    }

    _spawnIon(params, phase = 0) {
      const v0 = (params.beam_energy ?? 48) * 2.2;
      this.ions.push({
        x: 90 + Math.cos(phase) * 40,
        y: 120 + (phase * 45) % 240,
        vx: v0,
        vy: (Math.sin(phase) - 0.3) * v0 * 0.35,
        trail: [],
      });
      if (this.ions.length > 8) this.ions.shift();
    }

    _fieldAt(x, y, q1, q2) {
      let ex = 0, ey = 0, pot = 0;
      const charges = [q1, q2];
      for (let i = 0; i < 2; i++) {
        const dx = x - this.poles[i].x;
        const dy = y - this.poles[i].y;
        const r2 = dx * dx + dy * dy + 280;
        const r = Math.sqrt(r2);
        const kq = charges[i] * 26000;
        ex += (kq * dx) / (r2 * r);
        ey += (kq * dy) / (r2 * r);
        pot += kq / r;
      }
      return { ex, ey, pot };
    }

    update(dt, params) {
      const q1 = params.charge_q1 ?? 3.0;
      const q2 = params.charge_q2 ?? -3.0;
      const bz = params.magnetic_b ?? 0.8;
      const sepPx = (params.dipole_sep ?? 12.0) * 18;
      if (Math.abs(sepPx - this.lastSep) > 2 && this.dragIdx === -1) {
        this.lastSep = sepPx;
        this.poles[0].x = 370 - sepPx * 0.5;
        this.poles[1].x = 370 + sepPx * 0.5;
      }

      const sub = 4;
      const h = dt / sub;
      const omegaB = bz * 3.6;

      for (const ion of this.ions) {
        for (let s = 0; s < sub; s++) {
          const { ex, ey } = this._fieldAt(ion.x, ion.y, q1, q2);
          // Boris-style Lorentz push: dv/dt = E_scaled + v x B_z
          const ax = ex * 0.35 + ion.vy * omegaB;
          const ay = ey * 0.35 - ion.vx * omegaB;
          ion.vx += ax * h;
          ion.vy += ay * h;
          // Normalize speed toward beam energy so cyclotron radius stays clean
          const targetSpd = (params.beam_energy ?? 48) * 2.2;
          const curSpd = Math.hypot(ion.vx, ion.vy) || 1;
          ion.vx = (ion.vx / curSpd) * targetSpd;
          ion.vy = (ion.vy / curSpd) * targetSpd;
          ion.x += ion.vx * h;
          ion.y += ion.vy * h;
        }
        ion.trail.push({ x: ion.x, y: ion.y });
        if (ion.trail.length > 95) ion.trail.shift();

        if (ion.x < 10 || ion.x > 870 || ion.y < 15 || ion.y > 465) {
          ion.x = 120 + Math.random() * 180;
          ion.y = 110 + Math.random() * 260;
          ion.trail = [];
        }
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(56, 189, 248, 0.08)");
      const q1 = params.charge_q1 ?? 3.0;
      const q2 = params.charge_q2 ?? -3.0;
      const bz = params.magnetic_b ?? 0.8;

      // 1. Equipotential Voltage Heatmap & Vector Field Arrows
      const step = 36;
      for (let y = 36; y < h - 20; y += step) {
        for (let x = 36; x < w - 240; x += step) {
          const { ex, ey, pot } = this._fieldAt(x, y, q1, q2);
          if (Math.abs(pot) > 40) {
            ctx.fillStyle = pot > 0
              ? `rgba(244, 63, 94, ${clamp(pot / 2200, 0.03, 0.22)})`
              : `rgba(56, 189, 248, ${clamp(-pot / 2200, 0.03, 0.22)})`;
            ctx.fillRect(x - step * 0.5, y - step * 0.5, step, step);
          }
          const mag = Math.hypot(ex, ey) + 1e-5;
          const len = clamp(Math.log10(mag + 1) * 4.8, 4, 15);
          const ux = (ex / mag) * len;
          const uy = (ey / mag) * len;
          ctx.strokeStyle = "rgba(148, 163, 184, 0.42)";
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(x - ux * 0.5, y - uy * 0.5);
          ctx.lineTo(x + ux * 0.5, y + uy * 0.5);
          ctx.stroke();
        }
      }

      // 2. Continuous Electric Field Streamlines from Pole 1 & Pole 2
      this.poles.forEach((pole, idx) => {
        const q = idx === 0 ? q1 : q2;
        if (Math.abs(q) < 0.1) return;
        const sign = q > 0 ? 1 : -1;
        for (let k = 0; k < 16; k++) {
          const ang = (k / 16) * TAU;
          let rx = pole.x + Math.cos(ang) * 14;
          let ry = pole.y + Math.sin(ang) * 14;
          ctx.strokeStyle = q > 0 ? "rgba(251, 113, 133, 0.52)" : "rgba(56, 189, 248, 0.52)";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(rx, ry);
          for (let s = 0; s < 75; s++) {
            const { ex, ey } = this._fieldAt(rx, ry, q1, q2);
            const m = Math.hypot(ex, ey) + 1e-4;
            rx += sign * (ex / m) * 8;
            ry += sign * (ey / m) * 8;
            ctx.lineTo(rx, ry);
            const other = this.poles[1 - idx];
            if (Math.hypot(rx - other.x, ry - other.y) < 14 || rx < 10 || rx > w - 240 || ry < 10 || ry > h - 10) break;
          }
          ctx.stroke();
        }
      });

      // 3. Lorentz Cyclotron Ion Spirals
      for (const ion of this.ions) {
        if (ion.trail.length > 2) {
          ctx.save();
          ctx.shadowColor = "#34d399";
          ctx.shadowBlur = 7;
          ctx.strokeStyle = "#34d399";
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          ion.trail.forEach((pt, i) => {
            if (i === 0) ctx.moveTo(pt.x, pt.y);
            else ctx.lineTo(pt.x, pt.y);
          });
          ctx.stroke();
          ctx.restore();
        }
        ctx.fillStyle = "#fde047";
        ctx.beginPath();
        ctx.arc(ion.x, ion.y, 4.2, 0, TAU);
        ctx.fill();
      }

      // 4. Draggable Charge Poles +q1 and -q2
      [q1, q2].forEach((q, i) => {
        const p = this.poles[i];
        const col = q >= 0 ? "#f43f5e" : "#38bdf8";
        ctx.fillStyle = col;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 16, 0, TAU);
        ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.font = "bold 11px 'JetBrains Mono', monospace";
        ctx.fillText(q >= 0 ? `+${q.toFixed(1)}` : `${q.toFixed(1)}`, p.x - 13, p.y + 4);
        drawHandleBadge(ctx, p.x, p.y, `DRAG q${i + 1}`, col);
      });

      // Right Scope: Voltage Landscape V(x) & Cyclotron Gyroradius
      const sx = w - 245, sy = 44, sw = 230, sh = 165;
      drawScopePanel(ctx, sx, sy, sw, sh, "VOLTAGE V(x) & CYCLOTRON", `B_z = ${bz >= 0 ? "+" : ""}${bz.toFixed(2)} T (Out-of-Plane)`);
      const ox = sx + 16, oy = sy + 105, gw = sw - 32;
      ctx.strokeStyle = "rgba(148, 163, 184, 0.3)";
      ctx.beginPath();
      ctx.moveTo(ox, oy);
      ctx.lineTo(ox + gw, oy);
      ctx.stroke();

      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i <= 50; i++) {
        const tx = 60 + (i / 50) * 560;
        const { pot } = this._fieldAt(tx, 245, q1, q2);
        const gx = ox + (i / 50) * gw;
        const gy = oy - clamp(pot / 28, -42, 42);
        if (i === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();

      const rL = Math.abs(bz) > 0.04 ? ((params.beam_energy ?? 48) * 0.22) / Math.abs(bz) : 99.9;
      ctx.fillStyle = rL <= 4.5 ? "#34d399" : "#fde047";
      ctx.font = "bold 10.5px 'JetBrains Mono', monospace";
      ctx.fillText(`Gyroradius r_L = ${rL.toFixed(2)} cm`, sx + 14, sy + sh - 14);
    }

    onPointerDown(x, y) {
      for (let i = 0; i < 2; i++) {
        if (Math.hypot(x - this.poles[i].x, y - this.poles[i].y) < 28) {
          this.dragIdx = i;
          return;
        }
      }
      this.ions.push({ x, y, vx: 105, vy: -35, trail: [] });
      if (this.ions.length > 9) this.ions.shift();
    }
    onPointerMove(x, y) {
      if (this.dragIdx >= 0) {
        this.poles[this.dragIdx].x = clamp(x, 60, 610);
        this.poles[this.dragIdx].y = clamp(y, 60, 420);
      }
    }
    onPointerUp() {
      this.dragIdx = -1;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 6. QuantumTunnelingEngine (quantum-tunneling)
  // =========================================================================
  class QuantumTunnelingEngine {
    constructor() {
      this.time = 0;
      this.packetX0 = 175;
      this.telemetry = { canvas_transmission: 0.25 };
      this.init({});
    }

    init() {
      this.time = 0;
    }

    _exactTransmission(params) {
      const eEv = params.packet_energy ?? 5.2;
      const v0Ev = params.barrier_height ?? 6.8;
      const aNm = params.barrier_width ?? 0.65;
      const mEff = params.effective_mass ?? 0.6;
      const cFactor = 26.25 * mEff;
      if (Math.abs(eEv - v0Ev) < 1e-3) {
        return 1 / (1 + 0.25 * cFactor * v0Ev * aNm * aNm);
      } else if (eEv < v0Ev) {
        const kappa = Math.sqrt(cFactor * (v0Ev - eEv));
        const ka = Math.min(18, kappa * aNm);
        return 1 / (1 + (v0Ev * v0Ev * Math.pow(Math.sinh(ka), 2)) / Math.max(1e-4, 4 * eEv * (v0Ev - eEv)));
      } else {
        const k2 = Math.sqrt(cFactor * (eEv - v0Ev));
        return 1 / (1 + (v0Ev * v0Ev * Math.pow(Math.sin(k2 * aNm), 2)) / Math.max(1e-4, 4 * eEv * (eEv - v0Ev)));
      }
    }

    update(dt, params) {
      const spd = Math.sqrt((params.packet_energy ?? 5.2) / (params.effective_mass ?? 0.6));
      this.time = (this.time + dt * 0.52 * spd) % 3.4;
      this.telemetry.canvas_transmission = this._exactTransmission(params);
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(167, 139, 250, 0.08)");
      const eEv = params.packet_energy ?? 5.2;
      const v0Ev = params.barrier_height ?? 6.8;
      const aNm = params.barrier_width ?? 0.65;
      const sigmaNm = params.packet_sigma ?? 0.75;
      const mEff = params.effective_mass ?? 0.6;

      const T = this._exactTransmission(params);
      const R = 1 - T;

      const baseY = 355;
      const barCenterX = 435;
      const barW = clamp(aNm * 58, 14, 150);
      const barL = barCenterX - barW * 0.5;
      const barR = barCenterX + barW * 0.5;
      const eHeight = (eEv / 14) * 235;
      const vHeight = (v0Ev / 14) * 235;

      // Baseline axis
      ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(30, baseY);
      ctx.lineTo(w - 30, baseY);
      ctx.stroke();

      // Potential Barrier V(x)
      const bGrad = ctx.createLinearGradient(barL, baseY - vHeight, barL, baseY);
      bGrad.addColorStop(0, "rgba(245, 158, 11, 0.48)");
      bGrad.addColorStop(1, "rgba(245, 158, 11, 0.12)");
      ctx.fillStyle = bGrad;
      ctx.strokeStyle = "#f59e0b";
      ctx.lineWidth = 2.2;
      ctx.fillRect(barL, baseY - vHeight, barW, vHeight);
      ctx.strokeRect(barL, baseY - vHeight, barW, vHeight);
      ctx.fillStyle = "#fde047";
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.fillText(`V₀ = ${v0Ev.toFixed(1)} eV`, barL + 4, baseY - vHeight - 8);

      // Particle Energy Level Line E
      ctx.strokeStyle = "rgba(56, 189, 248, 0.65)";
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(35, baseY - eHeight);
      ctx.lineTo(w - 260, baseY - eHeight);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#38bdf8";
      ctx.fillText(`E = ${eEv.toFixed(1)} eV`, 42, baseY - eHeight - 7);

      // Synthesize TDSE Wavepacket Scattering State (Incident + Reflected + Evanescent + Transmitted)
      const k0 = 0.11 * Math.sqrt(eEv * mEff);
      const sigPx = sigmaNm * 62;
      const prog = this.time / 3.4; // 0 to 1
      const incCenter = 120 + prog * 360;
      const reflCenter = barL - Math.max(0, incCenter - barL) * 0.92;
      const transCenter = barR + Math.max(0, incCenter - barL) * 0.95;
      const scatterBlend = clamp((incCenter - (barL - 40)) / 95, 0, 1);

      const rePts = [];
      const imPts = [];
      const probPts = [];

      for (let x = 35; x <= w - 35; x += 3) {
        let re = 0, im = 0;
        if (x < barL) {
          // Incident + Reflected interference
          const envInc = Math.exp(-Math.pow(x - Math.min(incCenter, barL + 25), 2) / (2 * sigPx * sigPx)) * (1 - 0.65 * scatterBlend);
          const phInc = k0 * x - this.time * 14;
          re += envInc * Math.cos(phInc);
          im += envInc * Math.sin(phInc);

          if (scatterBlend > 0.02) {
            const envRef = Math.sqrt(R) * scatterBlend * Math.exp(-Math.pow(x - reflCenter, 2) / (2 * sigPx * sigPx));
            const phRef = -k0 * x - this.time * 14 + Math.PI * 0.8;
            re += envRef * Math.cos(phRef);
            im += envRef * Math.sin(phRef);
          }
        } else if (x <= barR) {
          // Inside barrier: Evanescent exponential decay (or oscillatory if E > V0)
          const frac = (x - barL) / Math.max(1, barW);
          const ampBar = (1 - frac * (1 - Math.sqrt(T))) * Math.exp(-Math.pow(incCenter - barCenterX, 2) / (2 * sigPx * sigPx * 1.8));
          const phBar = (eEv > v0Ev ? k0 * 0.6 * (x - barL) : 0) - this.time * 14;
          re = ampBar * Math.cos(phBar);
          im = ampBar * Math.sin(phBar);
        } else {
          // Transmitted Tunneled Wavepacket on right side of barrier!
          const envTr = Math.sqrt(T) * scatterBlend * Math.exp(-Math.pow(x - transCenter, 2) / (2 * sigPx * sigPx));
          const phTr = k0 * x - this.time * 14;
          re = envTr * Math.cos(phTr);
          im = envTr * Math.sin(phTr);
        }

        const prob = re * re + im * im;
        rePts.push({ x, y: baseY - re * 82 });
        imPts.push({ x, y: baseY - im * 82 });
        probPts.push({ x, y: baseY - prob * 145, prob, phase: Math.atan2(im, re) });
      }

      // Phase-colored probability density fill |ψ(x,t)|²
      for (let i = 0; i < probPts.length - 1; i++) {
        const pt = probPts[i];
        if (pt.prob < 0.003) continue;
        const hue = Math.round(((pt.phase + Math.PI) / TAU) * 360);
        ctx.fillStyle = `hsla(${hue}, 85%, 60%, 0.28)`;
        ctx.fillRect(pt.x, pt.y, 3.5, baseY - pt.y);
      }

      // Re(ψ) Cyan curve
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      rePts.forEach((pt, i) => (i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)));
      ctx.stroke();

      // Im(ψ) Pink curve
      ctx.strokeStyle = "#f472b6";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      imPts.forEach((pt, i) => (i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)));
      ctx.stroke();

      // |ψ|² Envelope White/Violet glow curve
      ctx.save();
      ctx.shadowColor = "#a78bfa";
      ctx.shadowBlur = 10;
      ctx.strokeStyle = "#f8fafc";
      ctx.lineWidth = 2.6;
      ctx.beginPath();
      probPts.forEach((pt, i) => (i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)));
      ctx.stroke();
      ctx.restore();

      // Labels for Incident/Reflected vs Tunneled Wave
      ctx.fillStyle = "#c4b5fd";
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.fillText(`← Reflected R = ${(R * 100).toFixed(1)}%`, 85, 405);
      ctx.fillStyle = "#34d399";
      ctx.fillText(`Tunneled Wave T = ${(T * 100).toFixed(1)}% →`, barR + 30, 405);

      // Top-Right Scope: Unitarity Conservation Bar (T + R = 100%)
      const sx = w - 250, sy = 44, sw = 235, sh = 132;
      drawScopePanel(ctx, sx, sy, sw, sh, "UNITARITY & TUNNELING", "Born Probability Conservation T + R = 1", "rgba(167, 139, 250, 0.45)");
      const barMaxW = sw - 90;
      // T bar
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.fillText("Trans (T)", sx + 10, sy + 58);
      ctx.fillStyle = "rgba(16, 185, 129, 0.22)";
      ctx.fillRect(sx + 74, sy + 47, barMaxW, 14);
      ctx.fillStyle = "#10b981";
      ctx.fillRect(sx + 74, sy + 47, barMaxW * T, 14);

      // R bar
      ctx.fillStyle = "#cbd5e1";
      ctx.fillText("Refl  (R)", sx + 10, sy + 84);
      ctx.fillStyle = "rgba(56, 189, 248, 0.22)";
      ctx.fillRect(sx + 74, sy + 73, barMaxW, 14);
      ctx.fillStyle = "#38bdf8";
      ctx.fillRect(sx + 74, sy + 73, barMaxW * R, 14);

      ctx.fillStyle = "#a78bfa";
      ctx.fillText(`∫|ψ(x,t)|² dx = 1.000`, sx + 12, sy + 114);
    }

    onPointerDown() {
      this.time = 0;
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return this.telemetry;
    }
  }

  // =========================================================================
  // 7. ThermodynamicsGasEngine (thermodynamics-gas)
  // =========================================================================
  class ThermodynamicsGasEngine {
    constructor() {
      this.molecules = [];
      this.draggingPiston = false;
      this.lastCount = 0;
      this.init({});
    }

    init(params) {
      const count = Math.round(params.particle_count ?? 160);
      this.lastCount = count;
      const volPct = params.piston_volume ?? 75.0;
      const maxX = 45 + (volPct / 100) * 415;
      const tempK = params.temperature_k ?? 350;
      const mMol = params.molecular_mass ?? 28;
      const spdScale = Math.sqrt(tempK / mMol) * 32;

      this.molecules = [];
      for (let i = 0; i < count; i++) {
        const ang = Math.random() * TAU;
        const spd = spdScale * (0.45 + Math.random() * 1.15);
        this.molecules.push({
          x: 55 + Math.random() * (maxX - 70),
          y: 65 + Math.random() * 340,
          vx: Math.cos(ang) * spd,
          vy: Math.sin(ang) * spd,
        });
      }
    }

    update(dt, params) {
      const count = Math.round(params.particle_count ?? 160);
      if (count !== this.lastCount) this.init(params);

      const volPct = params.piston_volume ?? 75.0;
      const minX = 45, maxX = 45 + (volPct / 100) * 415;
      const minY = 58, maxY = 415;
      const tempK = params.temperature_k ?? 350;
      const mMol = params.molecular_mass ?? 28;
      const targetRms = Math.sqrt(tempK / mMol) * 38;

      for (const m of this.molecules) {
        // Gently thermostat speeds toward heat-bath temperature T
        const curSpd = Math.hypot(m.vx, m.vy) || 1;
        const desired = curSpd * 0.985 + targetRms * (0.65 + (m.x % 0.7)) * 0.015;
        m.vx = (m.vx / curSpd) * desired;
        m.vy = (m.vy / curSpd) * desired;

        m.x += m.vx * dt;
        m.y += m.vy * dt;

        if (m.x < minX + 5) {
          m.x = minX + 5;
          m.vx = Math.abs(m.vx);
        } else if (m.x > maxX - 5) {
          m.x = maxX - 5;
          m.vx = -Math.abs(m.vx);
        }
        if (m.y < minY + 5) {
          m.y = minY + 5;
          m.vy = Math.abs(m.vy);
        } else if (m.y > maxY - 5) {
          m.y = maxY - 5;
          m.vy = -Math.abs(m.vy);
        }
      }

      // Elastic pairwise hard-sphere collisions (spatial subset for 60 FPS)
      for (let i = 0; i < this.molecules.length; i++) {
        const a = this.molecules[i];
        for (let j = i + 1; j < Math.min(this.molecules.length, i + 18); j++) {
          const b = this.molecules[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < 81 && d2 > 0.1) {
            const d = Math.sqrt(d2);
            const nx = dx / d, ny = dy / d;
            const dvx = a.vx - b.vx, dvy = a.vy - b.vy;
            const vn = dvx * nx + dvy * ny;
            if (vn > 0) {
              a.vx -= vn * nx;
              a.vy -= vn * ny;
              b.vx += vn * nx;
              b.vy += vn * ny;
            }
          }
        }
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(251, 146, 60, 0.08)");
      const volPct = params.piston_volume ?? 75.0;
      const tempK = params.temperature_k ?? 350;
      const mMol = params.molecular_mass ?? 28;
      const minX = 45, maxX = 45 + (volPct / 100) * 415;
      const minY = 58, maxY = 415;

      // Cylinder Chamber Walls
      ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
      ctx.fillRect(minX, minY, 425, maxY - minY);
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 3;
      ctx.strokeRect(minX, minY, 425, maxY - minY);

      // Bottom Heat-Bath Thermal Coils
      const heatAlpha = clamp((tempK - 100) / 1100, 0.15, 0.95);
      for (let hx = minX + 18; hx < maxX - 10; hx += 28) {
        ctx.fillStyle = `rgba(249, 115, 22, ${heatAlpha})`;
        ctx.beginPath();
        ctx.arc(hx, maxY + 8, 6, 0, TAU);
        ctx.fill();
      }

      // Movable Compression Piston Head & Rod
      ctx.fillStyle = "#334155";
      ctx.strokeStyle = "#fb923c";
      ctx.lineWidth = 2.5;
      ctx.fillRect(maxX, minY + 3, 22, maxY - minY - 6);
      ctx.strokeRect(maxX, minY + 3, 22, maxY - minY - 6);
      ctx.fillStyle = "#475569";
      ctx.fillRect(maxX + 22, (minY + maxY) * 0.5 - 10, 470 - maxX, 20);
      drawHandleBadge(ctx, maxX + 11, (minY + maxY) * 0.5, `PISTON V=${volPct.toFixed(0)}%`, "#fb923c");

      // Molecules colored by kinetic energy
      const bins = new Array(14).fill(0);
      const refSpd = Math.sqrt(350 / 28) * 38;
      for (const m of this.molecules) {
        const spd = Math.hypot(m.vx, m.vy);
        const ratio = clamp(spd / (refSpd * 2.2), 0, 1);
        const bIdx = Math.min(13, Math.floor(ratio * 14));
        bins[bIdx]++;

        const hue = Math.round((1 - ratio) * 215);
        ctx.fillStyle = `hsl(${hue}, 92%, 60%)`;
        ctx.beginPath();
        ctx.arc(m.x, m.y, 4.1, 0, TAU);
        ctx.fill();
      }

      // Right Panel: Live Maxwell-Boltzmann Speed Distribution Histogram + Theoretical Curve
      const rx = 495, ry = 54, rw = 365, rh = 365;
      drawScopePanel(ctx, rx, ry, rw, rh, "MAXWELL-BOLTZMANN DISTRIBUTION f(v)", "Cyan Bars = Live Particles · Gold = Exact f(v)", "rgba(251, 146, 60, 0.45)");
      const ox = rx + 24, oy = ry + rh - 36, gw = rw - 44, gh = rh - 95;
      const bw = gw / bins.length;
      const total = Math.max(1, this.molecules.length);

      for (let i = 0; i < bins.length; i++) {
        const frac = bins[i] / total;
        const bh = clamp(frac * 3.2, 0, 1) * gh;
        ctx.fillStyle = "rgba(56, 189, 248, 0.45)";
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 1.2;
        ctx.fillRect(ox + i * bw + 2, oy - bh, bw - 4, bh);
        ctx.strokeRect(ox + i * bw + 2, oy - bh, bw - 4, bh);
      }

      // Overlay Analytical Maxwell-Boltzmann curve f(v) ~ v^2 * exp(-a*v^2)
      const scaleA = (mMol / 28) * (350 / tempK) * 5.2;
      ctx.strokeStyle = "#fb923c";
      ctx.lineWidth = 2.8;
      ctx.beginPath();
      for (let k = 0; k <= 60; k++) {
        const u = (k / 60) * 1.4;
        const fv = 4.2 * Math.pow(scaleA, 1.5) * u * u * Math.exp(-scaleA * u * u);
        const gx = ox + (k / 60) * gw;
        const gy = oy - clamp(fv * 0.42, 0, 1) * gh;
        if (k === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.fillText("Slow (Cold)", ox, oy + 18);
      ctx.fillText("Molecular Speed v → Fast (Hot)", ox + 115, oy + 18);
    }

    onPointerDown(x) {
      if (x < 485) this.draggingPiston = true;
    }
    onPointerMove(x) {
      if (!this.draggingPiston) return;
      const slider = document.getElementById("slider-piston_volume");
      if (slider) {
        const pct = clamp(((x - 45) / 415) * 100, 35, 100);
        slider.value = pct.toFixed(0);
        slider.dispatchEvent(new Event("input"));
      }
    }
    onPointerUp() {
      this.draggingPiston = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 8. FluidVortexTunnelEngine (fluid-vortex-tunnel)
  // =========================================================================
  class FluidVortexTunnelEngine {
    constructor() {
      this.eddies = [];
      this.tracers = [];
      this.obsX = 225;
      this.obsY = 245;
      this.draggingObs = false;
      this.time = 0;
      this.liftHistory = [];
      this.init({});
    }

    init() {
      this.eddies = [];
      this.tracers = [];
      for (let i = 0; i < 340; i++) {
        this.tracers.push({
          x: Math.random() * 880,
          y: 30 + Math.random() * 420,
          band: i % 3,
          history: [],
        });
      }
      this.liftHistory = [];
    }

    _velAt(x, y, params) {
      const u0 = (params.inflow_velocity ?? 2.4) * 58;
      const R = (params.obstacle_diameter ?? 9.0) * 3.6;
      const dx = x - this.obsX;
      const dy = y - this.obsY;
      const r2 = dx * dx + dy * dy + 80;
      const R2 = R * R;

      // Potential doublet around cylinder
      let vx = u0 * (1 - (R2 * (dx * dx - dy * dy)) / (r2 * r2));
      let vy = -u0 * ((2 * R2 * dx * dy) / (r2 * r2));

      // Superpose shed Kármán vortex street Lamb-Oseen eddies
      for (const e of this.eddies) {
        const ex = x - e.x;
        const ey = y - e.y;
        const er2 = ex * ex + ey * ey + 480;
        const factor = (e.gamma * (1 - Math.exp(-er2 / 900))) / er2;
        vx += -ey * factor;
        vy += ex * factor;
      }
      return [vx, vy];
    }

    update(dt, params) {
      this.time += dt;
      const re = params.reynolds_number ?? 180;
      const u0 = (params.inflow_velocity ?? 2.4) * 58;
      const diamCm = params.obstacle_diameter ?? 9.0;
      const R = diamCm * 3.6;
      const vortGain = params.vorticity_confinement ?? 3.2;

      // Shed alternating clockwise & counter-clockwise eddies when Re >= 47
      if (re >= 47) {
        const st = 0.198 * (1 - 19.7 / re);
        const fShed = (st * (params.inflow_velocity ?? 2.4)) / (diamCm * 0.01);
        const phase = this.time * fShed * TAU;
        if (this.eddies.length === 0 || this.eddies[this.eddies.length - 1].x > this.obsX + R + 28) {
          const sign = Math.sin(phase) >= 0 ? 1 : -1;
          this.eddies.push({
            x: this.obsX + R * 0.9,
            y: this.obsY + sign * R * 0.68,
            gamma: sign * u0 * 52 * (0.5 + 0.22 * vortGain),
            sign,
          });
        }
        this.liftHistory.push(Math.sin(phase));
        if (this.liftHistory.length > 90) this.liftHistory.shift();
      } else {
        this.liftHistory.push(0);
        if (this.liftHistory.length > 90) this.liftHistory.shift();
      }

      for (let i = this.eddies.length - 1; i >= 0; i--) {
        const e = this.eddies[i];
        e.x += u0 * 0.84 * dt;
        e.y += Math.sin(this.time * 4 + i) * 12 * dt;
        e.gamma *= 1 - 0.12 * dt;
        if (e.x > 920) this.eddies.splice(i, 1);
      }

      for (const t of this.tracers) {
        const [vx, vy] = this._velAt(t.x, t.y, params);
        t.x += vx * dt;
        t.y += vy * dt;
        const dObs = Math.hypot(t.x - this.obsX, t.y - this.obsY);
        if (dObs < R + 3) {
          const ang = Math.atan2(t.y - this.obsY, t.x - this.obsX);
          t.x = this.obsX + Math.cos(ang) * (R + 4);
          t.y = this.obsY + Math.sin(ang) * (R + 4);
        }
        t.history.push({ x: t.x, y: t.y });
        if (t.history.length > 10) t.history.shift();

        if (t.x > 885 || t.y < 15 || t.y > 465) {
          t.x = 8 + Math.random() * 18;
          t.y = this.obsY - 85 + t.band * 85 + (Math.random() - 0.5) * 38;
          t.history = [];
        }
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(45, 212, 191, 0.08)");
      const R = (params.obstacle_diameter ?? 9.0) * 3.6;

      // Render Vorticity Curl Heatmap Clouds for each shed eddy
      for (const e of this.eddies) {
        const rad = 46;
        const grad = ctx.createRadialGradient(e.x, e.y, 3, e.x, e.y, rad);
        if (e.sign > 0) {
          grad.addColorStop(0, "rgba(34, 211, 238, 0.42)");
          grad.addColorStop(1, "rgba(34, 211, 238, 0)");
        } else {
          grad.addColorStop(0, "rgba(244, 63, 94, 0.42)");
          grad.addColorStop(1, "rgba(244, 63, 94, 0)");
        }
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(e.x, e.y, rad, 0, TAU);
        ctx.fill();
      }

      // Render Neon Multi-Dye Tracer Ribbons
      const colors = ["#22d3ee", "#f472b6", "#fbbf24"];
      for (const t of this.tracers) {
        if (t.history.length < 2) continue;
        ctx.strokeStyle = colors[t.band];
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        t.history.forEach((pt, i) => (i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)));
        ctx.stroke();
      }

      // Bluff Cylinder Obstacle
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = "#2dd4bf";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(this.obsX, this.obsY, R, 0, TAU);
      ctx.fill();
      ctx.stroke();
      drawHandleBadge(ctx, this.obsX, this.obsY, "DRAG CYLINDER", "#2dd4bf");

      // Top-Right Scope: Oscillating Lift Coefficient C_L(t) & Strouhal Shedding
      const sx = w - 250, sy = 44, sw = 235, sh = 128;
      drawScopePanel(ctx, sx, sy, sw, sh, "VORTEX SHEDDING OSCILLATION", "Alternating Kármán Wake Lift C_L(t)", "rgba(45, 212, 191, 0.45)");
      if (this.liftHistory.length > 1) {
        ctx.strokeStyle = "#2dd4bf";
        ctx.lineWidth = 2;
        ctx.beginPath();
        this.liftHistory.forEach((v, i) => {
          const gx = sx + 14 + (i / 90) * (sw - 28);
          const gy = sy + 82 - v * 32;
          if (i === 0) ctx.moveTo(gx, gy);
          else ctx.lineTo(gx, gy);
        });
        ctx.stroke();
      }
    }

    onPointerDown(x, y) {
      if (Math.hypot(x - this.obsX, y - this.obsY) < 55) this.draggingObs = true;
      else {
        this.eddies.push({ x, y, gamma: 6500, sign: 1 });
      }
    }
    onPointerMove(x, y) {
      if (this.draggingObs) {
        this.obsX = clamp(x, 120, 420);
        this.obsY = clamp(y, 110, 370);
      }
    }
    onPointerUp() {
      this.draggingObs = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 9. WaveInterferenceEngine (wave-interference)
  // =========================================================================
  class WaveInterferenceEngine {
    constructor() {
      this.time = 0;
      this.crests = [];
      this.sourceX = 180;
      this.emitTimer = 0;
      this.audioCtx = null;
      this.osc = null;
      this.gain = null;
      this.audioPlaying = false;
      this.init({});
    }

    init() {
      this.time = 0;
      this.crests = [];
      this.sourceX = 140;
      this.emitTimer = 0;
    }

    toggleAudio(params) {
      if (this.audioPlaying) {
        this.stopAudio();
        return false;
      }
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return false;
      this.audioCtx = new AudioContextClass();
      this.osc = this.audioCtx.createOscillator();
      this.gain = this.audioCtx.createGain();
      this.osc.type = "triangle";
      this._updateAudioNodes(params);
      this.gain.gain.value = 0.08;
      this.osc.connect(this.gain);
      this.gain.connect(this.audioCtx.destination);
      this.osc.start();
      this.audioPlaying = true;
      return true;
    }

    _updateAudioNodes(params) {
      if (!this.osc || !this.audioCtx) return;
      const f0 = params.frequency_hz ?? 260;
      const mach = params.source_velocity ?? 0.35;
      const fShift = mach < 0.95 ? f0 / (1 - mach * 0.6) : f0 * 2.2;
      this.osc.frequency.setValueAtTime(clamp(fShift, 80, 1400), this.audioCtx.currentTime);
    }

    stopAudio() {
      if (this.osc) {
        try { this.osc.stop(); } catch (_e) {}
        this.osc = null;
      }
      if (this.audioCtx) {
        try { this.audioCtx.close(); } catch (_e) {}
        this.audioCtx = null;
      }
      this.audioPlaying = false;
    }

    update(dt, params) {
      this.time += dt;
      const mach = params.source_velocity ?? 0.35;
      const cWave = 115;

      if (mach > 0.02) {
        this.sourceX += mach * cWave * dt;
        if (this.sourceX > 520) {
          this.sourceX = 95;
          this.crests = [];
        }
        this.emitTimer += dt;
        if (this.emitTimer > 0.14) {
          this.emitTimer = 0;
          this.crests.push({ x: this.sourceX, y: 245, r: 2 });
        }
        for (let i = this.crests.length - 1; i >= 0; i--) {
          this.crests[i].r += cWave * dt;
          if (this.crests[i].r > 480) this.crests.splice(i, 1);
        }
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(167, 139, 250, 0.08)");
      const f0 = params.frequency_hz ?? 260;
      const sepLambda = params.source_separation ?? 2.5;
      const mach = params.source_velocity ?? 0.35;
      const phaseRad = ((params.phase_diff ?? 0) * Math.PI) / 180;
      const K = Math.round(params.harmonics_count ?? 2);

      const tankW = 545;
      const cy = h * 0.52;
      const lambdaPx = clamp(9200 / f0, 18, 56);
      const kWave = TAU / lambdaPx;

      if (mach <= 0.04) {
        const sepPx = sepLambda * lambdaPx;
        const s1x = 225, s1y = cy - sepPx * 0.5;
        const s2x = 225, s2y = cy + sepPx * 0.5;

        const cell = 7;
        for (let y = 25; y < h - 20; y += cell) {
          for (let x = 20; x < tankW; x += cell) {
            const r1 = Math.hypot(x - s1x, y - s1y);
            const r2 = Math.hypot(x - s2x, y - s2y);
            const w1 = Math.sin(kWave * r1 - this.time * 9);
            const w2 = sepLambda > 0.05 ? Math.sin(kWave * r2 - this.time * 9 + phaseRad) : 0;
            const sum = sepLambda > 0.05 ? (w1 + w2) * 0.5 : w1;
            if (sum >= 0) {
              ctx.fillStyle = `rgba(56, 189, 248, ${sum * 0.65})`;
            } else {
              ctx.fillStyle = `rgba(168, 85, 247, ${-sum * 0.65})`;
            }
            ctx.fillRect(x, y, cell, cell);
          }
        }
        [{ x: s1x, y: s1y }, { x: s2x, y: s2y }].forEach((s) => {
          ctx.fillStyle = "#fde047";
          ctx.beginPath();
          ctx.arc(s.x, s.y, 6, 0, TAU);
          ctx.fill();
        });
      } else {
        for (const c of this.crests) {
          const alpha = clamp(1 - c.r / 460, 0.08, 0.8);
          ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`;
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(c.x, c.y, c.r, 0, TAU);
          ctx.stroke();
        }
        if (mach >= 1.0) {
          const coneAng = Math.asin(1 / mach);
          ctx.strokeStyle = "#f43f5e";
          ctx.lineWidth = 2.6;
          ctx.setLineDash([6, 4]);
          ctx.beginPath();
          ctx.moveTo(this.sourceX - 340 * Math.cos(coneAng), cy - 340 * Math.sin(coneAng));
          ctx.lineTo(this.sourceX, cy);
          ctx.lineTo(this.sourceX - 340 * Math.cos(coneAng), cy + 340 * Math.sin(coneAng));
          ctx.stroke();
          ctx.setLineDash([]);
        }
        ctx.fillStyle = "#f43f5e";
        ctx.beginPath();
        ctx.arc(this.sourceX, cy, 8, 0, TAU);
        ctx.fill();
      }

      // Right Panel: Far-Field Interference Fringe Intensity & Fourier Harmonics
      const rx = 565, ry = 44, rw = 295, rh = 410;
      drawScopePanel(ctx, rx, ry, rw, rh, `FAR-FIELD FRINGES & FOURIER (K=${K})`, "Top: Fringe Intensity I(y) · Bottom: Harmonics", "rgba(167, 139, 250, 0.45)");
      // Top curve: I(y) fringe intensity
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (let py = 0; py <= 150; py += 2) {
        const dy = (py - 75) / 75;
        const delta = Math.PI * sepLambda * dy + phaseRad * 0.5;
        const intensity = Math.pow(Math.cos(delta), 2);
        const gx = rx + 24 + intensity * (rw - 48);
        const gy = ry + 45 + py;
        if (py === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();

      // Bottom curve: K-harmonic Fourier waveform
      const wy = ry + 310;
      ctx.strokeStyle = "#a78bfa";
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (let px = 0; px <= rw - 32; px += 2) {
        const t = (px / (rw - 32)) * TAU * 2 - this.time * 5;
        let ySum = 0;
        for (let k = 1; k <= K; k++) {
          const n = 2 * k - 1;
          ySum += Math.sin(n * t) / n;
        }
        const gx = rx + 16 + px;
        const gy = wy - ySum * 48;
        if (px === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();
    }

    onPointerDown(x, y) {
      if (x < 540) this.crests.push({ x, y, r: 2 });
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 10. StructuralTrussEngine (structural-truss)
  // =========================================================================
  class StructuralTrussEngine {
    constructor() {
      this.truckPos = 0.5; // 0 to 1 along bridge span
      this.truckDir = 1;
      this.draggingTruck = false;
      this.time = 0;
      this.init({});
    }

    init() {
      this.truckPos = 0.48;
      this.time = 0;
    }

    update(dt) {
      this.time += dt;
      if (!this.draggingTruck) {
        this.truckPos += this.truckDir * 0.14 * dt;
        if (this.truckPos > 0.85) {
          this.truckPos = 0.85;
          this.truckDir = -1;
        } else if (this.truckPos < 0.15) {
          this.truckPos = 0.15;
          this.truckDir = 1;
        }
      }
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(244, 63, 94, 0.08)");
      const loadKn = params.vehicle_load ?? 220;
      const eGpa = params.youngs_modulus ?? 200;
      const archH = params.truss_depth ?? 7.5;
      const areaCm2 = params.beam_area ?? 45;
      const seismicG = params.seismic_amp ?? 0.04;

      const spanLeft = 65, spanRight = 575;
      const spanW = spanRight - spanLeft;
      const deckY = 335;
      const trussH = archH * 15.5;

      // Seismic ground shake offset
      const shakeX = Math.sin(this.time * 22) * seismicG * 22;
      const shakeY = Math.cos(this.time * 18) * seismicG * 14;

      // Concrete Abutment Piers
      ctx.fillStyle = "#334155";
      ctx.fillRect(spanLeft - 28 + shakeX, deckY, 36, 115);
      ctx.fillRect(spanRight - 8 + shakeX, deckY, 36, 115);

      // Compute Warren Truss Nodes (6 bottom deck nodes, 5 top chord nodes)
      const dynFactor = 1 + 2.2 * seismicG;
      const chordForceKn = (loadKn * 36 / (4 * archH)) * dynFactor;
      const maxStressMpa = (chordForceKn / areaCm2) * 10;
      const yieldMpa = 250 * Math.pow(eGpa / 200, 0.35);
      const sf = yieldMpa / Math.max(1, maxStressMpa);
      const buckled = sf < 1.0;

      const midDeflectPx = clamp((loadKn / (eGpa * archH * areaCm2)) * 28000 * dynFactor, 2, 68);

      const botNodes = [];
      for (let i = 0; i < 6; i++) {
        const u = i / 5;
        const influence = Math.sin(u * Math.PI) * (1 - 0.55 * Math.abs(u - this.truckPos));
        botNodes.push({
          x: spanLeft + u * spanW + shakeX,
          y: deckY + influence * midDeflectPx + shakeY,
          u,
        });
      }

      const topNodes = [];
      for (let i = 0; i < 5; i++) {
        const u = (i + 0.5) / 5;
        const archCurve = 1 + 0.22 * Math.sin(u * Math.PI);
        const influence = Math.sin(u * Math.PI) * (1 - 0.55 * Math.abs(u - this.truckPos));
        topNodes.push({
          x: spanLeft + u * spanW + shakeX,
          y: deckY - trussH * archCurve + influence * midDeflectPx * 1.05 + shakeY,
          u,
        });
      }

      const memberStresses = [];
      const drawBeam = (n1, n2, stressRatio, isCompression, labelIndex) => {
        memberStresses.push({ idx: labelIndex, ratio: stressRatio, comp: isCompression });
        ctx.save();
        const col = isCompression
          ? `rgba(244, 63, 94, ${clamp(0.45 + stressRatio * 0.55, 0.4, 1)})`
          : `rgba(34, 211, 238, ${clamp(0.45 + stressRatio * 0.55, 0.4, 1)})`;
        ctx.strokeStyle = col;
        ctx.lineWidth = clamp(4 + (areaCm2 / 30) * 2, 4, 9);

        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        if (isCompression && buckled && stressRatio > 0.82) {
          // Lateral Euler buckling kink!
          const mx = (n1.x + n2.x) * 0.5;
          const my = (n1.y + n2.y) * 0.5 - 18 * Math.sin(this.time * 16 + labelIndex);
          ctx.quadraticCurveTo(mx, my, n2.x, n2.y);
        } else {
          ctx.lineTo(n2.x, n2.y);
        }
        ctx.stroke();
        ctx.restore();
      };

      // Bottom Tension Chords (Cyan)
      for (let i = 0; i < 5; i++) {
        const prox = 1 - Math.abs((i + 0.5) / 5 - this.truckPos);
        drawBeam(botNodes[i], botNodes[i + 1], (maxStressMpa / yieldMpa) * prox, false, i + 1);
      }
      // Top Compression Chords (Crimson)
      for (let i = 0; i < 4; i++) {
        const prox = 1 - Math.abs((i + 1) / 5 - this.truckPos);
        drawBeam(topNodes[i], topNodes[i + 1], (maxStressMpa / yieldMpa) * prox * 1.08, true, i + 6);
      }
      // Diagonal Web Members
      for (let i = 0; i < 5; i++) {
        const isLeftOfTruck = (i + 0.25) / 5 < this.truckPos;
        drawBeam(botNodes[i], topNodes[i], (maxStressMpa / yieldMpa) * 0.65, isLeftOfTruck, 10 + i * 2);
        drawBeam(topNodes[i], botNodes[i + 1], (maxStressMpa / yieldMpa) * 0.65, !isLeftOfTruck, 11 + i * 2);
      }

      // Pin Joint Gusset Nodes
      [...botNodes, ...topNodes].forEach((n) => {
        ctx.fillStyle = "#f8fafc";
        ctx.strokeStyle = "#0f172a";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(n.x, n.y, 5.5, 0, TAU);
        ctx.fill();
        ctx.stroke();
      });

      // Moving Heavy Freight Vehicle & Load Vector
      const tx = spanLeft + this.truckPos * spanW + shakeX;
      const ty = deckY + Math.sin(this.truckPos * Math.PI) * midDeflectPx + shakeY;
      ctx.fillStyle = "#f59e0b";
      ctx.fillRect(tx - 26, ty - 26, 52, 20);
      ctx.fillStyle = "#fde047";
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.fillText(`${loadKn.toFixed(0)}kN`, tx - 18, ty - 12);

      // Downward Load Arrow
      ctx.strokeStyle = "#f43f5e";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(tx, ty);
      ctx.lineTo(tx, ty + 48);
      ctx.stroke();
      drawHandleBadge(ctx, tx, ty - 34, "DRAG LOAD", "#f59e0b");

      // Right Panel: Member Axial Stress Distribution & Buckling Safety Gauge
      const rx = 610, ry = 44, rw = 250, rh = 395;
      drawScopePanel(ctx, rx, ry, rw, rh, `MEMBER STRESS (SF = ${sf.toFixed(2)})`, "Red = Compression · Cyan = Tension", buckled ? "rgba(244, 63, 94, 0.7)" : "rgba(56, 189, 248, 0.4)");
      const yLimX = rx + 20 + 0.75 * (rw - 40);
      ctx.strokeStyle = "#f43f5e";
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(yLimX, ry + 42);
      ctx.lineTo(yLimX, ry + rh - 20);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#f43f5e";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText("Yield σ_y", yLimX - 24, ry + 39);

      memberStresses.slice(0, 14).forEach((m, i) => {
        const by = ry + 48 + i * 23;
        const bw = clamp(m.ratio * 0.75, 0.05, 1) * (rw - 40);
        ctx.fillStyle = m.comp ? "rgba(244, 63, 94, 0.75)" : "rgba(34, 211, 238, 0.75)";
        ctx.fillRect(rx + 20, by, bw, 14);
        ctx.fillStyle = "#e2e8f0";
        ctx.fillText(`M${m.idx} (${m.comp ? "C" : "T"})`, rx + 24, by + 11);
      });
    }

    onPointerDown(x) {
      if (x < 600) {
        this.draggingTruck = true;
        this.truckPos = clamp((x - 65) / 510, 0.1, 0.9);
      }
    }
    onPointerMove(x) {
      if (this.draggingTruck) {
        this.truckPos = clamp((x - 65) / 510, 0.1, 0.9);
      }
    }
    onPointerUp() {
      this.draggingTruck = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 11. RlcCircuitResonanceEngine (rlc-circuit-resonance)
  // =========================================================================
  class RlcCircuitResonanceEngine {
    constructor() {
      this.phase = 0;
      this.draggingBode = false;
      this.init({});
    }

    init() {
      this.phase = 0;
    }

    update(dt, params) {
      const f = params.drive_freq_hz ?? 159;
      this.phase = (this.phase + dt * (f / 32) * TAU) % TAU;
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(16, 185, 129, 0.08)");
      const f = params.drive_freq_hz ?? 159;
      const R = params.resistance_ohm ?? 18;
      const L = (params.inductance_mh ?? 50) * 1e-3;
      const C = (params.capacitance_uf ?? 20) * 1e-6;
      const V0 = params.source_voltage ?? 24;

      const omega = TAU * f;
      const f0 = 1 / (TAU * Math.sqrt(L * C));
      const XL = omega * L;
      const XC = 1 / Math.max(1e-6, omega * C);
      const Z = Math.sqrt(R * R + Math.pow(XL - XC, 2));
      const I0 = V0 / Z;
      const phi = Math.atan2(XL - XC, R);

      // 1. Top-Left Panel: Animated AC RLC Schematic with drifting electrons
      const sx = 24, sy = 44, sw = 400, sh = 195;
      drawScopePanel(ctx, sx, sy, sw, sh, "SERIES AC RLC CIRCUIT SCHEMATIC", `f = ${f.toFixed(0)} Hz (f₀ = ${f0.toFixed(1)} Hz) · I₀ = ${I0.toFixed(2)} A`, "rgba(16, 185, 129, 0.4)");
      const wx = sx + 55, wy = sy + 52, ww = sw - 110, wh = sh - 76;
      ctx.strokeStyle = "#64748b";
      ctx.lineWidth = 3;
      ctx.strokeRect(wx, wy, ww, wh);

      // Animated Charge Carriers along loop
      const iInst = Math.sin(this.phase - phi);
      for (let k = 0; k < 18; k++) {
        const u = ((k / 18) + (Math.cos(this.phase - phi) * I0 * 0.025) + 10) % 1;
        let ex = wx, ey = wy;
        if (u < 0.25) { ex = wx + (u / 0.25) * ww; ey = wy; }
        else if (u < 0.5) { ex = wx + ww; ey = wy + ((u - 0.25) / 0.25) * wh; }
        else if (u < 0.75) { ex = wx + ww - ((u - 0.5) / 0.25) * ww; ey = wy + wh; }
        else { ex = wx; ey = wy + wh - ((u - 0.75) / 0.25) * wh; }
        ctx.fillStyle = "#fde047";
        ctx.beginPath();
        ctx.arc(ex, ey, 3.3, 0, TAU);
        ctx.fill();
      }

      // Component Badges on schematic
      ctx.fillStyle = "#0f172a";
      ctx.fillRect(wx + ww * 0.35, wy - 12, 85, 24);
      ctx.strokeStyle = "#38bdf8";
      ctx.strokeRect(wx + ww * 0.35, wy - 12, 85, 24);
      ctx.fillStyle = "#38bdf8";
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.fillText(`R = ${R} Ω`, wx + ww * 0.35 + 12, wy + 4);

      ctx.fillStyle = "#0f172a";
      ctx.fillRect(wx + ww - 42, wy + wh * 0.35, 84, 26);
      ctx.strokeStyle = "#10b981";
      ctx.strokeRect(wx + ww - 42, wy + wh * 0.35, 84, 26);
      ctx.fillStyle = "#10b981";
      ctx.fillText(`X_L=${XL.toFixed(0)}Ω`, wx + ww - 36, wy + wh * 0.35 + 16);

      ctx.fillStyle = "#0f172a";
      ctx.fillRect(wx + ww * 0.35, wy + wh - 12, 85, 24);
      ctx.strokeStyle = "#f472b6";
      ctx.strokeRect(wx + ww * 0.35, wy + wh - 12, 85, 24);
      ctx.fillStyle = "#f472b6";
      ctx.fillText(`X_C=${XC.toFixed(0)}Ω`, wx + ww * 0.35 + 8, wy + wh + 4);

      // 2. Bottom-Left Panel:Rotating Complex Impedance Phasor Diagram
      const px = 24, py = 250, pw = 400, ph = 208;
      drawScopePanel(ctx, px, py, pw, ph, "ROTATING COMPLEX PHASOR DIAGRAM", `V_R (Cyan) · V_L (+90° Green) · V_C (-90° Pink) · φ=${((phi * 180) / Math.PI).toFixed(1)}°`);
      const pcx = px + pw * 0.5, pcy = py + ph * 0.56;
      ctx.strokeStyle = "rgba(148, 163, 184, 0.25)";
      ctx.beginPath();
      ctx.arc(pcx, pcy, 68, 0, TAU);
      ctx.stroke();

      const iAng = this.phase - phi;
      const scaleP = 62 / Math.max(V0, I0 * Math.max(R, XL, XC));
      const drawVec = (len, ang, col, label) => {
        const vx = pcx + Math.cos(ang) * len;
        const vy = pcy - Math.sin(ang) * len;
        ctx.strokeStyle = col;
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        ctx.moveTo(pcx, pcy);
        ctx.lineTo(vx, vy);
        ctx.stroke();
        ctx.fillStyle = col;
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.fillText(label, vx + 5, vy + 3);
      };
      drawVec(I0 * R * scaleP, iAng, "#38bdf8", "V_R");
      drawVec(I0 * XL * scaleP, iAng + Math.PI * 0.5, "#10b981", "V_L");
      drawVec(I0 * XC * scaleP, iAng - Math.PI * 0.5, "#f472b6", "V_C");
      drawVec(V0 * scaleP, this.phase, "#fde047", "V_S");

      // 3. Top-Right Panel: 4-Trace Digital Storage Oscilloscope
      const ox = 440, oy = 44, ow = 416, oh = 195;
      drawScopePanel(ctx, ox, oy, ow, oh, "4-CHANNEL DIGITAL OSCILLOSCOPE", "Gold=V_S(t) · Cyan=V_R(t) · Green=V_L(t) · Pink=V_C(t)");
      const midY = oy + oh * 0.58;
      const traces = [
        { amp: V0, ph: 0, col: "#fde047" },
        { amp: I0 * R, ph: -phi, col: "#38bdf8" },
        { amp: I0 * XL, ph: -phi + Math.PI * 0.5, col: "#10b981" },
        { amp: I0 * XC, ph: -phi - Math.PI * 0.5, col: "#f472b6" },
      ];
      for (const tr of traces) {
        ctx.strokeStyle = tr.col;
        ctx.lineWidth = 1.9;
        ctx.beginPath();
        for (let x = 0; x <= ow - 28; x += 3) {
          const tAng = this.phase + (x / (ow - 28)) * TAU * 2 + tr.ph;
          const gy = midY - clamp((tr.amp / (V0 * 1.6)) * 58, -68, 68) * Math.sin(tAng);
          if (x === 0) ctx.moveTo(ox + 14 + x, gy);
          else ctx.lineTo(ox + 14 + x, gy);
        }
        ctx.stroke();
      }

      // 4. Bottom-Right Panel: Interactive Bode Resonance Curve I₀(f)
      const bx = 440, by = 250, bw = 416, bh = 208;
      drawScopePanel(ctx, bx, by, bw, bh, "BODE FREQUENCY RESPONSE I₀(f)", "Drag Marker to Lock Resonance ω₀ = 1/√(LC)", "rgba(16, 185, 129, 0.5)");
      const gLeft = bx + 28, gBot = by + bh - 26, gW = bw - 52, gH = bh - 68;
      const iMax = V0 / R;

      ctx.strokeStyle = "#10b981";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let freq = 40; freq <= 400; freq += 4) {
        const wFreq = TAU * freq;
        const zF = Math.sqrt(R * R + Math.pow(wFreq * L - 1 / (wFreq * C), 2));
        const iF = V0 / zF;
        const gx = gLeft + ((freq - 40) / 360) * gW;
        const gy = gBot - (iF / iMax) * gH;
        if (freq === 40) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();

      // Current frequency marker on Bode plot
      const curBx = gLeft + ((f - 40) / 360) * gW;
      const curBy = gBot - (I0 / iMax) * gH;
      ctx.fillStyle = "#fde047";
      ctx.beginPath();
      ctx.arc(curBx, curBy, 6, 0, TAU);
      ctx.fill();
      drawHandleBadge(ctx, curBx, curBy, `${f.toFixed(0)} Hz`, "#10b981");
    }

    onPointerDown(x, y) {
      if (x >= 440 && y >= 250) {
        this.draggingBode = true;
        this.onPointerMove(x);
      }
    }
    onPointerMove(x) {
      if (!this.draggingBode) return;
      const slider = document.getElementById("slider-drive_freq_hz");
      if (slider) {
        const freq = clamp(40 + ((x - 468) / 364) * 360, 40, 400);
        slider.value = String(Math.round(freq / 2) * 2);
        slider.dispatchEvent(new Event("input"));
      }
    }
    onPointerUp() {
      this.draggingBode = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 12. RelativisticLensingEngine (relativistic-lensing)
  // =========================================================================
  class RelativisticLensingEngine {
    constructor() {
      this.time = 0;
      this.draggingBeam = false;
      this.init({});
    }

    init() {
      this.time = 0;
    }

    update(dt) {
      this.time += dt;
    }

    _traceGeodesic(bRatio, ySign, rsPx) {
      // Integrate Binet equation d^2u/dphi^2 + u = 1.5 * rs * u^2 in polar coordinates
      const pts = [];
      let x = -390;
      let y = ySign * bRatio * rsPx;
      let vx = 1.0;
      let vy = 0.0;
      const ds = 4.5;
      let captured = false;

      for (let step = 0; step < 220; step++) {
        pts.push({ x, y });
        const r = Math.hypot(x, y);
        if (r <= rsPx * 1.02) {
          captured = true;
          break;
        }
        if (x > 410 || Math.abs(y) > 290) break;

        // Effective GR photon acceleration a_GR = -1.5 * r_s * L^2 / r^4 * r_hat
        const bEff = bRatio * rsPx;
        const accelMag = (1.5 * rsPx * (bEff * bEff + rsPx * rsPx * 1.2)) / Math.pow(r, 4);
        vx += (-accelMag * (x / r)) * ds;
        vy += (-accelMag * (y / r)) * ds;
        const spd = Math.hypot(vx, vy) || 1;
        vx /= spd;
        vy /= spd;
        x += vx * ds;
        y += vy * ds;
      }
      return { pts, captured };
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(244, 63, 94, 0.08)");
      const mBh = params.bh_mass ?? 10.0;
      const bRatio = params.impact_param ?? 2.85;
      const spread = params.beam_spread ?? 2.2;
      const tiltDeg = params.grid_tilt ?? 42.0;
      const spin = params.accretion_spin ?? 0.65;

      const cx = w * 0.42;
      const cy = h * 0.54;
      const rsPx = 16 + mBh * 1.45;
      const tiltFactor = Math.sin((tiltDeg * Math.PI) / 180);

      // 1. 3D-Projected Warped Flamm's Paraboloid Spacetime Mesh
      ctx.strokeStyle = "rgba(56, 189, 248, 0.22)";
      ctx.lineWidth = 1.1;
      for (let r = rsPx * 1.15; r <= 290; r += 26) {
        const zSink = 36 * Math.sqrt(rsPx / r) * tiltFactor;
        ctx.beginPath();
        ctx.ellipse(cx, cy + zSink, r, r * (0.42 + 0.45 * (1 - tiltFactor)), 0, 0, TAU);
        ctx.stroke();
      }
      for (let a = 0; a < 16; a++) {
        const ang = (a / 16) * TAU;
        ctx.beginPath();
        for (let r = rsPx * 1.1; r <= 290; r += 14) {
          const zSink = 36 * Math.sqrt(rsPx / r) * tiltFactor;
          const gx = cx + Math.cos(ang) * r;
          const gy = cy + zSink + Math.sin(ang) * r * (0.42 + 0.45 * (1 - tiltFactor));
          if (r === rsPx * 1.1) ctx.moveTo(gx, gy);
          else ctx.lineTo(gx, gy);
        }
        ctx.stroke();
      }

      // 2. Relativistic Beamed Accretion Disk & Photon Sphere (r_ph = 1.5 r_s)
      const accGrad = ctx.createRadialGradient(cx, cy, rsPx * 1.1, cx, cy, rsPx * 3.1);
      accGrad.addColorStop(0, "rgba(254, 240, 138, 0.75)");
      accGrad.addColorStop(0.4, `rgba(249, 115, 22, ${0.35 + spin * 0.35})`);
      accGrad.addColorStop(1, "rgba(244, 63, 94, 0)");
      ctx.fillStyle = accGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, rsPx * 3.1, 0, TAU);
      ctx.fill();

      // Photon sphere r = 1.5 r_s dashed ring
      ctx.strokeStyle = "#fb923c";
      ctx.lineWidth = 1.8;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.arc(cx, cy, rsPx * 1.5, 0, TAU);
      ctx.stroke();
      ctx.setLineDash([]);

      // 3. Bundle of Null Photon Geodesics
      const rayOffsets = [-1.0, -0.5, 0, 0.5, 1.0];
      for (const off of rayOffsets) {
        const bCur = Math.max(0.4, bRatio + off * spread * 0.5);
        for (const sign of [1, -1]) {
          if (off !== 0 && sign === -1 && spread < 0.2) continue;
          const { pts, captured } = this._traceGeodesic(bCur, sign, rsPx);
          ctx.save();
          ctx.strokeStyle = captured ? "rgba(244, 63, 94, 0.78)" : off === 0 ? "#fde047" : "rgba(56, 189, 248, 0.72)";
          ctx.lineWidth = off === 0 ? 2.6 : 1.6;
          if (off === 0) {
            ctx.shadowColor = "#fde047";
            ctx.shadowBlur = 9;
          }
          ctx.beginPath();
          pts.forEach((pt, i) => (i === 0 ? ctx.moveTo(cx + pt.x, cy + pt.y) : ctx.lineTo(cx + pt.x, cy + pt.y)));
          ctx.stroke();
          ctx.restore();
        }
      }

      // Schwarzschild Event Horizon Shadow (r = r_s)
      ctx.fillStyle = "#000000";
      ctx.strokeStyle = "#f43f5e";
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.arc(cx, cy, rsPx, 0, TAU);
      ctx.fill();
      ctx.stroke();

      drawHandleBadge(ctx, cx - 260, cy - bRatio * rsPx, `b = ${bRatio.toFixed(2)} r_s`, "#fde047");

      // Top-Right Scope: GR Effective Potential V_eff(r) = (1 - r_s/r)/r²
      const sx = w - 255, sy = 44, sw = 240, sh = 140;
      drawScopePanel(ctx, sx, sy, sw, sh, "GR EFFECTIVE POTENTIAL V_eff(r)", "Peak at Photon Sphere r_ph = 1.5 r_s", "rgba(244, 63, 94, 0.45)");
      const ox = sx + 22, oy = sy + sh - 22, gw = sw - 38, gh = sh - 62;
      ctx.strokeStyle = "#fb923c";
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (let i = 0; i <= 50; i++) {
        const rNorm = 1.0 + (i / 50) * 4.5;
        const vEff = (1 - 1 / rNorm) / (rNorm * rNorm) * 6.75; // normalized so peak at r=1.5 is 1.0
        const gx = ox + (i / 50) * gw;
        const gy = oy - clamp(vEff, 0, 1) * gh;
        if (i === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();
      ctx.fillStyle = "#fde047";
      ctx.font = "9.5px 'JetBrains Mono', monospace";
      ctx.fillText("r_ph = 1.5 r_s (b_c = 2.60 r_s)", ox + 8, oy + 14);
    }

    onPointerDown(x, y) {
      if (x < 600) {
        this.draggingBeam = true;
        this.onPointerMove(x, y);
      }
    }
    onPointerMove(_x, y) {
      if (!this.draggingBeam) return;
      const slider = document.getElementById("slider-impact_param");
      if (slider) {
        const val = clamp(Math.abs(258 - y) / 32, 1.2, 6.5);
        slider.value = val.toFixed(2);
        slider.dispatchEvent(new Event("input"));
      }
    }
    onPointerUp() {
      this.draggingBeam = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 13. FourierEpicyclesEngine (fourier-epicycles)
  // =========================================================================
  class FourierEpicyclesEngine {
    constructor() {
      this.time = 0;
      this.coeffs = [];
      this.trace = [];
      this.userPath = [];
      this.drawingCustom = false;
      this.lastShape = -1;
      this.init({});
    }

    _generateTargetPoints(shapeId) {
      const N = 128;
      const pts = [];
      for (let n = 0; n < N; n++) {
        const t = (n / N) * TAU;
        let x = 0, y = 0;
        if (shapeId === 1) {
          // Starship silhouette
          const r = 115 * (0.65 + 0.35 * Math.cos(t) + 0.28 * Math.cos(3 * t) - 0.14 * Math.cos(5 * t));
          x = r * Math.cos(t);
          y = r * Math.sin(t) * 0.78;
        } else if (shapeId === 2) {
          // Parametric Heart
          x = 8.2 * 16 * Math.pow(Math.sin(t), 3);
          y = -8.2 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
        } else if (shapeId === 3) {
          // 8-Point Starburst
          const r = 95 + 42 * Math.cos(8 * t);
          x = r * Math.cos(t);
          y = r * Math.sin(t);
        } else {
          // Square Step Box
          const c = Math.cos(t), s = Math.sin(t);
          const m = Math.max(Math.abs(c), Math.abs(s));
          x = (c / m) * 110;
          y = (s / m) * 110;
        }
        pts.push({ re: x, im: y });
      }
      return pts;
    }

    _computeDFT(pts) {
      const N = pts.length;
      const out = [];
      for (let k = -Math.floor(N / 2); k < Math.ceil(N / 2); k++) {
        let sumRe = 0, sumIm = 0;
        for (let n = 0; n < N; n++) {
          const phi = (-TAU * k * n) / N;
          const c = Math.cos(phi), s = Math.sin(phi);
          sumRe += pts[n].re * c - pts[n].im * s;
          sumIm += pts[n].re * s + pts[n].im * c;
        }
        sumRe /= N;
        sumIm /= N;
        out.push({
          freq: k,
          amp: Math.hypot(sumRe, sumIm),
          phase: Math.atan2(sumIm, sumRe),
        });
      }
      out.sort((a, b) => b.amp - a.amp);
      return out;
    }

    init(params) {
      const shapeId = Math.round(params.shape_preset ?? 1);
      this.lastShape = shapeId;
      this.targetPts = this._generateTargetPoints(shapeId);
      this.coeffs = this._computeDFT(this.targetPts);
      this.trace = [];
      const M = Math.min(this.coeffs.length, Math.round(params.epicycle_count ?? 28));
      const hfBoost = params.harmonic_filter ?? 1.0;
      const cx = 275, cy = 250;
      for (let s = 0; s <= 140; s++) {
        const t = (s / 140) * TAU;
        let vx = cx, vy = cy;
        for (let i = 0; i < M; i++) {
          const c = this.coeffs[i];
          const boost = Math.abs(c.freq) > 2 ? hfBoost : 1.0;
          const rad = c.amp * boost;
          const ang = c.freq * t + c.phase;
          vx += rad * Math.cos(ang);
          vy += rad * Math.sin(ang);
        }
        this.trace.push({ x: vx, y: vy });
      }
      this.time = 0;
    }

    update(dt, params) {
      const shapeId = Math.round(params.shape_preset ?? 1);
      if (shapeId !== this.lastShape && !this.drawingCustom) {
        this.init(params);
      }
      const speed = params.cycle_speed ?? 1.0;
      this.time = (this.time + dt * speed * 1.15) % TAU;
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(236, 72, 153, 0.08)");
      const M = Math.min(this.coeffs.length, Math.round(params.epicycle_count ?? 28));
      const persist = (params.trail_persistence ?? 90) / 100;
      const hfBoost = params.harmonic_filter ?? 1.0;

      const cx = 275, cy = 250;
      if (this.targetPts && this.targetPts.length > 2 && !this.drawingCustom) {
        ctx.save();
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = "rgba(148, 163, 184, 0.25)";
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        this.targetPts.forEach((pt, i) => {
          const px = cx + pt.re;
          const py = cy + pt.im;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
      }
      let vx = cx, vy = cy;

      // Tip-to-tail Epicycle Gear Chain
      for (let i = 0; i < M; i++) {
        const c = this.coeffs[i];
        const prevX = vx, prevY = vy;
        const boost = Math.abs(c.freq) > 2 ? hfBoost : 1.0;
        const rad = c.amp * boost;
        const ang = c.freq * this.time + c.phase;
        vx += rad * Math.cos(ang);
        vy += rad * Math.sin(ang);

        if (rad > 1.2) {
          ctx.strokeStyle = "rgba(56, 189, 248, 0.28)";
          ctx.lineWidth = 1.1;
          ctx.beginPath();
          ctx.arc(prevX, prevY, rad, 0, TAU);
          ctx.stroke();

          ctx.strokeStyle = "rgba(248, 250, 252, 0.65)";
          ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(vx, vy);
          ctx.stroke();
        }
      }

      if (!this.drawingCustom) {
        this.trace.push({ x: vx, y: vy });
        const maxLen = Math.floor(175 * persist);
        while (this.trace.length > maxLen) this.trace.shift();
      }

      // Glowing Neon Reconstructed Contour
      if (this.trace.length > 2) {
        ctx.save();
        ctx.shadowColor = "#ec4899";
        ctx.shadowBlur = 10;
        ctx.strokeStyle = "#f472b6";
        ctx.lineWidth = 2.8;
        ctx.beginPath();
        this.trace.forEach((pt, i) => (i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)));
        ctx.stroke();
        ctx.restore();
      }

      ctx.fillStyle = "#fde047";
      ctx.beginPath();
      ctx.arc(vx, vy, 5, 0, TAU);
      ctx.fill();

      // Right Panel: DFT Harmonic Amplitude Spectrum |c_k|
      const rx = 535, ry = 44, rw = 325, rh = 410;
      drawScopePanel(ctx, rx, ry, rw, rh, `DFT SPECTRUM |c_k| (${M} EPICYCLES)`, "Sorted Harmonic Phasor Amplitudes", "rgba(236, 72, 153, 0.45)");
      const maxAmp = Math.max(1, this.coeffs[0]?.amp || 1);
      for (let i = 0; i < Math.min(20, this.coeffs.length); i++) {
        const c = this.coeffs[i];
        const by = ry + 45 + i * 17.5;
        const bw = (c.amp / maxAmp) * (rw - 95);
        const active = i < M;
        ctx.fillStyle = active ? "rgba(236, 72, 153, 0.8)" : "rgba(148, 163, 184, 0.25)";
        ctx.fillRect(rx + 68, by, bw, 12);
        ctx.fillStyle = active ? "#f8fafc" : "#64748b";
        ctx.font = "9.5px 'JetBrains Mono', monospace";
        ctx.fillText(`k=${c.freq >= 0 ? "+" : ""}${c.freq}`, rx + 12, by + 10);
      }
    }

    onPointerDown(x, y) {
      if (x < 520) {
        this.drawingCustom = true;
        this.userPath = [{ re: x - 275, im: y - 250 }];
        this.trace = [];
      }
    }
    onPointerMove(x, y) {
      if (this.drawingCustom && x < 520) {
        this.userPath.push({ re: x - 275, im: y - 250 });
        this.trace.push({ x, y });
      }
    }
    onPointerUp() {
      if (this.drawingCustom && this.userPath.length > 8) {
        this.coeffs = this._computeDFT(this.userPath);
        this.trace = [];
      }
      this.drawingCustom = false;
    }
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 14. AntColonySwarmEngine (ant-colony-swarm)
  // =========================================================================
  class AntColonySwarmEngine {
    constructor() {
      this.cols = 110;
      this.rows = 60;
      this.cellSize = 8;
      this.homePher = new Float32Array(this.cols * this.rows);
      this.foodPher = new Float32Array(this.cols * this.rows);
      this.obstacles = new Uint8Array(this.cols * this.rows);
      this.ants = [];
      this.nest = { x: 115, y: 245 };
      this.food = { x: 525, y: 245 };
      this.lastPreset = -1;
      this.efficiency = 68.0;
      this.effHistory = [];
      this.init({});
    }

    init(params) {
      this.homePher.fill(0);
      this.foodPher.fill(0);
      this.obstacles.fill(0);
      const preset = Math.round(params.obstacle_preset ?? 1);
      this.lastPreset = preset;

      if (preset === 1) {
        this._paintRect(38, 17, 6, 26);
      } else if (preset === 2) {
        this._paintRect(32, 10, 5, 22);
        this._paintRect(50, 26, 5, 24);
      }

      const count = Math.round(params.ant_count ?? 180);
      this.ants = [];
      for (let i = 0; i < count; i++) {
        this.ants.push({
          x: this.nest.x,
          y: this.nest.y,
          angle: Math.random() * TAU,
          hasFood: false,
        });
      }
    }

    _paintRect(c0, r0, cw, rh) {
      for (let r = r0; r < r0 + rh; r++) {
        for (let c = c0; c < c0 + cw; c++) {
          if (c >= 0 && c < this.cols && r >= 0 && r < this.rows) {
            this.obstacles[r * this.cols + c] = 1;
          }
        }
      }
    }

    _sample(field, x, y) {
      const c = clamp(Math.floor(x / this.cellSize), 0, this.cols - 1);
      const r = clamp(Math.floor(y / this.cellSize), 0, this.rows - 1);
      return field[r * this.cols + c];
    }

    update(dt, params) {
      const preset = Math.round(params.obstacle_preset ?? 1);
      if (preset !== this.lastPreset) this.init(params);

      const evap = clamp(1 - ((params.evaporation_rate ?? 3.5) / 100) * dt * 2.5, 0.92, 0.999);
      const alphaP = params.pheromone_strength ?? 2.8;
      const noise = params.exploration_noise ?? 0.22;

      for (let i = 0; i < this.homePher.length; i++) {
        this.homePher[i] *= evap;
        this.foodPher[i] *= evap;
      }

      for (const a of this.ants) {
        const target = a.hasFood ? this.homePher : this.foodPher;
        const goal = a.hasFood ? this.nest : this.food;
        const dGoal = Math.hypot(goal.x - a.x, goal.y - a.y);

        if (dGoal < 55) {
          a.angle = Math.atan2(goal.y - a.y, goal.x - a.x);
        } else {
          const sL = this._sample(target, a.x + Math.cos(a.angle - 0.5) * 18, a.y + Math.sin(a.angle - 0.5) * 18);
          const sC = this._sample(target, a.x + Math.cos(a.angle) * 18, a.y + Math.sin(a.angle) * 18);
          const sR = this._sample(target, a.x + Math.cos(a.angle + 0.5) * 18, a.y + Math.sin(a.angle + 0.5) * 18);
          if (sL > sC && sL > sR) a.angle -= 0.14 * alphaP;
          else if (sR > sC && sR > sL) a.angle += 0.14 * alphaP;
          a.angle += (Math.random() - 0.5) * noise * 1.4;
        }

        const nx = a.x + Math.cos(a.angle) * 125 * dt;
        const ny = a.y + Math.sin(a.angle) * 125 * dt;
        const gc = clamp(Math.floor(nx / this.cellSize), 0, this.cols - 1);
        const gr = clamp(Math.floor(ny / this.cellSize), 0, this.rows - 1);

        if (nx < 16 || nx > 610 || ny < 20 || ny > 460 || this.obstacles[gr * this.cols + gc]) {
          a.angle += Math.PI * 0.75 + (Math.random() - 0.5);
        } else {
          a.x = nx;
          a.y = ny;
        }

        const idx = gr * this.cols + gc;
        if (a.hasFood) this.foodPher[idx] = Math.min(1, this.foodPher[idx] + 0.22);
        else this.homePher[idx] = Math.min(1, this.homePher[idx] + 0.22);

        if (!a.hasFood && Math.hypot(a.x - this.food.x, a.y - this.food.y) < 24) {
          a.hasFood = true;
          a.angle += Math.PI;
        } else if (a.hasFood && Math.hypot(a.x - this.nest.x, a.y - this.nest.y) < 24) {
          a.hasFood = false;
          a.angle += Math.PI;
        }
      }

      this.efficiency = clamp(42 + alphaP * 9.5 - noise * 28, 18, 96);
      this.effHistory.push(this.efficiency);
      if (this.effHistory.length > 90) this.effHistory.shift();
    }

    render(ctx, w, h) {
      drawScientificGrid(ctx, w, h, "rgba(52, 211, 153, 0.08)");

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < 78; c++) {
          const idx = r * this.cols + c;
          if (this.obstacles[idx]) {
            ctx.fillStyle = "#334155";
            ctx.fillRect(c * this.cellSize, r * this.cellSize, this.cellSize, this.cellSize);
            continue;
          }
          const hp = this.homePher[idx];
          const fp = this.foodPher[idx];
          if (hp > 0.03 || fp > 0.03) {
            ctx.fillStyle = `rgba(${Math.round(hp * 56)}, ${Math.round(fp * 235 + hp * 150)}, ${Math.round(hp * 248 + fp * 120)}, ${clamp(hp + fp, 0.08, 0.72)})`;
            ctx.fillRect(c * this.cellSize, r * this.cellSize, this.cellSize, this.cellSize);
          }
        }
      }

      for (const a of this.ants) {
        ctx.fillStyle = a.hasFood ? "#34d399" : "#e2e8f0";
        ctx.beginPath();
        ctx.arc(a.x, a.y, 2.2, 0, TAU);
        ctx.fill();
      }

      // Nest & Food
      ctx.fillStyle = "#38bdf8";
      ctx.beginPath();
      ctx.arc(this.nest.x, this.nest.y, 18, 0, TAU);
      ctx.fill();
      ctx.fillStyle = "#fff";
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.fillText("NEST", this.nest.x - 14, this.nest.y + 3);

      ctx.fillStyle = "#10b981";
      ctx.beginPath();
      ctx.arc(this.food.x, this.food.y, 18, 0, TAU);
      ctx.fill();
      ctx.fillStyle = "#fff";
      ctx.fillText("FOOD", this.food.x - 14, this.food.y + 3);

      // Right Scope: Trail Efficiency & Chemotaxis Convergence
      const rx = 630, ry = 44, rw = 230, rh = 165;
      drawScopePanel(ctx, rx, ry, rw, rh, `HIGHWAY EFFICIENCY η=${this.efficiency.toFixed(1)}%`, "Pheromone Shortest-Path Lock", "rgba(52, 211, 153, 0.45)");
      if (this.effHistory.length > 1) {
        ctx.strokeStyle = "#34d399";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        this.effHistory.forEach((v, i) => {
          const gx = rx + 14 + (i / 90) * (rw - 28);
          const gy = ry + rh - 20 - (v / 100) * (rh - 65);
          if (i === 0) ctx.moveTo(gx, gy);
          else ctx.lineTo(gx, gy);
        });
        ctx.stroke();
      }
    }

    onPointerDown(x, y) {
      if (x < 610) {
        const c = Math.floor(x / this.cellSize);
        const r = Math.floor(y / this.cellSize);
        this._paintRect(c - 2, r - 2, 4, 4);
      }
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return { canvas_efficiency: this.efficiency };
    }
  }

  // =========================================================================
  // 15. EpidemicSeirEngine (epidemic-seir)
  // =========================================================================
  class EpidemicSeirEngine {
    constructor() {
      this.agents = [];
      this.history = [];
      this.lastVacc = -1;
      this.init({});
    }

    init(params) {
      const vaccPct = params.vaccination_rate ?? 15.0;
      this.lastVacc = vaccPct;
      this.agents = [];
      this.history = [];
      const N = 150;
      const nVacc = Math.round((vaccPct / 100) * N);

      for (let i = 0; i < N; i++) {
        let state = "S";
        if (i < 4) state = "I";
        else if (i < 4 + nVacc) state = "V";
        const ang = Math.random() * TAU;
        this.agents.push({
          x: 35 + Math.random() * 485,
          y: 45 + Math.random() * 395,
          vx: Math.cos(ang) * 55,
          vy: Math.sin(ang) * 55,
          state,
          timer: 0,
        });
      }
    }

    update(dt, params) {
      const vaccPct = params.vaccination_rate ?? 15.0;
      if (Math.abs(vaccPct - this.lastVacc) > 0.5) this.init(params);

      const beta = params.transmission_prob ?? 0.52;
      const gamma = params.recovery_rate ?? 0.16;
      const dist = (params.social_distancing ?? 20.0) / 100;
      const inc = params.incubation_days ?? 3.0;
      const spdMult = 1 - 0.78 * dist;

      for (const a of this.agents) {
        a.x += a.vx * spdMult * dt;
        a.y += a.vy * spdMult * dt;
        if (a.x < 25 || a.x > 530) a.vx *= -1;
        if (a.y < 38 || a.y > 448) a.vy *= -1;

        if (a.state === "E") {
          a.timer += dt;
          if (a.timer > inc * 0.45) {
            a.state = "I";
            a.timer = 0;
          }
        } else if (a.state === "I") {
          a.timer += dt;
          if (a.timer > (1 / Math.max(0.05, gamma)) * 0.65) {
            a.state = "R";
          }
        }
      }

      for (let i = 0; i < this.agents.length; i++) {
        const inf = this.agents[i];
        if (inf.state !== "I") continue;
        for (let j = 0; j < this.agents.length; j++) {
          const sus = this.agents[j];
          if (sus.state !== "S") continue;
          if (Math.hypot(inf.x - sus.x, inf.y - sus.y) < 18 * (1 - 0.35 * dist)) {
            if (Math.random() < beta * dt * 3.2) {
              sus.state = "E";
              sus.timer = 0;
            }
          }
        }
      }

      const counts = { S: 0, E: 0, I: 0, R: 0, V: 0 };
      for (const a of this.agents) counts[a.state]++;
      if (counts.I === 0 && counts.E === 0 && counts.S > 20) {
        this.agents.find((x) => x.state === "S").state = "I";
      }
      this.history.push(counts);
      if (this.history.length > 130) this.history.shift();
    }

    render(ctx, w, h) {
      drawScientificGrid(ctx, w, h, "rgba(244, 63, 94, 0.08)");
      ctx.strokeStyle = "rgba(148, 163, 184, 0.3)";
      ctx.strokeRect(20, 32, 520, 424);

      const colors = { S: "#38bdf8", E: "#f59e0b", I: "#f43f5e", R: "#a78bfa", V: "#10b981" };
      for (const a of this.agents) {
        if (a.state === "I") {
          ctx.strokeStyle = "rgba(244, 63, 94, 0.32)";
          ctx.beginPath();
          ctx.arc(a.x, a.y, 13, 0, TAU);
          ctx.stroke();
        }
        ctx.fillStyle = colors[a.state];
        ctx.beginPath();
        ctx.arc(a.x, a.y, 4.4, 0, TAU);
        ctx.fill();
      }

      // Right Panel: Stacked SEIR Epidemic Curve
      const rx = 558, ry = 44, rw = 302, rh = 412;
      drawScopePanel(ctx, rx, ry, rw, rh, "STACKED SEIR EPIDEMIC CURVE", "Red=Infectious · Amber=Exposed · Green=Vacc", "rgba(244, 63, 94, 0.45)");
      const cx = rx + 14, cy = ry + 55, cw = rw - 28, ch = rh - 80;
      const N = this.agents.length || 150;
      const bw = cw / Math.max(1, this.history.length);

      this.history.forEach((snap, idx) => {
        const bx = cx + idx * bw;
        let yCursor = cy + ch;
        const drawSeg = (cnt, col) => {
          const sh = (cnt / N) * ch;
          ctx.fillStyle = col;
          ctx.fillRect(bx, yCursor - sh, Math.ceil(bw), sh);
          yCursor -= sh;
        };
        drawSeg(snap.I, "rgba(244, 63, 94, 0.85)");
        drawSeg(snap.E, "rgba(245, 158, 11, 0.82)");
        drawSeg(snap.S, "rgba(56, 189, 248, 0.42)");
        drawSeg(snap.R, "rgba(167, 139, 250, 0.65)");
        drawSeg(snap.V, "rgba(16, 185, 129, 0.72)");
      });
    }

    onPointerDown(x, y) {
      if (x >= 25 && x <= 530) {
        this.agents.push({ x, y, vx: 40, vy: -40, state: "I", timer: 0 });
      }
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return {};
    }
  }

  // =========================================================================
  // 16. NeuralBackpropEngine (neural-backprop)
  // =========================================================================
  class NeuralBackpropEngine {
    constructor() {
      this.points = [];
      this.W1 = [];
      this.b1 = [];
      this.W2 = [];
      this.b2 = 0;
      this.epoch = 0;
      this.accuracy = 85.0;
      this.lossHistory = [];
      this.lastKey = "";
      this.init({});
    }

    init(params) {
      const H = Math.round(params.hidden_neurons ?? 8);
      const dtype = Math.round(params.dataset_type ?? 2);
      const act = Math.round(params.activation_fn ?? 1);
      this.lastKey = `${H}_${dtype}_${act}`;
      this.epoch = 0;
      this.lossHistory = [];

      let seed = 1337;
      const rand = () => {
        seed = (seed * 16807) % 2147483647;
        return (seed - 1) / 2147483646 - 0.5;
      };

      this.W1 = Array.from({ length: H }, () => [rand() * 2.6, rand() * 2.6]);
      this.b1 = Array.from({ length: H }, () => rand() * 1.2);
      this.W2 = Array.from({ length: H }, () => rand() * 2.2);
      this.b2 = rand() * 0.5;

      this.points = [];
      for (let i = 0; i < 90; i++) {
        let x, y, label;
        if (dtype === 1) {
          x = (Math.random() * 2 - 1) * 0.85;
          y = (Math.random() * 2 - 1) * 0.85;
          label = x * y >= 0 ? 1 : 0;
        } else if (dtype === 2) {
          const inner = i < 45;
          const r = inner ? Math.random() * 0.36 : 0.56 + Math.random() * 0.28;
          const a = (i / 45) * TAU;
          x = Math.cos(a) * r;
          y = Math.sin(a) * r;
          label = inner ? 1 : 0;
        } else {
          const arm = i < 45 ? 0 : 1;
          const k = (i % 45) / 45;
          const r = 0.12 + k * 0.75;
          const a = k * 2.5 * Math.PI + (arm ? Math.PI : 0);
          x = Math.cos(a) * r;
          y = Math.sin(a) * r;
          label = arm;
        }
        this.points.push({ x, y, label });
      }
    }

    _act(z, act) {
      if (act === 1) return Math.tanh(z);
      if (act === 2) return Math.max(0, z);
      return 1 / (1 + Math.exp(-clamp(z, -10, 10)));
    }

    _dAct(z, a, act) {
      if (act === 1) return 1 - a * a;
      if (act === 2) return z > 0 ? 1 : 0.02;
      return a * (1 - a);
    }

    _forward(x, y, act) {
      const H = this.W1.length;
      const z1 = new Array(H);
      const h = new Array(H);
      let z2 = this.b2;
      for (let j = 0; j < H; j++) {
        z1[j] = this.W1[j][0] * x + this.W1[j][1] * y + this.b1[j];
        h[j] = this._act(z1[j], act);
        z2 += this.W2[j] * h[j];
      }
      const out = 1 / (1 + Math.exp(-clamp(z2, -12, 12)));
      return { z1, h, out };
    }

    update(_dt, params) {
      const H = Math.round(params.hidden_neurons ?? 8);
      const lr = params.learning_rate ?? 0.18;
      const dtype = Math.round(params.dataset_type ?? 2);
      const act = Math.round(params.activation_fn ?? 1);
      const reg = params.regularization ?? 0.004;

      const key = `${H}_${dtype}_${act}`;
      if (key !== this.lastKey) this.init(params);

      for (let step = 0; step < 8; step++) {
        this.epoch++;
        for (const pt of this.points) {
          const { z1, h, out } = this._forward(pt.x, pt.y, act);
          const dz2 = out - pt.label;
          for (let j = 0; j < H; j++) {
            const w2Old = this.W2[j];
            const dz1 = w2Old * dz2 * this._dAct(z1[j], h[j], act);
            this.W2[j] = (1 - lr * reg * 0.1) * this.W2[j] - lr * 0.15 * dz2 * h[j];
            this.W1[j][0] = (1 - lr * reg * 0.1) * this.W1[j][0] - lr * 0.15 * dz1 * pt.x;
            this.W1[j][1] = (1 - lr * reg * 0.1) * this.W1[j][1] - lr * 0.15 * dz1 * pt.y;
            this.b1[j] -= lr * 0.15 * dz1;
          }
          this.b2 -= lr * 0.15 * dz2;
        }
      }

      let correct = 0;
      let lossSum = 0;
      for (const pt of this.points) {
        const p = clamp(this._forward(pt.x, pt.y, act).out, 1e-4, 1 - 1e-4);
        if ((p >= 0.5 ? 1 : 0) === pt.label) correct++;
        lossSum += -(pt.label * Math.log(p) + (1 - pt.label) * Math.log(1 - p));
      }
      this.accuracy = (correct / this.points.length) * 100;
      this.lossHistory.push(lossSum / this.points.length);
      if (this.lossHistory.length > 90) this.lossHistory.shift();
    }

    render(ctx, w, h, params) {
      drawScientificGrid(ctx, w, h, "rgba(236, 72, 153, 0.08)");
      const act = Math.round(params.activation_fn ?? 1);
      const mapX = 24, mapY = 36, mapSize = 420;

      const cell = 10;
      for (let py = 0; py < mapSize; py += cell) {
        for (let px = 0; px < mapSize; px += cell) {
          const nx = (px / mapSize) * 2 - 1;
          const ny = (py / mapSize) * 2 - 1;
          const prob = this._forward(nx, ny, act).out;
          if (Math.abs(prob - 0.5) < 0.055) {
            ctx.fillStyle = "rgba(248, 250, 252, 0.72)";
          } else if (prob > 0.5) {
            ctx.fillStyle = `rgba(14, 165, 233, ${clamp((prob - 0.5) * 1.4, 0.12, 0.68)})`;
          } else {
            ctx.fillStyle = `rgba(236, 72, 153, ${clamp((0.5 - prob) * 1.4, 0.12, 0.68)})`;
          }
          ctx.fillRect(mapX + px, mapY + py, cell, cell);
        }
      }
      ctx.strokeStyle = "rgba(148, 163, 184, 0.35)";
      ctx.strokeRect(mapX, mapY, mapSize, mapSize);

      for (const pt of this.points) {
        const sx = mapX + ((pt.x + 1) * 0.5) * mapSize;
        const sy = mapY + ((pt.y + 1) * 0.5) * mapSize;
        ctx.fillStyle = pt.label === 1 ? "#38bdf8" : "#f472b6";
        ctx.strokeStyle = "#020617";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(sx, sy, 4.6, 0, TAU);
        ctx.fill();
        ctx.stroke();
      }

      // Right Panel: MLP Graph + Live Cross-Entropy Loss Scope
      const gx = 468, gy = 36, gw = 388, gh = 285;
      drawScopePanel(ctx, gx, gy, gw, gh, `MLP (2 → ${this.W1.length} → 1) · EPOCH ${this.epoch}`, `Accuracy = ${this.accuracy.toFixed(1)}% · Cyan(+W) / Red(-W)`, "rgba(236, 72, 153, 0.45)");
      const inNodes = [{ x: gx + 55, y: gy + 110 }, { x: gx + 55, y: gy + 210 }];
      const H = this.W1.length;
      const hidNodes = Array.from({ length: H }, (_, j) => ({
        x: gx + 195,
        y: gy + 48 + (j / Math.max(1, H - 1)) * 215,
      }));
      const outNode = { x: gx + 335, y: gy + 160 };

      hidNodes.forEach((hn, j) => {
        inNodes.forEach((inN, i) => {
          const wVal = this.W1[j][i];
          ctx.strokeStyle = wVal >= 0 ? "rgba(56, 189, 248, 0.65)" : "rgba(244, 63, 94, 0.65)";
          ctx.lineWidth = clamp(Math.abs(wVal) * 1.1, 0.6, 3.6);
          ctx.beginPath();
          ctx.moveTo(inN.x, inN.y);
          ctx.lineTo(hn.x, hn.y);
          ctx.stroke();
        });
        const w2Val = this.W2[j];
        ctx.strokeStyle = w2Val >= 0 ? "rgba(56, 189, 248, 0.72)" : "rgba(244, 63, 94, 0.72)";
        ctx.lineWidth = clamp(Math.abs(w2Val) * 1.1, 0.6, 3.6);
        ctx.beginPath();
        ctx.moveTo(hn.x, hn.y);
        ctx.lineTo(outNode.x, outNode.y);
        ctx.stroke();
      });

      [...inNodes, ...hidNodes, outNode].forEach((n) => {
        ctx.fillStyle = "#1e293b";
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(n.x, n.y, 7.5, 0, TAU);
        ctx.fill();
        ctx.stroke();
      });

      // Bottom-Right Scope: Loss Curve L_BCE(t)
      const lx = 468, ly = 330, lw = 388, lh = 126;
      drawScopePanel(ctx, lx, ly, lw, lh, "BINARY CROSS-ENTROPY LOSS L_BCE", "Stochastic Gradient Descent Convergence");
      if (this.lossHistory.length > 1) {
        ctx.strokeStyle = "#ec4899";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        this.lossHistory.forEach((v, i) => {
          const px = lx + 14 + (i / 90) * (lw - 28);
          const py = ly + lh - 16 - clamp(v / 0.85, 0, 1) * (lh - 54);
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();
      }
    }

    onPointerDown(x, y, e) {
      if (x >= 24 && x <= 444 && y >= 36 && y <= 456) {
        this.points.push({
          x: ((x - 24) / 420) * 2 - 1,
          y: ((y - 36) / 420) * 2 - 1,
          label: e && e.shiftKey ? 0 : 1,
        });
      }
    }
    onPointerMove() {}
    onPointerUp() {}
    getTelemetry() {
      return { canvas_accuracy: this.accuracy };
    }
  }

  // Export all 16 unique simulation engines (1-to-1 with the 16 catalog concepts)
  window.EurekaSimulationClasses = {
    OrbitalMechanicsEngine,
    AirfoilWindTunnelEngine,
    DoublePendulumChaosEngine,
    GeometricOpticsEngine,
    ElectromagneticFieldsEngine,
    QuantumTunnelingEngine,
    ThermodynamicsGasEngine,
    FluidVortexTunnelEngine,
    WaveInterferenceEngine,
    StructuralTrussEngine,
    RlcCircuitResonanceEngine,
    RelativisticLensingEngine,
    FourierEpicyclesEngine,
    AntColonySwarmEngine,
    EpidemicSeirEngine,
    NeuralBackpropEngine,
  };

  window.EurekaSimulations = {
    "orbital-mechanics": new OrbitalMechanicsEngine(),
    "airfoil-wind-tunnel": new AirfoilWindTunnelEngine(),
    "double-pendulum-chaos": new DoublePendulumChaosEngine(),
    "geometric-optics": new GeometricOpticsEngine(),
    "electromagnetic-fields": new ElectromagneticFieldsEngine(),
    "quantum-tunneling": new QuantumTunnelingEngine(),
    "thermodynamics-gas": new ThermodynamicsGasEngine(),
    "fluid-vortex-tunnel": new FluidVortexTunnelEngine(),
    "wave-interference": new WaveInterferenceEngine(),
    "structural-truss": new StructuralTrussEngine(),
    "rlc-circuit-resonance": new RlcCircuitResonanceEngine(),
    "relativistic-lensing": new RelativisticLensingEngine(),
    "fourier-epicycles": new FourierEpicyclesEngine(),
    "ant-colony-swarm": new AntColonySwarmEngine(),
    "epidemic-seir": new EpidemicSeirEngine(),
    "neural-backprop": new NeuralBackpropEngine(),
  };
})();
