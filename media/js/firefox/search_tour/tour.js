/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var $document = $(document);
    var doorhangerClosed = false;
    var userForced = false;
    var queryIsLargeScreen = matchMedia('(min-width: 600px)');
    var highlightTimeout;
    var variants = ['ravioli', 'flare', 'independence'];
    var icon;
    var _trackingID;
    var pageId = $('body').prop('id');

    /*
     * Set the default search provider to Yahoo!
     */
    function setDefaultSearchProvider() {
        Mozilla.UITour.setDefaultSearchEngine('yahoo');
    }

    /*
     * Doorhanger for users who we're brute forced
     * into having their default set to Yahoo!
     */
    function showForcedDoorhanger() {

        var buttons = [
            {
                label: window.trans('later'),
                callback: closeForcedDoorhanger
            },
            {
                label: window.trans('forcedCta'),
                style: 'primary',
                callback: trySearch
            }
        ];

        var options = {
            closeButtonCallback: closeForcedDoorhanger
        };

        if (queryIsLargeScreen.matches && !document.hidden) {
            Mozilla.UITour.showInfo(
                'search',
                window.trans('forcedTitle'),
                window.trans('forcedText'),
                icon,
                buttons,
                options
            );
        }
    }

    function trySearch() {
        doorhangerClosed = true;
        Mozilla.UITour.setSearchTerm('Firefox');
        Mozilla.UITour.openSearchPanel(function() {});
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Try');
        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', _trackingID, 'Try']);
    }

    /*
     * User closes brute forced doorhanger
     */
    function closeForcedDoorhanger() {
        doorhangerClosed = true;
        $document.off('visibilitychange', handleVisibilityChange);
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Close');
        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', _trackingID, 'Close']);
    }

    /*
     * Doorhanger for users who can opt-in to Yahoo!
     */
    function showOptInDoorhanger() {

        var buttons = [
            {
                label: window.trans('later'),
                style: 'link',
                callback: closeOptInDoorhanger
            },
            {
                label: window.trans('optInCta'),
                style: 'primary',
                callback: tryYahoo
            }
        ];

        var options = {
            closeButtonCallback: closeOptInDoorhanger
        };

        if (queryIsLargeScreen.matches && !document.hidden) {
            Mozilla.UITour.showInfo(
                'search',
                window.trans('optInTitle'),
                window.trans('optInText'),
                icon,
                buttons,
                options
            );
        }
    }

    /*
     * User opts in to setting Yahoo as their default
     */
    function tryYahoo() {
        setDefaultSearchProvider();
        doorhangerClosed = true;
        Mozilla.UITour.setSearchTerm('Firefox');
        Mozilla.UITour.openSearchPanel(function() {});
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Switch');
        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', _trackingID, 'Switch']);
    }

    /*
     * User closes the opt-in doorhanger
     */
    function closeOptInDoorhanger() {
        doorhangerClosed = true;
        $document.off('visibilitychange', handleVisibilityChange);
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Close');
        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', _trackingID, 'Close']);
    }

    function showPageVariant(variant) {
        $('header > .default').hide();
        $('.features.default').hide();
        $('header > .' + variant).show();
        $('.features.' + variant).css('display', 'table');

        trackPageVariant(variant);
    }

    function trackPageVariant(variant) {
        var id;
        var doorhanger = userForced ? 1 : 2;

        switch(variant) {
        case 'ravioli':
            id = 'A';
            break;
        case 'flare':
            id = 'B';
            break;
        case 'independence':
            id = 'C';
            break;
        default:
            id = 'Unknown';
        }

        _trackingID = doorhanger + id;

        Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_' + _trackingID);
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ShowHanger');
        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', _trackingID, 'ShowHanger']);
    }

    function determinePageVariation() {
        var rand = variants[Math.floor(Math.random() * variants.length)];

        if (pageId === 'whatsnew-search-tour-35-beta') {
            rand = 'independence';
        }

        showPageVariant(rand);
    }

    /*
     * Dice roll to decide if user is brute forced into using
     * Yahoo or can choose opt-in
     */
    function rollTheDice() {
        var SAMPLE_RATE = 0.5;
        var forced = (Math.random() < SAMPLE_RATE) ? true : false;

        if (pageId === 'whatsnew-search-tour-35-beta') {
            forced = true;
        }

        if (forced) {
            userForced = true;
            setDefaultSearchProvider();
            determinePageVariation();
            showForcedDoorhanger();
        } else {
            determinePageVariation();
            showOptInDoorhanger();
        }
    }

    /*
     * Handle page visibility events to hide/show the doorhanger
     */
    function handleVisibilityChange() {
        if (document.hidden) {
            Mozilla.UITour.hideInfo();
        } else {
            reShowDoorhanger();
        }
    }

    /*
     * Reshows the doorhanger if needed, depending on if the user was opt-in or forced
     */
    function reShowDoorhanger() {
        if (doorhangerClosed) {
            return;
        }
        clearInterval(highlightTimeout);
        highlightTimeout = setTimeout(function() {
            Mozilla.UITour.getConfiguration('availableTargets', function (config) {
                if (config.targets && $.inArray('search', config.targets) !== -1 && $.inArray('searchEngine-yahoo', config.targets) !== -1) {
                    if (userForced) {
                        showForcedDoorhanger();
                    } else {
                        showOptInDoorhanger();
                    }
                }
            });
        }, 900);
    }

    function bindEvents() {
        queryIsLargeScreen.addListener(function(mq) {
            if (mq.matches) {
                reShowDoorhanger();
            } else {
                Mozilla.UITour.hideInfo();
            }
        });

        $document.on('visibilitychange', handleVisibilityChange);
    }

    // Timezone method used to determine if user is in US timezone
    // Code here is copied directly from in-product check in Firefox (Bug 1102416)
    function getIsUS() {
        // Timezone assumptions! We assume that if the system clock's timezone is
        // between Newfoundland and Hawaii, that the user is in North America.

        // This includes all of South America as well, but we have relatively few
        // en-US users there, so that's OK.

        // 150 minutes = 2.5 hours (UTC-2.5), which is
        // Newfoundland Daylight Time (http://www.timeanddate.com/time/zones/ndt)

        // 600 minutes = 10 hours (UTC-10), which is
        // Hawaii-Aleutian Standard Time (http://www.timeanddate.com/time/zones/hast)

        var UTCOffset = (new Date()).getTimezoneOffset();
        var isNA = UTCOffset >= 150 && UTCOffset <= 600;

        return isNA;
    }

    // use a slight delay for showing the main page content
    // to allow variation to be set first.
    setTimeout(function() {
        $('main').css('visibility', 'visible');
    }, 500);

    //Only run the tour if user is on Firefox 34 and in US timezone.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 34) {

        if (getIsUS()) {

            // set search doorhanger icon
            icon = Mozilla.ImageHelper.isHighDpi() ? window.trans('iconHighRes') : window.trans('icon');

            // query available UITour highlight targets
            Mozilla.UITour.getConfiguration('availableTargets', function (config) {
                if (config.targets) {

                    // check if search bar target is available in the UI and Yahoo is a search provider
                    if ($.inArray('search', config.targets) !== -1 && $.inArray('searchEngine-yahoo', config.targets) !== -1) {

                        // get the user's currently selected search engine
                        Mozilla.UITour.getConfiguration('selectedSearchEngine', function (data) {
                            var selectedEngineID = data.searchEngineIdentifier;

                            // clear the current search term if any
                            Mozilla.UITour.setSearchTerm('');

                            // check if user does not have yahoo as default already
                            if (selectedEngineID && selectedEngineID !== 'yahoo') {

                                // check is user has google as default
                                if (selectedEngineID === 'google') {
                                    // roll the dice for opt-in or forced update

                                    rollTheDice();
                                    bindEvents();
                                } else {
                                    Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
                                    Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                                    gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'Default', 'ViewPage']);
                                }

                                gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'All', 'otherDefault']);

                            } else {
                                // user already has yahoo as default
                                Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
                                Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                                gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'All', 'yahooDefault']);
                            }
                        });
                    } else {
                        // searchbar is not present in main browser toolbar
                        Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
                        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                        gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'All', 'noSearchbox']);
                    }
                }
            });
        } else {
            Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
            Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
            gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'Default', 'ViewPage']);
        }

        Mozilla.UITour.registerPageID(pageId);
    }

})(window.jQuery, window.Mozilla);
