/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var Utils = {};

    // Replace Google Play links on Android devices to let them open the marketplace app
    Utils.initMobileDownloadLinks = function() {
        if (site.platform === 'android') {
            $('a[href^="https://play.google.com/store/apps/"]').each(function() {
                $(this).attr('href', $(this).attr('href')
                    .replace('https://play.google.com/store/apps/', 'market://'));
            });
        }
    };

    // Bug 1264843: link to China build of Fx4A, for display within Fx China repack
    Utils.maybeSwitchToDistDownloadLinks = function(client) {
        if (!client.distribution || client.distribution === 'default') {
            return;
        }

        var distribution = client.distribution.toLowerCase();
        $('a[data-' + distribution + '-link]').each(function() {
            $(this).attr('href', $(this).data(distribution + 'Link'));
        });
        $('img[data-' + distribution + '-link]').each(function() {
            $(this).attr('src', $(this).data(distribution + 'Link'));
        });
    };

    Utils.switchPathLanguage = function(location, newLang) {
        // get path without locale
        var urlpath = location.pathname.slice(1).split('/').slice(1).join('/');
        return '/' + newLang + '/' + urlpath + location.search;
    };

    // client-side redirects (handy for testing)
    Utils.doRedirect = function(destination) {
        if (destination) {
            window.location.href = destination;
        }
    };

    // Create text translation function using #strings element.
    // TODO: Move to docs
    // In order to use it, you need a block string_data bit inside your template,
    // then, each key name needs to be preceded by data- as this uses data attributes
    // to work. After this, you can access all strings defined inside the
    // string_data block in JS using Mozilla.Utils.trans('keyofstring'); Thank @mkelly
    var _$strings = $('#strings');
    Utils.trans = function(stringId) {
        return _$strings.data(stringId);
    };

    window.Mozilla.Utils = Utils;

})();
