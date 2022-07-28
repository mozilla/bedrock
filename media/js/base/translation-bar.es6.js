/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const translationBar = {};

// Normalize language in the form of ab or ab-CD.
translationBar.normalize = function (lang) {
    return lang.replace(/^(\w+)(?:-(\w+))?$/, function (m, p1, p2) {
        return p1.toLowerCase() + (p2 ? '-' + p2.toUpperCase() : '');
    });
};

// Returns boolean if lang matches target lang.
translationBar.isLangMatch = function (targetLang, lang, exact = false) {
    if (exact) {
        return targetLang === lang;
    } else {
        return (
            targetLang === lang ||
            targetLang === lang.split('-')[0] ||
            targetLang.split('-')[0] === lang.split('-')[0]
        );
    }
};

// Return best matched available language, or `false` if none found.
translationBar.getBestMatch = function (acceptLangs, availableLangs) {
    // Map short locale names to long, preferred locale names.
    const preferred = new Map([
        ['en', 'en-US'],
        ['es', 'es-ES'],
        ['ja-jp-mac', 'ja'],
        ['no', 'nb-NO'],
        ['pt', 'pt-BR'],
        ['sv', 'sv-SE'],
        ['zh-hant', 'zh-TW'], // Bug 1263193
        ['zh-hant-tw', 'zh-TW'], // Bug 1263193
        ['zh-hk', 'zh-TW'], // Bug 1338072
        ['zh-hant-hk', 'zh-TW'] // Bug 1338072
    ]);
    // Map of preferred fallback locales, if available.
    const fallbackLocales = new Map([
        ['es-AR', 'es-ES'],
        ['es-CL', 'es-ES'],
        ['es-MX', 'es-ES']
    ]);
    // Note: Do not use `forEach` here since you can't break the loop and
    // will return the least best language.
    for (const acceptLang of acceptLangs) {
        for (const availableLang of availableLangs) {
            // Next check available languages, exact matches first.
            if (this.isLangMatch(acceptLang, availableLang, true)) {
                return availableLang;
            }
        }
    }
    for (const acceptLang of acceptLangs) {
        for (const availableLang of availableLangs) {
            // Check preferred mappings first.
            if (preferred.has(acceptLang)) {
                return preferred.get(acceptLang);
            }
            // Next check available languages, exact matches first.
            if (this.isLangMatch(acceptLang, availableLang)) {
                return availableLang;
            }
            // Finally, check alternate fallback locales.
            if (fallbackLocales.has(acceptLang)) {
                return fallbackLocales.get(acceptLang);
            }
        }
    }
    return false;
};

translationBar.createBar = function (barElem, strings, link) {
    const fragment = `
        <p><a href="${link}">${strings.message}</a></p>
        <button class="translation-bar-close" type="button">${strings.close}</button>
    `;
    barElem.insertAdjacentHTML('beforeend', fragment);

    // wire up close button.
    barElem
        .querySelector('button')
        .addEventListener('click', translationBar.destroyBar, false);
};

translationBar.destroyBar = function () {
    document.getElementById('translation-bar').remove();
};

translationBar.init = function () {
    const barElem = document.getElementById('translation-bar');
    if (!barElem) {
        return false;
    }

    const pageLang = document.documentElement.lang;
    const availableLangs = Array.from(
        document.querySelectorAll('link[hreflang]'),
        (link) => this.normalize(link.hreflang)
    ).filter((e) => e !== 'x-DEFAULT');
    const acceptLangs = navigator.languages.map((lang) => this.normalize(lang));
    const bestLang = this.getBestMatch(acceptLangs, availableLangs);
    const bestLink = document.querySelector(
        `link[hreflang='${bestLang}']`
    ).href;

    let showBar = true;
    if (
        !bestLang ||
        this.isLangMatch(pageLang, availableLangs[0]) ||
        this.isLangMatch(pageLang, bestLang)
    ) {
        showBar = false;
    }

    if (showBar) {
        // Fetch the localized strings and show the Translation Bar
        fetch(`/${bestLang}/translation-bar.jsonp`)
            .then((resp) => {
                return resp.json();
            })
            .then((r) => {
                this.createBar(barElem, r, bestLink);
            })
            .catch(() => {
                // Ignore errors.
            });
    }
};

export default translationBar;
