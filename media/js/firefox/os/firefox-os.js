/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
  http://dev.maxmind.com/geoip/legacy/csv (used by geo.mozilla.org)
  http://en.wikipedia.org/wiki/ISO_3166-1 (full list of cc's)
*/
;(function($) {
    'use strict';

    window.pause_ga_tracking = false;

    var COUNTRY_CODE = '';

    /*
    * Set page specific content relating to geo for partner data etc
    */
    function setPartnerContent () {
        var links = '';
        var partners_available = [];

        if (Mozilla.FxOs.Countries.hasOwnProperty(COUNTRY_CODE)) {
            // make sure there are consumer-focused (non 'developer_only') partners
            // available in the current country
            $.each(Mozilla.FxOs.Countries[COUNTRY_CODE].partner, function(i, data) {
                if (!data.developer_only) {
                    partners_available.push(data);
                }
            });
        }

        // if there are partners available, update UI
        if (partners_available.length > 0) {
            // show get phone calls to action
            $('#primary-cta-phone').fadeIn();
            $('#primary-cta-signup').addClass('visibility', 'hidden');
            $('#secondary-cta-phone').css('display', 'inline-block');

            // if country has more than one provider, show the multi intro text
            if (partners_available.length > 1) {
                $('#provider-text-single').hide();
                $('#provider-text-multi').show();
            }

            // show partner specific links on modal etc
            $.each(partners_available, function(i, data) {
                //set data.name, data.url etc
                var index = i === partners_available.length - 1 ? 'last' : '';
                var filename = data.name.toLowerCase().replace(/\s+/g, '-');

                links += '<a class="' + filename + ' ' + index + '" href="' + data.url + '">' + data.name + '</a>';
            });

            // add country class as an extra style hook and inject the links
            $('#provider-links').addClass(COUNTRY_CODE).html(links);

            // setup GA event tracking on telecom provider exit links
            $('#provider-links a').on('click', trackProviderExit);

            // persistent pencil icon is distracting/obtrusive on small screens
            if ($(window).width() > 480) {
                $('#signup-toggle-icon').fadeIn();
            }
        } else {
            $('#primary-cta-signup').fadeIn();
            $('#primary-cta-phone').addClass('visibility', 'hidden');
            $('#secondary-cta-signup').css('display', 'inline-block');
        }
    }

    /*
    * Track telecom provider link clicks/page exits in Google Analytics
    */
    function trackProviderExit (e) {
        e.preventDefault();
        var $this = $(this);
        var href = this.href;

        var callback = function () {
            window.location = href;
        };

        trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'Get A Phone Exit', $this.text()], callback);
    }

    /*
    * Set newsletter default options based on cc
    */
    function setNewsletterDefaults () {
        var countrySelection = $('#id_country option[value='+ COUNTRY_CODE +']');

        // if cc is in the country option list, select it
        // remove the default selection first
        if (countrySelection.length !== 0) {
            $('#id_country option:selected').prop('selected', false);
            countrySelection.prop('selected', true);
        }

        // for ve and co set the default language to es
        // other countries auto select based on cc
        switch(COUNTRY_CODE) {
        case 've':
            $('#id_lang option[value="es"]').prop('selected', true);
            break;
        case 'co':
            $('#id_lang option[value="es"]').prop('selected', true);
            break;
        default:
            $('#id_lang option[value="' + COUNTRY_CODE + '"]').prop('selected', true);
        }
    }

    /*
    * Get country code via geo-ip lookup
    */
    function getGeoLocation () {
        try {
            COUNTRY_CODE = geoip_country_code().toLowerCase();
        } catch (e) {
            COUNTRY_CODE = "";
        }
    }

    window.trackGAEvent = function (eventsArray, callback) {
        if (!pause_ga_tracking) {
            var timer = null;
            var hasCallback = typeof(callback) == 'function';
            var gaCallback = function () {
                clearTimeout(timer);
                callback();
            };

            if (typeof(window._gaq) == 'object') {
                if (hasCallback) {
                    timer = setTimeout(gaCallback, 500);
                    window._gaq.push(eventsArray, gaCallback);
                } else {
                    window._gaq.push(eventsArray);
                }
            } else if (hasCallback) {
                callback();
            }
        }
    };

    $('#useful-links').on('click', 'a', function (e) {
        e.preventDefault();
        var that = this;
        var callback = function () {
            window.location = that.href;
        };

        //track GA event for useful links
        trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', this.href], callback);
    });

    $script('//geo.mozilla.org/country.js', function() {
        getGeoLocation();
        setNewsletterDefaults();
        setPartnerContent();
    });
})(jQuery);
