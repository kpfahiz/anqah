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
    shapeFromImage(new URL('./images/logo-mark.png', import.meta.url).href).then(p => { if (p) shapes[0].pos = p; });

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
/* PRODUCT: SELLO Lite — phone running the real app; more screens fly   */
/* out on hover                                                         */
/* ------------------------------------------------------------------ */
const LITE_SCREENS = {
    main: 'images/products/sello-lite/sello-lite-sell.webp',
    left: 'images/products/sello-lite/sello-lite-report.webp',
    right: 'images/products/sello-lite/sello-lite-portions.webp',
};

// A phone body with a screenshot on its screen; screenshots are 738x1600 (20:9)
// `texture` (optional) shows a live CanvasTexture instead of loading `url`
function makePhone(url, { W = 1.02, H = 2.1, body = '#15181d', texture = null } = {}) {
    const group = new THREE.Group();
    const geo = new THREE.ExtrudeGeometry(roundedRectShape(W, H, 0.14), {
        depth: 0.08, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 4, curveSegments: 16,
    });
    geo.center();
    const bodyMat = new THREE.MeshStandardMaterial({ color: body, metalness: 0.75, roughness: 0.3, transparent: true });
    group.add(new THREE.Mesh(geo, bodyMat));
    const sw = W - 0.1, sh = H - 0.1;
    const screenGeo = new THREE.ShapeGeometry(roundedRectShape(sw, sh, 0.1));
    const uv = screenGeo.attributes.uv, pos = screenGeo.attributes.position;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / sw + 0.5, pos.getY(i) / sh + 0.5);
    const screenMat = new THREE.MeshBasicMaterial({ color: '#0d1013', toneMapped: false, transparent: true });
    const screen = new THREE.Mesh(screenGeo, screenMat);
    screen.position.z = 0.072;
    group.add(screen);
    const apply = tex => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = 8;
        screenMat.map = tex;
        screenMat.color.set('#ffffff');
        screenMat.needsUpdate = true;
    };
    if (texture) apply(texture);
    else new THREE.TextureLoader().load(new URL(`./${url}`, import.meta.url).href, apply);
    group.userData.materials = [bodyMat, screenMat];
    return group;
}

