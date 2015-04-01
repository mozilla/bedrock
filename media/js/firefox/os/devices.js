/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

;(function($, Mozilla) {
    'use strict';

    var COUNTRY_CODE = '';
    var selectedDevice;

    // Will be used when color pickers are activated
    //var isSmallViewport = $(window).width() < 760;
    //var isTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints || isSmallViewport;

    var $purchaseDeviceButtons = $('.purchase-button');
    var $locationSelect = $('#location');
    var $deviceThumbnails = $('.device-thumbnail');
    var $deviceDetailLists = $('.device-detail-list');
    var $deviceDetails = $('.device-detail');
    var $providerTextSingle = $('#provider-text-single');
    var $providerTextMulti = $('#provider-text-multi');

    var $providerLinks = $('#provider-links');

    // create namespace
    if (typeof Mozilla.FxOs === 'undefined') {
        Mozilla.FxOs = {};
    }

    // select available devices & set modal partner content based on chosen/detected location
    var selectDevicesAndSetPartnerContent = function() {
        var $provider = $providerLinks.find('.provider[data-country="' + COUNTRY_CODE + '"]');

        // de-select all devices
        $deviceThumbnails.removeClass('available');

        if (COUNTRY_CODE !== '' && $provider.length > 0) {

            // make sure all provider links are hidden
            $providerLinks.find('.provider').hide();

            if ($provider.find('li').length > 1) {
                $providerTextSingle.hide();
                $providerTextMulti.show();
            } else {
                $providerTextSingle.show();
                $providerTextMulti.hide();
            }

            // make sure no option is selected
            $locationSelect.find('option:selected').prop('selected', false);

            // select the current COUNTRY_CODE
            $locationSelect.find('option[value="' + COUNTRY_CODE + '"]').prop('selected', 'selected');

            $purchaseDeviceButtons.addClass('visible');

            for (var device in Mozilla.FxOs.Devices) {
                if ($.inArray(COUNTRY_CODE, Mozilla.FxOs.Devices[device].countries) > -1) {
                    $('.device-thumbnail[href="#' + device + '"]').addClass('available');
                }
            }

            // show the provider applicable for the user country.
            $provider.show();
        } else {
            $purchaseDeviceButtons.removeClass('visible');
        }
    };

    /*
    * Track telecom provider link clicks/page exits in Google Analytics
    */
    var trackProviderExit = function(e) {
        var $this = $(this);
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);

        if (newTab) {
            gaTrack(['_trackEvent', '/os/devices/ Interactions', 'Get a Phone Overlay Exits', $this.text()]);
        } else {
            e.preventDefault();

            var href = this.href;
            var callback = (newTab) ? null : function() {
                window.location = href;
            };

            gaTrack(['_trackEvent', '/os/devices/ Interactions', 'Get a Phone Overlay Exits', $this.text()], callback);
        }
    };

    // setup GA event tracking on telecom provider exit links
    $providerLinks.on('click', 'a', trackProviderExit);

    /*
    * Disable/enable mozilla-pagers.js
    */
    var togglePagers = function(enable) {
        if (enable) {
            Mozilla.Pager.createPagers();
        } else {
            Mozilla.Pager.destroyPagers();
        }
    };

    // wire up location select
    $locationSelect.on('change', function() {
        COUNTRY_CODE = $locationSelect.val();
        selectDevicesAndSetPartnerContent();

        gaTrack(['_trackEvent', '/os/devices/ Interactions', 'drop-down menu', COUNTRY_CODE, 0, false]);
    });

    // wire up purchase button
    $purchaseDeviceButtons.on('click', function(e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $('#get-device'), {
            allowScroll: false,
            title: '<img src="/media/img/firefox/os/logo/firefox-os-white.png" alt="mozilla" />'
        });

        gaTrack(['_trackEvent', '/os/devices/ Interactions', 'Get a Phone CTA Clicks', (selectedDevice || 'none selected')]);
    });

    // wire up thumbnail select
    $('.device-thumbnails').on('click', '.device-thumbnail', function(e) {
        var $this = $(this);

        // make sure device has specs (coming soon devices may not have specs)
        var hasSpecs = $this.data('specs') !== false;

        if (hasSpecs) {
            selectedDevice = $this.attr('href').replace(/#/gi, '');
            var $targetDevice = $('#' + selectedDevice);

            if (!$targetDevice.is(':visible')) {
                $deviceThumbnails.removeClass('selected');
                $this.addClass('selected');

                $deviceDetailLists.slideUp('fast', function() {
                    setTimeout(function() {
                        $deviceDetails.hide();
                        $targetDevice.show();

                        $targetDevice.parents('.device-detail-list:first').slideDown('fast');
                    }, 200);
                });

                gaTrack(['_trackEvent', '/os/devices/ Interactions', selectedDevice + ' Interactions', 'Open Features']);
            }
        } else {
            e.preventDefault();
        }
    });

    // wire up device detail close
    $('.device-detail-close').on('click', function(e) {
        e.preventDefault();

        $deviceThumbnails.removeClass('selected');

        $(this).parents('.device-detail-list:first').slideUp('fast', function() {
            $deviceDetails.hide();
        });

        gaTrack(['_trackEvent', '/os/devices/ Interactions', selectedDevice + ' Interactions', 'Close Features']);

        selectedDevice = null;
    });

    /*
    Color pickers disabled until image assets are available
    // enable color pickers
    $('.color-picker').on('click', 'a', function(e) {
        e.preventDefault();

        var $this = $(this);

        var $phoneImage = $this.parents('.device-details').find('.image img');

        $phoneImage.attr('src', $this.data('image'));
    });

    // enable tooltips on color pickers for non-touch screens
    if (!isTouch) {
        $('.color-picker a').tipsy();
    }
    */

    // only if coming from /firefox/os/, detect country
    if (/firefox\/os\/$/.test(document.referrer)) {
        $.getScript('//geo.mozilla.org/country.js', function() {
            var $provider;

            try {
                COUNTRY_CODE = geoip_country_code().toLowerCase();
            } catch (e) {
                COUNTRY_CODE = '';
            }

            $provider = $providerLinks.find('.provider[data-country="' + COUNTRY_CODE + '"]');

            if (COUNTRY_CODE !== '' && $provider.length > 0) {
                gaTrack(['_trackEvent', '/os/devices/ Interactions', 'drop-down menu', COUNTRY_CODE, 0, true]);
                selectDevicesAndSetPartnerContent();
            }
        });
    }

    // hide/disable pagers in mobile view
    if (typeof matchMedia !== 'undefined') {
        var queryIsMobile = matchMedia('(max-width: 480px)');

        setTimeout(function() {
            if (!queryIsMobile.matches) {
                togglePagers(true);
            }
        }, 500);

        queryIsMobile.addListener(function(mq) {
            if (mq.matches) {
                togglePagers(false);
            } else {
                togglePagers(true);
            }
        });
    }

    // display specific device if in URL hash
    if (window.location.hash !== '') {
        setTimeout(function() {
            var $deviceThumb = $('.device-thumbnail[href="' + window.location.hash + '"]');

            if ($deviceThumb.length) {
                $deviceThumb.trigger('click');
                $('html, body').animate({
                    scrollTop: $deviceThumb.offset().top
                }, 600);
            }
        }, 500);
    }

    // GA specific interactions

    // track all 'regular' links (non-CTA, non-device)
    $('.standard-link').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);

        var href = this.href;

        if (newTab) {
            gaTrack(['_trackEvent', '/os/devices/ Interactions', 'link clicks', href]);
        } else {
            e.preventDefault();

            var callback = function() {
                window.location = href;
            };

            gaTrack(['_trackEvent', '/os/devices/ Interactions', 'link clicks', href], callback);
        }
    });

    // track mozilla pager tab clicks
    $('.pager-tabs').on('click', 'a', function() {
        gaTrack(['_trackEvent', '/os/devices/ Interactions', selectedDevice + ' Interactions', $(this).data('label') + ' Tab']);
    });

    // initialize fx family nav
    Mozilla.FxFamilyNav.init({ primaryId: 'os', subId: 'devices' });
})(window.jQuery, window.Mozilla);
