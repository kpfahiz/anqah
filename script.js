document.addEventListener('DOMContentLoaded', () => {
    const whatsappNumber = '971505762100';

    // Mobile menu
    const toggle = document.getElementById('menuToggle');
    const links = document.getElementById('navLinks');
    toggle.addEventListener('click', () => {
        const open = links.classList.toggle('open');
        toggle.classList.toggle('open', open);
        toggle.setAttribute('aria-expanded', open);
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
        links.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
    }));

    // Header background on scroll
    const header = document.getElementById('header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 30);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Scroll reveals (also triggers the status bars)
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // Stat counters
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = Number(el.dataset.count);
        const suffix = el.dataset.suffix || '';
        const start = performance.now();
        const tick = now => {
            const t = Math.min((now - start) / 1400, 1);
            el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3))) + suffix;
            if (t < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    });

    // 3D tilt + spotlight on service cards
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    document.querySelectorAll('.tilt').forEach(card => {
        if (!finePointer) return;
        card.addEventListener('mousemove', e => {
            const r = card.getBoundingClientRect();
            const x = (e.clientX - r.left) / r.width;
            const y = (e.clientY - r.top) / r.height;
            card.style.transform = `rotateX(${(0.5 - y) * 10}deg) rotateY(${(x - 0.5) * 12}deg)`;
            card.style.setProperty('--mx', `${x * 100}%`);
            card.style.setProperty('--my', `${y * 100}%`);
        });
        card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });

    // "Enquire" buttons prefill the contact form
    const interest = document.getElementById('interestSelect');
    document.querySelectorAll('[data-enquire]').forEach(btn => {
        btn.addEventListener('click', e => {
            e.stopPropagation();
            interest.value = btn.dataset.enquire;
            document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Contact form -> WhatsApp
    document.getElementById('contactForm').addEventListener('submit', e => {
        e.preventDefault();
        const f = new FormData(e.target);
        const lines = [
            `Hello Anqah Tech, I'm ${[f.get('first'), f.get('last')].filter(Boolean).join(' ')}.`,
            f.get('interest') && `Interested in: ${f.get('interest')}`,
            f.get('phone') && `Phone: ${f.get('phone')}`,
            f.get('email') && `Email: ${f.get('email')}`,
            '',
            f.get('message'),
        ].filter(v => v !== null && v !== undefined && v !== false);
        window.open(`https://wa.me/${whatsappNumber}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
    });

    document.getElementById('year').textContent = new Date().getFullYear();

    // Status bar clock (Gulf Standard Time, Abu Dhabi)
    const clock = document.getElementById('clock');
    const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Dubai', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    const tickClock = () => { clock.textContent = fmt.format(new Date()); };
    tickClock();
    setInterval(tickClock, 1000);

    // Terminal: types a few commands in a loop
    const typed = document.getElementById('typed');
    const commands = [
        'anqah --init smart-systems',
        'deploy sello --edition=pro',
        'bell.schedule load timetable.json',
        'water.monitor --tank=1 --alerts=on',
    ];
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) {
        typed.textContent = commands[0];
    } else {
        let ci = 0, pos = 0, deleting = false;
        const step = () => {
            const cmd = commands[ci];
            pos += deleting ? -1 : 1;
            typed.textContent = cmd.slice(0, pos);
            let delay = deleting ? 28 : 55 + Math.random() * 60;
            if (!deleting && pos === cmd.length) { deleting = true; delay = 1800; }
            else if (deleting && pos === 0) { deleting = false; ci = (ci + 1) % commands.length; delay = 400; }
            setTimeout(step, delay);
        };
        setTimeout(step, 600);
    }
});
