// Interactive 3D scenes (Three.js). Each scene reacts to hover:
// the hero particle core morphs between shapes, and each product model animates.
import * as THREE from 'three';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
// Palette mirrors the CSS theme tokens: logo blue, ice white and lime signal
const BLUE = new THREE.Color('#4d8dff');
const ICE = new THREE.Color('#dfe8ff');
const SIGNAL = new THREE.Color('#b6ff3b');

const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const clamp01 = t => Math.min(Math.max(t, 0), 1);

/* ------------------------------------------------------------------ */
/* Stage: renderer + camera + resize + visibility + hover factor       */
/* ------------------------------------------------------------------ */
const stages = [];

function createStage(canvas, { fov = 35, z = 6, hoverTarget = canvas, minAspect = 0 } = {}) {
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(fov, 1, 0.1, 100);
    camera.position.set(0, 0, z);

    const stage = { renderer, scene, camera, canvas, visible: false, hover: false, h: 0, mouse: new THREE.Vector2(), update: null };

    const resize = () => {
        const { clientWidth: w, clientHeight: h } = canvas;
        if (!w || !h) return;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        // pull the camera back on narrow stages so wide models stay in frame
        if (minAspect) camera.position.setLength(z * Math.max(1, minAspect / camera.aspect));
        camera.updateProjectionMatrix();
    };
    new ResizeObserver(resize).observe(canvas);
    resize();

    new IntersectionObserver(([e]) => { stage.visible = e.isIntersecting; }, { rootMargin: '100px' }).observe(canvas);

    hoverTarget.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') setHover(true); });
    hoverTarget.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') setHover(false); });
    hoverTarget.addEventListener('pointermove', e => {
        const r = canvas.getBoundingClientRect();
        stage.mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    });
    // Touch: tap toggles the hover state
    hoverTarget.addEventListener('click', e => {
        if (finePointer || e.target.closest('button, a')) return;
        setHover(!stage.hover);
    });
    function setHover(v) {
        stage.hover = v;
        hoverTarget.classList.toggle('is-hover', v);
        stage.onHover?.(v);
    }

    stages.push(stage);
    return stage;
}

function addLights(scene) {
    scene.add(new THREE.HemisphereLight('#bfe9ff', '#0a1428', 1.1));
    const key = new THREE.DirectionalLight('#ffffff', 2.2);
    key.position.set(3, 4, 5);
    scene.add(key);
    const rim = new THREE.PointLight('#22d3ee', 18, 12);
    rim.position.set(-3, 1, -2);
    scene.add(rim);
    const fill = new THREE.PointLight('#8b5cf6', 10, 12);
    fill.position.set(3, -2, 2);
    scene.add(fill);
}

function canvasTexture(w, h, draw) {
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const ctx = c.getContext('2d');
    draw(ctx, w, h);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;
    tex.userData = { ctx, draw };
    return tex;
}

function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
}

function roundedRectShape(w, h, r) {
    const s = new THREE.Shape();
    const x = -w / 2, y = -h / 2;
    s.moveTo(x + r, y);
    s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
    s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
    return s;
}

/* ------------------------------------------------------------------ */
/* HERO: particle core that morphs into other shapes on hover          */
/* ------------------------------------------------------------------ */
const N = 4200;

function shapeSphere() {
    const a = new Float32Array(N * 3);
    const g = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < N; i++) {
        const y = 1 - (i / (N - 1)) * 2;
        const r = Math.sqrt(1 - y * y);
        const th = g * i;
        const R = 1.55 + (Math.random() - 0.5) * 0.04;
        a.set([Math.cos(th) * r * R, y * R, Math.sin(th) * r * R], i * 3);
    }
    return a;
}

function shapeTorusKnot() {
    const a = new Float32Array(N * 3);
    const p = 2, q = 3, v = new THREE.Vector3();
    for (let i = 0; i < N; i++) {
        const t = (i / N) * Math.PI * 2;
        const r = Math.cos(q * t) + 2;
        v.set(r * Math.cos(p * t), r * Math.sin(p * t), -Math.sin(q * t)).multiplyScalar(0.62);
        v.add(new THREE.Vector3().randomDirection().multiplyScalar(0.16 * Math.cbrt(Math.random())));
        a.set([v.x, v.y, v.z], i * 3);
    }
    return a;
}