function initLitePhone(canvas) {
    const card = canvas.closest('.product, .pd-stage') || canvas;
    const stage = createStage(canvas, { fov: 32, z: 5.8, hoverTarget: card, minAspect: 1.2 });
    const { scene } = stage;
    addLights(scene);

    const root = new THREE.Group();
    scene.add(root);
    const phone = makePhone(LITE_SCREENS.main);
    root.add(phone);

    // Secondary phones (real Reports and portion-picker screens) that fly out on hover
    const extras = [
        { url: LITE_SCREENS.left, to: [-1.35, -0.05, -0.55], rot: 0.45, delay: 0 },
        { url: LITE_SCREENS.right, to: [1.35, -0.05, -0.55], rot: -0.45, delay: 0.12 },
    ].map(d => {
        const p = makePhone(d.url);
        p.userData = { ...p.userData, ...d };
        p.userData.materials.forEach(m => { m.opacity = 0; });
        root.add(p);
        return p;
    });

    stage.update = (t) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        root.position.y = Math.sin(t * 1.4) * 0.05 * motion;
        phone.rotation.y = lerp(Math.sin(t * 0.6) * 0.45 * motion, stage.mouse.x * 0.3, h);
        phone.rotation.x = lerp(0.06, -stage.mouse.y * 0.15, h);
        phone.rotation.z = lerp(0.1, 0, h);
        extras.forEach(p => {
            const k = ease(clamp01((h - p.userData.delay) / (1 - p.userData.delay)));
            const [x, y, z] = p.userData.to;
            p.position.set(lerp(0, x, k), lerp(0, y, k) + Math.sin(t * 1.8 + x) * 0.03 * k, lerp(-0.2, z, k));
            p.rotation.y = lerp(0, p.userData.rot, k);
            p.scale.setScalar(lerp(0.6, 0.86, k));
            p.visible = k > 0.01;
            p.userData.materials.forEach(m => { m.opacity = k; });
        });
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: SELLO — countertop POS terminal with the real SELLO screen  */
/* ------------------------------------------------------------------ */
function initTerminal(canvas) {
    const card = canvas.closest('.product, .pd-stage') || canvas;
    const stage = createStage(canvas, { fov: 30, z: 8.2, hoverTarget: card, minAspect: 1.1 });
    const { scene, camera } = stage;
    camera.position.y = 1.4;
    camera.lookAt(0, -0.15, 0);
    addLights(scene);

    const dark = new THREE.MeshStandardMaterial({ color: '#1a1d22', metalness: 0.6, roughness: 0.38 });
    const darker = new THREE.MeshStandardMaterial({ color: '#0f1114', metalness: 0.5, roughness: 0.45 });
    const steel = new THREE.MeshStandardMaterial({ color: '#8a929c', metalness: 0.9, roughness: 0.28 });
    const rounded = (w, h, r, depth) => {
        const g = new THREE.ExtrudeGeometry(roundedRectShape(w, h, r), { depth, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 3, curveSegments: 10 });
        g.center();
        return g;
    };

    const root = new THREE.Group();
    root.position.y = -0.2;
    scene.add(root);

    // Cash-drawer cabinet the terminal stands on
    const cabinet = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.42, 1.7), dark);
    cabinet.position.set(0, -0.95, 0);
    root.add(cabinet);
    const drawer = new THREE.Group();
    root.add(drawer);
    const front = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.32, 0.06), darker);
    front.position.set(0, -0.97, 0.86);
    drawer.add(front);
    const keyhole = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.02, 16), steel);
    keyhole.rotation.x = Math.PI / 2;
    keyhole.position.set(0, -0.97, 0.9);
    drawer.add(keyhole);
    // Tray with AED notes and coins (revealed as the drawer opens)
    const tray = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.05, 1.0), new THREE.MeshStandardMaterial({ color: '#2a2f36', roughness: 0.7 }));
    tray.position.set(0, -0.86, 0.34);
    drawer.add(tray);
    ['#7a5a3a', '#3f7a52', '#6b4f8f', '#2f6f8f'].forEach((c, i) => {
        const note = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.04, 0.62), new THREE.MeshStandardMaterial({ color: c, roughness: 0.8 }));
        note.position.set(-0.9 + i * 0.5, -0.82, 0.24);
        drawer.add(note);
    });
    for (let i = 0; i < 5; i++) {
        const coin = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.03, 20), new THREE.MeshStandardMaterial({ color: '#c9a646', metalness: 0.9, roughness: 0.3 }));
        coin.position.set(-0.95 + i * 0.47, -0.82, 0.68);
        drawer.add(coin);
    }

    // Stand
    const neck = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.95, 0.2), steel);
    neck.position.set(0, -0.32, -0.38);
    neck.rotation.x = -0.18;
    root.add(neck);
    const foot = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.06, 0.55), steel);
    foot.position.set(0, -0.72, -0.4);
    root.add(foot);

    // Touchscreen (16:9) showing the real SELLO point-of-sale screen
    const head = new THREE.Group();
    head.position.set(0, 0.42, -0.25);
    root.add(head);
    const SW = 2.56, SH = 1.44;
    const housing = new THREE.Mesh(rounded(SW + 0.18, SH + 0.2, 0.08, 0.1), dark);
    head.add(housing);
    const screenMat = new THREE.MeshBasicMaterial({ color: '#0b1220', toneMapped: false });
    const screen = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), screenMat);
    screen.position.set(0, 0.02, 0.082);
    head.add(screen);
    new THREE.TextureLoader().load(new URL('./images/products/sello/sello-pos.webp', import.meta.url).href, tex => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = 8;
        screenMat.map = tex;
        screenMat.color.set('#ffffff');
        screenMat.needsUpdate = true;
    });
    // glass sheen
    const sheen = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshBasicMaterial({
        map: canvasTexture(256, 144, (ctx, w, h) => {
            const g = ctx.createLinearGradient(0, 0, w, h);
            g.addColorStop(0, 'rgba(255,255,255,0.18)'); g.addColorStop(0.35, 'rgba(255,255,255,0.03)'); g.addColorStop(0.5, 'rgba(255,255,255,0)');
            ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
        }), transparent: true, depthWrite: false,
    }));
    sheen.position.set(0, 0.02, 0.085);
    head.add(sheen);
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.018, 10, 10), new THREE.MeshBasicMaterial({ color: '#b6ff3b' }));
    led.position.set(SW / 2 - 0.05, -SH / 2 - 0.05, 0.082);
    head.add(led);

    // Receipt printer (right) with a receipt that prints on hover
    const printer = new THREE.Group();
    printer.position.set(1.28, -0.5, 0.35);
    root.add(printer);
    const pBody = new THREE.Mesh(rounded(0.62, 0.5, 0.1, 0.62), new THREE.MeshStandardMaterial({ color: '#e7eaee', metalness: 0.2, roughness: 0.45 }));
    printer.add(pBody);
    const slot = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.02, 0.05), darker);
    slot.position.set(0, 0.26, -0.05);
    printer.add(slot);
    const receiptTex = canvasTexture(160, 320, (ctx, w, h) => {
        ctx.fillStyle = '#fbfbf8'; ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = '#111827'; ctx.font = 'bold 15px monospace'; ctx.fillText('SELLO POS', 36, 26);
        ctx.font = '11px monospace';
        ['2x Spanish Latte  39.90', '1x Manakeesh     10.50', '1x Kunafa        23.10', '1x Orange Juice  14.70', '1x Croissant      9.45', '----------------------', 'VAT 5%            4.65', 'TOTAL AED        97.65']
            .forEach((l, i) => ctx.fillText(l, 8, 56 + i * 20));
        for (let x = 12; x < w - 12; x += 3) { ctx.fillRect(x, 230, Math.random() > 0.5 ? 2 : 1, 34); }
    });
    receiptTex.wrapT = THREE.ClampToEdgeWrapping;
    const receipt = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.8), new THREE.MeshBasicMaterial({ map: receiptTex, side: THREE.DoubleSide }));
    receipt.geometry.translate(0, 0.4, 0); // grow upwards from the slot
    receipt.position.set(0, 0.26, -0.05);
    receipt.rotation.x = -0.12;
    printer.add(receipt);

    // Card machine (left) that lights up "TAP TO PAY"
    const cardM = new THREE.Group();
    cardM.position.set(-1.3, -0.62, 0.45);
    cardM.rotation.set(-0.5, 0.35, 0);
    root.add(cardM);
    cardM.add(new THREE.Mesh(rounded(0.34, 0.6, 0.06, 0.08), darker));
    const tapTex = canvasTexture(128, 96, (ctx, w, h) => {
        ctx.fillStyle = '#0b1220'; ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = '#b6ff3b'; ctx.font = 'bold 13px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('TAP TO PAY', w / 2, 36);
        ctx.fillStyle = '#e9edf0'; ctx.font = 'bold 18px sans-serif'; ctx.fillText('AED 97.65', w / 2, 66);
    });
    const tapMat = new THREE.MeshBasicMaterial({ map: tapTex, transparent: true, opacity: 0.35, toneMapped: false });
    const tap = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.2), tapMat);
    tap.position.set(0, 0.14, 0.062);
    cardM.add(tap);
    const keyMat = ['#3a414b', '#3a414b', '#3a414b', '#ef4444', '#f59e0b', '#22c55e'];
    keyMat.forEach((c, i) => {
        const k = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.04, 0.02), new THREE.MeshStandardMaterial({ color: c }));
        k.position.set(-0.09 + (i % 3) * 0.09, -0.08 - Math.floor(i / 3) * 0.08, 0.06);
        cardM.add(k);
    });

    stage.update = (t) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        root.rotation.y = lerp(Math.sin(t * 0.45) * 0.32 * motion, stage.mouse.x * 0.35, h);
        root.position.y = -0.2 + Math.sin(t * 1.2) * 0.03 * motion;
        head.rotation.x = lerp(-0.2, -0.08 - stage.mouse.y * 0.08, h);
        drawer.position.z = ease(h) * 0.75;
        const print = ease(clamp01(h * 1.3 - 0.15));
        receipt.scale.y = Math.max(0.02, print);
        receiptTex.repeat.y = Math.max(0.02, print);
        receiptTex.offset.y = 1 - Math.max(0.02, print);
        tapMat.opacity = 0.35 + h * 0.65 * (0.75 + 0.25 * Math.sin(t * 6));
        led.material.color.set(Math.sin(t * 3) > 0 ? '#b6ff3b' : '#4a6a1a');
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: Automatic Bell — wall control panel + phone running the    */
/* real School Bell app; hovering rings the bell from the phone         */
/* ------------------------------------------------------------------ */
function brushedTexture(tint = 200) {
    return canvasTexture(512, 512, (ctx, w, h) => {
        ctx.fillStyle = `rgb(${tint},${tint + 2},${tint + 5})`;
        ctx.fillRect(0, 0, w, h);
        for (let y = 0; y < h; y++) {
            const v = tint + (Math.random() - 0.5) * 34;
            ctx.fillStyle = `rgba(${v},${v + 2},${v + 5},0.55)`;
            ctx.fillRect(0, y, w, 1);
        }
    });
}

