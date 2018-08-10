/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function removeParams() {
        window.history.replaceState({}, document.title, window.location.href.split('?')[0]);
    }

    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Check that cookies are supported.
    if (typeof Mozilla.Cookies === 'undefined' || !Mozilla.Cookies.enabled()) {
        return;
    }

    // Test criteria is Windows on desktop only.
    if (window.site.platform !== 'windows') {
        return;
    }

    // Exclude existing Firefox users.
    if (/\s(Firefox)/.test(navigator.userAgent)) {
        return;
    }

    // Check that history API is supported.
    if (!window.history && !window.history.replaceState) {
        return;
    }

    var source = getUrlParam('utm_source');
    var medium = getUrlParam('utm_medium');
    var campaign = getUrlParam('utm_campaign');

    var params = {
        utmSource: source ? source : 'www.mozilla.org',
        utmMedium: medium ? medium : 'download_button',
        utmCampaign: campaign ? campaign : 'firefox_page',
        utmContent: 'downloader_email_form_experiment_'
    };

    var stringA = 'v=a&utm_source=' + params.utmSource + '&utm_medium=' + params.utmMedium + '&utm_campaign=' + params.utmCampaign + '&utm_content=' + params.utmContent + 'va';
    var stringB = 'v=b&utm_source=' + params.utmSource + '&utm_medium=' + params.utmMedium + '&utm_campaign=' + params.utmCampaign + '&utm_content=' + params.utmContent + 'vb';
    var stringC = 'v=c&utm_source=' + params.utmSource + '&utm_medium=' + params.utmMedium + '&utm_campaign=' + params.utmCampaign + '&utm_content=' + params.utmContent + 'vc';

    var queries = {};

    queries[stringA] = 20;
    queries[stringB] = 20;
    queries[stringC] = 20;

    // remove existing params as we're amending our own and passing to Traffic Cop.
    removeParams();

    // Remove existing stub attribution data before Traffic Cop redirect.
    Mozilla.Cookies.removeItem('moz-stub-attribution-code', '/');
    Mozilla.Cookies.removeItem('moz-stub-attribution-sig', '/');

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-firefox-home-pre-download',
        variations: queries
    });

    cop.init();

})(window.Mozilla);
