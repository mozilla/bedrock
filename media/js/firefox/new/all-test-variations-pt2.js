/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, dataLayer) {
    'use strict';

    // check page version for tests
    var version = Number($('#masthead').data('version'));

    // adds sort value & (optional) new text to direct download li
    var prepLi = function(li) {
        var $li = $(li);
        var $liA = $li.find('a');
        var newOsName;

        switch ($liA.text()) {
        case 'Windows':
            newOsName = 'Windows 32-bit';
            $li.attr('data-sort', 1);
            $li.addClass('win32'); // differentiate between normal & XP/Vista
            break;
        case 'Windows (XP/Vista)':
            newOsName = 'Windows 32-bit';
            $li.attr('data-sort', 2);
            $li.addClass('winsha1');
            break;
        case 'Linux':
            newOsName = 'Linux 32-bit';
            $li.attr('data-sort', 3);
            break;
        case 'Windows 64-bit':
            $li.attr('data-sort', 4);
            break;
        case 'Linux 64-bit':
            $li.attr('data-sort', 5);
            break;
        case 'OS X':
            $li.attr('data-sort', 6);
            break;
        // shouldn't be encountered, but just in case...
        default:
            $li.attr('data-sort', 99);
            break;
        }

        if (newOsName) {
            $liA.text(newOsName);
        }

        return li;
    };

    var setupTest = function(version) {
        var $dlButton = $('#download-button-desktop-release');
        var $html = $('html');

        // make sure desktop download button exists, user is not on Android or iOS, and user is on a recognized platform
        if (!$html.hasClass('ios') && !$html.hasClass('android') && $dlButton.length && $dlButton.find('.unrecognized-download:visible').length === 0) {
            // pull the nojs links out of the primary CTA
            var $directLis = $dlButton.find('.nojs-download li').remove();
            // container to hold direct download links
            var $modalDirectDownloadList = $('#test-direct-downloads');
            // os's to filter out of modal (as we have the app store specific buttons displayed already)
            var mobileOs = ['android', 'ios'];
            // array to hold re-sorted download li's
            var sortedLis = [];

            // remove button-y CSS
            $directLis.find('a').removeClass('button green');

            // massage the download links
            $directLis.each(function(i, li) {
                // do not include mobileOs's
                if ($.inArray($(li).find('a').data('download-os').toLowerCase(), mobileOs) === -1) {
                    sortedLis.push(prepLi(li));
                }
            });

            // sort the download links
            sortedLis.sort(function(a, b) {
                if (Number($(a).attr('data-sort')) < Number($(b).attr('data-sort'))) {
                    return 1;
                } else {
                    return -1;
                }
            });

            // add the download links to the DOM
            for (var i = sortedLis.length; i >= 0; i--) {
                $modalDirectDownloadList.append(sortedLis[i]);
            }

            // set up modal-opening link underneath primary CTA for version 1
            if (version === 1) {
                // get current user platform display name
                var platformDisplayName = $dlButton.find('.download-list li:visible a').data('display-name');

                if (platformDisplayName) {
                    // put "for {user's os}" text underneath modal primary dl button
                    $('#test-modal-user-platform').text('for ' + platformDisplayName);
                } else {
                    $('#test-modal-user-platform').remove();
                }

                // conjure up a new link that will trigger the modal
                var $newLink = $('<button id="test-modal-link">Download Firefox for another platform</button>');

                $newLink.on('click', function(e) {
                    e.preventDefault();

                    // open up said modal
                    Mozilla.Modal.createModal(this, $('#test-modal'));

                    dataLayer.push({
                        'event': 'alternate-version',
                        'link-name': 'Systems & Languages'
                    });
                });

                // place the new link underneath the main download button
                $('.main-content').append($newLink);
            }
        }
    };

    // initiate test if valid version supplied
    if (version === 1 || version === 2) {
        setupTest(version);
    }
})(window.jQuery, window.dataLayer = window.dataLayer || []);
