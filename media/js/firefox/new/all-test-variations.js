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
            $li.addClass('win32');
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
        }

        if (newOsName) {
            $liA.text(newOsName);
        }

        return li;
    };

    var setupTest = function(version) {
        var $dlButton = $('#download-button-desktop-release');
        var $html = $('html');
        var $newLink;

        // make sure desktop download button exists, user is not on Android or iOS, and user is on a recognized platform
        if (!$html.hasClass('ios') && !$html.hasClass('android') && $dlButton.length && $dlButton.find('.unrecognized-download:visible').length === 0) {
            if (version === 1) {
                // snag the link from the footer and clone it
                $newLink = $('#fx-footer-links-desktop-all').clone();
            } else if (version === 2) {
                // pull the nojs links out of the modal's download button
                var $directLis = $('#fx-modal-download .nojs-download li').remove();
                // container to hold direct download links in the modal
                var $modalDirectDownloadList = $('#fx-modal-direct-downloads');
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

                // get current user platform display name
                var platformDisplayName = $dlButton.find('.download-list li:visible a').data('display-name');

                if (platformDisplayName) {
                    // put "for {user's os}" text underneath modal primary dl button
                    $('#fx-modal-user-platform').text('for ' + platformDisplayName);
                } else {
                    $('#fx-modal-user-platform').remove();
                }

                // conjure up a new link that will trigger the modal
                $newLink = $('<a href="#" id="fx-modal-link">Download Firefox for another platform</a>');

                $newLink.on('click', function(e) {
                    e.preventDefault();

                    // open up said modal
                    Mozilla.Modal.createModal(this, $('#fx-modal'));

                    dataLayer.push({
                        'event': 'alternate-version',
                        'link-name': 'Systems & Languages'
                    });
                });
            }

            // double check that we have a new link to add
            if ($newLink.length) {
                // apply common styles
                $newLink.css({
                    'display': 'inline-block',
                    'paddingTop': '10px'
                });

                // place the new link underneath the main download button
                $dlButton.append($newLink);
            }
        }
    };

    // initiate test if valid version supplied
    if (version === 1 || version === 2) {
        setupTest(version);
    }
})(window.jQuery, window.dataLayer = window.dataLayer || []);
