/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

;(function($) {
    'use strict';

    var COUNTRY_CODE = '';

    var isSmallViewport = $(window).width() < 760;
    var isTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints || isSmallViewport;

    var $purchaseDeviceButton = $('#purchase-device');
    var $locationSelect = $('#location');
    var $deviceThumbnails = $('.device-thumbnail');
    var $deviceDetailLists = $('.device-detail-list');
    var $deviceDetails = $('.device-detail');

    var $pagerPages = $('.pager-page');

    // create namespace
    if (typeof Mozilla.FxOs == 'undefined') {
        Mozilla.FxOs = {};
    }

    // select available devices & set modal partner content based on chosen/detected location
    var selectDevicesAndSetPartnerContent = function() {
        var links = '';

        // de-select all devices
        $deviceThumbnails.removeClass('available');

        if (COUNTRY_CODE !== '' && Mozilla.FxOs.Countries.hasOwnProperty(COUNTRY_CODE)) {
            // make sure country is selected in select box
            $locationSelect.val(COUNTRY_CODE);

            $purchaseDeviceButton.fadeIn('fast');

            for (var device in Mozilla.FxOs.Devices) {
                if ($.inArray(COUNTRY_CODE, Mozilla.FxOs.Devices[device].countries) > -1) {
                    $('.device-thumbnail[data-device="' + device + '"]').addClass('available');
                }
            }

            // set up partner modal contents

            // if country has more than one provider, show the multi intro text
            if (Mozilla.FxOs.Countries[COUNTRY_CODE].partner.length > 1) {
                $('#provider-text-single').hide();
                $('#provider-text-multi').show();
            }

            // show partner specific links on modal etc
            $.each(Mozilla.FxOs.Countries[COUNTRY_CODE].partner, function(i, data) {
                //set data.name, data.url etc
                var index = i === 1 ? 'last' : '';
                links += '<a class="' + data.name.toLowerCase() + ' ' + index + '" href="' + data.url + '">' + data.name + '</a>';
            });

            // add country class as an extra style hook and inject the links
            $('#provider-links').addClass(COUNTRY_CODE).html(links);

            // setup GA event tracking on telecom provider exit links
            $('#provider-links a').on('click', trackProviderExit);
        } else {
            $purchaseDeviceButton.fadeOut('fast');
        }
    };

    /*
    * Track telecom provider link clicks/page exits in Google Analytics
    */
    var trackProviderExit = function(e) {
        e.preventDefault();
        var $this = $(this);
        var href = this.href;

        var callback = function () {
            window.location = href;
        };

        trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'Get A Phone Exit', $this.text()], callback);
    };

    /*
    * Disable/enable mozilla-pagers.js
    */
    var togglePagers = function(enable) {
        if (enable) {
            $pagerPages.each(function(i, page) {
                var $page = $(page);

                $page.attr('style', $page.data('oldstyle')).data('oldstyle', '');
            });
        } else {
            $pagerPages.each(function(i, page) {
                var $page = $(page);
                $page.data('oldstyle', $page.attr('style'));

                $page.attr('style', '');
            });
        }
    };

    // tablets are coming!
    Mozilla.FxOs.Devices = {
        'alcatel_onetouchfire': {
            'type': 'smartphone',
            'display': 'Alcatel One Touch Fire',
            'countries': ['br', 'co', 'de', 'gr', 'hu', 'me', 'mx', 'pl', 'rs', 'uy', 've']
        },
        'zte_open': {
            'type': 'smartphone',
            'display': 'ZTE Open',
            'countries': ['co', 'es', 'mx', 'pe', 'uy', 've']
        },
        'lg_fireweb': {
            'type': 'smartphone',
            'display': 'LG Fireweb',
            'countries': ['br']
        }
    };

    // wire up location select
    $locationSelect.on('change', function(e) {
        COUNTRY_CODE = $locationSelect.val();
        selectDevicesAndSetPartnerContent();
    });

    // wire up purchase button
    $purchaseDeviceButton.on('click', function(e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $('#get-device'), {
            allowScroll: false,
            title: '<img src="/media/img/firefox/os/logo/firefox-os-white.png" alt="mozilla" />'
        });
    });

    // wire up thumbnail select
    $('.device-thumbnails').on('click', '.device-thumbnail', function(e) {
        e.preventDefault();

        var $this = $(this);
        var $targetDevice = $('#' + $this.data('device'));

        if (!$targetDevice.is(':visible')) {
            $deviceThumbnails.removeClass('selected');
            $this.addClass('selected');

            $deviceDetailLists.slideUp('normal', function() {
                setTimeout(function() {
                    $deviceDetails.hide();
                    $targetDevice.show();

                    $targetDevice.parents('.device-detail-list:first').slideDown('fast');
                }, 200);
            });
        }
    });

    // wire up device detail close
    $('.device-detail-close').on('click', function(e) {
        e.preventDefault();

        $deviceThumbnails.removeClass('selected');

        $(this).parents('.device-detail-list:first').slideUp('normal', function() {
            $deviceDetails.hide();
        });
    });

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

    // only if coming from /firefox/os/, detect country
    if (/firefox\/os\/$/.test(document.referrer)) {
        $.getScript('//geo.mozilla.org/country.js', function() {
            try {
                COUNTRY_CODE = geoip_country_code().toLowerCase();
            } catch (e) {
                COUNTRY_CODE = "";
            }

            selectDevicesAndSetPartnerContent();
        });
    }

    // hide/disable pagers in mobile view
    var queryIsMobile = matchMedia('(max-width: 480px)');

    setTimeout(function() {
        if (queryIsMobile.matches) {
            togglePagers(false);
        }
    }, 500);

    queryIsMobile.addListener(function(mq) {
        if (mq.matches) {
            togglePagers(false);
        } else {
            togglePagers(true);
        }
    });
})(window.jQuery);
