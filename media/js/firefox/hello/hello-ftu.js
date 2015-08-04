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
    var _highlightTimeout;
    var $defaultCopy = $('.default');
    var $startCopy = $('.start');
    var $endCopy = $('.end');

    HelloFTU.highlightSupressed = false;

    // Used for unit testing purposes only as "document.hidden" is read only.
    HelloFTU.documentHidden = null;

    HelloFTU.tourSource = 'none';

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
                HelloFTU.tourStep = HelloFTU.getInitialTourStep();
                HelloFTU.setInitialPageState();
                HelloFTU.bindPageEvents();
                HelloFTU.bindHelloEvents();
                HelloFTU.trackTourSource();
                HelloFTU.showTourStep();
            }
        });
    };

    HelloFTU.getInitialTourStep = function() {
        // URL query param populated at template level in the view
        var incomingConversation = HelloFTU.getParameterByName('incomingConversation');
        var tourStep = 'get-started';

        // set the tour state based on incomingConversation status
        switch(incomingConversation) {
        case 'waiting':
            tourStep = 'conversation-waiting';
            break;
        case 'open':
            tourStep = 'conversation-open';
            break;
        }

        return tourStep;
    };

    HelloFTU.setInitialPageState = function() {
        if (HelloFTU.tourStep === 'conversation-open') {
            HelloFTU.showPageState('end');
            HelloFTU.replaceURLState('open', 'done');
            HelloFTU.trackGAConversationConnect();
        } else {
            HelloFTU.showPageState('start');
        }
    };

    /*
     * Show the Hello panel and trigger callback once opening animation finishes
     * @param callback (function)
     */
    HelloFTU.showHelloPanel = function(callback) {
        // Only open the info panel if tab is visible
        if (HelloFTU.documentHidden || document.hidden) {
            return;
        }
        // Make sure loop icon is available before opening Hello panel (bug 1111828)
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop', config.targets) !== -1) {
                Mozilla.UITour.showMenu('loop', function() {
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
            }
        });
    };

    // Close any open menus and hide info panels
    HelloFTU.hideUITourHighlights = function() {
        Mozilla.UITour.hideInfo();
        Mozilla.UITour.hideMenu('loop');
    };

    // Highlights Hello panel target.
    HelloFTU.highlightNewRoomButton = function() {
        Mozilla.UITour.showInfo(
            'loop-newRoom',
            HelloFTU.getText('getStartedTitle'),
            HelloFTU.getText('getStartedText')
        );
    };

    // Highlights Hello room list when a conversation is waiting.
    HelloFTU.highlightRoomList = function() {
        Mozilla.UITour.showInfo(
            'loop-roomList',
            HelloFTU.getText('roomListTitle'),
            HelloFTU.getText('roomListText')
        );
    };

    // Add door-hanger to selected room buttons in conversation view
    HelloFTU.highlightSelectedRoomButtons = function() {
        Mozilla.UITour.showInfo(
            'loop-selectedRoomButtons',
            HelloFTU.getText('inviteTitle'),
            HelloFTU.getText('inviteText')
        );
    };

    // Add door-hanger to conversation view once room has been copied/shared
    HelloFTU.showSharedInfoPanel = function() {
        Mozilla.UITour.showInfo(
            'loop-selectedRoomButtons',
            HelloFTU.getText('sharedTitle'),
            HelloFTU.getText('sharedText')
        );
    };

    /*
     * Determine if conversation view and room button targets are visible
     * @param callback (function) to excecute if target is available
     */
    HelloFTU.targetConversationView = function(callback) {
        // Only open the info panel if tab is visible
        if (HelloFTU.documentHidden || document.hidden) {
            return;
        }

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop-selectedRoomButtons', config.targets) !== -1) {
                if (typeof callback === 'function') {
                    callback();
                }
            }
        });
    };

    /*
     * Strips HTML from string to make sure markup
     * does not get injected in any UITour door-hangers.
     * @param string (data attribute string)
     */
    HelloFTU.getText = function(string) {
        return $('<div/>').html(window.trans(string)).text();
    };

    /*
     * Tells Firefox to re-connect to the FTE tour when user has their first conversation.
     * We do this only once the user has interacted with the FTE.
     */
    HelloFTU.resumeTourOnFirstJoin = function() {
        Mozilla.UITour.setConfiguration('Loop:ResumeTourOnFirstJoin', true);
    };

    /**
     * Shows the current step of the FTE tour
     */
    HelloFTU.showTourStep = function() {
        switch(HelloFTU.tourStep) {
        case 'get-started':
            HelloFTU.showHelloPanel(HelloFTU.highlightNewRoomButton);
            break;
        case 'invite':
            HelloFTU.targetConversationView(HelloFTU.highlightSelectedRoomButtons);
            break;
        case 'shared':
            HelloFTU.targetConversationView(HelloFTU.showSharedInfoPanel);
            break;
        case 'conversation-waiting':
            HelloFTU.showHelloPanel(HelloFTU.highlightRoomList);
            break;
        }
    };

    /*
     * Show FTE web page copy state
     * @param state (string)
     * @param anim (boolean)
     */
    HelloFTU.showPageState = function(state, anim) {
        $defaultCopy.hide();

        if (state && state === 'start') {
            $startCopy.show();
            $endCopy.hide();
        } else if (state && state === 'end') {
            if (anim) {
                $startCopy.stop().fadeOut('fast', function () {
                    $endCopy.stop().fadeIn('fast');
                });
            } else {
                $startCopy.hide();
                $endCopy.show();
            }
        } else {
            $startCopy.hide();
            $endCopy.hide();
            $defaultCopy.show();
        }
    };

    /*
     * Sets incomingConversation URL param to 'done' using replaceState
     * @param {currentValue} string to be replaced.
     * @param {newValue} string for new value.
     * @param {url} optional string for testing pruposes.
    */
    HelloFTU.replaceURLState = function(currentValue, newValue, url) {
        var href = url !== undefined ? url : window.location.href;
        var currentParam;

        if (!currentValue || !newValue) {
            return;
        }

        currentParam = 'incomingConversation=' + currentValue;

        if (href.indexOf(currentParam) !== -1) {
            href = href.replace(currentParam, 'incomingConversation=' + newValue);
            window.history.replaceState({}, '', href);
        }
    };

    /**
     * Handles tab visibility changes triggered via the Page Visibility API.
     * Used to show/hide UITour panels and bind Loop events.
     */
    HelloFTU.handleVisibilityChange = function() {
        if (HelloFTU.documentHidden || document.hidden) {
            HelloFTU.hideUITourHighlights();
            HelloFTU.unbindHelloEvents();
        } else {
            clearTimeout(_highlightTimeout);
            HelloFTU.bindHelloEvents();
            _highlightTimeout = setTimeout(HelloFTU.showTourStep, 900);
        }
    };

    /**
     * Hides the Hello panel on page resize. XUL popups with an anchor element don't
     * hide when the anchor loses visibility i.e. the Hello icon moves into the
     * overflow pallet (bug 1109868).
     */
    HelloFTU.handleResize = function() {
        clearTimeout(_highlightTimeout);
        if (!HelloFTU.highlightSupressed) {
            HelloFTU.hideUITourHighlights();
            HelloFTU.highlightSupressed = true;
        }
        _highlightTimeout = setTimeout(function() {
            HelloFTU.highlightSupressed = false;
            HelloFTU.showTourStep();
        }, 300);
    };

    HelloFTU.trackRoomShareButton = function(button) {
        HelloFTU.tourStep = 'shared';
        HelloFTU.showTourStep();
        window.dataLayer.push({
            'event': 'hello-interactions',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': button
        });
    };

    HelloFTU.bindPageEvents = function() {
        $(window).on('resize.hello', HelloFTU.handleResize);
        $(document).on('visibilitychange.hello', HelloFTU.handleVisibilityChange);
    };

    /**
     * Binds an event handler for receiving custom events from the Loop client.
     */
    HelloFTU.bindHelloEvents = function() {
        Mozilla.UITour.observe(HelloFTU.handleHelloEvents);
    };

    /**
     * Stop receiving custom events from the Loop client.
     */
    HelloFTU.unbindHelloEvents = function() {
        Mozilla.UITour.observe(null);
    };

    /**
     * Processes custom events received from the Loop client.
     */
    HelloFTU.handleHelloEvents = function(event, data) {
        switch(event) {
        case 'Loop:ChatWindowOpened':
            HelloFTU.onChatWindowOpened();
            break;
        case 'Loop:ChatWindowClosed':
            HelloFTU.hideUITourHighlights();
            break;
        case 'Loop:ChatWindowHidden':
            HelloFTU.hideUITourHighlights();
            break;
        case 'Loop:ChatWindowDetached':
            HelloFTU.hideUITourHighlights();
            break;
        case 'Loop:IncomingConversation':
            HelloFTU.onIncomingConversation(data);
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
        case 'Loop:PanelTabChanged':
            // hide info panels if user switches to the Contacts tab in the Hello panel
            if (data && data === 'contacts') {
                Mozilla.UITour.hideInfo();
            }
        }
    };

    HelloFTU.onIncomingConversation = function(data) {
        if (!data) {
            throw new Error('onIncomingConversation: no data was passed from the event handler.');
        }

        if (data.conversationOpen === true) {
            HelloFTU.onConversationOpen();
        } else if (data.conversationOpen === false) {
            HelloFTU.onConversationWaiting();
        }
    };

    HelloFTU.onConversationWaiting = function() {
        HelloFTU.tourStep = 'conversation-waiting';
        HelloFTU.showTourStep();
    };

    HelloFTU.onConversationOpen = function() {
        HelloFTU.tourStep = 'conversation-open';
        HelloFTU.hideUITourHighlights();
        HelloFTU.showPageState('end', true);
        HelloFTU.trackGAConversationConnect();
    };

    /**
     * Event handler for when the Loop chat window is opened by the user.
     * The first time this is called we assume "Get Started" has been clicked
     * in the Hello panel, and the user has interacted with the tour.
     */
    HelloFTU.onChatWindowOpened = function() {

        switch(HelloFTU.tourStep) {
        case 'get-started':
            HelloFTU.tourStep = 'invite';
            HelloFTU.showTourStep();
            HelloFTU.resumeTourOnFirstJoin();
            HelloFTU.setTourSourceToStorage(HelloFTU.tourSource);

            window.dataLayer.push({
                'event': 'hello-interactions',
                'category': '/hello/start interactions',
                'location': 'tour',
                'browserAction': 'StartConversation-Tour'
            });
            break;
        case 'invite':
            HelloFTU.showTourStep();
            break;
        case 'conversation-waiting':
            HelloFTU.onConversationOpen();
            // set param to done, so if the user shares the URL
            // the next person can still take the tour from the start.
            HelloFTU.replaceURLState('waiting', 'done');
            break;
        }
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
     */
    HelloFTU.trackTourSource = function() {
        HelloFTU.tourSource = HelloFTU.getTourSource();
        window.dataLayer.push({
            'event': 'hello-interactions-referral',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': 'GetStarted',
            'helloFTUReferral': HelloFTU.tourSource
        });
    };

    // GA event for successful Hello conversations
    HelloFTU.trackGAConversationConnect = function() {
        // get source from localStorage
        var tourSource = HelloFTU.getTourSourceFromStorage();
        window.dataLayer.push({
            'event': 'hello-interactions',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': 'TourConnectConversation',
            'helloFTUReferral': tourSource
        });
        try {
            localStorage.removeItem('hello_ftu_tour_source');
        } catch (ex) { }
    };

    HelloFTU.getTourSourceFromStorage = function() {
        var source;
        try {
            source = localStorage.getItem('hello_ftu_tour_source');
        } catch (ex) {
            source = 'none';
        }
        return source;
    };

    // Save the tourSource to localStorage for use in conversation connect
    HelloFTU.setTourSourceToStorage = function(tourSource) {
        try {
            localStorage.setItem('hello_ftu_tour_source', tourSource);
        } catch (ex) { }
    };

    window.Mozilla.HelloFTU = HelloFTU;

})(window.jQuery);
