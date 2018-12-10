/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.firefoxConcertsOnYouTubeIframeAPIReady();
}


(function(Mozilla) {
    'use strict';

    var ConcertPage = {
        US_COUNTRY_CODE: 'us',
        COOKIE_ID: 'firefox-concerts',
        COOKIE_EXPIRATION_DAYS: 3,
    };

    var _geoTimeout;
    var _requestComplete = false;

    // take params from URL and pass through signup button
    ConcertPage.passThroughParams = function() {
        var params = window.location.search.slice(1);
        ['source','medium','campaign','content'].forEach(function(p) {
            var param = 'utm_' + p;
            if (params.indexOf(param) >= 0) {
                var regex = RegExp(param + '=([^\#\&\?]+).*$');
                if (regex.test(params)) {
                    var value = params.match(regex)[1];
                    document.getElementById(param).value = value;
                }
            }
        });
    };

    ConcertPage.getLocation = function() {
        // should /country-code.json be slow to load,
        // just show the regular messaging after 3 seconds waiting.
        _geoTimeout = setTimeout(ConcertPage.onRequestComplete, 3000);

        var xhr = new window.XMLHttpRequest();

        xhr.onload = function(r) {
            var country = 'none';

            // make sure status is in the acceptable range
            if (r.target.status >= 200 && r.target.status < 300) {

                try {
                    country = JSON.parse(r.target.responseText).country_code.toLowerCase();
                } catch (e) {
                    country = 'none';
                }
            }

            ConcertPage.onRequestComplete(country);
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    };

    ConcertPage.hasGeoOverride = function(location) {
        var loc = location || window.location.search;
        if (loc.indexOf('geo=') !== -1) {
            var urlRe = /geo=([a-z]{2})/i;
            var match = urlRe.exec(loc);
            if (match) {
                return match[1].toLowerCase();
            }
            return false;
        }
        return false;
    };

    ConcertPage.verifyLocation = function(location) {
        if (location) {
            return location !== ConcertPage.US_COUNTRY_CODE;
        }

        return false;
    };

    ConcertPage.onRequestComplete = function(data) {
        var country = typeof data === 'string' ? data : 'none';

        clearTimeout(_geoTimeout);

        if (!_requestComplete) {
            _requestComplete = true;

            // Set a cookie so we don't have to query location on repeated page loads.
            ConcertPage.setCookie(country);

            // Update page content based on location.
            ConcertPage.updatePageContent();
        }
    };

    ConcertPage.updatePageContent = function() {
        if (ConcertPage.shouldShowConcert() === 'false') {
            ConcertPage.showExcludedContent();
        } else {
            ConcertPage.showConcertContent();
        }
    };

    ConcertPage.showConcertContent = function() {
        // Add styling hook for us-specific CSS.
        document.body.classList.add('state-in-us');
    };

    ConcertPage.showExcludedContent = function() {
        // Add styling hook for excluded-specific CSS.
        document.body.classList.add('state-not-us');
    };

    ConcertPage.shouldShowConcert = function() {
        // Is user in the US?
        return ConcertPage.verifyLocation(ConcertPage.getCookie(ConcertPage.COOKIE_ID));
    };

    ConcertPage.cookieExpiresDate = function(date) {
        var d = date || new Date();
        d.setTime(d.getTime() + (ConcertPage.COOKIE_EXPIRATION_DAYS * 24 * 60 * 60 * 1000));
        return d.toUTCString();
    };

    ConcertPage.setCookie = function(country) {
        Mozilla.Cookies.setItem(ConcertPage.COOKIE_ID, country, ConcertPage.cookieExpiresDate());
    };

    ConcertPage.getCookie = function(id) {
        return Mozilla.Cookies.getItem(id);
    };

    ConcertPage.hasCookie = function() {
        return Mozilla.Cookies.hasItem(ConcertPage.COOKIE_ID);
    };

    ConcertPage.init = function() {
        ConcertPage.passThroughParams();

        var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' || Mozilla.Cookies.enabled();
        var override = ConcertPage.hasGeoOverride();

        // only show excluded content if cookies are enabled (let LiveNation deal with it)
        if (cookiesEnabled) {
            // if override URL is used, skip doing anything with cookies & show the expected content.
            if (override) {
                if (ConcertPage.verifyLocation(override)) {
                    ConcertPage.showExcludedContent();
                } else {
                    ConcertPage.showConcertContent();
                }
            } else {
                // if user already has a cookie, use that data and update page content straight away.
                if (ConcertPage.hasCookie()) {
                    ConcertPage.updatePageContent();
                }
                // else make a remote call to query location.
                else {
                    ConcertPage.getLocation();
                }
            }
        } else {
            ConcertPage.showConcertContent();
        }
    };
    window.Mozilla.ConcertPage = ConcertPage;


    var stateStorageKey = 'fxaOauthState';
    var verifiedStorageKey = 'fxaOauthVerified';
    var cookieDays = 14;

    var className;
    var state;

    /*
        This function initiates the OAuth process.

        It looks for a state key stored in a cookie, and, if not found, generates a new
        key and places it in a cookie.

        The state value is then set in the form and on the direct link URL.

        Next, we retrieve metrics information from an asynchronous FxA call. When this
        call completes, the submit button on the form is enabled.
    */
    function initOauth() {
        var fxaFormWrapper = document.getElementById('fxa-form-wrapper');
        var metricsFlowEndpoint = fxaFormWrapper.getAttribute('data-fxa-metrics-endpoint');
        var flowIdField = document.getElementById('flow_id');
        var flowBeginTimeField = document.getElementById('flow_begin_time');
        var stateField = document.getElementById('state');
        var fxaSignIn = document.getElementById('fxa-sign-in');

        // check for an existing state value in a cookie
        if (Mozilla.Cookies.hasItem(stateStorageKey)) {
            state = Mozilla.Cookies.getItem(stateStorageKey);
        } else {
            // generate a state token and put it in a cookie

            // the suffix below is superfluous for now, but will help us identify
            // different OAuth flows in the future
            state = Math.random() + '_concert_q42018';

            var d = new Date();
            d.setTime(d.getTime() + (cookieDays * 24 * 60 * 60 * 1000));
            Mozilla.Cookies.setItem(stateStorageKey, state, d.toUTCString(), '/');
        }

        // put state value in form & append to sign-in link
        stateField.value = state;
        fxaSignIn.href += '&state=' + state;

        // get metrics flow stuff from FxA
        fetchTokens(metricsFlowEndpoint);

        // get tokens from FxA for analytics purposes
        // copied from base/mozilla-fxa-form.js
        function fetchTokens(destURL) {
            // add required params to the token fetch request
            destURL += '?utm_campaign=firefox-concert-series-q4-2018&utm_source=mozilla.org';

            fetch(destURL).then(function(resp) {
                return resp.json();
            }).then(function(r) {
                flowIdField.value = r.flowId;
                flowBeginTimeField.value = r.flowBeginTime;
            }).catch(function() {
                // silently fail, leaving flow_id and flow_begin_time as default empty value
            });
        }
    }

    // update class based on cookie state so we can show/hide the appropriate content

    // if user has a verified cookie, we can skip the OAuth flow
    if (Mozilla.Cookies.hasItem(verifiedStorageKey)) {
        className = 'is-verified';
    } else {
        className = 'not-verified';
        initOauth();
    }

    // apply className determined above to show proper content
    document.body.classList.add(className);

    // Phosphorescent - December 11 at 8:00pm Eastern
    var showtimeOne = 'December 11 2018 20:00:00 GMT-0500';
    var countdownOne = document.getElementById('countdown-one');

    // Calculate time from now to a future endtime
    function getTimeRemaining(endtime) {
        var t = Date.parse(endtime) - Date.parse(new Date());
        var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
        var days = Math.floor(t / (1000 * 60 * 60 * 24));

        return {
            'total': t,
            'days': days,
            'hours': hours
        };
    }

    // Initialize the countdown timer
    function initializeClock(id, endtime) {
        var clock = document.getElementById(id);
        var daysSpan = clock.querySelector('.days');
        var hoursSpan = clock.querySelector('.hours');

        function updateClock() {
            var t = getTimeRemaining(endtime);

            daysSpan.innerHTML = t.days;
            hoursSpan.innerHTML = t.hours;

            if (t.total <= 0) {
                clearInterval(timeinterval);
            }
        }

        updateClock();
        var timeinterval = setInterval(updateClock, 60000);
    }

    if (countdownOne) { // To avoid errors make sure the thing exists first
        initializeClock('countdown-one', showtimeOne);
    }


    // Set up modal for the email privacy link
    var content = document.querySelector('.mzp-u-modal-content');
    var trigger = document.querySelector('.email-privacy-link');
    var title = document.querySelector('.email-privacy h3');

    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mzp.Modal.createModal(e.target, content, {
            title: title.innerHTML,
            className: 'mzp-t-firefox',
            closeText: window.Mozilla.Utils.trans('global-close'),
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'How will Mozilla use my email?'
        });
    }, false);


    // Video
    var videoLink = document.querySelector('.js-video-play');

    if (videoLink) {
        var tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function onYouTubeIframeAPIReady() {

        // lazy load video when visitor clicks the placeholder.
        var videoId = videoLink.getAttribute('data-id');

        videoLink.setAttribute('role', 'button');

        videoLink.addEventListener('click', function(e) {
            e.preventDefault();

            new YT.Player(videoLink, {
                height: '703',
                width: '1250',
                videoId: videoId,
                playerVars: {
                    modestbranding: 1, // hide YouTube logo.
                    rel: 0, // do not show related videos on end.
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();
            }

            function onPlayerStateChange(event) {
                var state;

                switch(event.data) {
                case YT.PlayerState.PLAYING:
                    state = 'video play';
                    break;
                case YT.PlayerState.PAUSED:
                    state = 'video paused';
                    break;
                case YT.PlayerState.ENDED:
                    state = 'video complete';
                    break;
                }

                if (state) {
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'videoTitle': 'Firefox Concert - Phosphorescent',
                        'interaction': state
                    });
                }
            }
        });
    }

    Mozilla.firefoxConcertsOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

})(window.Mozilla);