function initBell(canvas) {
    const card = canvas.closest('.product, .pd-stage') || canvas;
    const stage = createStage(canvas, { fov: 30, z: 7.4, hoverTarget: card, minAspect: 1.3 });
    const { scene, camera } = stage;
    camera.position.x = 1.1;
    camera.lookAt(0, 0, 0);
    scene.add(new THREE.HemisphereLight('#f4f1ea', '#3a3530', 1.2));
    const key = new THREE.DirectionalLight('#fff4e0', 2.4);
    key.position.set(-3, 3, 5);
    scene.add(key);
    const fill = new THREE.PointLight('#bfe0ff', 6, 10);
    fill.position.set(3, -1, 3);
    scene.add(fill);

    const root = new THREE.Group();
    scene.add(root);

    // Plaster wall, lit from the upper left
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(14, 9), new THREE.MeshStandardMaterial({
        roughness: 0.95,
        map: canvasTexture(512, 512, (ctx, w, h) => {
            const g = ctx.createRadialGradient(w * 0.35, h * 0.3, 20, w * 0.5, h * 0.5, w * 0.75);
            g.addColorStop(0, '#d8d4cc');
            g.addColorStop(1, '#8f8b84');
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, w, h);
            for (let i = 0; i < 9000; i++) {
                ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.03)';
                ctx.fillRect(Math.random() * w, Math.random() * h, 2, 2);
            }
        }),
    }));
    wall.position.z = -0.12;
    root.add(wall);

    // --- Control panel (brushed steel) ---
    const panel = new THREE.Group();
    panel.position.set(0.85, -0.05, 0);
    root.add(panel);
    const steelTex = brushedTexture(190);
    const steel = new THREE.MeshStandardMaterial({ color: '#d7dbe0', map: steelTex, metalness: 0.85, roughness: 0.32 });
    const plateGeo = new THREE.ExtrudeGeometry(roundedRectShape(1.7, 1.9, 0.14), {
        depth: 0.08, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 4, curveSegments: 12,
    });
    plateGeo.center();
    const plate = new THREE.Mesh(plateGeo, steel);
    plate.position.z = -0.02;
    panel.add(plate);
    const faceTex = canvasTexture(512, 576, (ctx, w) => {
        ctx.drawImage(steelTex.image, 0, 0, w, 576);
        ctx.fillStyle = 'rgba(30,34,40,0.85)';
        ctx.textAlign = 'center';
        ctx.font = '600 40px "Chakra Petch", sans-serif';
        ctx.fillText('SMART BELL SYSTEM', w / 2, 70);
        ctx.font = '500 26px "IBM Plex Sans", sans-serif';
        ctx.fillText('SCHEDULED CONTROL', w / 2, 108);
        ctx.font = '600 32px "Chakra Petch", sans-serif';
        ctx.fillText('ACTIVATE BELL', w / 2, 470);
        ctx.font = '500 21px "IBM Plex Sans", sans-serif';
        ctx.fillText('PRESS TO TRIGGER SCHEDULED BELL', w / 2, 508);
    });
    const face = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.69), new THREE.MeshStandardMaterial({ map: faceTex, metalness: 0.7, roughness: 0.4 }));
    face.position.z = 0.062;
    panel.add(face);

    // Status display
    const lcdTex = canvasTexture(256, 64, () => {});
    const drawLcd = (txt, col) => {
        const ctx = lcdTex.userData.ctx;
        ctx.fillStyle = '#081210';
        ctx.fillRect(0, 0, 256, 64);
        ctx.fillStyle = col;
        ctx.font = 'bold 26px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(txt, 128, 42);
        lcdTex.needsUpdate = true;
    };
    drawLcd('08:30  P1', '#3de0b0');
    const lcd = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.155), new THREE.MeshBasicMaterial({ map: lcdTex, toneMapped: false }));
    lcd.position.set(0, -0.77, 0.066);
    panel.add(lcd);

    // Bell button inside an LED ring
    const ringMat = new THREE.MeshBasicMaterial({ color: '#3de0b0', transparent: true, opacity: 0.35, toneMapped: false });
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.36, 0.035, 16, 64), ringMat);
    ring.position.z = 0.075;
    panel.add(ring);
    const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.42, 0.06, 64), steel);
    bezel.rotation.x = Math.PI / 2;
    bezel.position.z = 0.07;
    panel.add(bezel);
    const button = new THREE.Group();
    button.position.z = 0.12;
    panel.add(button);
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.31, 0.1, 64),
        new THREE.MeshStandardMaterial({ color: '#e3e6ea', map: brushedTexture(210), metalness: 0.9, roughness: 0.25 }));
    cap.rotation.x = Math.PI / 2;
    button.add(cap);
    const iconTex = canvasTexture(128, 128, (ctx) => {
        ctx.strokeStyle = 'rgba(40,46,54,0.9)';
        ctx.lineWidth = 6;
        ctx.lineJoin = 'round';
        ctx.beginPath();
        ctx.moveTo(40, 88); ctx.lineTo(44, 54);
        ctx.quadraticCurveTo(48, 30, 64, 30); ctx.quadraticCurveTo(80, 30, 84, 54);
        ctx.lineTo(88, 88); ctx.closePath(); ctx.stroke();
        ctx.beginPath(); ctx.arc(64, 96, 7, 0, Math.PI); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(64, 22); ctx.lineTo(64, 30); ctx.stroke();
    });
    const icon = new THREE.Mesh(new THREE.CircleGeometry(0.22, 48), new THREE.MeshBasicMaterial({ map: iconTex, transparent: true }));
    icon.position.z = 0.052;
    button.add(icon);
    const glow = new THREE.PointLight('#3de0b0', 0, 2.2);
    glow.position.set(0, 0, 0.4);
    panel.add(glow);

    // WiFi arcs above the panel
    const arcs = [0.18, 0.3, 0.42].map((r, i) => {
        const m = new THREE.Mesh(new THREE.TorusGeometry(r, 0.022, 8, 40, Math.PI / 2),
            new THREE.MeshBasicMaterial({ color: '#f2e6c9', transparent: true, opacity: 0.5, toneMapped: false }));
        m.rotation.z = Math.PI / 4;
        m.position.set(0, 1.12, 0.05);
        m.userData.i = i;
        panel.add(m);
        return m;
    });
    const dot = new THREE.Mesh(new THREE.CircleGeometry(0.045, 20), new THREE.MeshBasicMaterial({ color: '#f2e6c9', toneMapped: false }));
    dot.position.set(0, 1.12, 0.05);
    panel.add(dot);

    // --- Phone running the real School Bell app (left) ---
    const phone = makePhone('images/products/automatic-bell/bell-app-home.webp', { W: 1.12, H: 2.1, body: '#1b1e23' });
    phone.position.set(-1.4, -0.05, 0.6);
    phone.rotation.set(0.04, 0.38, 0.06);
    phone.scale.setScalar(1.18);
    root.add(phone);
    const phoneScreen = phone.userData.materials[1];
    const appTex = {};
    const loader = new THREE.TextureLoader();
    [['home', 'bell-app-home'], ['ringing', 'bell-app-ringing']].forEach(([k, f]) => {
        loader.load(new URL(`./images/products/automatic-bell/${f}.webp`, import.meta.url).href, tex => {
            tex.colorSpace = THREE.SRGBColorSpace;
            tex.anisotropy = 8;
            appTex[k] = tex;
        });
    });

    // WiFi link: dots that stream from the phone to the panel when ringing
    const link = new THREE.QuadraticBezierCurve3(
        new THREE.Vector3(-0.85, 0.75, 0.6), new THREE.Vector3(-0.2, 1.55, 0.45), new THREE.Vector3(0.45, 0.85, 0.12));
    const dots = Array.from({ length: 9 }, (_, i) => {
        const m = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 12), new THREE.MeshBasicMaterial({ color: '#3de0b0', transparent: true, opacity: 0.4, toneMapped: false }));
        m.userData.p = i / 9;
        m.position.copy(link.getPoint(m.userData.p));
        root.add(m);
        return m;
    });

    // Rings pulsing out from the panel while the bell rings
    const waves = [0, 1, 2].map(() => {
        const m = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.01, 8, 96),
            new THREE.MeshBasicMaterial({ color: '#3de0b0', transparent: true, opacity: 0, toneMapped: false }));
        m.position.set(0.85, -0.05, 0.14);
        root.add(m);
        return m;
    });

    let ringing = false;
    stage.update = (t) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        root.rotation.y = lerp(-0.18 + Math.sin(t * 0.4) * 0.08 * motion, -0.1 + stage.mouse.x * 0.2, h);
        root.rotation.x = lerp(Math.sin(t * 0.3) * 0.03 * motion, -stage.mouse.y * 0.08, h);
        button.position.z = lerp(0.12, 0.085, ease(h));
        const pulse = 0.75 + 0.25 * Math.sin(t * 8);
        ringMat.opacity = 0.35 + h * 0.65 * pulse;
        glow.intensity = h * 3.5 * pulse;
        phone.position.y = 0.05 + Math.sin(t * 1.3) * 0.04 * motion;
        phone.rotation.y = lerp(0.38, 0.22, h);
        waves.forEach((w, i) => {
            const ph = (t * 0.9 + i / 3) % 1;
            w.scale.setScalar(1 + ph * 1.6);
            w.material.opacity = (1 - ph) * 0.6 * h;
        });
        dots.forEach(d => {
            const p = (d.userData.p + t * 0.35 * (0.3 + h)) % 1;
            d.position.copy(link.getPoint(p));
            d.material.opacity = (0.25 + 0.75 * h) * Math.sin(p * Math.PI);
        });
        arcs.forEach(a => {
            const ph = (t * 1.5 - a.userData.i * 0.25) % 1;
            a.material.opacity = 0.35 + h * 0.6 * Math.max(0, Math.sin(ph * Math.PI));
        });
        const now = h > 0.5;
        if (now !== ringing && appTex.home && appTex.ringing) {
            phoneScreen.map = now ? appTex.ringing : appTex.home;
            phoneScreen.needsUpdate = true;
        }
        if (now !== ringing) {
            ringing = now;
            drawLcd(now ? 'RINGING...' : '08:30  P1', now ? '#b6ff3b' : '#3de0b0');
        }
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: Water Monitoring — the tank fills and drains, the phone app */
/* mirrors the level live, and Telegram alerts fire below 15% (empty)   */
/* and above 95% (overflow)                                             */
/* ------------------------------------------------------------------ */
const WATER_LOW = 15, WATER_HIGH = 95;

