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

    var $document = $(document);
    var $window = $(window);
    var $langContainer = $('#lang-panel-container');
    var $langButtonOpen = $('#open-lang-panel');
    var $langPanel = $('#lang-panel');
    var langTimer;

    var sessionLangPrefName = 'firefox.os.india-lang';

    /*
    * Set page specific content relating to geo for partner data etc
    */
    function setPartnerContent () {
        var $provider = $('#provider-links').find('.provider[data-country="' + COUNTRY_CODE + '"]');

        // show language content selector if user is in india visiting the en-US/en-GB page
        if (COUNTRY_CODE.toLowerCase() === 'in' && $('html').is('[lang|="en"]')) {
            var suppressLangContentSelector = false;

            // if user has already selected en-IN, don't bug them a second time
            try {
                if (sessionStorage.getItem(sessionLangPrefName) === 'en-IN') {
                    suppressLangContentSelector = true;
                    setEnInContent();
                }
            } catch (ex) {}

            initLangContentSelector(suppressLangContentSelector);
        }

        // if there are partners available, update UI
        if (COUNTRY_CODE !== '' && $provider.length > 0) {
            // show get phone calls to action
            $('#primary-cta-phone').fadeIn();
            $('#primary-cta-signup').addClass('visibility', 'hidden');
            $('#secondary-cta-phone').css('display', 'inline-block');

            // if country has more than one provider, show the multi intro text
            if ($provider.find('li').length > 1) {
                $('#provider-text-single').hide();
                $('#provider-text-multi').show();
            }

            // show the provider applicable for the user country.
            $provider.show();

            // setup GA event tracking on telecom provider exit links
            $('#provider-links a').each(function() {
                $(this).attr({
                    'data-element-location': $(this).text(), 
                    'data-interaction': 'Get A Phone Exit'
                });
            });

            // persistent pencil icon is distracting/obtrusive on small screens
            if ($window.width() > 480) {
                $('#signup-toggle-icon').fadeIn();
            }
        } else {
            $('#primary-cta-signup').fadeIn();
            $('#primary-cta-phone').addClass('visibility', 'hidden');
            $('#secondary-cta-signup').css('display', 'inline-block');
        }
    }

    /*
     * Init language content selector
     * Only applicable to en-US visitors in India
     */
    function initLangContentSelector (suppressSelector) {
        //show the panel on init
        $langContainer.fadeIn(function () {
            if (!suppressSelector) {
                $langButtonOpen.focus();
                toggleLangContentSelector();
            }
        });

        $langButtonOpen.on('click', toggleLangContentSelector);
    }

    /*
     * Directs page to show India specific content while still in en-US locale
     */
    function setEnInContent () {
        $('html').addClass('en-IN');
        $('.india-show').show();
        $('.india-hide').hide();
    }

    /*
     * Toggle language content selector visibility
     */
    function toggleLangContentSelector () {
        clearTimeout(langTimer);
        var href;

        if ($langPanel.hasClass('visible')) {
            $langPanel.removeClass('visible');

            // wait for CSS transition to complete before hiding
            langTimer = setTimeout(function() {
                $langPanel.hide();
                $langButtonOpen.attr('aria-expanded', false);
                $langButtonOpen.focus();
            }, 300);

            // remove listeners for performance boostingness
            $document.off('click.lang-panel');
            $window.off('scroll.lang-panel');
        } else {
            $langPanel.show();
            $langButtonOpen.attr('aria-expanded', true);
            langTimer = setTimeout(function () {
                $langPanel.addClass('visible');

                // hide panel when clicking outside in document
                $('.lang-panel').each(function() {
                    $this = $(this);
                    $this.attr({
                        'data-element-location': $this.data('lang'),
                        'data-interaciton': 'Indian Language Selection'
                    });
                    
                });
                $document.on('click.lang-panel', function (e) {
                    var $target = $(e.target);

                    if (!$target.parents().is('#lang-panel') || $target.attr('id') === 'close-lang-panel') {
                        toggleLangContentSelector();
                    } else {
                        e.preventDefault();

                        var language = $target.data('lang');

                        // if selecting English, swap content and remain on page
                        if (language === 'English') {
                            setEnInContent();

                            toggleLangContentSelector();

                            // save choice in session so as to not bug user a second time
                            try {
                                sessionStorage.setItem(sessionLangPrefName, 'en-IN');
                            } catch (ex) {}
                        }
                        href = $target.attr('href');
                        if (language !== 'English') {
                            window.location = href;
                        }
                    }
                });

                // hide panel on scroll
                $window.on('scroll.lang-panel', toggleLangContentSelector);
            }, 50);
        }
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
            COUNTRY_CODE = '';
        }
    }

    $('#useful-links').each(function() {
        $(this).attr({
            'data-interaction': 'click', 
            'data-element-location': $(this).href
        });
    });

    $script('//geo.mozilla.org/country.js', function() {
        getGeoLocation();
        setNewsletterDefaults();
        setPartnerContent();
    });
})(jQuery);
