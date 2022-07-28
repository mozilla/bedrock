/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const isReduced =
    window.matchMedia(`(prefers-reduced-motion: reduce)`) === true ||
    window.matchMedia(`(prefers-reduced-motion: reduce)`).matches === true;

function getHeaderStyle() {
    const header = document.querySelector('.c-stories-article-header');
    const articleBody = document.querySelector('.c-stories-article-body');

    if (!isReduced) {
        const headerHeight = getComputedStyle(header).height;
        articleBody.style.top = headerHeight;
        articleBody.style.marginBottom = headerHeight;
    }
}

window.addEventListener('resize', getHeaderStyle);

getHeaderStyle();
