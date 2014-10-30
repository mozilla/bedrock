/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    $('a.video-play').attr('role', 'button').click(function(e) {
        e.preventDefault();

        var $this = $(this);
        var $video = $this.siblings('.video');
        var $iframe = $('<iframe width="560" height="315" src="" frameborder="0" allowfullscreen></iframe>');

        // defer loading of iframe content until the user clicks to activate the modal
        // as loading the src triggers UITour panel content to close.
        $iframe.attr('src', $video.data('src'));
        $this.siblings('.video').html($iframe);

        Mozilla.Modal.createModal(this, $this.nextAll('.video'), {
            // grab the nearby h4 tag as the modal window title
            title: $this.siblings('h4,h2').text(),
            onCreate: function() {
                $('#modal').fitVids();
            }
        });
    });

})(window.jQuery, window.Mozilla);

;(function($, Mozilla) {
    'use strict';

    var availableTargets = [];
    var TARGET_1 = 'home'; // TODO replace with `Dev Tools` target once available to UITour
    var TARGET_2 = 'bookmarks'; // TODO replace with `WebIDE` target once available to UITour
    var TARGET_3 = 'appMenu';
    var TARGET_4 = 'accountStatus';
    var current = TARGET_1;
    var tourSkipped = false;
    var highlightTimeout;

    function showDevToolsDoorhanger() {
        var icon = '';
        var buttons = [];
        var options = {};
        var nextTarget = TARGET_2;

        Mozilla.UITour.getConfiguration('availableTargets', function(config) {

            if (!config.targets) {
                return;
            }

            var nextAvailable = $.inArray(nextTarget, config.targets) !== -1;
            var nextLabel = nextAvailable ? 'nextWebide' : 'nextSync';
            var nextStep = nextAvailable ? showWebIDEDoorhanger : showSyncDoorhanger;

            buttons = [
                {
                    label: window.trans('doorhangerClose'),
                    style: 'link',
                    callback: skipTour
                },
                {
                    label: window.trans(nextLabel),
                    style: 'primary',
                    callback: nextStep
                }
            ];

            options = {
                closeButtonCallback: skipTour
            };

            showHighlight(TARGET_1);

            Mozilla.UITour.showInfo(
                TARGET_1,
                window.trans('devtoolsTitle'),
                window.trans('devtoolsText'),
                icon,
                buttons,
                options
            );

            current = TARGET_1;
        });
    }

    function showWebIDEDoorhanger() {
        var icon = '';
        var buttons = [];
        var options = {};

        Mozilla.UITour.getConfiguration('availableTargets', function(config) {

            if (!config.targets || $.inArray(TARGET_2, config.targets) === -1) {
                return;
            }

            buttons = [
                {
                    label: window.trans('doorhangerClose'),
                    style: 'link',
                    callback: skipTour
                },
                {
                    label: window.trans('nextSync'),
                    style: 'primary',
                    callback: showSyncDoorhanger
                }
            ];

            options = {
                closeButtonCallback: skipTour
            };

            Mozilla.UITour.hideInfo();
            showHighlight(TARGET_2);

            Mozilla.UITour.showInfo(
                TARGET_2,
                window.trans('webideTitle'),
                window.trans('webideText'),
                icon,
                buttons,
                options
            );

            current = TARGET_2;
        });
    }

    function showSyncDoorhanger() {
        var icon = '';
        var buttons = [
            {
                label: window.trans('doorhangerNothanks'),
                style: 'link',
                callback: skipTour
            },
            {
                label: window.trans('doorhangerSync'),
                style: 'primary',
                callback: showSyncInMenu
            }
        ];
        var options = {
            closeButtonCallback: skipTour
        };

        Mozilla.UITour.hideInfo();
        showHighlight(TARGET_3);

        Mozilla.UITour.showInfo(
            TARGET_3,
            window.trans('syncTitle'),
            window.trans('syncText'),
            icon,
            buttons,
            options
        );

        current = TARGET_3;
    }

    function showSyncInMenu() {

        showHighlight(TARGET_4);

        // hide app menu when user clicks anywhere on the page
        $(document.body).one('click', function () {
            Mozilla.UITour.hideHighlight();
        });

        current = TARGET_4;
    }

    function hideAnnotation() {
        Mozilla.UITour.hideMenu('appMenu');
        Mozilla.UITour.hideHighlight();
    }

    function skipTour() {
        tourSkipped = true;
        hideAnnotation();
    }

    function showHighlight(target) {
        Mozilla.UITour.showHighlight(target, 'wobble');
        Mozilla.UITour.showHighlight(target, 'wobble');
    }

    function getAllAvailableTargets(callback) {
        Mozilla.UITour.getConfiguration('availableTargets', function(config) {
            var targets = [];
            if (config.targets) {
                targets = config.targets;
            }
            if (typeof callback === 'function') {
                callback(targets);
            }
        });
    }

    function showTourStep() {
        Mozilla.UITour.getConfiguration('availableTargets', function(config) {
            if (config.targets) {

                var showStep1 = $.inArray(TARGET_1, config.targets) !== -1;
                var showStep2 = $.inArray(TARGET_2, config.targets) !== -1;

                if (current === TARGET_1) {
                    if (showStep1) {
                        showDevToolsDoorhanger();
                    } else if (showStep2) {
                        showWebIDEDoorhanger();
                    } else {
                        showSyncDoorhanger();
                    }
                } else if (current === TARGET_2) {
                    if (showStep2) {
                        showWebIDEDoorhanger();
                    } else {
                        showSyncDoorhanger();
                    }
                } else if (current === TARGET_3) {
                    showSyncDoorhanger();
                } else if (current === TARGET_4) {
                    showSyncInMenu();
                }
            }
        });
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            Mozilla.UITour.hideInfo();
            hideAnnotation();
            clearTimeout(highlightTimeout);
        } else if (!tourSkipped) {
            highlightTimeout = setTimeout(function () {
                showTourStep();
            }, 900);
        }
    }

    //Only run the tour if user is on Firefox 35 for desktop.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 35) {

        $(document).on('visibilitychange', handleVisibilityChange);

        showTourStep();
    }

})(window.jQuery, window.Mozilla);


