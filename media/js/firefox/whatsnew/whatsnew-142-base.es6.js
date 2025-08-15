/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    const storageKey = 'wnp-theme';
    const root = document.documentElement;
    const toggle = document.querySelector('.wnp-nav-toggle');
    const hamburger = document.querySelector('.wnp-hamburger');
    const nav = document.getElementById('wnp-nav');
    const themeButtons = document.querySelectorAll('.wnp-theme-btn');

    function swapStickerSourcesForTheme(theme) {
        const stickers = document.querySelectorAll(
            '.wnp-card-sticker[data-dark-src]'
        );
        stickers.forEach(function (img) {
            // Preserve the original light src once
            if (!img.getAttribute('data-light-src')) {
                img.setAttribute('data-light-src', img.getAttribute('src'));
            }
            const lightSrc = img.getAttribute('data-light-src');
            const darkSrc = img.getAttribute('data-dark-src');
            if (!darkSrc) return;
            if (theme === 'dark') {
                if (img.getAttribute('src') !== darkSrc)
                    img.setAttribute('src', darkSrc);
            } else {
                if (img.getAttribute('src') !== lightSrc)
                    img.setAttribute('src', lightSrc);
            }
        });
    }

    function applyStoredTheme() {
        const stored = localStorage.getItem(storageKey);
        if (stored === 'light' || stored === 'dark') {
            root.setAttribute('data-theme', stored);
            if (toggle) toggle.setAttribute('aria-pressed', stored === 'dark');
            themeButtons.forEach(function (btn) {
                btn.classList.toggle(
                    'is-active',
                    btn.getAttribute('data-theme') === stored
                );
            });
            swapStickerSourcesForTheme(stored);
        } else {
            const sys =
                window.matchMedia &&
                window.matchMedia('(prefers-color-scheme: dark)').matches
                    ? 'dark'
                    : 'light';
            root.setAttribute('data-theme', sys);

            if (toggle) {
                toggle.setAttribute('aria-pressed', sys === 'dark');
            }
            themeButtons.forEach(function (btn) {
                btn.classList.toggle(
                    'is-active',
                    btn.getAttribute('data-theme') === sys
                );
            });
            swapStickerSourcesForTheme(sys);
        }
    }

    function toggleTheme() {
        const forced = root.getAttribute('data-theme');
        if (!forced) {
            const isSystemDark =
                window.matchMedia &&
                window.matchMedia('(prefers-color-scheme: dark)').matches;
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
        const closedLabel =
            hamburger.getAttribute('data-label-closed') || 'Menu';
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
        const onChange = function () {
            if (!localStorage.getItem(storageKey)) applyStoredTheme();
        };
        mql.addEventListener
            ? mql.addEventListener('change', onChange)
            : mql.addListener && mql.addListener(onChange);
    }

    // Inclusive Card Pattern - Making entire cards clickable
    // Based on https://inclusive-components.design/cards/
    function initInclusiveCards() {
        addInclusiveInteraction('.wnp-feature', '.wnp-feature-content-inner');
        addInclusiveInteraction('.wnp-card', '.wnp-card-content');
    }

    function addInclusiveInteraction(cardClass, wrapperClass) {
        const cards = document.querySelectorAll(cardClass);
        cards.forEach(function (card) {
            const link = card.querySelector('.wnp-subtitle a');
            if (!link) return;
            card.style.cursor = 'pointer';
            const contentWrapper = card.querySelector(wrapperClass);
            if (contentWrapper) {
                let down, up;
                contentWrapper.onmousedown = () => (down = +new Date());
                contentWrapper.onmouseup = () => {
                    up = +new Date();
                    const clickDuration = up - down;
                    const button = card.querySelector('.wnp-button');
                    if (
                        event.target === link ||
                        link.contains(event.target) ||
                        (button &&
                            (event.target === button ||
                                button.contains(event.target)))
                    ) {
                        return;
                    }
                    if (clickDuration > 200) {
                        return;
                    }
                    link.click();
                };
            }
        });
    }

    function initCustomDropdowns() {
        const customSelects = document.querySelectorAll('.wnp-custom-select');

        customSelects.forEach(function (select) {
            const button = select.querySelector('.wnp-select-button');
            const dropdown = select.querySelector('.wnp-select-dropdown');
            const options = select.querySelectorAll('.wnp-select-option');
            const hiddenInput = select.querySelector('input[type="hidden"]');
            const textSpan = select.querySelector('.wnp-select-text');

            if (!button || !dropdown || !hiddenInput || !textSpan) return;

            button.addEventListener('click', function (e) {
                e.preventDefault();
                const isExpanded =
                    button.getAttribute('aria-expanded') === 'true';

                customSelects.forEach(function (otherSelect) {
                    if (otherSelect !== select) {
                        otherSelect
                            .querySelector('.wnp-select-button')
                            .setAttribute('aria-expanded', 'false');
                        otherSelect
                            .querySelector('.wnp-select-dropdown')
                            .classList.remove('wnp-select-open');
                    }
                });
                button.setAttribute('aria-expanded', !isExpanded);
                dropdown.classList.toggle('wnp-select-open');
            });

            options.forEach(function (option) {
                option.addEventListener('click', function () {
                    const value = option.dataset.value;
                    const text = option.textContent;

                    hiddenInput.value = value;

                    textSpan.textContent = text;

                    options.forEach(function (opt) {
                        opt.classList.remove('wnp-select-selected');
                    });
                    option.classList.add('wnp-select-selected');

                    button.setAttribute('aria-expanded', 'false');
                    dropdown.classList.remove('wnp-select-open');

                    hiddenInput.dispatchEvent(new Event('change'));
                });
            });

            document.addEventListener('click', function (e) {
                if (!select.contains(e.target)) {
                    button.setAttribute('aria-expanded', 'false');
                    dropdown.classList.remove('wnp-select-open');
                }
            });

            button.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    button.click();
                }
            });

            dropdown.addEventListener('keydown', function (e) {
                const currentOption =
                    dropdown.querySelector(
                        '.wnp-select-option[tabindex="0"]'
                    ) || options[0];

                switch (e.key) {
                    case 'ArrowDown': {
                        e.preventDefault();
                        const nextOption =
                            currentOption.nextElementSibling || options[0];
                        options.forEach((opt) =>
                            opt.setAttribute('tabindex', '-1')
                        );
                        nextOption.setAttribute('tabindex', '0');
                        nextOption.focus();
                        break;
                    }
                    case 'ArrowUp': {
                        e.preventDefault();
                        const prevOption =
                            currentOption.previousElementSibling ||
                            options[options.length - 1];
                        options.forEach((opt) =>
                            opt.setAttribute('tabindex', '-1')
                        );
                        prevOption.setAttribute('tabindex', '0');
                        prevOption.focus();
                        break;
                    }
                    case 'Enter':
                    case ' ':
                        e.preventDefault();
                        currentOption.click();
                        break;
                    case 'Escape':
                        button.setAttribute('aria-expanded', 'false');
                        dropdown.classList.remove('wnp-select-open');
                        button.focus();
                        break;
                }
            });
        });
    }

    function initNewsletterForm() {
        const emailInput = document.getElementById('wnp-email');
        const formDetails = document.querySelector('.wnp-form-details');
        const checkbox = document.getElementById('wnp-privacy');
        const submit = document.getElementById('newsletter-submit');

        const include_country = document.getElementById('id_country') !== null;
        const include_language = document.getElementById('id_lang') !== null;

        if (!emailInput || !formDetails || !checkbox || !submit) {
            return;
        }

        let isFormExpanded = false;

        emailInput.addEventListener('input', function () {
            if (this.value.length > 0 && !isFormExpanded) {
                formDetails.classList.remove('wnp-form-row-hidden');
                emailInput
                    .closest('.wnp-subscribe')
                    .classList.add('wnp-subscribe-expanded');
                isFormExpanded = true;
            } else if (this.value.length === 0 && isFormExpanded) {
                formDetails.classList.add('wnp-form-row-hidden');
                emailInput
                    .closest('.wnp-subscribe')
                    .classList.remove('wnp-subscribe-expanded');
                isFormExpanded = false;
            }
        });

        emailInput.addEventListener('focus', function () {
            if (this.value.length > 0 && !isFormExpanded) {
                formDetails.classList.remove('wnp-form-row-hidden');
                emailInput
                    .closest('.wnp-subscribe')
                    .classList.add('wnp-subscribe-expanded');
                isFormExpanded = true;
            }
        });

        function sync() {
            const emailValid = emailInput.value.length > 0;
            const countryValid =
                !include_country ||
                (document.getElementById('id_country') &&
                    document.getElementById('id_country').value !== '');
            const languageValid =
                !include_language ||
                (document.getElementById('id_lang') &&
                    document.getElementById('id_lang').value !== '');
            const consentValid = checkbox.checked;

            submit.disabled = !(
                emailValid &&
                countryValid &&
                languageValid &&
                consentValid
            );
        }

        emailInput.addEventListener('input', sync);
        checkbox.addEventListener('change', sync);

        // Initialize custom dropdowns
        initCustomDropdowns();

        if (include_country && document.getElementById('id_country')) {
            document
                .getElementById('id_country')
                .addEventListener('change', sync);
        }
        if (include_language && document.getElementById('id_lang')) {
            document.getElementById('id_lang').addEventListener('change', sync);
        }

        sync();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initInclusiveCards();
            initNewsletterForm();
        });
    } else {
        initInclusiveCards();
        initNewsletterForm();
    }

    applyStoredTheme();
})();
