/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

{% set_lang_files "main" %}

Tabzilla.Infobar.items.update = function (ua, latestVersion, esrVersions) {
    'use strict';
    var updatebar = new Tabzilla.Infobar('updatebar', 'Update Bar');
    ua = ua || navigator.userAgent;
    var isFirefox = ((/\sFirefox\/\d+/).test(ua) &&
                     !(/like Firefox/i).test(ua) && // Camino
                     !(/SeaMonkey/i).test(ua));
    var isMobile = (/Mobile|Tablet|Fennec/i).test(ua);
    var userVersion = (isFirefox) ? parseInt(ua.match(/Firefox\/(\d+)/)[1], 10) : 0;
    latestVersion = latestVersion || parseInt('{{ latest_firefox_version }}', 10);
    esrVersions = esrVersions || {{ esr_firefox_versions }};

    if (updatebar.disabled || !isFirefox || isMobile ||
            userVersion >= latestVersion ||
            $.inArray(userVersion, esrVersions) > -1) {
        return false;
    }

    // Log the used Firefox version
    updatebar.onshow.trackLabel = updatebar.onaccept.trackLabel
                                = updatebar.oncancel.trackLabel
                                = userVersion;

    // If the user accepts, show the SUMO article
    updatebar.onaccept.callback = function () {
        location.href = 'https://support.mozilla.org/{{ LANG }}/kb/update-firefox-latest-version';
    };

    // The message and accept strings are the same as /firefox/new/
    updatebar.show({
        message: '{{ _("Looks like you’re using an older version of Firefox.")|js_escape }}',
        accept: '{{ _("Update to stay fast and safe.")|js_escape }}',
        cancel: '{{ _("Later")|js_escape }}'
    });

    return true;
};
