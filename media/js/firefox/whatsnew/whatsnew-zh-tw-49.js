/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.HkTwWhatsNew = (function($) {
    'use strict';

    var _client = Mozilla.Client;
    var _geoTimeout;
    var _mainContainer = document.getElementById('main-container');
    var _searchEngineGeoMap = {
        'hk': 'yahoo-zh-TW-HK',
        'tw': 'yahoo-zh-TW'
    };
    var _$shield;

    // wire up default behavior (subset of variant-a.js)
    function _enableDefaultContent() {
        _$shield = $('#tracking-protection-animation');

        Mozilla.HighlightTarget.init('.button.dark');

        $('.button.dark').on('highlight-target', function() {
            _$shield.addClass('blocked');
        });
    }

    return {
        displayComplete: false,
        displayContent: function(conditionsOk, countryCode) {
            clearTimeout(_geoTimeout);

            if (!Mozilla.HkTwWhatsNew.displayComplete) {
                // make sure not called twice if geo lookup is slow
                Mozilla.HkTwWhatsNew.displayComplete = true;

                var contentClass;

                // display custom content
                if (conditionsOk) {
                    $('#copy-' + countryCode).removeClass('hidden');
                    $('#image-' + countryCode).removeClass('hidden');
                    $('#special-content').removeClass('hidden js-hidden');
                    contentClass = 'special';
                // display standard content
                } else {
                    $('#default-content').removeClass('js-hidden');
                    _enableDefaultContent();
                    contentClass = 'default';
                }

                $('#outer-wrapper').addClass('loaded ' + contentClass);
            }
        },
        // make sure user is in list of accepted countries
        geoCheck: function(countryCode, searchEngineGeoMap) {
            searchEngineGeoMap = searchEngineGeoMap || _searchEngineGeoMap;

            return new Promise(function(resolve, reject) {
                if (searchEngineGeoMap.hasOwnProperty(countryCode)) {
                    resolve();
                } else {
                    reject();
                }
            });
        },
        // make sure user's search engine is set to a mapped value for their country
        searchCheck: function(countryCode, searchEngineGeoMap) {
            searchEngineGeoMap = searchEngineGeoMap || _searchEngineGeoMap;

            return new Promise(function(resolve, reject) {
                Mozilla.UITour.getConfiguration('search', function(data) {
                    if (searchEngineGeoMap[countryCode] && searchEngineGeoMap[countryCode] === data.searchEngineIdentifier) {
                        resolve();
                    } else {
                        reject();
                    }
                });
            });
        },
        versionCheck: function(version) {
            // must be on Fx 49.0
            // (safe enough to ignore channel for our purposes here)
            return version === '49.0';
        },
        init: function() {
            // if version is eligible, geolocate user
            if (Mozilla.HkTwWhatsNew.versionCheck(_client.FirefoxVersion)) {
                // fallback if geolocation fails/is very slow
                _geoTimeout = setTimeout(Mozilla.HkTwWhatsNew.displayContent, 5000);

                $.get('https://location.services.mozilla.com/v1/country?key=' + _mainContainer.dataset.geoKey)
                    .done(function(data) {
                        var countryCode = data.country_code.toLowerCase();

                        // make sure 5s fallback hasn't already fired
                        if (!Mozilla.HkTwWhatsNew.displayComplete) {
                            // make sure user is in supported locale & search engine matches expected value
                            Promise.all([Mozilla.HkTwWhatsNew.geoCheck(countryCode), Mozilla.HkTwWhatsNew.searchCheck(countryCode)]).then(function() {
                                // show conditional content
                                Mozilla.HkTwWhatsNew.displayContent(true, countryCode);
                            }).catch(function() {
                                // show default content
                                Mozilla.HkTwWhatsNew.displayContent();
                            });
                        }
                    })
                    .fail(function() {
                        // if geo fails, display default content
                        Mozilla.HkTwWhatsNew.displayContent();
                    });
            } else {
                // if version & channel do not match, show default content
                Mozilla.HkTwWhatsNew.displayContent();
            }
        }
    };
})(window.jQuery);
