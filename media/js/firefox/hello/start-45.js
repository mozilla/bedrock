/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 /* globals Promise */

(function($, Mozilla) {
    'use strict';

    var $window = $(window);
    var $document = $(document);
    var client = Mozilla.Client;
    var params = new window._SearchParams();
    // if URL query param noopenpanel=1 exists then don't open the Hello menu.
    var shouldOpenPanel = params.get('noopenpanel') === 1 ? false : true;
    var chatWindowOpened = false;

    /**
     * Queries the icon targets available to UITour.
     * @returns Promise (resolve) Array of available targets.
     */
    function getAvailableTargets() {
        return new Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('availableTargets', function(config) {
                if (config && config.targets) {
                    resolve(config.targets);
                } else {
                    reject('UITour: targets property not found.');
                }
            });
        });
    }

    function openHelloMenu() {
        Mozilla.UITour.showMenu('loop', function() {
            $document.one('click.hello', closeHelloMenu);
            $window.one('resize.hello', closeHelloMenu);
            $document.on('visibilitychange.hello', handleVisibilityChange);
        });
    }

    function closeHelloMenu() {
        Mozilla.UITour.hideMenu('loop');
        $document.off('click.hello');
        $document.off('visibilitychange.hello');
        $window.off('resize.hello');
    }

    function trackInteraction(action) {
        window.dataLayer.push({
            'event': 'hello-interactions',
            'category': '/hello/start interactions',
            'location': 'tour',
            'browserAction': action
        });
    }

    function handleHelloEvents(event) {
        switch(event) {
        case 'Loop:ChatWindowOpened':
            // track in GA the first time the chat window is opened.
            if (!chatWindowOpened) {
                trackInteraction('StartConversation-Tour');
                chatWindowOpened = true;
            }
            break;
        case 'Loop:RoomURLCopied':
            trackInteraction('URLCopied-Tour');
            break;
        case 'Loop:RoomURLEmailed':
            trackInteraction('URLEmailed-Tour');
            break;
        case 'Loop:RoomURLShared':
            trackInteraction('URLShared-Tour');
            break;
        }
    }

    function bindHelloEvents() {
        Mozilla.UITour.observe(handleHelloEvents);
    }

    function unbindHelloEvents() {
        Mozilla.UITour.observe(null);
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            closeHelloMenu();
            unbindHelloEvents();
        } else {
            bindHelloEvents();
        }
    }


    if (client.isFirefoxDesktop && shouldOpenPanel) {
        getAvailableTargets().then(function(targets) {
            // Only open the Hello menu if target is in the user pallet.
            if (targets && targets.indexOf('loop') > -1) {
                openHelloMenu();
                bindHelloEvents();
                trackInteraction('GetStarted');
            }
        });
    }

})(window.jQuery, window.Mozilla);
