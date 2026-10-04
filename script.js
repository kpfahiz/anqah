// Shared by index.html and the product pages, so every block checks its elements exist.
document.addEventListener('DOMContentLoaded', () => {
    const whatsappNumber = '971505762100';
    const $ = id => document.getElementById(id);
    const ar = document.documentElement.lang === 'ar';
    // UI strings for the Arabic pages; English is the default
    const t = ar ? {
        hello: name => `مرحبًا Anqah Tech، أنا ${name}.`, interest: 'مهتم بـ', phone: 'الهاتف', email: 'البريد',
        prev: 'الصورة السابقة', next: 'الصورة التالية', close: 'إغلاق',
    } : {
        hello: name => `Hello Anqah Tech, I'm ${name}.`, interest: 'Interested in', phone: 'Phone', email: 'Email',
        prev: 'Previous screen', next: 'Next screen', close: 'Close',
    };

    // Mobile menu
    const toggle = $('menuToggle');
    const links = $('navLinks');
    if (toggle && links) {
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
    }

    // Header background on scroll
    const header = $('header');
    if (header) {
        const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 30);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Scroll reveals
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

    // "Enquire" buttons prefill the contact form (home page)
    const interest = $('interestSelect');
    document.querySelectorAll('[data-enquire]').forEach(btn => {
        btn.addEventListener('click', e => {
            e.stopPropagation();
            if (!interest) return;
            interest.value = btn.dataset.enquire;
            $('contact').scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Contact form -> WhatsApp
    const form = $('contactForm');
    if (form) {
        form.addEventListener('submit', e => {
            e.preventDefault();
            const f = new FormData(form);
            const lines = [
                t.hello([f.get('first'), f.get('last')].filter(Boolean).join(' ')),
                f.get('interest') && `${t.interest}: ${f.get('interest')}`,
                f.get('phone') && `${t.phone}: ${f.get('phone')}`,
                f.get('email') && `${t.email}: ${f.get('email')}`,
                '',
                f.get('message'),
            ].filter(v => v !== null && v !== undefined && v !== false);
            window.open(`https://wa.me/${whatsappNumber}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
        });
    }

    // Screenshot lightbox: links marked data-lightbox="group" open in a dialog with prev/next
    const shots = [...document.querySelectorAll('a[data-lightbox]')];
    if (shots.length && window.HTMLDialogElement) {
        const dlg = document.createElement('dialog');
        dlg.className = 'lightbox';
        dlg.innerHTML = '<figure><img alt=""><figcaption><span class="lb-cap"></span><span class="lb-count"></span></figcaption></figure>' +
            `<button class="lb-btn lb-prev" aria-label="${t.prev}">&larr;</button>` +
            `<button class="lb-btn lb-next" aria-label="${t.next}">&rarr;</button>` +
            `<button class="lb-close" aria-label="${t.close}">&times;</button>`;
        document.body.appendChild(dlg);
        const img = dlg.querySelector('img');
        let index = 0;
        const show = i => {
            index = (i + shots.length) % shots.length;
            const a = shots[index];
            img.src = a.href;
            img.alt = a.querySelector('img')?.alt || '';
            dlg.querySelector('.lb-cap').textContent = a.dataset.caption || '';
            dlg.querySelector('.lb-count').textContent = `${String(index + 1).padStart(2, '0')} / ${String(shots.length).padStart(2, '0')}`;
        };
        shots.forEach((a, i) => a.addEventListener('click', e => {
            e.preventDefault();
            show(i);
            dlg.showModal();
        }));
        dlg.querySelector('.lb-prev').addEventListener('click', () => show(index - 1));
        dlg.querySelector('.lb-next').addEventListener('click', () => show(index + 1));
        dlg.querySelector('.lb-close').addEventListener('click', () => dlg.close());
        dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); }); // backdrop click
        dlg.addEventListener('keydown', e => {
            if (e.key === 'ArrowLeft') show(index - 1);
            if (e.key === 'ArrowRight') show(index + 1);
        });
    }

    // Feature tabs: click or use arrow keys / Home / End to switch panels
    document.querySelectorAll('[data-tabs]').forEach(box => {
        const tabs = [...box.querySelectorAll('[role="tab"]')];
        const select = (tab, focus) => {
            tabs.forEach(t => {
                const on = t === tab;
                t.setAttribute('aria-selected', on);
                t.tabIndex = on ? 0 : -1;
                document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
            });
            if (focus) tab.focus();
            tab.scrollIntoView({ block: 'nearest', inline: 'nearest' });
        };
        tabs.forEach((t, i) => {
            t.addEventListener('click', () => select(t));
            t.addEventListener('keydown', e => {
                const next = { ArrowDown: i + 1, ArrowRight: i + 1, ArrowUp: i - 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
                if (next === undefined) return;
                e.preventDefault();
                select(tabs[(next + tabs.length) % tabs.length], true);
            });
        });
    });

    const year = $('year');
    if (year) year.textContent = new Date().getFullYear();

    // Status bar clock (Gulf Standard Time, Abu Dhabi)
    const clock = $('clock');
    if (clock) {
        const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Dubai', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
        const tickClock = () => { clock.textContent = fmt.format(new Date()); };
        tickClock();
        setInterval(tickClock, 1000);
    }

    // Terminal: types a few commands in a loop
    const typed = $('typed');
    if (typed) {
        const commands = (typed.dataset.commands || [
            'anqah --init smart-systems',
            'deploy sello --mode=retail,restaurant',
            'bell.schedule load timetable.json',
            'water.monitor --tank=1 --alerts=on',
        ].join('|')).split('|');
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
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
    }
});
