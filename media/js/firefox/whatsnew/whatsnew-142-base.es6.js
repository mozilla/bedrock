(function () {
    const storageKey = 'wnp-theme';
    const root = document.documentElement;
    const toggle = document.querySelector('.wnp-nav-toggle');
    const hamburger = document.querySelector('.wnp-hamburger');
    const nav = document.getElementById('wnp-nav');
    const themeButtons = document.querySelectorAll('.wnp-theme-btn');

    function applyStoredTheme() {
        const stored = localStorage.getItem(storageKey);
        if (stored === 'light' || stored === 'dark') {
        root.setAttribute('data-theme', stored);
        if (toggle) toggle.setAttribute('aria-pressed', stored === 'dark');
        themeButtons.forEach(function (btn) {
            btn.classList.toggle('is-active', btn.getAttribute('data-theme') === stored);
        });
        } else {
        root.removeAttribute('data-theme');
        if (toggle) {
            const isSystemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            toggle.setAttribute('aria-pressed', isSystemDark);
        }
        const sys = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
        themeButtons.forEach(function (btn) {
            btn.classList.toggle('is-active', btn.getAttribute('data-theme') === sys);
        });
        }
    }

    function toggleTheme() {
        const forced = root.getAttribute('data-theme');
        if (!forced) {
            const isSystemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const next = isSystemDark ? 'light' : 'dark';
            localStorage.setItem(storageKey, next);
        } else {
            const nextForced = forced === 'dark' ? 'light' : 'dark';
            localStorage.setItem(storageKey, nextForced);
        }
        applyStoredTheme();
    }

    if (toggle) {
        toggle.addEventListener('click', toggleTheme);
    }

    function toggleMobileNav() {
        if (!nav || !hamburger) return;
        const open = nav.classList.toggle('is-open');
        hamburger.setAttribute('aria-expanded', open);
        const openLabel = hamburger.getAttribute('data-label-open') || 'Close';
        const closedLabel = hamburger.getAttribute('data-label-closed') || 'Menu';
        hamburger.setAttribute('aria-label', open ? openLabel : closedLabel);
        // Lock scroll when open
        document.body.style.overflow = open ? 'hidden' : '';
    }

    if (hamburger && nav) {
        hamburger.addEventListener('click', toggleMobileNav);
        document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && nav.classList.contains('is-open')) {
            toggleMobileNav();
        }
        });
    }

    if (themeButtons.length) {
        themeButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const choice = btn.getAttribute('data-theme');
            if (choice === 'light' || choice === 'dark') {
            localStorage.setItem(storageKey, choice);
            applyStoredTheme();
            }
        });
        });
    }

    if (window.matchMedia) {
        const mql = window.matchMedia('(prefers-color-scheme: dark)');
        mql.addEventListener ? mql.addEventListener('change', function () {
        if (!localStorage.getItem(storageKey)) applyStoredTheme();
        }) : mql.addListener && mql.addListener(function () {
        if (!localStorage.getItem(storageKey)) applyStoredTheme();
        });
    }

    applyStoredTheme();
})();