function waterStatus(pct) {
    if (pct < WATER_LOW) return { text: 'LOW — REFILL NEEDED', col: '#ef4444' };
    if (pct > WATER_HIGH) return { text: 'FULL — OVERFLOW RISK', col: '#f59e0b' };
    return { text: 'NORMAL', col: '#22c55e' };
}

// Phone app screen: live tank level, status, pump state and Telegram alerts
function drawWaterApp(ctx, w, h, pct, rising) {
    const st = waterStatus(pct);
    ctx.fillStyle = '#0d141b';
    ctx.fillRect(0, 0, w, h);
    // status bar + header
    ctx.fillStyle = '#9aa7b4';
    ctx.font = '600 15px "IBM Plex Sans", sans-serif';
    ctx.fillText('10:42', 22, 30);
    ctx.textAlign = 'right';
    ctx.fillText('5G  ▮▮▮  82%', w - 20, 30);
    ctx.textAlign = 'left';
    ctx.fillStyle = '#e8eef4';
    ctx.font = 'bold 24px "Chakra Petch", sans-serif';
    ctx.fillText('Water Monitor', 22, 78);
    ctx.fillStyle = '#22c55e';
    ctx.beginPath(); ctx.arc(w - 72, 70, 6, 0, Math.PI * 2); ctx.fill();
    ctx.font = 'bold 14px "JetBrains Mono", monospace';
    ctx.fillText('LIVE', w - 60, 75);
    ctx.fillStyle = '#7d8a97';
    ctx.font = '14px "IBM Plex Sans", sans-serif';
    ctx.fillText('Overhead tank · Villa 12', 22, 102);

    // tank card
    roundRect(ctx, 16, 122, w - 32, 300, 18);
    ctx.fillStyle = '#16212b'; ctx.fill();
    const tx = 40, ty = 150, tw = 104, th = 246;
    roundRect(ctx, tx, ty, tw, th, 14);
    ctx.lineWidth = 3; ctx.strokeStyle = '#3b4b5b'; ctx.stroke();
    ctx.save();
    roundRect(ctx, tx + 4, ty + 4, tw - 8, th - 8, 10); ctx.clip();
    const fillH = (th - 8) * pct / 100, top = ty + th - 4 - fillH;
    const g = ctx.createLinearGradient(0, top, 0, ty + th);
    g.addColorStop(0, '#4fc3ff'); g.addColorStop(1, '#1d6fe0');
    ctx.fillStyle = g;
    ctx.fillRect(tx, top, tw, fillH + 4);
    ctx.restore();
    // threshold marks
    [[WATER_HIGH, '#f59e0b'], [WATER_LOW, '#ef4444']].forEach(([v, c]) => {
        const y = ty + th - 4 - (th - 8) * v / 100;
        ctx.strokeStyle = c; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
        ctx.beginPath(); ctx.moveTo(tx - 6, y); ctx.lineTo(tx + tw + 6, y); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = c; ctx.font = 'bold 12px "JetBrains Mono", monospace';
        ctx.fillText(`${v}%`, tx + tw + 10, y + 4);
    });
    ctx.fillStyle = '#e8eef4';
    ctx.font = 'bold 54px "Chakra Petch", sans-serif';
    ctx.fillText(`${pct}%`, 172, 230);
    ctx.fillStyle = '#7d8a97';
    ctx.font = '14px "IBM Plex Sans", sans-serif';
    ctx.fillText('Water level', 174, 254);
    ctx.fillStyle = rising ? '#4fc3ff' : '#9aa7b4';
    ctx.font = 'bold 15px "IBM Plex Sans", sans-serif';
    ctx.fillText(rising ? '▲ Filling' : '▼ In use', 174, 290);
    ctx.fillStyle = '#7d8a97';
    ctx.font = '14px "IBM Plex Sans", sans-serif';
    ctx.fillText('Updated just now', 174, 318);

    // status pill
    roundRect(ctx, 16, 440, w - 32, 54, 14);
    ctx.fillStyle = st.col + '26'; ctx.fill();
    ctx.lineWidth = 2; ctx.strokeStyle = st.col; ctx.stroke();
    ctx.fillStyle = st.col;
    ctx.font = 'bold 17px "Chakra Petch", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(st.text, w / 2, 474);
    ctx.textAlign = 'left';

    // alert rules
    roundRect(ctx, 16, 512, w - 32, 112, 14);
    ctx.fillStyle = '#16212b'; ctx.fill();
    ctx.fillStyle = '#e8eef4';
    ctx.font = 'bold 15px "IBM Plex Sans", sans-serif';
    ctx.fillText('Telegram alerts', 32, 542);
    ctx.font = '14px "IBM Plex Sans", sans-serif';
    ctx.fillStyle = '#ef8a8a';
    ctx.fillText(`● Below ${WATER_LOW}% → Tank empty`, 32, 572);
    ctx.fillStyle = '#f5c26b';
    ctx.fillText(`● Above ${WATER_HIGH}% → Overflow`, 32, 600);
}