function shapeCube() {
    const a = new Float32Array(N * 3);
    const s = 1.15;
    for (let i = 0; i < N; i++) {
        const face = i % 6, axis = face >> 1, sign = face & 1 ? 1 : -1;
        // bias points towards edges for a crisp "wireframe" look
        const u = Math.random() < 0.35 ? Math.sign(Math.random() - 0.5) * (1 - Math.random() * 0.05) : Math.random() * 2 - 1;
        const w = Math.random() * 2 - 1;
        const p = [0, 0, 0];
        p[axis] = sign * s;
        p[(axis + 1) % 3] = u * s;
        p[(axis + 2) % 3] = w * s;
        a.set(p, i * 3);
    }
    return a;
}

function shapeHelix() {
    const a = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
        const t = Math.random();
        const y = (t - 0.5) * 3.8;
        const ang = t * Math.PI * 6;
        if (i % 7 === 0) {
            // rungs between the strands
            const k = Math.random() * 2 - 1;
            a.set([Math.cos(ang) * 0.75 * k, y, Math.sin(ang) * 0.75 * k], i * 3);
        } else {
            const off = i % 2 ? Math.PI : 0;
            const j = () => (Math.random() - 0.5) * 0.12;
            a.set([Math.cos(ang + off) * 0.75 + j(), y + j(), Math.sin(ang + off) * 0.75 + j()], i * 3);
        }
    }
    return a;
}

// Samples the Anqah wings logo from its PNG alpha channel
function shapeFromImage(src) {
    return new Promise(resolve => {
        const img = new Image();
        img.onload = () => {
            const w = 220, h = Math.round((img.height / img.width) * w);
            const c = document.createElement('canvas');
            c.width = w; c.height = h;
            const ctx = c.getContext('2d');
            ctx.drawImage(img, 0, 0, w, h);
            const data = ctx.getImageData(0, 0, w, h).data;
            const pts = [];
            for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (data[(y * w + x) * 4 + 3] > 120) pts.push(x, y);
            if (!pts.length) return resolve(null);
            const a = new Float32Array(N * 3);
            const scale = 3.8 / w;
            for (let i = 0; i < N; i++) {
                const k = Math.floor(Math.random() * (pts.length / 2)) * 2;
                a.set([
                    (pts[k] - w / 2 + Math.random()) * scale,
                    -(pts[k + 1] - h / 2 + Math.random()) * scale + 0.1,
                    (Math.random() - 0.5) * 0.12,
                ], i * 3);
            }
            resolve(a);
        };
        img.onerror = () => resolve(null);
        img.src = src;
    });
}

