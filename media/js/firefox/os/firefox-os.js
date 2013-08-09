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

  var PARTNER_DATA = {
    "co": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.movistar.co"
        }
      ]
    },
    "es": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.movistar.es/firefoxos?aff=aff-firefoxOS1"
        }
      ]
    },
    "pl": {
      "partner": [
        {
          "name": "T-Mobile",
          "url": "http://www.t-mobile.pl/pl/firefox"
        }
      ]
    },
    "ve": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.movistar.com.ve/movistar_firefox/index.html"
        }
      ]
    }
  };

  /*
   * Set page specific content relating to geo for partner data etc
   */
  function setPartnerContent () {
    var $getPhoneContent = $('#get-phone-wrapper .content');
    var $providerLinks = $('#provider-links');
    var links = '';

    if(PARTNER_DATA[COUNTRY_CODE]) {

      // show get phone call to actions
      $('#primary-cta-phone').fadeIn();
      $('#primary-cta-signup').addClass('visibility', 'hidden');
      $('#secondary-cta-phone').css('display', 'inline-block');

      // if country has more than one provider, show the multi intro text
      if (PARTNER_DATA[COUNTRY_CODE].partner.length > 1) {
        $('#provider-text-single').hide();
        $('#provider-text-multi').show();
      }
      // show partner specific links on modal etc
      $.each(PARTNER_DATA[COUNTRY_CODE].partner, function(i, data) {
        //set data.name, data.url etc
        var index = i === 1 ? 'last' : '';
        links += '<a class="' + data.name.toLowerCase() + ' ' + index + '" href="' + data.url + '">' + data.name + '</a>';
      });
      $('#provider-links').html(links);
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
   * Set newsletter default options based on cc
   */
  function setNewsletterDefaults () {
    var countrySelection = $('#id_country option[value='+ COUNTRY_CODE +']');

    // if cc is in the country option list, select it
    // remove the default selection first
    if (countrySelection.length !== 0) {
      $('#id_country option:selected').removeAttr('selected');
      countrySelection.attr('selected', 'selected');
    }

    // for ve and co set the default language to es
    // other countries auto select based on cc
    switch(COUNTRY_CODE) {
    case 've':
      $('#id_lang option[value="es"]').attr('selected', 'selected');
      break;
    case 'co':
      $('#id_lang option[value="es"]').attr('selected', 'selected');
      break;
    default:
      $('#id_lang option[value="' + COUNTRY_CODE + '"]').attr('selected', 'selected');
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
          window._gaq.push(
            ['_set', 'hitCallback', gaCallback],
            eventsArray
          );
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
