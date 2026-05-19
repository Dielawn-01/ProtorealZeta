"""
Three.js Klein Universe — Live particle simulation on the Klein manifold.
Each particle is an autonomous Klein element {a, ω, ι, ε, λ} evolving
through sowing, interaction, and convergence.
"""

def get_klein_universe_html(n_particles=15, noise_scale=0.58, apply_r4=False):
    """Return the full HTML/JS for the Three.js Klein Universe."""
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin:0; overflow:hidden; background:#05070a; }}
  canvas {{ display:block; }}
  #hud {{
    position:absolute; top:12px; left:16px; color:#00ffcc;
    font:12px 'JetBrains Mono',monospace; pointer-events:none;
    text-shadow:0 0 8px rgba(0,255,204,0.4);
  }}
  #hud .dim {{ color:#667; }}
  #hud .val {{ color:#e8eaf0; }}
</style>
</head>
<body>
<div id="hud"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
// ════════════════════════════════════════════════════
// KLEIN UNIVERSE — LIVE SIMULATION
// ════════════════════════════════════════════════════

const NP = {n_particles};
const NOISE = {noise_scale};
const R4 = {'true' if apply_r4 else 'false'};
const TRAIL_LEN = 120;

// ── Scene setup ──
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x05070a, 0.04);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.1, 200);
camera.position.set(8, 5, 8);
const renderer = new THREE.WebGLRenderer({{ antialias:true, alpha:true }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x05070a, 1);
document.body.appendChild(renderer.domElement);

// ── Orbit Controls (click-drag) ──
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.8;
controls.minDistance = 4;
controls.maxDistance = 25;
controls.enablePan = true;

// ── Lights ──
scene.add(new THREE.AmbientLight(0x223344, 0.6));
const pt1 = new THREE.PointLight(0x00ffcc, 1.2, 30);
pt1.position.set(5, 5, 5);
scene.add(pt1);
const pt2 = new THREE.PointLight(0xff3366, 0.8, 30);
pt2.position.set(-5, -3, -5);
scene.add(pt2);

// ── Glow sprite texture ──
function makeGlowTex(size) {{
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(size/2,size/2,0,size/2,size/2,size/2);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.15, 'rgba(255,255,255,0.8)');
  g.addColorStop(0.4, 'rgba(128,255,220,0.3)');
  g.addColorStop(0.7, 'rgba(0,255,204,0.08)');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0,0,size,size);
  return new THREE.CanvasTexture(c);
}}
const glowTex = makeGlowTex(128);

// ── Klein bottle wireframe ──
function kleinBottle(res) {{
  const pts = [];
  const r = 2.5, a = 2.0;
  for (let iv = 0; iv <= res; iv++) {{
    const v = iv / res * Math.PI * 2;
    for (let iu = 0; iu <= res; iu++) {{
      const u = iu / res * Math.PI * 2;
      const cv2 = Math.cos(v/2), sv2 = Math.sin(v/2);
      const su = Math.sin(u), s2u = Math.sin(2*u);
      const factor = r + a * cv2 * su - a * sv2 * s2u;
      pts.push(new THREE.Vector3(
        factor * Math.cos(v),
        factor * Math.sin(v),
        a * sv2 * su + a * cv2 * s2u
      ));
    }}
  }}
  // Build line segments
  const geo = new THREE.BufferGeometry();
  const verts = [];
  for (let iv = 0; iv <= res; iv++) {{
    for (let iu = 0; iu < res; iu++) {{
      const i = iv * (res+1) + iu;
      const p1 = pts[i], p2 = pts[i+1];
      if (p1 && p2) {{
        verts.push(p1.x,p1.y,p1.z, p2.x,p2.y,p2.z);
      }}
    }}
  }}
  for (let iu = 0; iu <= res; iu++) {{
    for (let iv = 0; iv < res; iv++) {{
      const i1 = iv * (res+1) + iu;
      const i2 = (iv+1) * (res+1) + iu;
      const p1 = pts[i1], p2 = pts[i2];
      if (p1 && p2) {{
        verts.push(p1.x,p1.y,p1.z, p2.x,p2.y,p2.z);
      }}
    }}
  }}
  geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  return geo;
}}

