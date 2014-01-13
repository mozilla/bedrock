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
    "br": {
      "partner": [
        {
          "name": "Vivo",
          "url": "http://www.vivo.com.br/firefox"
        }
      ]
    },
    "co": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.movistar.co"
        }
      ]
    },
    "de": {
      "partner": [
        {
          "name": "congstar",
          "url": "http://aktion.congstar.de/firefox-os"
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
    "gr": {
      "partner": [
        {
          "name": "Cosmote",
          "url": "http://www.cosmote.gr/cosmoportal/cosmote.portal?_nfpb=true&_pageLabel=HDV&sku=20290038&s=0"
        }
      ]
    },
    "hu": {
      "partner": [
        {
          "name": "T-Mobile",
          "url": "https://webshop.t-mobile.hu/webapp/wcs/stores/ProductDisplay?catalogId=2001&storeId=2001&langId=-11&productId=644566"
        },
        {
          "name": "Telenor",
          "url": "http://www.telenor.hu/mobiltelefon/alcatel/one-touch-fire"
        }
      ]
    },
    "it": {
      "partner": [
        {
          "name": "TIM",
          "url": "http://www.tim.it/prodotti/alcatel-one-touch-fire-mozilla-orange"
        }
      ]
    },
    "me": {
      "partner": [
        {
          "name": "Telenor",
          "url": "http://www.telenor.me/sr/Privatni-korisnici/Uredjaji/Mobilni-telefoni/Alcatel/OT_Fire"
        }
      ]
    },
    "mx": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.movistar.com.mx/firefox"
        }
      ]
    },
    "pe": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://catalogo.movistar.com.pe/zte-open"
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
    "rs": {
      "partner": [
        {
          "name": "Telenor",
          "url": "https://www.telenor.rs/sr/Privatni-korisnici/webshop/Mobilni-telefoni/Alcatel/One_Touch_Fire"
        }
      ]
    },
    "uy": {
      "partner": [
        {
          "name": "Movistar",
          "url": "http://www.firefoxos.movistar.com.uy/"
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

    if (PARTNER_DATA.hasOwnProperty(COUNTRY_CODE)) {

      // show get phone calls to action
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
