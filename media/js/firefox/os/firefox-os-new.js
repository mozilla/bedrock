/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var COUNTRY_CODE = '';

    var $window = $(window);
    var isSmallViewport = $window.width() < 760;
    var $signupContent;
    var $getPhoneContent;

    var $appGroupSelector = $('.app-group-selector');
    var $apps = $('li', '.apps');
    var $categoryTriggers = $('a', $appGroupSelector);

    //get modal logo path from data attribute in template
    var modalLogo = $('#modal-logo').data('src');

    var fxNavConfig = {
        primaryId: 'os',
        subId: 'index'
    };

    Mozilla.FxFamilyNav.init(fxNavConfig);

    /*
    * Sign up form
    */
    $('.newsletter-signup-toggle').on('click', function(e) {
      e.preventDefault();

      if (!$signupContent) {
        $signupContent = $('#email-form-content').detach();
      }

      Mozilla.Modal.createModal(this, $signupContent, {
          allowScroll: !isSmallViewport,
          title: '<img src="' + modalLogo + '" alt="Firefox OS" />'
      });

      //track GA event for newsletter CTA
      gaTrack(['_trackEvent', 'FxOs Consumer Page', 'click', 'Sign Me Up - Primary']);
    });

    $('#sign-up-form-close').on('click', function() {
      Mozilla.Modal.closeModal();
    });

    /*
    * Purchase modal
    */
    $('a[href="#get-device"]').on('click', function(e) {
      e.preventDefault();

      if (!$getPhoneContent) {
        $getPhoneContent= $('#get-device').detach();
      }

      Mozilla.Modal.createModal(this, $getPhoneContent, {
          allowScroll: !isSmallViewport,
          title: '<img src="' + modalLogo + '" alt="Firefox OS" />'
      });

      //track GA event for get a phone CTA
      gaTrack(['_trackEvent', 'FxOs Consumer Page', 'click', 'Get a Phone']);
    });

    $appGroupSelector.on('click', 'a', function(event) {
        event.preventDefault();
        var $eventTarget = $(this);
        var category = $eventTarget.data('category');

        // reset all the app icons
        $apps.addClass('fade');
        // reset all the category selector buttons
        $categoryTriggers.removeClass('active-state');
        // set the clicked element to active
        $eventTarget.addClass('active-state');

        $apps.each(function() {
            var $currentImg = $(this);
            if ($currentImg.hasClass(category)) {
                $currentImg.removeClass('fade');
            }
        });
    });

    window.pause_ga_tracking = false;

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
    * Track telecom provider link clicks/page exits in Google Analytics
    */
    function trackProviderExit (e) {
        var $this = $(this);
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;

        var callback = function () {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'FxOs Consumer Page', 'Get A Phone Exit', $this.text()]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'FxOs Consumer Page', 'Get A Phone Exit', $this.text()], callback);
        }
    }

    /*
    * Set page specific content relating to geo for partner data etc
    */
    function setPartnerContent () {

        var $provider = $('#provider-links').find('.provider[data-country="' + COUNTRY_CODE + '"]');

        // if there are partners available, update UI
        if (COUNTRY_CODE !== '' && $provider.length > 0) {
            // show get phone calls to action
            $('.primary-cta-phone').removeClass('hidden');

            // if country has more than one provider, show the multi intro text
            if ($provider.find('li').length > 1) {
                $('#provider-text-single').hide();
                $('#provider-text-multi').show();
            }

            // show the provider applicable for the user country.
            $provider.show();

            // setup GA event tracking on telecom provider exit links
            $('#provider-links a').on('click', trackProviderExit);
        } else {
            $('.primary-cta-signup').removeClass('hidden');
        }
    }

    $script('//geo.mozilla.org/country.js', function() {
        getGeoLocation();
        setNewsletterDefaults();
        setPartnerContent();
    });

})(jQuery);
