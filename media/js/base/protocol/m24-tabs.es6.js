/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const M24Tabs = {};

const _options = {
    onTabChange: null
};

/**
 * Get all tab links belonging to the same tablist.
 * @param {Object} tab - a `.m24-c-tabs-link` element.
 * @returns {Array}
 */
M24Tabs.getGroupTabs = (tab) => {
    const tablist = tab.closest('.m24-c-tabs-list');

    return tablist
        ? Array.from(tablist.querySelectorAll('.m24-c-tabs-link'))
        : [tab];
};

/**
 * Read the id of the panel referenced by location.hash, if it matches
 * one of the given tabs.
 * @param {Array} tabs - array of tab link elements.
 * @returns {Object} the matching tab link, or the first tab.
 */
M24Tabs.getInitialTab = (tabs) => {
    const hash = window.location.hash.replace('#', '');

    if (hash) {
        const match = tabs.find(
            (tab) => tab.getAttribute('aria-controls') === hash
        );

        if (match) {
            return match;
        }
    }

    return tabs[0];
};

/**
 * Replace the current history entry with one that points at the given
 * panel id, without adding a new entry (so back/forward don't step
 * through individual tab clicks).
 * @param {String} id - id of the panel now selected.
 */
M24Tabs.setHash = (id) => {
    if (window.history && window.history.replaceState) {
        window.history.replaceState(
            null,
            '',
            window.location.pathname + window.location.search + '#' + id
        );
    }
};

/**
 * Select a tab: update ARIA/roving tabindex across its group, and show
 * its panel while hiding the others.
 * @param {Object} tab - the tab link element to select.
 * @param {Object} options - configurable options.
 *   - setFocus {Boolean} - move focus to the tab. Defaults to true.
 *   - announce {Boolean} - update the URL hash, log a GA4 event, and call
 *     onTabChange. Defaults to true. Pass false for the automatic initial
 *     selection on page load.
 */
M24Tabs.select = (tab, options) => {
    options = options || {};
    const setFocus = options.setFocus !== false;
    const announce = options.announce !== false;

    const tabs = M24Tabs.getGroupTabs(tab);

    tabs.forEach((currentTab) => {
        const panel = document.getElementById(
            currentTab.getAttribute('aria-controls')
        );
        const selected = currentTab === tab;

        currentTab.setAttribute('aria-selected', selected ? 'true' : 'false');
        currentTab.setAttribute('tabindex', selected ? '0' : '-1');

        if (panel) {
            panel.hidden = !selected;
        }
    });

    if (setFocus) {
        tab.focus();
    }

    if (announce) {
        M24Tabs.setHash(tab.getAttribute('aria-controls'));

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: 'widget_action',
            type: 'tabs',
            action: 'change',
            name: tab.textContent.trim()
        });

        if (typeof _options.onTabChange === 'function') {
            _options.onTabChange(tab);
        }
    }
};

/**
 * Click handler for a tab link.
 * @param {Event} e - click event.
 */
M24Tabs.onTabClick = (e) => {
    e.preventDefault();
    M24Tabs.select(e.currentTarget);
};

/**
 * Keyboard support per the ARIA APG tabs pattern: Left/Right move (and
 * wrap) between tabs, Home/End jump to the first/last tab. Up/Down Arrow
 * are intentionally left alone here — this is a horizontal tab list, so
 * those keys should still scroll the page rather than being intercepted.
 * This is a roving tabindex, not a focus trap — Tab still moves focus in
 * and out of the widget normally.
 * @param {Event} e - keydown event.
 */
M24Tabs.onTabKeyDown = (e) => {
    const tabs = M24Tabs.getGroupTabs(e.currentTarget);
    const currentIndex = tabs.indexOf(e.currentTarget);
    let newIndex;

    switch (e.key) {
        case 'ArrowLeft':
            newIndex = currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;
            break;

        case 'ArrowRight':
            newIndex = currentIndex === tabs.length - 1 ? 0 : currentIndex + 1;
            break;

        case 'Home':
            newIndex = 0;
            break;

        case 'End':
            newIndex = tabs.length - 1;
            break;

        default:
            return;
    }

    e.preventDefault();
    e.stopPropagation();
    M24Tabs.select(tabs[newIndex]);
};

/**
 * Bind click/keydown handlers for a set of tab links.
 * @param {Array} tabs - array of tab link elements.
 */
M24Tabs.bindEvents = (tabs) => {
    tabs.forEach((tab) => {
        tab.addEventListener('click', M24Tabs.onTabClick, false);
        tab.addEventListener('keydown', M24Tabs.onTabKeyDown, false);
    });
};

/**
 * Remove click/keydown handlers for a set of tab links.
 * @param {Array} tabs - array of tab link elements.
 */
M24Tabs.unbindEvents = (tabs) => {
    tabs.forEach((tab) => {
        tab.removeEventListener('click', M24Tabs.onTabClick, false);
        tab.removeEventListener('keydown', M24Tabs.onTabKeyDown, false);
    });
};

/**
 * A panel needs its own place in the tab order only if nothing inside it
 * can already be reached by pressing Tab.
 * @param {Object} panel - a `.m24-c-tabs-panel` element.
 * @returns {Boolean}
 */
