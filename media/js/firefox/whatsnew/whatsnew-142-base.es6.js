/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    const storageKey = 'wnp-theme';
    const root = document.documentElement;
    const hamburger = document.querySelector('.wnp-hamburger');
    const nav = document.getElementById('wnp-nav');

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
            swapStickerSourcesForTheme(stored);
        } else {
            const sys =
                window.matchMedia &&
                window.matchMedia('(prefers-color-scheme: dark)').matches
                    ? 'dark'
                    : 'light';
            root.setAttribute('data-theme', sys);
            swapStickerSourcesForTheme(sys);
        }
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
