/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var pager = document.querySelector('.c-pager');
    var pagerTab = pager.querySelector('.c-pager-tab');
    var pagerTabButtons = pagerTab.querySelectorAll('.c-pager-tab-button');

    function hideActivePage() {
        for (var i = 0; i < pagerTabButtons.length; i++) {
            pagerTabButtons[i].setAttribute('aria-expanded', false);
            var pageId = pagerTabButtons[i].getAttribute('aria-controls');
            document.getElementById(pageId).setAttribute('aria-hidden', true);
        }
    }

    function showPage(target) {
        var pageId = target.getAttribute('aria-controls');
        target.setAttribute('aria-expanded', true);
        document.getElementById(pageId).setAttribute('aria-hidden', false);
    }

    function onPagerTabClick(e) {
        e.preventDefault();

        hideActivePage();
        showPage(e.target);
    }

    function destroyPager() {
        pagerTab.removeEventListener('click', onPagerTabClick, false);
        hideActivePage();
        pager.classList.remove('is-active');
    }

    function initPager() {
        hideActivePage();
        // show the first page as default.
        showPage(pagerTabButtons[0]);
        pagerTab.addEventListener('click', onPagerTabClick, false);
        pager.classList.add('is-active');
    }

    // Initialize the pager on small viewports only.
    var mqWide = matchMedia('(max-width: 767px)');

    if (mqWide.matches) {
        initPager();
    }

    mqWide.addListener(function(mq) {
        if (mq.matches) {
            initPager();
        } else {
            destroyPager();
        }
    });

})();