// Telegram-style notification card
function drawTelegram(ctx, w, h, kind, pct) {
    ctx.clearRect(0, 0, w, h);
    roundRect(ctx, 4, 4, w - 8, h - 8, 22);
    ctx.fillStyle = 'rgba(250,251,252,0.97)'; ctx.fill();
    // paper-plane avatar
    ctx.fillStyle = '#2aabee';
    ctx.beginPath(); ctx.arc(62, h / 2, 36, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(42, h / 2 - 2); ctx.lineTo(82, h / 2 - 18); ctx.lineTo(74, h / 2 + 20); ctx.lineTo(62, h / 2 + 6);
    ctx.lineTo(56, h / 2 + 16); ctx.lineTo(56, h / 2 + 3); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#111827';
    ctx.font = 'bold 22px "IBM Plex Sans", sans-serif';
    ctx.fillText('Telegram · Tank Alert Bot', 116, 46);
    ctx.fillStyle = '#6b7280';
    ctx.font = '17px "IBM Plex Sans", sans-serif';
    ctx.textAlign = 'right'; ctx.fillText('now', w - 24, 46); ctx.textAlign = 'left';
    ctx.fillStyle = kind === 'empty' ? '#b91c1c' : '#b45309';
    ctx.font = 'bold 21px "IBM Plex Sans", sans-serif';
    ctx.fillText(kind === 'empty' ? `⚠ Tank empty — level ${pct}%` : `⚠ Overflow alert — level ${pct}%`, 116, 84);
    ctx.fillStyle = '#374151';
    ctx.font = '17px "IBM Plex Sans", sans-serif';
    ctx.fillText(kind === 'empty' ? 'Please refill the tank / start the pump.' : 'Tank almost full — stop the pump.', 116, 114);
}

function initWater(canvas) {
    const card = canvas.closest('.product, .pd-stage') || canvas;
    const stage = createStage(canvas, { fov: 32, z: 8.2, hoverTarget: card, minAspect: 1.05 });
    const { scene, camera } = stage;
    camera.position.y = 1.0;
    camera.lookAt(0, 0.1, 0);
    addLights(scene);

    const world = new THREE.Group();
    world.position.x = -0.12;
    scene.add(world);
    const root = new THREE.Group();     // the tank
    root.position.set(-0.85, -0.25, 0);
    world.add(root);
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
    // threshold rings on the glass: 95% (overflow) and 15% (empty)
    [[WATER_HIGH, '#f59e0b'], [WATER_LOW, '#ef4444']].forEach(([v, c]) => {
        const m = new THREE.Mesh(new THREE.TorusGeometry(R + 0.035, 0.008, 6, 80), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.7 }));
        m.rotation.x = Math.PI / 2;
        m.position.y = -TH / 2 + TH * v / 100;
        root.add(m);
    });
    const base = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.12, R + 0.18, 0.14, 64), new THREE.MeshStandardMaterial({ color: '#1e2a44', metalness: 0.7, roughness: 0.4 }));
    base.position.y = -TH / 2 - 0.08;
    root.add(base);

    // Water column + wavy surface
    const waterMat = new THREE.MeshStandardMaterial({ color: '#1d8bff', emissive: '#0a3d8f', emissiveIntensity: 0.6, transparent: true, opacity: 0.78, roughness: 0.15, metalness: 0.1 });
    const colGeo = new THREE.CylinderGeometry(R - 0.01, R - 0.01, 1, 64);
    colGeo.translate(0, 0.5, 0);
    const column = new THREE.Mesh(colGeo, waterMat);
    column.position.y = -TH / 2;
    root.add(column);
    const surfGeo = new THREE.RingGeometry(0, R - 0.01, 64, 10);
    surfGeo.rotateX(-Math.PI / 2);
    const surfBase = surfGeo.attributes.position.array.slice();
    const surface = new THREE.Mesh(surfGeo, new THREE.MeshStandardMaterial({ color: '#4fc3ff', emissive: '#1260c9', emissiveIntensity: 0.7, transparent: true, opacity: 0.9, side: THREE.DoubleSide, roughness: 0.1 }));
    root.add(surface);

    // Lid with ultrasonic sensor, LED and sonar pulses
    const lid = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.04, R + 0.04, 0.06, 64), new THREE.MeshStandardMaterial({ color: '#1e2a44', metalness: 0.7, roughness: 0.35 }));
    lid.position.y = TH / 2 + 0.03;
    root.add(lid);
    const sensor = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.16, 0.26), new THREE.MeshStandardMaterial({ color: '#0f766e', metalness: 0.4, roughness: 0.4 }));
    sensor.position.set(-0.2, TH / 2 + 0.14, 0);
    root.add(sensor);
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), new THREE.MeshBasicMaterial({ color: '#22c55e' }));
    led.position.set(-0.05, TH / 2 + 0.18, 0.14);
    root.add(led);
    const pulses = [0, 1].map(() => {
        const m = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.008, 6, 40), new THREE.MeshBasicMaterial({ color: SIGNAL, transparent: true, opacity: 0 }));
        m.rotation.x = Math.PI / 2;
        m.position.x = -0.2;
        root.add(m);
        return m;
    });

    // Inlet pipe + droplets (only while filling)
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

    // Phone app mirroring the level live
    const appTex = canvasTexture(300, 640, () => {});
    const phone = makePhone(null, { W: 1.02, H: 2.1, body: '#1b1e23', texture: appTex });
    phone.position.set(1.45, 0.0, 0.3);
    phone.rotation.set(0.02, -0.32, 0.03);
    world.add(phone);
    // Wireless link: dots from the tank sensor to the phone
    const link = new THREE.QuadraticBezierCurve3(
        new THREE.Vector3(-0.85, 0.85, 0), new THREE.Vector3(0.3, 1.6, 0.2), new THREE.Vector3(1.2, 0.95, 0.35));
    const dots = Array.from({ length: 8 }, (_, i) => {
        const m = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 10), new THREE.MeshBasicMaterial({ color: '#4fc3ff', transparent: true, opacity: 0.5, toneMapped: false }));
        m.userData.p = i / 8;
        world.add(m);
        return m;
    });

    // Telegram notification that drops in when a threshold is crossed
    const tgTex = canvasTexture(560, 150, () => {});
    const tgMat = new THREE.MeshBasicMaterial({ map: tgTex, transparent: true, opacity: 0, toneMapped: false, depthTest: false });
    const tg = new THREE.Mesh(new THREE.PlaneGeometry(2.1, 0.56), tgMat);
    tg.renderOrder = 10;
    tg.position.set(0.45, 1.55, 0.8);
    world.add(tg);
    let alertUntil = -1, alertKind = null;

    let phase = -Math.PI / 2 + 0.6, level = 0.3, prevLevel = 0.3, shown = -1, shownRising = null, zone = 'normal';
    stage.update = (t, dt) => {
        const h = stage.h;
        const motion = reducedMotion ? 0.2 : 1;
        // level keeps cycling between ~3% and ~98%; hovering speeds it up
        phase += dt * (0.32 + h * 0.5) * (reducedMotion ? 0.4 : 1);
        prevLevel = level;
        level = 0.505 + 0.475 * Math.sin(phase);
        const rising = level >= prevLevel;
        column.scale.y = Math.max(0.001, level * TH);
        const surfY = -TH / 2 + level * TH;
        surface.position.y = surfY;

        const p = surfGeo.attributes.position;
        const amp = (rising ? 0.035 : 0.015) * motion;
        for (let i = 0; i < p.count; i++) {
            const x = surfBase[i * 3], z = surfBase[i * 3 + 2];
            const r = Math.hypot(x - 0.32, z);
            p.setY(i, Math.sin(r * 14 - t * 6) * amp * Math.max(0, 1 - r * 0.6) + Math.sin(x * 4 + t * 2) * 0.01);
        }
        p.needsUpdate = true;
        surfGeo.computeVertexNormals();

        drops.forEach(d => {
            const ph = (t * 1.2 + d.userData.phase) % 1;
            d.position.y = lerp(TH / 2 + 0.1, surfY, ph * ph);
            d.material.opacity = rising ? (ph < 0.95 ? 1 : 0) : 0;
        });
        pulses.forEach((m, i) => {
            const ph = (t * 0.8 + i * 0.5) % 1;
            m.position.y = lerp(TH / 2, surfY + 0.02, ph);
            m.scale.setScalar(1 + ph * 2);
            m.material.opacity = (1 - ph) * 0.7;
        });
        dots.forEach(d => {
            const q = (d.userData.p + t * 0.45) % 1;
            d.position.copy(link.getPoint(q));
            d.material.opacity = 0.7 * Math.sin(q * Math.PI);
        });
        led.material.color.set(Math.sin(t * 6) > 0 ? '#22c55e' : '#064e3b');
        world.rotation.y = lerp(Math.sin(t * 0.35) * 0.18 * motion, stage.mouse.x * 0.3, h);
        phone.position.y = Math.sin(t * 1.3) * 0.04 * motion;

        const pct = Math.round(level * 100);
        if (pct !== shown || rising !== shownRising) {
            shown = pct; shownRising = rising;
            drawWaterApp(appTex.userData.ctx, 300, 640, pct, rising);
            appTex.needsUpdate = true;
        }
        // Telegram alerts when crossing into the empty / overflow zones
        const nextZone = pct < WATER_LOW ? 'empty' : pct > WATER_HIGH ? 'overflow' : 'normal';
        if (nextZone !== zone) {
            zone = nextZone;
            if (zone !== 'normal') {
                alertKind = zone;
                alertUntil = t + 3.2;
                drawTelegram(tgTex.userData.ctx, 560, 150, zone, pct);
                tgTex.needsUpdate = true;
            }
        }
        const showing = t < alertUntil;
        tgMat.opacity = lerp(tgMat.opacity, showing ? 1 : 0, Math.min(dt * 6, 1));
        tg.position.y = lerp(tg.position.y, showing ? 1.55 : 1.85, Math.min(dt * 6, 1));
        tg.visible = tgMat.opacity > 0.01;
    };
}