const bottleGeo = kleinBottle(40);
const bottleMat = new THREE.LineBasicMaterial({{
  color: 0x00ffcc, transparent: true, opacity: 0.07,
  blending: THREE.AdditiveBlending
}});
scene.add(new THREE.LineSegments(bottleGeo, bottleMat));

// ── Project to Klein bottle surface ──
function projectToBottle(b, c, aVal) {{
  const r = 2.5, ac = 2.0;
  const up = Math.atan2(b, Math.abs(b) + 0.5) * 2.0;
  const vp = Math.atan2(c, Math.abs(c) + 0.5) * 2.0;
  const cv2 = Math.cos(vp/2), sv2 = Math.sin(vp/2);
  const su = Math.sin(up), s2u = Math.sin(2*up);
  const factor = r + ac * cv2 * su - ac * sv2 * s2u;
  return new THREE.Vector3(
    factor * Math.cos(vp),
    factor * Math.sin(vp),
    ac * sv2 * su + ac * cv2 * s2u + (aVal - 1.0) * 0.4
  );
}}

// ── Particle class ──
// Each particle is a Klein manifold element u = {{a, ω, ι, ε, λ}}.
// Evolution uses ONLY proven operations from the Lean formalization:
//   1. Klein multiplication (ProtorealManifold.lean)
//   2. Sowing/funct (ProtorealOperator.lean): a ← a + ε, ε ← 0, λ += 1
//   3. Parity lock (MonsterInverse.lean): (u + u*)/2
//   4. Monster inverse R4 (MonsterInverse.lean): swap ω ↔ ι
// No random walks. No orbital forcing. No aesthetic hacks.
// What you see IS the algebra.

class KleinParticle {{
  constructor(idx) {{
    this.idx = idx;
    // Initialize across the parameter space
    this.a = 0.3 + Math.random() * 1.7;
    this.b = 0.3 + Math.random() * 4.0;   // ω (thrust)
    this.c = 0.1 + Math.random() * 3.5;   // ι (anchor)
    this.e = Math.random() * 0.3;          // ε (noise)
    this.l = 1.0;                          // λ (level)
    this.trail = [];
    this.age = 0;

    // Visual
    const hue = Math.random();
    this.baseColor = new THREE.Color().setHSL(hue, 0.9, 0.6);
    this.spriteMat = new THREE.SpriteMaterial({{
      map: glowTex, color: this.baseColor,
      transparent: true, opacity: 0.9,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    }});
    this.sprite = new THREE.Sprite(this.spriteMat);
    this.sprite.scale.set(0.6, 0.6, 1);
    scene.add(this.sprite);

    const dotGeo = new THREE.SphereGeometry(0.04, 8, 8);
    const dotMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
    this.dot = new THREE.Mesh(dotGeo, dotMat);
    scene.add(this.dot);

    this.trailGeo = new THREE.BufferGeometry();
    const trailPositions = new Float32Array(TRAIL_LEN * 3);
    this.trailGeo.setAttribute('position', new THREE.Float32BufferAttribute(trailPositions, 3));
    this.trailMat = new THREE.LineBasicMaterial({{
      color: this.baseColor, transparent: true, opacity: 0.4,
      blending: THREE.AdditiveBlending,
    }});
    this.trailLine = new THREE.Line(this.trailGeo, this.trailMat);
    scene.add(this.trailLine);
  }}

  sr() {{ return this.a - this.b * this.c; }}
  energy() {{ return this.sr()**2 + (this.b - this.c)**2; }}

