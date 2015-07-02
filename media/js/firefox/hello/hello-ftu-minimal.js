/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function($) {
    'use strict';

    var HelloFTU = {};
    var _helloPanelTimeout;

    // User has clicked "Get Started" button in the Hello panel.
    HelloFTU.getStartedClicked = false;

    // Tour page has opened Hello Panel
    HelloFTU.helloPanelVisible = false;

    // Used for unit testing purposes only as "document.hidden" is read only.
    HelloFTU.documentHidden = null;

    /**
     * Initialize Hello FTU.
     * Only start the tour if the Hello icon is present in the tool pallet.
     * Given that this tour should only be accessed via the Hello panel itself,
     * this should always be "true". However, it's always possible someone may
     * share the URL directly with someone who has disabled or removed Hello.
     */
    HelloFTU.init = function() {
        // Hello is still referred to as 'loop' internally for legacy reasons.
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop', config.targets) !== -1) {
                HelloFTU.showHelloPanel();
                HelloFTU.bindPageEvents();
                HelloFTU.bindHelloEvents();
                HelloFTU.trackTourSource(HelloFTU.getTourSource());
            }
        });
    };

    HelloFTU.showHelloPanel = function() {
        // Only open the info panel if tab is visible
        if (HelloFTU.documentHidden || document.hidden) {
            return;
        }
        // Make sure loop icon is available before opening Hello panel (bug 1111828)
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop', config.targets) !== -1) {
                Mozilla.UITour.showMenu('loop', function() {
                    HelloFTU.helloPanelVisible = true;
                    $(window).one('resize.hello', HelloFTU.handleResize);
                });
            }
        });
    };

    HelloFTU.hideHelloPanel = function() {
        Mozilla.UITour.hideMenu('loop');
    };

    /**
     * Handles tab visibility changes triggered via the Page Visibility API.
     * Used to show/hide UITour panels and bind Loop events.
     */
    HelloFTU.handleVisibilityChange = function() {
        if (HelloFTU.documentHidden || document.hidden) {
            HelloFTU.hideHelloPanel();
            HelloFTU.unbindHelloEvents();
        } else {
            clearTimeout(_helloPanelTimeout);
            HelloFTU.bindHelloEvents();

            if (!HelloFTU.getStartedClicked) {
                _helloPanelTimeout = setTimeout(HelloFTU.showHelloPanel, 900);
            }
        }
    };

    /**
     * Hides the Hello panel on page resize. XUL popups with an anchor element don't
     * hide when the anchor loses visibility i.e. the Hello icon moves into the
     * overflow pallet (bug 1109868).
     */
    HelloFTU.handleResize = function() {
        if (!HelloFTU.getStartedClicked && HelloFTU.helloPanelVisible) {
            HelloFTU.hideHelloPanel();
            HelloFTU.helloPanelVisible = false;
        }
    };

    HelloFTU.trackRoomShareButton = function(button) {
        window.dataLayer.push({
            'event': 'hello-interactions',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': button
        });
    };

    HelloFTU.bindPageEvents = function() {
        $(document).on('visibilitychange.hello', HelloFTU.handleVisibilityChange);
    };

    /**
     * Binds an event handler for receiving custom events from the Loop client.
     */
    HelloFTU.bindHelloEvents = function() {
        Mozilla.UITour.observe(HelloFTU.handleHelloEvents);
    };

    /**
     * Processes custom events received from the Loop client.
     */
    HelloFTU.handleHelloEvents = function(event) {
        switch(event) {
        case 'Loop:ChatWindowOpened':
            HelloFTU.onChatWindowOpened();
            break;
        case 'Loop:RoomURLCopied':
            HelloFTU.trackRoomShareButton('URLCopied-Tour');
            break;
        case 'Loop:RoomURLEmailed':
            HelloFTU.trackRoomShareButton('URLEmailed-Tour');
            break;
        case 'Loop:RoomURLShared':
            HelloFTU.trackRoomShareButton('URLShared-Tour');
            break;
        }
    };

    /**
     * Stop receiving custom events from the Loop client.
     */
    HelloFTU.unbindHelloEvents = function() {
        Mozilla.UITour.observe(null);
    };

    /**
     * Event handler for when the Loop chat window is opened by the user.
     * The first time this is called we assume "Get Started" has been clicked
     * in the Hello panel, and the user has interacted with the tour.
     */
    HelloFTU.onChatWindowOpened = function() {
        // Only track the event the first time the chat window is opened.
        if (HelloFTU.getStartedClicked) {
            return;
        }

        window.dataLayer.push({
            'event': 'hello-interactions',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': 'StartConversation-Tour'
        });

        HelloFTU.getStartedClicked = true;
    };

    /**
     * Gets the value for a given URL parameter name.
     * @param {string} name - URL parameter name.
     * @param {string} paramString - optional value used for testing.
     * @returns value for the given parameter or 'none'.
     */
    HelloFTU.getParameterByName = function(name, paramString) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var params = paramString || location.search;
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(params);
        return results === null ? 'none' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    /**
     * Helper function to get the value for 'utm_content' parameter if present.
     * @param {string} paramString - optional value used for testing.
     * @returns shortened parameter value.
     */
    HelloFTU.getTourSource = function(paramString) {
        return HelloFTU.getParameterByName('utm_content', paramString).replace('hello-tour_OpenPanel_','');
    };

    /**
     * Tracks tour source in GTM
     * @param {string} tourSource - the attributed source for the tour referral.
     */
    HelloFTU.trackTourSource = function(tourSource) {
        window.dataLayer.push({
            'event': 'hello-interactions-referral',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': 'GetStarted',
            'helloFTUReferral': tourSource
        });
    };

    window.Mozilla.HelloFTU = HelloFTU;

})(window.jQuery);
