/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


/**
 * Twitter sharing
 */
(function() {
    'use strict';

    function openTwitterSubwin(url) {
        var width = 550;
        var height = 420;
        var options = {
            'scrollbars': 'yes',
            'resizable': 'yes',
            'toolbar': 'no',
            'location': 'yes',
            'width': width,
            'height': height,
            'top': screen.height > height ? Math.round((screen.height / 2) - (height / 2)) : 0,
            'left': Math.round((screen.width / 2) - (width / 2))
        };

        window.open(url, 'twitter_share', window._SearchParams.objectToQueryString(options).replace(/&/g, ',')).focus();
    }

    function handleShareSubmit(e) {
        var input = document.querySelector('.c-tell-input');
        var url = document.querySelector('.c-tell').getAttribute('action');

        if (input && input.value) {
            var text = encodeURIComponent(input.value);

            url += '&text=' + text;
            // Track the event in GA
            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'form submit',
                'eLabel': 'share page: tweet'
            });

            // Open Twitter in a sub window
            openTwitterSubwin(url);
            e.preventDefault();
        }
    }

    function handleShareLinkClick(e) {
        var id = e.target.getAttribute('data-id');
        var href = e.target.href;

        if (id && href) {
            // Track the event in GA
            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'checklist',
                'eLabel': 'share page: ' + id
            });

            // Open Twitter in a sub window
            openTwitterSubwin(href);
            e.preventDefault();
        }
    }

    function onLoad() {
        // Set up twitter submit button handler
        var shareButton = document.querySelector('.js-tell-button');

        shareButton.addEventListener('click', handleShareSubmit, false);

        // Set up twitter link handler
        var shareLinks = document.querySelectorAll('.js-twitter-share');

        for (var i = 0; i < shareLinks.length; i++) {
            shareLinks[i].addEventListener('click', handleShareLinkClick, false);
        }
    }

    window.Mozilla.run(onLoad);
})();


/**
 * Download GIF
 */
(function() {
    'use strict';

    function watchDownloads() {
        var downloadLinks = document.querySelectorAll('.js-download-gif');

        for (var i = 0; i < downloadLinks.length; i++) {
            downloadLinks[i].addEventListener('click', function(e) {
                var id = e.target.getAttribute('data-id');
                // Track the event in GA
                window.dataLayer.push({
                    'event': 'in-page-interaction',
                    'eAction': 'checklist',
                    'eLabel': 'download gif: ' + id
                });
            }, false);
        }
    }

    window.Mozilla.run(watchDownloads);

})();


/**
 * Copy link to clipboard
 */
(function() {
    'use strict';

    function showNotification(target, successText, closeText) {
        var notification = document.querySelector('.mzp-c-notification-bar');
        var showTimeout;

        // if there's already a notification on screen, don't create another.
        if (notification) {
            return;
        }

        clearTimeout(showTimeout);

        Mzp.Notification.init(target, {
            title: successText,
            closeText: closeText,
            className: 'mzp-t-success',
            hasDismiss: true,
            isSticky: true,
            onNotificationClose: function() {
                clearTimeout(showTimeout);
            }
        });

        showTimeout = setTimeout(function() {
            var button = document.querySelector('.mzp-c-notification-bar-button');
            if (button) {
                button.click();
            }
        }, 5000);
    }

    function onCopyClick(e) {
        var item = e.target.closest('.c-item-unfck');
        var id = e.target.getAttribute('data-id');
        var successText = e.target.getAttribute('data-success');
        var closeText = e.target.getAttribute('data-close');
        var link;

        if (item) {
            link = item.querySelector('.c-item-gif');
        }

        if (link && link.src && id) {
            e.preventDefault();
            try {
                navigator.clipboard.writeText(link.src).then(function() {
                    // Show success notification
                    if (successText && closeText) {
                        showNotification(e.target, successText, closeText);
                    }

                    // Track the event in GA
                    window.dataLayer.push({
                        'event': 'in-page-interaction',
                        'eAction': 'checklist',
                        'eLabel': 'copy gif: ' + id
                    });
                });
            } catch (err) {
                // do nothing
            }
        }
    }

    function copyToClipboard() {
        var copyLinks = document.querySelectorAll('.js-copy-link');

        if (!navigator.clipboard && !Element.prototype.closest) {
            return;
        }

        for (var i = 0; i < copyLinks.length; i++) {
            // show icons if clipboard API is supported
            copyLinks[i].classList.add('is-supported');
            copyLinks[i].addEventListener('click', onCopyClick, false);
        }
    }

    window.Mozilla.run(copyToClipboard);

})();