function dotTexture() {
    return canvasTexture(64, 64, (ctx) => {
        const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        g.addColorStop(0, 'rgba(255,255,255,1)');
        g.addColorStop(0.35, 'rgba(255,255,255,0.8)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, 64, 64);
    });
}

async function initHero() {
    const canvas = document.getElementById('heroCanvas');
    if (!canvas) return;
    const stage = createStage(canvas, { fov: 40, z: 6.2 });
    const { scene } = stage;
    const label = document.getElementById('shapeName');

    const sphere = shapeSphere();
    const shapes = [
        { name: 'anqah wings', pos: shapeTorusKnot(), face: true },
        { name: 'torus knot', pos: shapeTorusKnot() },
        { name: 'data cube', pos: shapeCube() },
        { name: 'dna helix', pos: shapeHelix() },
    ];
    shapeFromImage('images/logo-mark.png').then(p => { if (p) shapes[0].pos = p; });

    const geo = new THREE.BufferGeometry();
    const current = sphere.slice();
    geo.setAttribute('position', new THREE.BufferAttribute(current, 3));
    const colors = new Float32Array(N * 3);
    const c = new THREE.Color();
    for (let i = 0; i < N; i++) {
        if (Math.random() < 0.12) c.copy(SIGNAL);
        else c.copy(BLUE).lerp(ICE, Math.random() * 0.75);
        colors.set([c.r, c.g, c.b], i * 3);
    }
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const mat = new THREE.PointsMaterial({
        size: 0.06, map: dotTexture(), vertexColors: true, transparent: true,
        depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true,
    });
    const group = new THREE.Group();
    group.add(new THREE.Points(geo, mat));
    scene.add(group);

    // Orbit rings + nodes, like a tech HUD
    const rings = new THREE.Group();
    [2.25, 2.7].forEach((r, i) => {
        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(r, 0.006, 8, 160),
            new THREE.MeshBasicMaterial({ color: i ? SIGNAL : BLUE, transparent: true, opacity: 0.35 })
        );
        ring.rotation.x = Math.PI / 2 + (i ? 0.35 : -0.25);
        ring.rotation.y = i ? 0.3 : -0.2;
        rings.add(ring);
        for (let k = 0; k < 3; k++) {
            const node = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 16), new THREE.MeshBasicMaterial({ color: k % 2 ? SIGNAL : BLUE }));
            node.userData = { r, ring, phase: (k / 3) * Math.PI * 2 + i, speed: 0.25 + i * 0.15 };
            rings.add(node);
        }
    });
    scene.add(rings);

    let from = sphere.slice(), to = sphere, progress = 1, morphStart = 0, idx = -1;
    const morphMs = reducedMotion ? 300 : 1200;
    let faceCamera = false;
    function morphTo(arr) {
        from = current.slice();
        to = arr;
        progress = 0;
        morphStart = performance.now();
    }
    stage.onHover = (on) => {
        if (on) {
            idx = (idx + 1) % shapes.length;
            morphTo(shapes[idx].pos);
            faceCamera = !!shapes[idx].face;
            label.textContent = shapes[idx].name;
        } else {
            morphTo(sphere);
            faceCamera = false;
            label.textContent = 'core';
        }
    };

    const tmp = new THREE.Vector3();
    stage.update = (t, dt) => {
        if (progress < 1) {
            progress = Math.min((performance.now() - morphStart) / morphMs, 1);
            for (let i = 0; i < N; i++) {
                // stagger each particle slightly for a flowing morph
                const local = ease(clamp01(progress * 1.35 - (i / N) * 0.35));
                const j = i * 3;
                current[j] = lerp(from[j], to[j], local);
                current[j + 1] = lerp(from[j + 1], to[j + 1], local);
                current[j + 2] = lerp(from[j + 2], to[j + 2], local);
            }
            geo.attributes.position.needsUpdate = true;
        }
        const spin = reducedMotion ? 0.05 : 0.22;
        if (faceCamera) {
            const target = Math.round(group.rotation.y / (Math.PI * 2)) * Math.PI * 2 + stage.mouse.x * 0.35;
            group.rotation.y = lerp(group.rotation.y, target, 0.05);
        } else {
            group.rotation.y += dt * spin;
        }
        group.rotation.x = lerp(group.rotation.x, -stage.mouse.y * 0.3, 0.05);
        mat.size = lerp(mat.size, stage.hover ? 0.052 : 0.06, 0.1);
        rings.rotation.z = Math.sin(t * 0.2) * 0.1;
        rings.children.forEach(o => {
            if (!o.userData.ring) return;
            const { r, ring, phase, speed } = o.userData;
            const a = phase + t * speed;
            tmp.set(Math.cos(a) * r, Math.sin(a) * r, 0).applyEuler(ring.rotation);
            o.position.copy(tmp);
        });
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: SELLO / SELLO Lite — phone with floating UI panels         */
/* ------------------------------------------------------------------ */
function drawAppScreen(ctx, w, h, { title, accent, lite }) {
    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0b1730');
    bg.addColorStop(1, '#050b18');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = accent;
    ctx.font = 'bold 36px "Chakra Petch", sans-serif';
    ctx.fillText(title, 24, 70);
    ctx.fillStyle = '#8ea3c4';
    ctx.font = '16px "IBM Plex Sans", sans-serif';
    ctx.fillText(lite ? 'Quick Billing' : 'Business Dashboard', 24, 98);
    // total card
    roundRect(ctx, 20, 120, w - 40, 96, 14);
    ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill();
    ctx.fillStyle = '#8ea3c4'; ctx.font = '14px "IBM Plex Sans", sans-serif'; ctx.fillText("TODAY'S SALES", 36, 150);
    ctx.fillStyle = '#e6eefc'; ctx.font = 'bold 36px "IBM Plex Sans", sans-serif'; ctx.fillText('₹ 24,580', 36, 196);
    // bars
    const bars = lite ? [0.4, 0.7, 0.55, 0.9] : [0.35, 0.6, 0.45, 0.8, 0.65, 0.95, 0.75];
    const bw = (w - 60) / bars.length;
    bars.forEach((v, i) => {
        const bh = v * 120;
        const g = ctx.createLinearGradient(0, 360 - bh, 0, 360);
        g.addColorStop(0, accent); g.addColorStop(1, '#3b82f6');
        ctx.fillStyle = g;
        roundRect(ctx, 30 + i * bw, 360 - bh, bw - 10, bh, 5); ctx.fill();
    });
    // list rows
    for (let i = 0; i < (lite ? 2 : 3); i++) {
        roundRect(ctx, 20, 384 + i * 40, w - 40, 32, 8);
        ctx.fillStyle = 'rgba(255,255,255,0.05)'; ctx.fill();
        ctx.fillStyle = '#e6eefc'; ctx.font = '13px "IBM Plex Sans", sans-serif';
        ctx.fillText(['Invoice #1042', 'Invoice #1041', 'Stock update'][i], 32, 405 + i * 40);
        ctx.fillStyle = accent; ctx.fillText(['₹ 1,250', '₹ 860', '+24'][i], w - 90, 405 + i * 40);
    }
    // bottom button
    roundRect(ctx, 20, h - 64, w - 40, 44, 12);
    ctx.fillStyle = accent; ctx.fill();
    ctx.fillStyle = '#0a0d05'; ctx.font = 'bold 16px "IBM Plex Sans", sans-serif';
    ctx.fillText('+ NEW BILL', w / 2 - 50, h - 36);
}

function drawPanel(ctx, w, h, { icon, title, value, accent }) {
    roundRect(ctx, 4, 4, w - 8, h - 8, 22);
    ctx.fillStyle = 'rgba(10,20,40,0.92)'; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = accent; ctx.stroke();
    ctx.font = '44px sans-serif'; ctx.fillText(icon, 22, 74);
    ctx.fillStyle = '#8ea3c4'; ctx.font = '20px "IBM Plex Sans", sans-serif'; ctx.fillText(title, 90, 50);
    ctx.fillStyle = '#e6eefc'; ctx.font = 'bold 32px "IBM Plex Sans", sans-serif'; ctx.fillText(value, 90, 88);
}

function initPhone(canvas, { lite }) {
    const card = canvas.closest('.product');
    const stage = createStage(canvas, { fov: 32, z: 5.6, hoverTarget: card, minAspect: 1.5 });
    const { scene } = stage;
    addLights(scene);
    const accent = lite ? '#4d8dff' : '#b6ff3b';
    const title = lite ? 'SELLO Lite' : 'SELLO';

    const root = new THREE.Group();
    scene.add(root);
    const phone = new THREE.Group();
    root.add(phone);

    const W = lite ? 1.0 : 1.12, H = lite ? 2.0 : 2.24;
    const bodyGeo = new THREE.ExtrudeGeometry(roundedRectShape(W, H, 0.16), {
        depth: 0.1, bevelEnabled: true, bevelThickness: 0.035, bevelSize: 0.035, bevelSegments: 4, curveSegments: 16,
    });
    bodyGeo.center();
    const body = new THREE.Mesh(bodyGeo, new THREE.MeshStandardMaterial({ color: lite ? '#16314f' : '#1d1f3f', metalness: 0.8, roughness: 0.3 }));
    phone.add(body);

    const screenTex = canvasTexture(256, 512, (ctx, w, h) => drawAppScreen(ctx, w, h, { title, accent, lite }));
    const screen = new THREE.Mesh(
        new THREE.ShapeGeometry(roundedRectShape(W - 0.1, H - 0.1, 0.12)),
        new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false })
    );
    // map ShapeGeometry UVs (shape space) to 0..1
    const uv = screen.geometry.attributes.uv, pos = screen.geometry.attributes.position;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / (W - 0.1) + 0.5, pos.getY(i) / (H - 0.1) + 0.5);
    screen.position.z = 0.087;
    phone.add(screen);

    // Camera bump on the back
    const cam = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.04, 24), new THREE.MeshStandardMaterial({ color: '#0a0f1f', metalness: 0.9, roughness: 0.2 }));
    cam.rotation.x = Math.PI / 2;
    cam.position.set(-W / 2 + 0.25, H / 2 - 0.25, -0.09);
    phone.add(cam);

    // Floating UI panels that fly out of the screen on hover
    const panelDefs = lite
        ? [
            { icon: '🧾', title: 'Bill saved', value: '₹ 860', to: [1.25, 0.55, 0.6], rot: -0.25 },
            { icon: '⚡', title: 'Checkout', value: '3 sec', to: [-1.25, -0.45, 0.5], rot: 0.25 },
        ]
        : [
            { icon: '📦', title: 'Inventory', value: '1,284', to: [1.35, 0.75, 0.6], rot: -0.3 },
            { icon: '📈', title: 'Growth', value: '+18%', to: [-1.4, 0.35, 0.7], rot: 0.3 },
            { icon: '👥', title: 'Customers', value: '342', to: [1.25, -0.7, 0.5], rot: -0.2 },
        ];
    const panels = panelDefs.map((d, i) => {
        const tex = canvasTexture(320, 120, (ctx, w, h) => drawPanel(ctx, w, h, { ...d, accent }));
        const m = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 0.43), new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0, side: THREE.DoubleSide, toneMapped: false }));
        m.userData = { ...d, delay: i * 0.12 };
        root.add(m);
        return m;
    });

    // Lite: a receipt that prints out of the top of the phone
    let receipt;
    if (lite) {
        const tex = canvasTexture(128, 256, (ctx, w, h) => {
            ctx.fillStyle = '#f1f5f9'; ctx.fillRect(0, 0, w, h);
            ctx.fillStyle = '#0b1730'; ctx.font = 'bold 16px monospace'; ctx.fillText('SELLO LITE', 14, 28);
            ctx.font = '12px monospace';
            ['Item A   ₹ 250', 'Item B   ₹ 410', 'Item C   ₹ 200', '--------------', 'TOTAL    ₹ 860'].forEach((l, i) => ctx.fillText(l, 10, 62 + i * 22));
            for (let x = 0; x < w; x += 12) { ctx.beginPath(); ctx.moveTo(x, h); ctx.lineTo(x + 6, h - 8); ctx.lineTo(x + 12, h); ctx.fill(); }
        });
        receipt = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 1.24), new THREE.MeshBasicMaterial({ map: tex, transparent: true, side: THREE.DoubleSide }));
        receipt.position.set(0, H / 2 - 0.62, -0.02);
        phone.add(receipt);
    }

    stage.update = (t, dt) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        root.position.y = Math.sin(t * 1.4) * 0.06 * motion;
        phone.rotation.y = lerp(Math.sin(t * 0.6) * 0.5 * motion, stage.mouse.x * 0.35, h);
        phone.rotation.x = lerp(0.08, -stage.mouse.y * 0.2, h);
        phone.rotation.z = lerp(0.12, 0, h);
        phone.scale.setScalar(lerp(1, 0.9, h));
        panels.forEach(p => {
            const k = ease(clamp01((h - p.userData.delay) / (1 - p.userData.delay)));
            const [x, y, z] = p.userData.to;
            p.position.set(lerp(0, x, k), lerp(0, y, k) + Math.sin(t * 2 + x) * 0.04 * k, lerp(0, z, k));
            p.rotation.y = lerp(0, p.userData.rot, k);
            p.scale.setScalar(lerp(0.3, 1, k));
            p.material.opacity = k;
        });
        if (receipt) receipt.position.y = H / 2 - 0.62 + ease(h) * 0.85;
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: Automatic Bell — swings and emits sound rings on hover      */
/* ------------------------------------------------------------------ */
function initBell(canvas) {
    const card = canvas.closest('.product');
    const stage = createStage(canvas, { fov: 32, z: 7.2, hoverTarget: card, minAspect: 1.5 });
    const { scene } = stage;
    addLights(scene);

    const root = new THREE.Group();
    root.position.y = -0.15;
    scene.add(root);

    const metal = new THREE.MeshStandardMaterial({ color: '#c9a646', metalness: 0.95, roughness: 0.25, side: THREE.DoubleSide, emissive: '#3a2a05', emissiveIntensity: 0.4 });
    const steel = new THREE.MeshStandardMaterial({ color: '#1e2a44', metalness: 0.8, roughness: 0.35 });

    // Wall mount bracket
    const plate = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.18, 0.4), steel);
    plate.position.y = 1.3;
    root.add(plate);

    const pivot = new THREE.Group();
    pivot.position.y = 1.2;
    root.add(pivot);

    // Bell body (lathe profile, like a Blender screw/spin modifier)
    const profile = [
        [0.0, 0.02], [0.14, 0.0], [0.24, -0.08], [0.31, -0.28], [0.36, -0.6], [0.43, -0.9],
        [0.58, -1.12], [0.76, -1.28], [0.82, -1.36], [0.78, -1.4],
    ].map(([x, y]) => new THREE.Vector2(x, y));
    const bell = new THREE.Mesh(new THREE.LatheGeometry(profile, 64), metal);
    pivot.add(bell);
    const crown = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.035, 12, 24), metal);
    crown.position.y = 0.06;
    pivot.add(crown);

    // Clapper hangs from the inside top
    const clapperPivot = new THREE.Group();
    clapperPivot.position.y = -0.1;
    pivot.add(clapperPivot);
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.0, 8), steel);
    rod.position.y = -0.5;
    clapperPivot.add(rod);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 24), steel);
    ball.position.y = -1.05;
    clapperPivot.add(ball);

    // Controller box with a timetable display
    const timerTex = canvasTexture(256, 128, (ctx, w, h) => {
        ctx.fillStyle = '#04101f'; ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = '#b6ff3b'; ctx.font = 'bold 54px "JetBrains Mono", monospace'; ctx.fillText('08:30', 36, 74);
        ctx.fillStyle = '#8ea3c4'; ctx.font = '18px "IBM Plex Sans", sans-serif'; ctx.fillText('NEXT: PERIOD 1', 50, 108);
    });
    const ctrl = new THREE.Group();
    ctrl.position.set(1.35, -0.75, 0.2);
    ctrl.rotation.y = -0.4;
    ctrl.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.55, 0.16), steel));
    const disp = new THREE.Mesh(new THREE.PlaneGeometry(0.76, 0.38), new THREE.MeshBasicMaterial({ map: timerTex, toneMapped: false }));
    disp.position.z = 0.081;
    ctrl.add(disp);
    root.add(ctrl);

    // Sound rings
    const rings = [0, 1, 2].map(() => {
        const r = new THREE.Mesh(new THREE.TorusGeometry(0.9, 0.012, 8, 96), new THREE.MeshBasicMaterial({ color: SIGNAL, transparent: true, opacity: 0 }));
        r.position.y = 0.4;
        root.add(r);
        return r;
    });

    stage.update = (t) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        const swing = Math.sin(t * 8) * 0.42 * h * motion + Math.sin(t * 1.3) * 0.04 * motion;
        pivot.rotation.z = swing;
        clapperPivot.rotation.z = -Math.sin(t * 8 - 0.9) * 0.35 * h * motion;
        root.rotation.y = lerp(Math.sin(t * 0.5) * 0.35, stage.mouse.x * 0.4, h);
        metal.emissiveIntensity = 0.4 + h * 0.5;
        rings.forEach((r, i) => {
            const p = (t * 0.9 + i / 3) % 1;
            r.scale.setScalar(0.6 + p * 1.6);
            r.material.opacity = (1 - p) * 0.8 * h;
        });
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: Water Monitoring — tank fills, waves and live level label   */
/* ------------------------------------------------------------------ */
function initWater(canvas) {
    const card = canvas.closest('.product');
    const stage = createStage(canvas, { fov: 32, z: 7.6, hoverTarget: card, minAspect: 1.5 });
    const { scene, camera } = stage;
    camera.position.y = 1.2;
    camera.lookAt(0, 0, 0);
    addLights(scene);

    const root = new THREE.Group();
    root.position.y = -0.25;
    scene.add(root);
    const R = 0.75, TH = 1.8;

    // Glass tank
    const glass = new THREE.Mesh(
        new THREE.CylinderGeometry(R + 0.03, R + 0.03, TH, 64, 1, true),
        new THREE.MeshStandardMaterial({ color: '#9fc0ff', transparent: true, opacity: 0.12, metalness: 0.1, roughness: 0.05, side: THREE.DoubleSide, depthWrite: false })
    );
    root.add(glass);
    const edgeMat = new THREE.MeshBasicMaterial({ color: SIGNAL });
    [-TH / 2, TH / 2].forEach(y => {
        const e = new THREE.Mesh(new THREE.TorusGeometry(R + 0.03, 0.02, 8, 80), edgeMat);
        e.rotation.x = Math.PI / 2;
        e.position.y = y;
        root.add(e);
    });
    // level ticks
    for (let i = 1; i < 5; i++) {
        const tick = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.012, 0.012), new THREE.MeshBasicMaterial({ color: '#7f8892' }));
        tick.position.set(R + 0.1, -TH / 2 + (TH * i) / 5, 0);
        root.add(tick);
    }
    const base = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.12, R + 0.18, 0.14, 64), new THREE.MeshStandardMaterial({ color: '#1e2a44', metalness: 0.7, roughness: 0.4 }));
    base.position.y = -TH / 2 - 0.08;
    root.add(base);

    // Water column
    const waterMat = new THREE.MeshStandardMaterial({ color: '#1d8bff', emissive: '#0a3d8f', emissiveIntensity: 0.6, transparent: true, opacity: 0.78, roughness: 0.15, metalness: 0.1 });
    const colGeo = new THREE.CylinderGeometry(R - 0.01, R - 0.01, 1, 64);
    colGeo.translate(0, 0.5, 0);
    const column = new THREE.Mesh(colGeo, waterMat);
    column.position.y = -TH / 2;
    root.add(column);

    // Wavy surface
    const surfGeo = new THREE.RingGeometry(0, R - 0.01, 64, 10);
    surfGeo.rotateX(-Math.PI / 2);
    const surfBase = surfGeo.attributes.position.array.slice();
    const surface = new THREE.Mesh(surfGeo, new THREE.MeshStandardMaterial({ color: '#4fc3ff', emissive: '#1260c9', emissiveIntensity: 0.7, transparent: true, opacity: 0.9, side: THREE.DoubleSide, roughness: 0.1 }));
    root.add(surface);

    // Lid with ultrasonic sensor + blinking LED
    const lid = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.04, R + 0.04, 0.06, 64), new THREE.MeshStandardMaterial({ color: '#1e2a44', metalness: 0.7, roughness: 0.35 }));
    lid.position.y = TH / 2 + 0.03;
    root.add(lid);
    const sensor = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.16, 0.26), new THREE.MeshStandardMaterial({ color: '#0f766e', metalness: 0.4, roughness: 0.4 }));
    sensor.position.set(-0.2, TH / 2 + 0.14, 0);
    root.add(sensor);
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), new THREE.MeshBasicMaterial({ color: '#22c55e' }));
    led.position.set(-0.05, TH / 2 + 0.18, 0.14);
    root.add(led);
    // Sonar pulses from the sensor down to the water
    const pulses = [0, 1].map(() => {
        const m = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.008, 6, 40), new THREE.MeshBasicMaterial({ color: SIGNAL, transparent: true, opacity: 0 }));
        m.rotation.x = Math.PI / 2;
        m.position.x = -0.2;
        root.add(m);
        return m;
    });

    // Inlet pipe + droplets
    const pipeMat = new THREE.MeshStandardMaterial({ color: '#64748b', metalness: 0.8, roughness: 0.3 });
    const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.9, 16), pipeMat);
    pipe.rotation.z = Math.PI / 2;
    pipe.position.set(0.75, TH / 2 + 0.35, 0);
    root.add(pipe);
    const elbow = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.25, 16), pipeMat);
    elbow.position.set(0.32, TH / 2 + 0.24, 0);
    root.add(elbow);
    const drops = Array.from({ length: 10 }, (_, i) => {
        const d = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 10), new THREE.MeshBasicMaterial({ color: '#8fb6ff', transparent: true, opacity: 0 }));
        d.userData.phase = i / 10;
        d.position.x = 0.32;
        root.add(d);
        return d;
    });

    // Floating level read-out
    let shown = -1;
    const labelTex = canvasTexture(256, 112, () => {});
    const drawLabel = (pct) => {
        const ctx = labelTex.userData.ctx;
        ctx.clearRect(0, 0, 256, 112);
        roundRect(ctx, 4, 4, 248, 104, 18);
        ctx.fillStyle = 'rgba(15,27,51,0.94)'; ctx.fill();
        ctx.lineWidth = 3; ctx.strokeStyle = pct > 85 ? '#ff6b3d' : '#b6ff3b'; ctx.stroke();
        ctx.fillStyle = '#8ea3c4'; ctx.font = '18px "IBM Plex Sans", sans-serif'; ctx.fillText('TANK LEVEL', 24, 40);
        ctx.fillStyle = '#e6eefc'; ctx.font = 'bold 46px "Chakra Petch", sans-serif'; ctx.fillText(`${pct}%`, 24, 90);
        ctx.fillStyle = pct > 85 ? '#f59e0b' : '#22c55e'; ctx.beginPath(); ctx.arc(220, 70, 10, 0, Math.PI * 2); ctx.fill();
        labelTex.needsUpdate = true;
    };
    const label = new THREE.Sprite(new THREE.SpriteMaterial({ map: labelTex, transparent: true, toneMapped: false }));
    label.scale.set(1.15, 0.5, 1);
    label.position.set(-1.3, 0.6, 0.4);
    root.add(label);

    let level = 0.3;
    stage.update = (t, dt) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        const target = lerp(0.3 + Math.sin(t * 0.4) * 0.02, 0.88, ease(h));
        level = lerp(level, target, Math.min(dt * 2.5, 1));
        column.scale.y = level * TH;
        const surfY = -TH / 2 + level * TH;
        surface.position.y = surfY;

        const p = surfGeo.attributes.position;
        const amp = (0.015 + h * 0.035) * motion;
        for (let i = 0; i < p.count; i++) {
            const x = surfBase[i * 3], z = surfBase[i * 3 + 2];
            const r = Math.hypot(x - 0.32, z);
            p.setY(i, Math.sin(r * 14 - t * 6) * amp * Math.max(0, 1 - r * 0.6) + Math.sin(x * 4 + t * 2) * 0.01);
        }
        p.needsUpdate = true;
        surfGeo.computeVertexNormals();

        drops.forEach(d => {
            const ph = (t * 1.2 + d.userData.phase) % 1;
            const top = TH / 2 + 0.1;
            d.position.y = lerp(top, surfY, ph * ph);
            d.material.opacity = h * (ph < 0.95 ? 1 : 0);
        });
        pulses.forEach((m, i) => {
            const ph = (t * 0.8 + i * 0.5) % 1;
            m.position.y = lerp(TH / 2, surfY + 0.02, ph);
            m.scale.setScalar(1 + ph * 2);
            m.material.opacity = (1 - ph) * 0.7;
        });
        led.material.color.set(Math.sin(t * 6) > 0 ? '#22c55e' : '#064e3b');
        root.rotation.y = lerp(Math.sin(t * 0.4) * 0.3, stage.mouse.x * 0.4, h);
        label.position.y = surfY + 0.25;

        const pct = Math.round(level * 100);
        if (pct !== shown) { shown = pct; drawLabel(pct); }
    };
}

/* ------------------------------------------------------------------ */
/* Boot + shared render loop                                           */
/* ------------------------------------------------------------------ */
function boot() {
    try {
        initHero();
        document.querySelectorAll('canvas[data-scene]').forEach(c => {
            const s = c.dataset.scene;
            if (s === 'sello') initPhone(c, { lite: false });
            else if (s === 'selloLite') initPhone(c, { lite: true });
            else if (s === 'bell') initBell(c);
            else if (s === 'water') initWater(c);
        });
    } catch (err) {
        console.warn('3D scenes unavailable:', err);
        return;
    }

    const clock = new THREE.Clock();
    const loop = () => {
        const dt = Math.min(clock.getDelta(), 0.1);
        const t = clock.elapsedTime;
        for (const s of stages) {
            if (!s.visible || !s.update) continue;
            s.h = lerp(s.h, s.hover ? 1 : 0, Math.min(dt * 4, 1));
            s.update(t, dt);
            s.renderer.render(s.scene, s.camera);
        }
        requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
}

// Wait for fonts so canvas textures use Orbitron / Inter
(document.fonts?.ready ?? Promise.resolve()).then(boot);