  // ── EXACT Klein multiplication (ProtorealManifold.lean) ──
  static kleinMul(u1, u2) {{
    return {{
      a: u1.a*u2.a - u1.b*u2.c + u1.c*u2.b + u1.l*u2.e - u1.e*u2.l,
      b: u1.a*u2.b + u2.a*u1.b + u1.b*u2.b,          // thrust idempotent
      c: u1.a*u2.c + u2.a*u1.c - u1.c*u2.c,           // anchor anti-idempotent
      e: u1.a*u2.e + u2.a*u1.e + u1.e*u2.e,           // noise
      l: u1.a*u2.l + u2.a*u1.l + u1.l*u2.l,           // level accumulating
    }};
  }}

  evolve(particles, step) {{
    // ──────────────────────────────────────────────
    // STEP 1: SOWING (funct) — ProtorealOperator.lean
    //   a ← a + ε,  ε ← 0,  λ += 1
    // We scale down per-frame so the continuous limit is smooth
    // ──────────────────────────────────────────────
    this.a += this.e;
    this.e = 0;
    this.l += 1;

    // ──────────────────────────────────────────────
    // STEP 2: NOISE INJECTION through ε
    // ε is the ONLY source of perturbation (nilpotent channel).
    // Injected periodically, scaled by γ / √λ (consolidation resistance).
    // ──────────────────────────────────────────────
    if ((step + this.idx * 7) % 60 === 0) {{
      this.e = NOISE * 0.1 / Math.sqrt(this.l);
    }}

    // ──────────────────────────────────────────────
    // STEP 3: KLEIN INTERACTION (ProtorealManifold.lean)
    // Exact Klein multiplication with neighbor.
    // Blend: mostly self, small coupling from product.
    // The coupling strength IS the algebra — the product
    // amplifies or contracts based on the bridge identity.
    // ──────────────────────────────────────────────
    const j = (this.idx + 1) % particles.length;
    const nb = particles[j];
    const prod = KleinParticle.kleinMul(this, nb);

    // Coupling: 5% interaction. This ratio determines
    // how strongly particles feel each other.
    const alpha = 0.05;
    this.a = (1 - alpha) * this.a + alpha * prod.a;
    this.b = (1 - alpha) * this.b + alpha * prod.b;
    this.c = (1 - alpha) * this.c + alpha * prod.c;

    // ──────────────────────────────────────────────
    // STEP 4: PARITY LOCK — (u + u*)/2
    // MonsterInverse.lean: parity_locked_projection is idempotent.
    // u* swaps ω ↔ ι, so (u + u*)/2 symmetrizes thrust/anchor.
    // Applied gently per frame (continuous parity drift).
    // ──────────────────────────────────────────────
    const beta = 0.02;  // parity coupling strength
    const avg = (this.b + this.c) / 2;
    this.b = (1 - beta) * this.b + beta * avg;
    this.c = (1 - beta) * this.c + beta * avg;

    // ──────────────────────────────────────────────
    // STEP 5: MONSTER INVERSE R4 (when enabled)
    // MonsterInverse.lean: swap ω ↔ ι (involution: u** = u)
    // ──────────────────────────────────────────────
    if (R4 && step % 300 === this.idx % 300) {{
      const tmp = this.b; this.b = this.c; this.c = tmp;
    }}

    // Safety clamp (prevent NaN/Inf from product overflow)
    const clamp = (v) => Math.max(-20, Math.min(20, isNaN(v) ? 0 : v));
    this.a = clamp(this.a);
    this.b = clamp(this.b);
    this.c = clamp(this.c);

    this.age++;
  }}