M24Tabs.hasFocusableContent = (panel) => {
    return !!panel.querySelector(
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
};

/**
 * Set the ARIA roles/relationships on a tablist that, with JS disabled,
 * is just a heading-and-jump-link list next to fully visible panels.
 * @param {Object} tablist - the `.m24-c-tabs-list` element.
 * @returns {Array} the tab link elements found inside it.
 */
M24Tabs.setAria = (tablist) => {
    tablist.setAttribute('role', 'tablist');

    // The tablist's own list markup no longer needs list semantics.
    Array.from(tablist.querySelectorAll('.m24-c-tabs-item')).forEach((item) => {
        item.setAttribute('role', 'presentation');
    });

    const tabs = Array.from(tablist.querySelectorAll('.m24-c-tabs-link'));

    tabs.forEach((tab) => {
        const panelId = tab.getAttribute('href').replace('#', '');
        const panel = document.getElementById(panelId);

        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-controls', panelId);
        tab.setAttribute('aria-selected', 'false');
        tab.setAttribute('tabindex', '-1');

        if (panel) {
            panel.setAttribute('role', 'tabpanel');
            panel.setAttribute('aria-labelledby', tab.id);

            // Only join the tab order if Tab wouldn't otherwise land
            // anywhere inside the panel.
            if (!M24Tabs.hasFocusableContent(panel)) {
                panel.setAttribute('tabindex', '0');
            }
        }
    });

    return tabs;
};

/**
 * Basic feature detect for tabs JS support.
 * @returns {Boolean}
 */
M24Tabs.isSupported = () => {
    if (typeof window.MzpSupports !== 'undefined') {
        return window.MzpSupports.matchMedia && window.MzpSupports.classList;
    } else {
        return false;
    }
};

/**
 * Enhances a tabs container for 1st class JS support.
 * @param {Object} container - the `.m24-c-tabs` element.
 */
M24Tabs.enhanceJS = (container) => {
    container.classList.remove('m24-c-tabs-is-basic');
    container.classList.add('m24-c-tabs-is-enhanced');
};

/**
 * Initialize a single tabs container.
 * @param {Object} container - the `.m24-c-tabs` element.
 */
M24Tabs.initItem = (container) => {
    const tablist = container.querySelector('.m24-c-tabs-list');

    // if it's already been initialized, don't do it again
    if (!tablist || tablist.getAttribute('role') === 'tablist') {
        return;
    }

    const tabs = M24Tabs.setAria(tablist);

    if (!tabs.length) {
        return;
    }

    M24Tabs.bindEvents(tabs);
    M24Tabs.enhanceJS(container);
    M24Tabs.select(M24Tabs.getInitialTab(tabs), {
        setFocus: false,
        announce: false
    });
};

/**
 * Tear a single tabs container back down to its basic (no-JS) state.
 * @param {Object} container - the `.m24-c-tabs` element.
 */
M24Tabs.destroyItem = (container) => {
    const tablist = container.querySelector('.m24-c-tabs-list');

    if (!tablist || tablist.getAttribute('role') !== 'tablist') {
        return;
    }

    const tabs = Array.from(tablist.querySelectorAll('.m24-c-tabs-link'));

    M24Tabs.unbindEvents(tabs);
    tablist.removeAttribute('role');
    container.classList.remove('m24-c-tabs-is-enhanced');
    container.classList.add('m24-c-tabs-is-basic');

    Array.from(tablist.querySelectorAll('.m24-c-tabs-item')).forEach((item) => {
        item.removeAttribute('role');
    });

    tabs.forEach((tab) => {
        const panel = document.getElementById(
            tab.getAttribute('aria-controls')
        );

        tab.removeAttribute('role');
        tab.removeAttribute('aria-selected');
        tab.removeAttribute('tabindex');
        tab.removeAttribute('aria-controls');

        if (panel) {
            panel.hidden = false;
            panel.removeAttribute('role');
            panel.removeAttribute('tabindex');
            panel.removeAttribute('aria-labelledby');
        }
    });
};

/**
 * Initialize all tabs containers matching `selector`.
 * @param {String} selector - CSS selector matching `.m24-c-tabs` containers.
 * @param {Object} options - configurable options.
 *   - onTabChange: called with the newly selected tab link element.
 */
M24Tabs.init = (selector, options) => {
    if (!M24Tabs.isSupported()) {
        return;
    }

    if (typeof selector !== 'string') {
        selector = '.m24-c-tabs';
    }

    if (typeof options === 'object') {
        for (const i in options) {
            if (Object.prototype.hasOwnProperty.call(options, i)) {
                _options[i] = options[i];
            }
        }
    }

    document
        .querySelectorAll(selector)
        .forEach((container) => M24Tabs.initItem(container));
};

/**
 * Destroy all tabs containers matching `selector`.
 * @param {String} selector - CSS selector matching `.m24-c-tabs` containers.
 */
M24Tabs.destroy = (selector) => {
    if (typeof selector !== 'string') {
        selector = '.m24-c-tabs';
    }

    document
        .querySelectorAll(selector)
        .forEach((container) => M24Tabs.destroyItem(container));
};

export default M24Tabs;
