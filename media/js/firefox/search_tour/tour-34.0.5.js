/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var $document = $(document);
    var doorhangerClosed = false;
    var queryIsLargeScreen = matchMedia('(min-width: 600px)');
    var highlightTimeout;
    var variants = ['ravioli', 'flare', 'independence'];
    var icon;
    var _trackingID;
    var pageId = $('body').prop('id');

    /*
     * Doorhanger for users who were brute forced
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
    }

    /*
     * User closes brute forced doorhanger
     */
    function closeForcedDoorhanger() {
        doorhangerClosed = true;
        $document.off('visibilitychange', handleVisibilityChange);
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Close');
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

        // '1' is code for user forced to Yahoo!, which is done in-product
        _trackingID = '1' + id;

        Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_' + _trackingID);
        Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ShowHanger');
    }

    function determinePageVariation() {
        var rand = variants[Math.floor(Math.random() * variants.length)];

        showPageVariant(rand);
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
     * Reshows the doorhanger
     */
    function reShowDoorhanger() {
        if (doorhangerClosed) {
            return;
        }
        clearInterval(highlightTimeout);
        highlightTimeout = setTimeout(function() {
            Mozilla.UITour.getConfiguration('availableTargets', function (config) {
                if (config.targets && $.inArray('search', config.targets) !== -1 && $.inArray('searchEngine-yahoo', config.targets) !== -1) {
                    showForcedDoorhanger();
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

    // use a slight delay for showing the main page content
    // to allow variation to be set first.
    setTimeout(function() {
        $('main').css('visibility', 'visible');
    }, 500);

    //Only run the tour if user is on Firefox 34 and in US timezone.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 34) {
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

                        // check if user has yahoo as default already (should be true for all en-US users)
                        if (selectedEngineID && selectedEngineID === 'yahoo') {
                            determinePageVariation();

                        } else {
                            // user does not have Yahoo! as default (en-US build user outside of US timezone)
                            Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
                            Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                        }

                        showForcedDoorhanger();
                        bindEvents();
                    });
                } else {
                    // searchbar is not present in main browser toolbar
                    Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'whatsnew_Default');
                    Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                }
            }
        });

        Mozilla.UITour.registerPageID(pageId);
    }

})(window.jQuery, window.Mozilla);