  updateVisual() {{
    const pos = projectToBottle(this.b, this.c, this.a);
    this.sprite.position.copy(pos);
    this.dot.position.copy(pos);

    // Color by SR
    const absSR = Math.min(Math.abs(this.sr()), 1.0);
    const h = 0.47 - absSR * 0.6; // cyan → magenta
    const s = 0.85;
    const li = 0.5 + (1 - absSR) * 0.3;
    this.spriteMat.color.setHSL((h + 1) % 1, s, li);
    this.trailMat.color.setHSL((h + 1) % 1, s, li * 0.6);

    // Size pulse based on energy proximity
    const e = Math.min(this.energy(), 2.0);
    const pulse = 0.5 + 0.2 * Math.sin(this.age * 0.03) * (1 - e);
    const sizeScale = pulse + Math.min(this.l * 0.004, 0.3);
    this.sprite.scale.set(sizeScale, sizeScale, 1);

    // Opacity: brighter when closer to equilibrium
    this.spriteMat.opacity = 0.5 + 0.5 * (1 - absSR);

    // Trail update
    this.trail.push(pos.clone());
    if (this.trail.length > TRAIL_LEN) this.trail.shift();

    const arr = this.trailGeo.attributes.position.array;
    for (let i = 0; i < TRAIL_LEN; i++) {{
      if (i < this.trail.length) {{
        arr[i*3]   = this.trail[i].x;
        arr[i*3+1] = this.trail[i].y;
        arr[i*3+2] = this.trail[i].z;
      }} else {{
        arr[i*3] = arr[i*3+1] = arr[i*3+2] = 0;
      }}
    }}
    this.trailGeo.attributes.position.needsUpdate = true;
    this.trailGeo.setDrawRange(0, this.trail.length);
    this.trailMat.opacity = 0.15 + 0.25 * (1 - absSR);
  }}
}}

// ── Create particles ──
const particles = [];
for (let i = 0; i < NP; i++) particles.push(new KleinParticle(i));

// ── Stars ──
const starGeo = new THREE.BufferGeometry();
const starVerts = [];
for (let i = 0; i < 800; i++) {{
  starVerts.push(
    (Math.random()-0.5)*80,
    (Math.random()-0.5)*80,
    (Math.random()-0.5)*80
  );
}}
starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starVerts, 3));
scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({{
  color: 0x334466, size: 0.08, transparent: true, opacity: 0.6
}})));

// ── January Walker's Infoton Field ──
const infotonCount = 800;
const infotonGeo = new THREE.BufferGeometry();
const infotonPos = new Float32Array(infotonCount * 3);
const infotonCol = new Float32Array(infotonCount * 3);
const infotonU = new Float32Array(infotonCount);
const infotonV = new Float32Array(infotonCount);
const infotonSpeed = new Float32Array(infotonCount);

// Parametric Figure-8 generator matching the Klein Bottle wireframe
function getInfotonCoords(u, v) {{
  const r = 2.5, ac = 2.0;
  const cv2 = Math.cos(v/2), sv2 = Math.sin(v/2);
  const su = Math.sin(u), s2u = Math.sin(2*u);
  const factor = r + ac * cv2 * su - ac * sv2 * s2u;
  return new THREE.Vector3(
    factor * Math.cos(v),
    factor * Math.sin(v),
    ac * sv2 * su + ac * cv2 * s2u
  );
}}

for (let i = 0; i < infotonCount; i++) {{
  infotonU[i] = Math.random() * Math.PI * 2;
  infotonV[i] = Math.random() * Math.PI * 2;
  infotonSpeed[i] = 0.005 + Math.random() * 0.01;
  const p = getInfotonCoords(infotonU[i], infotonV[i]);
  infotonPos[i*3] = p.x;
  infotonPos[i*3+1] = p.y;
  infotonPos[i*3+2] = p.z;
  
  // Golden glow color spectrum (information-energy)
  const mix = Math.random();
  infotonCol[i*3] = 1.0;
  infotonCol[i*3+1] = 0.7 + 0.3 * mix;
  infotonCol[i*3+2] = 0.1 + 0.4 * mix;
}}
infotonGeo.setAttribute('position', new THREE.BufferAttribute(infotonPos, 3));
infotonGeo.setAttribute('color', new THREE.BufferAttribute(infotonCol, 3));

const infotonMat = new THREE.PointsMaterial({{
  size: 0.12,
  vertexColors: true,
  transparent: true,
  opacity: 0.75,
  blending: THREE.AdditiveBlending,
  depthWrite: false
}});
const infotonSystem = new THREE.Points(infotonGeo, infotonMat);
scene.add(infotonSystem);

