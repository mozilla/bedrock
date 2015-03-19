/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';
    var versionBox = document.getElementById('version-box');
    var downloadBox = document.getElementById('download-link');
    var lang = document.getElementById('lightning').getAttribute('data-lang');

    $.ajax({
        type: 'GET',
        dataType: 'xml',
        url: 'https://services.addons.mozilla.org/' + lang + '/thunderbird/api/1.5/addon/lightning',
        success: function(xml){
            versionBox.textContent = 'Lightning ' + $(xml).find('version').text();
            downloadBox.className = downloadBox.className.replace('loading', '');

            var downloadLink = downloadBox.getAttribute('href');
            if (window.site.platform === 'windows') {
                downloadLink = $(xml).find("install[os='WINNT']").text();
            } else if (window.site.platform === 'osx') {
                downloadLink = $(xml).find("install[os='Darwin']").text();
            } else if (window.site.platform === 'linux') {
                downloadLink = $(xml).find("install[os='Linux']").text();
            }
            downloadBox.setAttribute('href', downloadLink);
        }
    });

});