/* ------------------------------------------------------------------ */
/* PRODUCT: SELLO Retail — supermarket checkout. Groceries ride the    */
/* conveyor, a gooseneck barcode scanner reads each one, the live bill */
/* builds on the POS screen, UPI payment, then the bill goes out on    */
/* WhatsApp and the owner's summary by email (HTML toasts on the .rc). */
/* Items and texts come from data-retail (tools/retail_showcase.py).   */
/* ------------------------------------------------------------------ */
function barcodeBars(ctx, x, y, w, h, seed) {
    let s = seed * 9301 + 49297;
    const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
    ctx.fillStyle = '#111';
    for (let cx = x; cx < x + w;) {
        const bw = 1 + Math.floor(rnd() * 3);
        if (rnd() < 0.62) ctx.fillRect(cx, y, bw, h);
        cx += bw + 1 + Math.floor(rnd() * 2);
    }
}

function drawRetailScreen(ctx, w, h, st, T, items, rtl) {
    const money = v => '₹' + v.toFixed(2);
    const box = (x, y, bw, bh) => [rtl ? w - x - bw : x, y, bw, bh];
    const tx = x => (rtl ? w - x : x);
    const al = a => (rtl ? (a === 'left' ? 'right' : 'left') : a);
    const FONT = rtl ? "'IBM Plex Sans Arabic', 'IBM Plex Sans', sans-serif" : "'IBM Plex Sans', system-ui, sans-serif";
    const text = (s, x, y, size, weight, colour, align = 'left') => {
        ctx.font = `${weight} ${size}px ${FONT}`; ctx.fillStyle = colour; ctx.textAlign = al(align); ctx.fillText(s, tx(x), y);
    };
    const panel = (x, y, bw, bh, r, fill, stroke) => {
        roundRect(ctx, ...box(x, y, bw, bh), r);
        if (fill) { ctx.fillStyle = fill; ctx.fill(); }
        if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 2; ctx.stroke(); }
    };
    ctx.direction = rtl ? 'rtl' : 'ltr';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#eef1f0'; ctx.fillRect(0, 0, w, h);
    // header
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, w, 58);
    ctx.fillStyle = '#dfe5e3'; ctx.fillRect(0, 58, w, 2);
    text((rtl ? '→ ' : '← ') + T.billing, 24, 30, 26, 600, '#1d2826');
    text('SELLO Retail · ' + T.counter, w - 24, 30, 22, 600, '#0f766e', 'right');
    const cw = ctx.measureText('SELLO Retail · ' + T.counter).width;
    ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(tx(w - 24 - cw - 16), 30, 7, 0, Math.PI * 2); ctx.fill();
    // search / scan field
    panel(16, 72, w - 32, 50, 10, '#ffffff', st.typed ? '#0f766e' : '#cfd8d5');
    text(st.typed || T.search, 34, 98, st.typed ? 24 : 20, st.typed ? 700 : 400, st.typed ? '#13201e' : '#8a9793');
    // bill rows (left)
    for (let i = 0; i < st.rows; i++) {
        const it = items[i], y = 136 + i * 86;
        panel(16, y, 600, 78, 10, i === st.flash ? '#c6efe3' : '#e1e8e6');
        text(String(i + 1), 34, y + 39, 18, 500, '#7b8985');
        text(it.name, 62, y + 27, 24, 600, '#1d2826');
        text(`${it.qty} ${T.pcs} × ${money(it.price)}`, 62, y + 56, 18, 400, '#66746f');
        text(money(it.qty * it.price), 596, y + 39, 24, 700, '#1d2826', 'right');
    }
    // summary (right)
    const R = 636, RW = w - R - 16;
    ctx.fillStyle = '#d5dedb'; ctx.fillRect(...box(R - 10, 136, 2, h - 152));
    panel(R, 136, RW, 46, 10, '#ffffff', '#cfd8d5');
    text(T.customer, R + 16, 159, 19, 400, '#4b5a56');
    ctx.globalAlpha = st.totals ? 1 : 0.28;
    [[T.subtotal, 557.5], [T.cgst, 12.52], [T.sgst, 12.52], [T.round, 0.5]].forEach(([k, v], i) => {
        text(k, R + 4, 206 + i * 28, 18, 400, '#5d6b67');
        text(money(v), R + RW - 4, 206 + i * 28, 18, 400, '#5d6b67', 'right');
    });
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#d5dedb'; ctx.fillRect(...box(R, 316, RW, 2));
    text(T.total, R + 4, 350, 22, 600, '#1d2826');
    text(money(st.total), R + RW - 4, 350, 40, 800, '#0f766e', 'right');
    panel(R, 384, RW, 56, 10, st.paying ? '#0b5d56' : '#0f766e');
    text(T.pay, R + RW / 2, 412, 22, 700, '#ffffff', 'center');
    if (st.paying) {
        [T.cash, T.card, T.upi].forEach((k, i) => {
            const cw = (RW - 16) / 3, on = i === 2 && st.upi;
            panel(R + i * (cw + 8), 454, cw, 46, 8, on ? '#0f766e' : '#ffffff', on ? '#0f766e' : '#c8d4d0');
            text(k, R + i * (cw + 8) + cw / 2, 477, 19, 600, on ? '#ffffff' : '#3d4a46', 'center');
        });
    }
    if (st.stamp) {
        ctx.save();
        ctx.translate(316, 330); ctx.rotate(-0.21); ctx.scale(st.stamp, st.stamp);
        ctx.font = `800 64px ${FONT}`; ctx.textAlign = 'center';
        const label = '✓ ' + T.paid, tw = ctx.measureText(label).width + 48;
        roundRect(ctx, -tw / 2, -46, tw, 92, 14);
        ctx.fillStyle = 'rgba(238,241,240,0.92)'; ctx.fill();
        ctx.lineWidth = 7; ctx.strokeStyle = '#0f9d58'; ctx.stroke();
        ctx.fillStyle = '#0f9d58'; ctx.fillText(label, 0, 4);
        ctx.restore();
    }
}

