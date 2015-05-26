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

    // smooth scrolling for device type nav
    $('#device-nav a').on('click', function(e) {
        e.preventDefault();

        var target = $(this).attr('href');

        $('html, body').animate({
            scrollTop: $(target).offset().top - 100
        }, 400);
    });

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

            $purchaseDeviceButtons.prop('disabled', false);

            for (var device in Mozilla.FxOs.Devices) {
                if ($.inArray(COUNTRY_CODE, Mozilla.FxOs.Devices[device].countries) > -1) {
                    $('.device-thumbnail[href="#' + device + '"]').addClass('available');
                }
            }

            // show the provider applicable for the user country.
            $provider.show();
        } else {
            $purchaseDeviceButtons.prop('disabled', true);
        }
    };

    /*
    * Track telecom provider link clicks/page exits in Google Analytics
    */

    // setup GA event tracking on telecom provider exit links
    $('#provider-links a').attr({'data-element-action': 'overlay exit'});


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
        window.dataLayer.push({
                event: 'device-drop-down',
                countryCode: COUNTRY_CODE,
                nonInteraction: false
        });
    });

    // wire up purchase button
    $purchaseDeviceButtons.attr('data-track', 'true');
    $purchaseDeviceButtons.on('click', function(e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $('#get-device'), {
            allowScroll: false,
            title: '<img src="/media/img/firefox/os/logo/firefox-os-white.png" alt="mozilla" />'
        });
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

                window.dataLayer.push({
                    'event': 'device-interaction',
                    'deviceName': selectedDevice + ' Interactions',
                    'browserAction': 'Open Features',
                    deviceSelected: selectedDevice
                });
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
        window.dataLayer.push({
            event: 'device-interaction',
            deviceName: selectedDevice + ' Interactions',
            browserAction: 'Close Features',
            deviceSelected: null
        });
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
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: 'device-drop-down',
                    countryCode: COUNTRY_CODE,
                    nonInteraction: true
                });
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
    $('.standard-link').attr('data-track', 'true');

    // track mozilla pager tab clicks
    $('.pager-tabs').on('click', 'a', function() {
        window.dataLayer.push({
            event: 'device-interaction',
            deviceName: selectedDevice + ' Interactions',
            browserAction: $(this).data('label') + ' Tab'
        });
    });

    // initialize fx family nav
    Mozilla.FxFamilyNav.init({ primaryId: 'os', subId: 'devices' });
})(window.jQuery, window.Mozilla);
