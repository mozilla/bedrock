/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var $main = $('main');
    var $defaultCopy = $('.default');
    var $startCopy = $('.start');
    var $endCopy = $('.end');

    var highlightTimeout;
    var highlightsSupressed = false;
    var tourStep = 'default';
    var tourSource = getParameterByName('utm_content').replace('hello-tour_OpenPanel_','');

    /*
     * Strips HTML from string to make sure markup
     * does not get injected in any UITour door-hangers.
     * @param string (data attribute string)
     */
    function _getText(string) {
        return $('<div/>').html(window.trans(string)).text();
    }

    // GA event for successful Hello conversations
    function trackGAConversationConnect() {
        // get source from localStorage
        try {
            tourSource = localStorage.getItem('hello_ftu_tour_source');
        } catch (ex) {
            tourSource = 'none';
        }
        gaTrack(['_setCustomVar', 13, 'Hello FTU Referral', tourSource, 2]);
        gaTrack(['_trackEvent', '/hello/start interactions', 'tour', 'TourConnectConversation']);
        try {
            localStorage.removeItem('hello_ftu_tour_source');
        } catch (ex) { }
    }

    // Save the tourSource to localStorage for use in conversation connect
    function saveTourSourceToLocalStorage() {
        try {
            localStorage.setItem('hello_ftu_tour_source', tourSource);
        } catch (ex) { }
    }

    // Get query string parameters
    function getParameterByName(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)'),
            results = regex.exec(location.search);
        return results === null ? 'none' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    /*
     * Tells Firefox to re-connect to the FTE tour when user has their first conversation.
     * We do this only once the user has interacted with the FTE.
     */
    function resumeTourOnFirstJoin() {
        Mozilla.UITour.setConfiguration('Loop:ResumeTourOnFirstJoin', true);
    }

    // Close any open menus and hide info panels
    function hideUITourHighlights() {
        Mozilla.UITour.hideInfo();
        Mozilla.UITour.hideMenu('loop');
    }

    // hide and reshow tour highlights on tab visibility
    function handleVisibilityChange() {
        if (document.hidden) {
            hideUITourHighlights();
            unbindHelloEvents();
        } else {
            clearTimeout(highlightTimeout);
            bindHelloEvents();
            highlightTimeout = setTimeout(showTourStep, 900);
        }
    }

    // hide and reshow tour highlights on page resize
    function handleResize() {
        clearTimeout(highlightTimeout);
        if (!highlightsSupressed) {
            hideUITourHighlights();
            highlightsSupressed = true;
        }
        highlightTimeout = setTimeout(function() {
            highlightsSupressed = false;
            showTourStep();
        }, 300);
    }

    // Shows the current step of the FTE tour
    function showTourStep() {
        switch(tourStep) {
        case 'get-started':
            showHelloPanel(highlightNewRoomButton);
            break;
        case 'invite':
            targetConversationView(highlightSelectedRoomButtons);
            break;
        case 'shared':
            targetConversationView(showSharedInfoPanel);
            break;
        case 'conversation-waiting':
            showHelloPanel(highlightRoomList);
            break;
        case 'conversation-open':
            showPageState('end', true);
            break;
        }
    }

    /*
     * Show FTE web page copy state
     * @param state (string)
     * @param anim (boolean)
     */
    function showPageState(state, anim) {
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
    }

    /*
     * Show the Hello panel and trigger callback once opening animation finishes
     * @param callback (function)
     */
    function showHelloPanel(callback) {
        // Only open the info panel if tab is visible
        if (document.hidden) {
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
    }

    // Highlights Hello panel target.
    function highlightNewRoomButton() {
        Mozilla.UITour.showInfo(
            'loop-newRoom',
            _getText('getStartedTitle'),
            _getText('getStartedText')
        );
    }

    // Highlights Hello room list when a conversation is waiting.
    function highlightRoomList() {
        Mozilla.UITour.showInfo(
            'loop-roomList',
            _getText('roomListTitle'),
            _getText('roomListText')
        );
    }

    /*
     * Determine if conversation view and room button targets are visible
     * @param callback (function) to excecute if target is available
     */
    function targetConversationView(callback) {
        // Only open the info panel if tab is visible
        if (document.hidden) {
            return;
        }

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop-selectedRoomButtons', config.targets) !== -1) {
                if (typeof callback === 'function') {
                    callback();
                }
            }
        });
    }

    // Add door-hanger to selected room buttons in conversation view
    function highlightSelectedRoomButtons() {
        Mozilla.UITour.showInfo(
            'loop-selectedRoomButtons',
            _getText('inviteTitle'),
            _getText('inviteText')
        );
    }

    // Add door-hanger to conversation view once room has been copied/shared
    function showSharedInfoPanel() {
        Mozilla.UITour.showInfo(
            'loop-selectedRoomButtons',
            _getText('sharedTitle'),
            _getText('sharedText')
        );
    }

    // register for Hello UITour events
    function bindHelloEvents() {
        Mozilla.UITour.observe(function(event, data) {

            switch(event) {
            case 'Loop:ChatWindowOpened':
                // only show invite step if conversation is not waiting
                if (tourStep === 'get-started') {

                    tourStep = 'invite';
                    showTourStep();

                    // User has interacted with FTE, so tell Firefox to resume
                    // when they have their first conversation.
                    resumeTourOnFirstJoin();

                    // track user has clicked "Start a conversation" button
                    gaTrack(['_trackEvent', '/hello/start interactions', 'tour', 'StartConversation-Tour']);

                } if (tourStep === 'invite') {

                    showTourStep();
                } else if (tourStep === 'conversation-waiting') {

                    tourStep = 'conversation-open';
                    showTourStep();
                    // set param to done, so if the user shares the URL
                    // the next person can still take the tour from the start.
                    replaceURLState('waiting', 'done');
                    // track conversation connect
                    trackGAConversationConnect();
                }
                break;
            case 'Loop:ChatWindowClosed':
                hideUITourHighlights();
                break;
            case 'Loop:ChatWindowHidden':
                hideUITourHighlights();
                break;
            case 'Loop:ChatWindowDetached':
                hideUITourHighlights();
                break;
            case 'Loop:IncomingConversation':
                if (data && data.conversationOpen === true) {
                    tourStep = 'conversation-open';

                    hideUITourHighlights();
                    showPageState('end', true);

                    // track conversation connect
                    trackGAConversationConnect();

                } else if (data && data.conversationOpen === false) {
                    tourStep = 'conversation-waiting';
                    showHelloPanel(highlightRoomList);
                }
                break;
            case 'Loop:RoomURLCopied':
                tourStep = 'shared';
                showTourStep();
                saveTourSourceToLocalStorage();
                // track user has clicked copy button
                gaTrack(['_trackEvent', '/hello/start interactions', 'tour', 'URLCopied-Tour']);
                break;
            case 'Loop:RoomURLEmailed':
                tourStep = 'shared';
                showTourStep();
                saveTourSourceToLocalStorage();
                // track user has clicked email button
                gaTrack(['_trackEvent', '/hello/start interactions', 'tour', 'URLEmailed-Tour']);
                break;
            case 'Loop:PanelTabChanged':
                // hide info panels if user switches to the Contacts tab in the Hello panel
                if (data && data === 'contacts') {
                    Mozilla.UITour.hideInfo();
                }
            }

        }, function () {
            // ping callback, nothing to actually do here!
        });
    }

    // Stop listening for UITour Hello events
    function unbindHelloEvents() {
        Mozilla.UITour.observe(null);
    }

    /*
     * Sets incomingConversation URL param to 'done' using replaceState
     * @param currentValue to be replaced (string)
     * @param newValue (string)
    */
    function replaceURLState(currentValue, newValue) {
        var url = window.location.href;
        var currentParam;

        if (!currentValue || !newValue) {
            return;
        }

        currentParam = 'incomingConversation=' + currentValue;

        if (url.indexOf(currentParam) !== -1) {
            url = url.replace(currentParam, 'incomingConversation=' + newValue);
            window.history.replaceState({}, '', url);
        }
    }

    function init() {
        // URL query param populated at template level in the view
        var incomingConversation = getParameterByName('incomingConversation');

        // set the tour state based on incomingConversation status
        switch(incomingConversation) {
        case 'none':
            tourStep = 'get-started';
            break;
        case 'done':
            tourStep = 'get-started';
            break;
        case 'waiting':
            tourStep = 'conversation-waiting';
            break;
        case 'open':
            tourStep = 'conversation-open';
            break;
        }

        // Make sure that the Hello icon is an available target in the UI.
        // Hello is still referred to as 'loop' internally for legacy reasons.
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray('loop', config.targets) !== -1) {

                // hide and reshow uitour highlights on resize
                $(window).on('resize', handleResize);

                // hide and reshow uitour highlights page visibility
                $(document).on('visibilitychange', handleVisibilityChange);

                if (tourStep === 'conversation-open') {
                    // conversation is open and rooms view is visible,
                    // so show the page end state. Job done! \o/
                    showPageState('end');
                    // set incomingConversation URL param to 'done'
                    replaceURLState('open', 'done');
                    // track conversation connect
                    trackGAConversationConnect();
                } else {
                    // show the first page copy state
                    showPageState('start');

                    // track start of tour in GA
                    if (tourStep === 'get-started') {
                        // Get referrer and set Custom Variable. none is okay here.
                        gaTrack(['_setCustomVar', 13, 'Hello FTU Referral', tourSource, 2]);
                        gaTrack(['_trackEvent', '/hello/start interactions', 'tour', 'GetStarted']);
                    }
                }

                // register for Hello events
                bindHelloEvents();

                // show tour step highlight
                showTourStep();
            }
        });
    }

    // use a slight delay for showing the main page content
    // to allow for initial page state to be determined
    setTimeout(function () {
        $main.css('visibility', 'visible');
    }, 500);

    // FTE will only run on Firefox Desktop 35 and above
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 35) {
        init();
    }

})(window.jQuery, window.Mozilla);