function initRetail(canvas) {
    const box = canvas.closest('.rc');
    let data = { items: [], text: {} };
    try { data = JSON.parse(box?.dataset.retail || '{}'); } catch (e) { /* keep defaults */ }
    const items = data.items || [], T = data.text || {};
    const rtl = document.documentElement.dir === 'rtl';
    const card = canvas.closest('.product, .pd-stage') || canvas;
    const stage = createStage(canvas, { fov: 30, z: 7.3, hoverTarget: card, minAspect: 1.6 });
    const { scene, camera } = stage;
    camera.position.set(0, 2.05, 7.0);
    camera.lookAt(0, 0.14, 0);
    addLights(scene);
    const warm = new THREE.SpotLight('#fff1d6', 26, 14, 0.7, 0.6);
    warm.position.set(-1, 5, 3);
    scene.add(warm);

    const root = new THREE.Group();
    root.position.x = 0.35;
    scene.add(root);
    const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.5, metalness: 0.1, ...o });
    const dark = std('#1b1f25', { metalness: 0.5, roughness: 0.4 });
    const steel = std('#9aa3ad', { metalness: 0.9, roughness: 0.25 });
    const TOP = -0.855;

    // checkout counter with a lime edge light
    const counter = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.36, 2.7), std('#14171c', { roughness: 0.6 }));
    counter.position.set(-0.3, TOP - 0.18, 0.25);
    root.add(counter);
    const edge = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.025, 0.025), new THREE.MeshBasicMaterial({ color: '#b6ff3b' }));
    edge.position.set(-0.3, TOP - 0.01, 1.6);
    root.add(edge);

    // conveyor belt (scrolling ribs), rails and end roller
    const beltTex = canvasTexture(64, 16, (ctx, w, h) => {
        ctx.fillStyle = '#1f242b'; ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = '#2f353e'; ctx.fillRect(0, 0, 10, h);
    });
    beltTex.wrapS = THREE.RepeatWrapping;
    beltTex.repeat.set(36, 1);
    const belt = new THREE.Mesh(new THREE.PlaneGeometry(3.5, 0.82), new THREE.MeshStandardMaterial({ map: beltTex, roughness: 0.8 }));
    belt.rotation.x = -Math.PI / 2;
    belt.position.set(-1.45, TOP + 0.012, 0.6);
    root.add(belt);
    [0.17, 1.03].forEach(z => {
        const rail = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.07, 0.05), steel);
        rail.position.set(-1.45, TOP + 0.035, z);
        root.add(rail);
    });
    const roller = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.86, 20), steel);
    roller.rotation.x = Math.PI / 2;
    roller.position.set(0.3, TOP + 0.02, 0.6);
    root.add(roller);

    // POS terminal: slim white all-in-one on a pole, live SELLO Retail bill on screen
    const pos = new THREE.Group();
    pos.position.set(-0.45, 0, -0.8);
    root.add(pos);
    const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.46, 0.05, 40), std('#e6eaee', { metalness: 0.3, roughness: 0.35 }));
    foot.position.y = TOP + 0.025;
    pos.add(foot);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.07, 1.05, 24), std('#cfd5db', { metalness: 0.7, roughness: 0.3 }));
    pole.position.y = TOP + 0.55;
    pos.add(pole);
    const head = new THREE.Group();
    head.position.set(0, 0.72, 0.02);
    head.rotation.x = -0.16;
    pos.add(head);
    const SW = 2.9, SH = 1.63;
    const housing = new THREE.Mesh((() => {
        const g = new THREE.ExtrudeGeometry(roundedRectShape(SW + 0.14, SH + 0.16, 0.07), { depth: 0.07, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.015, bevelSegments: 3, curveSegments: 10 });
        g.center(); return g;
    })(), std('#eef1f4', { metalness: 0.25, roughness: 0.3 }));
    head.add(housing);
    const bezel = new THREE.Mesh(new THREE.PlaneGeometry(SW + 0.06, SH + 0.06), new THREE.MeshBasicMaterial({ color: '#0d0f12' }));
    bezel.position.set(0, 0.01, 0.052);
    head.add(bezel);
    const state = { key: '' };
    const screenTex = canvasTexture(1024, 576, (ctx, w, h) => drawRetailScreen(ctx, w, h, { rows: 0, flash: -1, typed: '', total: 0 }, T, items, rtl));
    screenTex.anisotropy = 8;
    const screen = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false }));
    screen.position.set(0, 0.01, 0.055);
    head.add(screen);
    const sheen = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshBasicMaterial({
        map: canvasTexture(256, 144, (ctx, w, h) => {
            const g = ctx.createLinearGradient(0, 0, w, h);
            g.addColorStop(0, 'rgba(255,255,255,0.16)'); g.addColorStop(0.4, 'rgba(255,255,255,0.02)'); g.addColorStop(0.55, 'rgba(255,255,255,0)');
            ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
        }), transparent: true, depthWrite: false,
    }));
    sheen.position.set(0, 0.01, 0.058);
    head.add(sheen);

    // handheld barcode scanner on a gooseneck stand (white grip, dark head) aimed at the end of the belt
    const scanP = new THREE.Vector3(0.0, TOP, 0.6);        // where a product stops to be scanned
    const sc = new THREE.Group();
    root.add(sc);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.38, 0.07, 40), dark);
    base.scale.z = 0.72;
    base.position.set(1.0, TOP + 0.035, 0.72);
    sc.add(base);
    const H = new THREE.Vector3(0.42, 0.02, 0.66);          // centre of the scan head
    const target = new THREE.Vector3(0.02, TOP + 0.36, 0.62);
    const aim = target.clone().sub(H).normalize();
    const neckCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(1.0, TOP + 0.06, 0.72), new THREE.Vector3(1.02, TOP + 0.45, 0.7),
        new THREE.Vector3(0.9, -0.12, 0.68), new THREE.Vector3(0.7, -0.07, 0.66),
    ]);
    sc.add(new THREE.Mesh(new THREE.TubeGeometry(neckCurve, 40, 0.032, 10), dark));
    const scHead = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.15, 0.26, 32), dark);
    scHead.position.copy(H);
    scHead.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), aim);
    sc.add(scHead);
    const windowMat = new THREE.MeshBasicMaterial({ color: '#2a0a0a' });
    const win = new THREE.Mesh(new THREE.CircleGeometry(0.135, 32), windowMat);
    win.position.copy(H).addScaledVector(aim, 0.132);
    win.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), aim);
    sc.add(win);
    const gripDir = new THREE.Vector3(0.62, 0.16, 0).normalize();
    const grip = new THREE.Mesh(new THREE.CapsuleGeometry(0.095, 0.42, 8, 20), std('#eceae4', { roughness: 0.38 }));
    grip.position.copy(H).addScaledVector(gripDir, 0.34).add(new THREE.Vector3(0, 0.03, 0));
    grip.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), gripDir);
    sc.add(grip);
    const tail = new THREE.Mesh(new THREE.SphereGeometry(0.1, 20, 16), dark);
    tail.position.copy(H).addScaledVector(gripDir, 0.64).add(new THREE.Vector3(0, 0.03, 0));
    sc.add(tail);
    const trigger = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.12, 0.08), dark);
    trigger.position.copy(H).addScaledVector(gripDir, 0.2).add(new THREE.Vector3(0, -0.1, 0));
    trigger.rotation.z = 0.3;
    sc.add(trigger);
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.018, 10, 10), new THREE.MeshBasicMaterial({ color: '#2a3a1a' }));
    led.position.copy(grip.position).add(new THREE.Vector3(0, 0.1, 0.03));
    sc.add(led);
    // laser fan + scan line
    const laserMat = new THREE.MeshBasicMaterial({ color: '#ff2a2a', transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
    const fanLen = target.distanceTo(win.position);
    const fan = new THREE.Mesh(new THREE.ConeGeometry(0.26, fanLen, 32, 1, true), laserMat);
    fan.geometry.rotateZ(Math.PI);                            // tip at +y
    fan.geometry.translate(0, -fanLen / 2, 0);                 // tip at the origin, opening along -y
    fan.position.copy(win.position);
    fan.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), aim);
    sc.add(fan);
    const lineMat = new THREE.MeshBasicMaterial({ color: '#ff3030', transparent: true, opacity: 0, toneMapped: false });
    const scanLine = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.012, 0.012), lineMat);
    scanLine.position.copy(target).add(new THREE.Vector3(0, -0.02, 0.06));
    sc.add(scanLine);

    // paper shopping bag (open top) the scanned items drop into
    const bagP = new THREE.Vector3(2.15, TOP, 0.55);
    const kraft = std('#c9a27a', { roughness: 0.85, side: THREE.DoubleSide });
    const bag = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.78, 0.55), [kraft, kraft, new THREE.MeshBasicMaterial({ visible: false }), kraft, kraft, kraft]);
    bag.position.copy(bagP).add(new THREE.Vector3(0, 0.39, 0));
    root.add(bag);
    [-0.276, 0.276].forEach(z => {
        const handle = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.016, 8, 24, Math.PI), kraft);
        handle.position.copy(bagP).add(new THREE.Vector3(0, 0.78, z));
        root.add(handle);
    });

    // the groceries (origin at the bottom centre of each)
    const label = (it, w, h, seed) => canvasTexture(w, h, (ctx) => {
        ctx.fillStyle = '#fbfaf6'; ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = it.colour; ctx.fillRect(0, 0, w, h * 0.22);
        ctx.fillStyle = '#1b1f24'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.direction = rtl ? 'rtl' : 'ltr';
        ctx.font = `700 ${Math.round(h * 0.1)}px ${rtl ? "'IBM Plex Sans Arabic', sans-serif" : "'IBM Plex Sans', sans-serif"}`;
        ctx.fillText(it.name, w / 2, h * 0.42, w * 0.92);
        ctx.fillStyle = '#fff'; ctx.fillRect(w * 0.15, h * 0.58, w * 0.7, h * 0.3);
        barcodeBars(ctx, w * 0.18, h * 0.6, w * 0.64, h * 0.2, seed);
        ctx.fillStyle = '#111'; ctx.font = `500 ${Math.round(h * 0.055)}px monospace`; ctx.direction = 'ltr';
        ctx.fillText(it.code, w / 2, h * 0.845);
    });
    const boxProduct = (it, w, h, d, seed) => {
        const g = new THREE.Group();
        const side = std(it.colour, { roughness: 0.6 });
        const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), [side, side, side, side, new THREE.MeshStandardMaterial({ map: label(it, 256, 320, seed), roughness: 0.55 }), side]);
        m.position.y = h / 2;
        g.add(m);
        return g;
    };
    const bottle = (it, seed) => {
        const g = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.46, 32), std('#e8b923', { transparent: true, opacity: 0.88, roughness: 0.15 }));
        body.position.y = 0.23; g.add(body);
        const shoulder = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.12, 0.1, 32), body.material);
        shoulder.position.y = 0.51; g.add(shoulder);
        const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.07, 24), std('#d62828'));
        cap.position.y = 0.595; g.add(cap);
        const band = new THREE.Mesh(new THREE.CylinderGeometry(0.123, 0.123, 0.24, 32, 1, true, -1.25, 2.5),
            new THREE.MeshStandardMaterial({ map: label(it, 300, 240, seed), roughness: 0.5 }));
        band.position.y = 0.22; g.add(band);
        return g;
    };
    const tomatoes = (it, seed) => {
        const g = new THREE.Group();
        const tray = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.06, 0.34), std('#f2f2ee'));
        tray.position.y = 0.03; g.add(tray);
        const red = std('#d7261e', { roughness: 0.3 }), green = std('#2f7d32');
        [[-0.13, -0.07], [0.0, -0.08], [0.13, -0.07], [-0.07, 0.07], [0.08, 0.07]].forEach(([x, z]) => {
            const tm = new THREE.Mesh(new THREE.SphereGeometry(0.1, 20, 16), red);
            tm.scale.y = 0.85; tm.position.set(x, 0.14, z); g.add(tm);
            const st = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.04, 6), green);
            st.position.set(x, 0.23, z); g.add(st);
        });
        const tag = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.2), new THREE.MeshStandardMaterial({ map: label(it, 260, 200, seed) }));
        tag.position.set(0, 0.17, 0.2); tag.rotation.x = -0.35; g.add(tag);
        return g;
    };
    const makers = { bag: (it, s) => boxProduct(it, 0.46, 0.6, 0.2, s), bottle, tray: tomatoes, box: (it, s) => boxProduct(it, 0.3, 0.42, 0.18, s) };
    const products = items.map((it, i) => {
        const g = (makers[it.kind] || makers.box)(it, i + 7);
        g.visible = false;
        root.add(g);
        return g;
    });
    const amounts = items.map(it => it.qty * it.price);
    const sum = amounts.reduce((a, b) => a + b, 0);
    const rounded = Math.round(sum);
    const bagSlots = [[-0.18, -0.08], [0.2, 0.06], [0.05, -0.1], [-0.12, 0.1]];

    // timeline (seconds)
    const START = (i) => 0.6 + i * 2.4, MOVE = 1.2, BEEP = 0.45, FLY = 0.75;
    const last = START(items.length - 1) + MOVE + BEEP + FLY;
    const TOT = last + 0.3, PAY = TOT + 0.9, UPI = PAY + 0.6, PAID = UPI + 0.8, WA = PAID + 0.9, MAIL = WA + 1.5, LOOP = MAIL + 3.6;
    let clockT = 0;

    stage.update = (t, dt) => {
        clockT += dt;
        const tl = reducedMotion ? WA + 0.1 : clockT % LOOP;
        const h = stage.h;
        root.rotation.y = lerp(Math.sin(t * 0.35) * 0.1 * (reducedMotion ? 0 : 1), stage.mouse.x * 0.4, h);
        root.rotation.x = lerp(0, -stage.mouse.y * 0.06, h);

        let moving = false, beeping = -1, typed = '', flash = -1, rows = 0, total = 0;
        products.forEach((g, i) => {
            const s = tl - START(i);
            if (s < 0) { g.visible = false; return; }
            g.visible = true;
            g.rotation.set(0, 0, 0);
            if (s < MOVE) {
                moving = true;
                g.position.set(lerp(-3.05, scanP.x, 1 - Math.pow(1 - s / MOVE, 3)), scanP.y, scanP.z);
                g.scale.setScalar(1);
            } else if (s < MOVE + BEEP) {
                beeping = i;
                g.position.copy(scanP);
                g.scale.setScalar(1);
            } else {
                const k = ease(clamp01((s - MOVE - BEEP) / FLY));
                const [bx, bz] = bagSlots[i % bagSlots.length];
                const end = new THREE.Vector3(bagP.x + bx, bagP.y + 0.04, bagP.z + bz);
                g.position.lerpVectors(scanP, end, k);
                g.position.y += Math.sin(Math.PI * k) * 0.95;
                g.rotation.z = -k * 0.5;
                g.scale.setScalar(lerp(1, 0.8, k));
            }
            if (s >= MOVE && s < MOVE + BEEP + 0.35) typed = items[i].code;
            const rowAt = MOVE + 0.2;
            if (s >= rowAt) { rows = i + 1; total += amounts[i] * ease(clamp01((s - rowAt) / 0.5)); }
            if (s >= rowAt && s < rowAt + 0.8) flash = i;
        });
        if (moving && !reducedMotion) beltTex.offset.x -= dt * 0.9 * 36 / 3.5;
        if (tl >= TOT) total = sum + (rounded - sum) * ease(clamp01((tl - TOT) / 0.6));

        const beam = beeping >= 0 ? 0.55 + 0.25 * Math.sin(t * 60) : 0;
        laserMat.opacity = beam * 0.5;
        lineMat.opacity = beam ? 1 : 0;
        windowMat.color.set(beeping >= 0 ? '#ff4040' : '#2a0a0a');
        led.material.color.set(beeping >= 0 ? '#22c55e' : '#2a3a1a');

        const st = {
            rows, flash, typed, total: Math.round(total * 100) / 100,
            totals: tl >= TOT, paying: tl >= PAY, upi: tl >= UPI,
            stamp: tl >= PAID ? Math.round((1 + 0.8 * (1 - ease(clamp01((tl - PAID) / 0.3)))) * 50) / 50 : 0,
        };
        const key = JSON.stringify(st);
        if (key !== state.key) {
            state.key = key;
            drawRetailScreen(screenTex.userData.ctx, 1024, 576, st, T, items, rtl);
            screenTex.needsUpdate = true;
        }
        if (box) {
            box.classList.toggle('wa', tl >= WA);
            box.classList.toggle('mail', tl >= MAIL);
        }
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
            if (s === 'sello') initTerminal(c);
            else if (s === 'selloLite') initLitePhone(c);
            else if (s === 'bell') initBell(c);
            else if (s === 'water') initWater(c);
            else if (s === 'selloRetail') initRetail(c);
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