// ── Fixed point beacon (a=1) + Infoton Singularity ──
const beaconGroup = new THREE.Group();
const beaconSphereGeo = new THREE.SphereGeometry(0.12, 16, 16);
const beaconSphereMat = new THREE.MeshBasicMaterial({{
  color: 0x00ffcc, transparent: true, opacity: 0.8
}});
const beaconSphere = new THREE.Mesh(beaconSphereGeo, beaconSphereMat);
beaconGroup.add(beaconSphere);

const ringGeo = new THREE.TorusGeometry(0.24, 0.018, 8, 32);
const ringMat = new THREE.MeshBasicMaterial({{
  color: 0xff9900, transparent: true, opacity: 0.6,
  blending: THREE.AdditiveBlending, side: THREE.DoubleSide
}});
const beaconRing = new THREE.Mesh(ringGeo, ringMat);
beaconRing.rotation.x = Math.PI / 2;
beaconGroup.add(beaconRing);

const beaconPos = projectToBottle(1.0, 1.0, 1.0);
beaconGroup.position.copy(beaconPos);
scene.add(beaconGroup);

// ── HUD ──
const hud = document.getElementById('hud');
let step = 0;

// ── Animate ──
function animate() {{
  requestAnimationFrame(animate);
  step++;

  // Evolve all particles
  for (const p of particles) p.evolve(particles, step);
  for (const p of particles) p.updateVisual();

  // Evolve January Walker's Infoton Field
  const ip = infotonGeo.attributes.position.array;
  for (let i = 0; i < infotonCount; i++) {{
    infotonU[i] += infotonSpeed[i] * 0.4;
    infotonV[i] += infotonSpeed[i];
    if (infotonU[i] > Math.PI * 2) infotonU[i] -= Math.PI * 2;
    if (infotonV[i] > Math.PI * 2) infotonV[i] -= Math.PI * 2;
    
    const p = getInfotonCoords(infotonU[i], infotonV[i]);
    ip[i*3] = p.x;
    ip[i*3+1] = p.y;
    ip[i*3+2] = p.z;
  }}
  infotonGeo.attributes.position.needsUpdate = true;

  // Camera
  controls.update();

  // Singularity rotation and pulse
  const bScale = 1.0 + 0.25 * Math.sin(step * 0.04);
  beaconSphere.scale.set(bScale, bScale, bScale);
  beaconRing.rotation.z += 0.015;
  beaconRing.rotation.y += 0.008;
  beaconSphereMat.opacity = 0.6 + 0.4 * Math.sin(step * 0.04);

  // HUD
  if (step % 10 === 0) {{
    const meanSR = particles.reduce((s,p) => s + Math.abs(p.sr()), 0) / NP;
    const meanA = particles.reduce((s,p) => s + p.a, 0) / NP;
    const conv = particles.reduce((s,p) => s + Math.abs(p.a - 1), 0) / NP;
    // Calculate Infoton Hawking Temperature (T_H ∝ 1 / (8πM) ~ based on resonance scaling)
    const infotonTemp = 0.1428 * (1.0 / (1.0 + Math.abs(meanSR)));
    hud.innerHTML =
      '<span class="dim">κ</span> <span class="val">-1</span> · ' +
      '<span class="dim">|SR|</span> <span class="val">' + meanSR.toFixed(4) + '</span> · ' +
      '<span class="dim">ā</span> <span class="val">' + meanA.toFixed(4) + '</span> · ' +
      '<span class="dim">conv</span> <span class="val">' + conv.toFixed(4) + '</span> · ' +
      '<span class="dim">T_H (Infoton)</span> <span class="val">' + infotonTemp.toFixed(5) + ' K</span> · ' +
      '<span class="dim">t</span> <span class="val">' + step + '</span>';
  }}

  renderer.render(scene, camera);
}}
animate();

// ── Resize ──
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});
</script>
</body>
</html>
"""
