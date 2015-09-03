/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, jasmine */

describe('hello-ftu.js', function() {

    'use strict';

    var clock;

    beforeEach(function() {
        // use fake timers to make tests easier
        clock = sinon.useFakeTimers();

        // stub out Mozilla.UITour
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.showMenu = sinon.stub();
        Mozilla.UITour.hideMenu = sinon.stub();
        Mozilla.UITour.showInfo = sinon.stub();
        Mozilla.UITour.hideInfo = sinon.stub();
        Mozilla.UITour.observe = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();
        Mozilla.UITour.setConfiguration = sinon.stub();
        Mozilla.HelloFTU.documentHidden = null;
        Mozilla.HelloFTU.highlightSupressed = false;
        Mozilla.HelloFTU.tourStep = 'none';
        Mozilla.HelloFTU.tourSource = 'none';

        spyOn(Mozilla.UITour, 'showMenu').and.callFake(function(target, callback) {
            callback();
        });
    });

    afterEach(function() {
        Mozilla.HelloFTU.unbindHelloEvents();
        Mozilla.HelloFTU.documentHidden = null;
        Mozilla.HelloFTU.highlightSupressed = false;
        Mozilla.HelloFTU.tourStep = 'none';
        Mozilla.HelloFTU.tourSource = 'none';
        clock.restore();
    });

    describe('init', function () {

        beforeEach(function() {
            spyOn(Mozilla.HelloFTU, 'getInitialTourStep').and.callFake(function() {
                return 'get-started';
            });
            spyOn(Mozilla.HelloFTU, 'setInitialPageState');
            spyOn(Mozilla.HelloFTU, 'bindPageEvents');
            spyOn(Mozilla.HelloFTU, 'bindHelloEvents');
            spyOn(Mozilla.HelloFTU, 'trackTourSource');
            spyOn(Mozilla.HelloFTU, 'showTourStep');
        });

        it('should initialize FTU if loop target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            });
            Mozilla.HelloFTU.init();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.HelloFTU.setInitialPageState).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindPageEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.trackTourSource).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.tourStep).toEqual('get-started');
        });

        it('should not initialize FTU if loop target unavailable', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HelloFTU.init();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.HelloFTU.setInitialPageState).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindPageEvents).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.trackTourSource).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showTourStep).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.tourStep).toEqual('none');
        });
    });

    describe('getInitialTourStep', function() {

        it('should identify the start of the tour correctly', function() {
            spyOn(Mozilla.HelloFTU, 'getParameterByName').and.callFake(function() {
                return 'none';
            });
            var result = Mozilla.HelloFTU.getInitialTourStep();
            expect(result).toEqual('get-started');
        });

        it('should identify when a conversation is waiting', function() {
            spyOn(Mozilla.HelloFTU, 'getParameterByName').and.callFake(function() {
                return 'waiting';
            });
            var result = Mozilla.HelloFTU.getInitialTourStep();
            expect(result).toEqual('conversation-waiting');
        });

        it('should identify when a conversation is open', function() {
            spyOn(Mozilla.HelloFTU, 'getParameterByName').and.callFake(function() {
                return 'open';
            });
            var result = Mozilla.HelloFTU.getInitialTourStep();
            expect(result).toEqual('conversation-open');
        });
    });

    describe('setInitialPageState', function() {

        beforeEach(function() {
            spyOn(Mozilla.HelloFTU, 'showPageState');
            spyOn(Mozilla.HelloFTU, 'replaceURLState');
            spyOn(Mozilla.HelloFTU, 'trackGAConversationConnect');
        });

        it('should show the page start state correctly', function() {
            Mozilla.HelloFTU.setInitialPageState();
            expect(Mozilla.HelloFTU.showPageState).toHaveBeenCalledWith('start');
        });

        it('should show the page end state correctly', function() {
            Mozilla.HelloFTU.tourStep = 'conversation-open';
            Mozilla.HelloFTU.setInitialPageState();
            expect(Mozilla.HelloFTU.showPageState).toHaveBeenCalledWith('end');
            expect(Mozilla.HelloFTU.replaceURLState).toHaveBeenCalledWith('open', 'done');
            expect(Mozilla.HelloFTU.trackGAConversationConnect).toHaveBeenCalled();
        });
    });

    describe('showHelloPanel', function () {

        it('should open Hello panel if loop target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            });
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).toHaveBeenCalled();
        });

        it('should not open Hello panel if loop target unavailable', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).not.toHaveBeenCalled();
        });

        it('should excecute callback after opening Hello panel if supplied', function() {
            var foo = {
                callback: function() {}
            };
            spyOn(foo, 'callback');
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            });
            Mozilla.HelloFTU.showHelloPanel(foo.callback);
            expect(foo.callback).toHaveBeenCalled();
        });

        it('should not open Hello panel if document is hidden', function() {
            Mozilla.HelloFTU.documentHidden = true;
            spyOn(Mozilla.UITour, 'getConfiguration').and.callThrough();
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).not.toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).not.toHaveBeenCalled();
        });
    });

    describe('hideUITourHighlights', function() {

        it('should hide UITour panels as expected', function() {
            spyOn(Mozilla.UITour, 'hideInfo');
            spyOn(Mozilla.UITour, 'hideMenu');
            Mozilla.HelloFTU.hideUITourHighlights();
            expect(Mozilla.UITour.hideInfo).toHaveBeenCalled();
            expect(Mozilla.UITour.hideMenu).toHaveBeenCalledWith('loop');
        });
    });

    describe('highlightNewRoomButton', function() {

        it('should open an info panel on the expected target', function() {
            spyOn(Mozilla.UITour, 'showInfo');
            spyOn(Mozilla.HelloFTU, 'getText').and.callFake(function() {
                return 'foo';
            });
            Mozilla.HelloFTU.highlightNewRoomButton();
            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('loop-newRoom', 'foo', 'foo');
        });
    });

    describe('highlightRoomList', function() {

        it('should open an info panel on the expected target', function() {
            spyOn(Mozilla.UITour, 'showInfo');
            spyOn(Mozilla.HelloFTU, 'getText').and.callFake(function() {
                return 'foo';
            });
            Mozilla.HelloFTU.highlightRoomList();
            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('loop-roomList', 'foo', 'foo');
        });
    });

    describe('highlightSelectedRoomButtons', function() {

        it('should open an info panel on the expected target', function() {
            spyOn(Mozilla.UITour, 'showInfo');
            spyOn(Mozilla.HelloFTU, 'getText').and.callFake(function() {
                return 'foo';
            });
            Mozilla.HelloFTU.highlightSelectedRoomButtons();
            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('loop-selectedRoomButtons', 'foo', 'foo');
        });
    });

    describe('showSharedInfoPanel', function() {

        it('should open an info panel on the expected target', function() {
            spyOn(Mozilla.UITour, 'showInfo');
            spyOn(Mozilla.HelloFTU, 'getText').and.callFake(function() {
                return 'foo';
            });
            Mozilla.HelloFTU.showSharedInfoPanel();
            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('loop-selectedRoomButtons', 'foo', 'foo');
        });
    });

    describe('targetConversationView', function() {

        it('should excecute callback if the target is available', function() {
            var foo = {
                callback: function() {}
            };
            spyOn(foo, 'callback');
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop-selectedRoomButtons']
                });
            });
            Mozilla.HelloFTU.targetConversationView(foo.callback);
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(foo.callback).toHaveBeenCalled();
        });

        it('should not excecute callback if target is not available', function() {
            var foo = {
                callback: function() {}
            };
            spyOn(foo, 'callback');
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HelloFTU.targetConversationView(foo.callback);
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(foo.callback).not.toHaveBeenCalled();
        });

        it('should not excecute callback if document is hidden', function() {
            var foo = {
                callback: function() {}
            };
            spyOn(foo, 'callback');
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop-selectedRoomButtons']
                });
            });
            Mozilla.HelloFTU.documentHidden = true;
            Mozilla.HelloFTU.targetConversationView(foo.callback);
            expect(Mozilla.UITour.getConfiguration).not.toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(foo.callback).not.toHaveBeenCalled();
        });
    });

    describe('getText', function() {

        it ('should strip HTML from the queried string', function() {
            spyOn(window, 'trans').and.callFake(function() {
                return 'Hello <strong>hello</strong>';
            });
            var result = Mozilla.HelloFTU.getText('someID');
            expect(result).toEqual('Hello hello');
        });
    });

    describe('resumeTourOnFirstJoin', function() {

        it('should call setConfiguration as expected', function() {
            spyOn(Mozilla.UITour, 'setConfiguration');
            Mozilla.HelloFTU.resumeTourOnFirstJoin();
            expect(Mozilla.UITour.setConfiguration).toHaveBeenCalledWith('Loop:ResumeTourOnFirstJoin', true);
        });
    });

    describe('showTourStep', function() {

        beforeEach(function() {
            spyOn(Mozilla.HelloFTU, 'showHelloPanel');
            spyOn(Mozilla.HelloFTU, 'targetConversationView');
        });

        it('should handle "get-started" tour step correctly', function() {
            Mozilla.HelloFTU.tourStep = 'get-started';
            Mozilla.HelloFTU.showTourStep();
            expect(Mozilla.HelloFTU.showHelloPanel).toHaveBeenCalledWith(Mozilla.HelloFTU.highlightNewRoomButton);
        });

        it('should handle "invite" tour step correctly', function() {
            Mozilla.HelloFTU.tourStep = 'invite';
            Mozilla.HelloFTU.showTourStep();
            expect(Mozilla.HelloFTU.targetConversationView).toHaveBeenCalledWith(Mozilla.HelloFTU.highlightSelectedRoomButtons);
        });

        it('should handle "shared" tour step correctly', function() {
            Mozilla.HelloFTU.tourStep = 'shared';
            Mozilla.HelloFTU.showTourStep();
            expect(Mozilla.HelloFTU.targetConversationView).toHaveBeenCalledWith(Mozilla.HelloFTU.showSharedInfoPanel);
        });

        it('should handle "conversation-waiting" tour step correctly', function() {
            Mozilla.HelloFTU.tourStep = 'conversation-waiting';
            Mozilla.HelloFTU.showTourStep();
            expect(Mozilla.HelloFTU.showHelloPanel).toHaveBeenCalledWith(Mozilla.HelloFTU.highlightRoomList);
        });
    });

    describe('replaceURLState', function() {

        it('should replace current the page URL as expected', function() {
            spyOn(window.history, 'replaceState');
            Mozilla.HelloFTU.replaceURLState('open', 'done', '?incomingConversation=open');
            expect(window.history.replaceState).toHaveBeenCalledWith({}, '', '?incomingConversation=done');
        });
    });

    describe('handleVisibilityChange', function() {

        beforeEach(function() {
            spyOn(Mozilla.HelloFTU, 'showTourStep');
            spyOn(Mozilla.HelloFTU, 'bindHelloEvents');
            spyOn(Mozilla.HelloFTU, 'unbindHelloEvents');
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
        });

        it('should hide UITour highlights when document is hidden', function() {
            Mozilla.HelloFTU.documentHidden = true;
            Mozilla.HelloFTU.handleVisibilityChange();
            expect(Mozilla.HelloFTU.unbindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showTourStep).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).not.toHaveBeenCalled();
        });

        it('should show tour step when document is visible', function() {
            Mozilla.HelloFTU.documentHidden = false;
            Mozilla.HelloFTU.handleVisibilityChange();
            clock.tick(1000);
            expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.unbindHelloEvents).not.toHaveBeenCalled();
        });
    });

    describe('handleResize', function() {

        it('should hide and then reshow UITour panels on resize', function() {
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
            spyOn(Mozilla.HelloFTU, 'showTourStep');
            Mozilla.HelloFTU.handleResize();
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.highlightSupressed).toEqual(true);
            expect(Mozilla.HelloFTU.showTourStep).not.toHaveBeenCalled();
            clock.tick(400);
            expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.highlightSupressed).toEqual(false);
        });
    });

    describe('trackRoomShareButton', function () {

        it('should ackknowledge that a room was shared', function() {
            spyOn(Mozilla.HelloFTU, 'showTourStep');
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.trackRoomShareButton('foo');
            expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.tourStep).toEqual('shared');
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'hello-interactions',
                'category': '/hello/start interactions',
                'location': 'tour',
                'browserAction': 'foo'
            });
        });
    });

    describe('bindPageEvents', function () {

        it('should bind page visibility event listener', function() {
            spyOn($.fn, 'on');
            Mozilla.HelloFTU.bindPageEvents();
            expect($.fn.on).toHaveBeenCalledWith('resize.hello', Mozilla.HelloFTU.handleResize);
            expect($.fn.on).toHaveBeenCalledWith('visibilitychange.hello', Mozilla.HelloFTU.handleVisibilityChange);
        });
    });

    describe('bindHelloEvents', function () {

        it('should bind UITour observe event listener', function() {
            spyOn(Mozilla.UITour, 'observe');
            Mozilla.HelloFTU.bindHelloEvents();
            expect(Mozilla.UITour.observe).toHaveBeenCalled();
        });
    });


    describe('unbindHelloEvents', function () {

        it('should unbind UITour observe event listener', function() {
            spyOn(Mozilla.UITour, 'observe');
            Mozilla.HelloFTU.unbindHelloEvents();
            expect(Mozilla.UITour.observe).toHaveBeenCalledWith(null);
        });
    });

    describe('handleHelloEvents', function () {

        it('should handle Loop:ChatWindowOpened correctly', function() {
            spyOn(Mozilla.HelloFTU, 'onChatWindowOpened');
            Mozilla.HelloFTU.handleHelloEvents('Loop:ChatWindowOpened');
            expect(Mozilla.HelloFTU.onChatWindowOpened).toHaveBeenCalled();
        });

        it('should handle Loop:ChatWindowClosed correctly', function() {
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
            Mozilla.HelloFTU.handleHelloEvents('Loop:ChatWindowClosed');
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
        });

        it('should handle Loop:ChatWindowHidden correctly', function() {
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
            Mozilla.HelloFTU.handleHelloEvents('Loop:ChatWindowHidden');
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
        });

        it('should handle Loop:ChatWindowDetached correctly', function() {
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
            Mozilla.HelloFTU.handleHelloEvents('Loop:ChatWindowDetached');
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
        });

        it('should handle Loop:IncomingConversation correctly', function() {
            spyOn(Mozilla.HelloFTU, 'onIncomingConversation');
            Mozilla.HelloFTU.handleHelloEvents('Loop:IncomingConversation', 'foo');
            expect(Mozilla.HelloFTU.onIncomingConversation).toHaveBeenCalledWith('foo');
        });

        it('should handle Loop:RoomURLCopied correctly', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLCopied');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLCopied-Tour');
        });

        it('should handle Loop:RoomURLEmailed correctly', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLEmailed');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLEmailed-Tour');
        });

        it('should handle Loop:RoomURLShared correctly', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLShared');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLShared-Tour');
        });

        it('should handle Loop:PanelTabChanged correctly', function() {
            spyOn(Mozilla.UITour, 'hideInfo');
            Mozilla.HelloFTU.handleHelloEvents('Loop:PanelTabChanged', 'contacts');
            expect(Mozilla.UITour.hideInfo).toHaveBeenCalled();
        });
    });

    describe('onIncomingConversation', function() {

        it('should throw an error if no data was passed', function() {
            expect(function() {
                Mozilla.HelloFTU.onIncomingConversation();
            }).toThrowError('onIncomingConversation: no data was passed from the event handler.');
        });

        it('should respond correctly when a conversation is waiting', function() {
            var data = {
                conversationOpen: false
            };
            spyOn(Mozilla.HelloFTU, 'onConversationWaiting');
            Mozilla.HelloFTU.onIncomingConversation(data);
            expect(Mozilla.HelloFTU.onConversationWaiting).toHaveBeenCalled();
        });

        it('should respond correctly when a conversation is open', function() {
            var data = {
                conversationOpen: true
            };
            spyOn(Mozilla.HelloFTU, 'onConversationOpen');
            Mozilla.HelloFTU.onIncomingConversation(data);
            expect(Mozilla.HelloFTU.onConversationOpen).toHaveBeenCalled();
        });
    });

    describe('onConversationWaiting', function() {

        it('should show the correct tour step', function() {
            spyOn(Mozilla.HelloFTU, 'showTourStep');
            Mozilla.HelloFTU.onConversationWaiting();
            expect(Mozilla.HelloFTU.tourStep).toEqual('conversation-waiting');
            expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
        });
    });

    describe('onConversationOpen', function() {

        it('should show the correct tour step', function() {
            spyOn(Mozilla.HelloFTU, 'hideUITourHighlights');
            spyOn(Mozilla.HelloFTU, 'showPageState');
            spyOn(Mozilla.HelloFTU, 'trackGAConversationConnect');
            Mozilla.HelloFTU.onConversationOpen();
            expect(Mozilla.HelloFTU.tourStep).toEqual('conversation-open');
            expect(Mozilla.HelloFTU.hideUITourHighlights).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showPageState).toHaveBeenCalledWith('end', true);
            expect(Mozilla.HelloFTU.trackGAConversationConnect).toHaveBeenCalled();
        });
    });

    describe('onChatWindowOpened', function () {

        describe('get-started', function() {

            it('should proceed to "Invite" tour step', function() {
                spyOn(Mozilla.HelloFTU, 'showTourStep');
                spyOn(Mozilla.HelloFTU, 'resumeTourOnFirstJoin');
                spyOn(Mozilla.HelloFTU, 'setTourSourceToStorage');
                spyOn(window.dataLayer, 'push');
                Mozilla.HelloFTU.tourStep = 'get-started';
                Mozilla.HelloFTU.onChatWindowOpened();
                expect(Mozilla.HelloFTU.tourStep).toEqual('invite');
                expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
                expect(Mozilla.HelloFTU.resumeTourOnFirstJoin).toHaveBeenCalled();
                expect(Mozilla.HelloFTU.setTourSourceToStorage).toHaveBeenCalled();
                expect(window.dataLayer.push).toHaveBeenCalledWith({
                    'event': 'hello-interactions',
                    'category': '/hello/start interactions',
                    'location': 'tour',
                    'browserAction': 'StartConversation-Tour'
                });
            });
        });

        describe('invite', function() {

            it('should show the tour step correctly', function() {
                spyOn(Mozilla.HelloFTU, 'showTourStep');
                Mozilla.HelloFTU.tourStep = 'invite';
                Mozilla.HelloFTU.onChatWindowOpened();
                expect(Mozilla.HelloFTU.showTourStep).toHaveBeenCalled();
            });
        });

        describe('conversation-waiting', function() {

            it('should proceed to the end of the tour', function() {
                spyOn(Mozilla.HelloFTU, 'onConversationOpen');
                spyOn(Mozilla.HelloFTU, 'replaceURLState');
                Mozilla.HelloFTU.tourStep = 'conversation-waiting';
                Mozilla.HelloFTU.onChatWindowOpened();
                expect(Mozilla.HelloFTU.onConversationOpen).toHaveBeenCalled();
                expect(Mozilla.HelloFTU.replaceURLState).toHaveBeenCalledWith('waiting', 'done');
            });
        });
    });

    describe('getParameterByName', function () {

        it('should return the supplied parameter value', function() {
            var url = '/hello/start/?utm_source=firefox-browser&utm_medium=firefox-browser&utm_campaign=settings-menu&utm_content=hello-tour_OpenPanel_snippet';
            var result = Mozilla.HelloFTU.getParameterByName('utm_content', url);
            expect(result).toEqual('hello-tour_OpenPanel_snippet');
        });

        it('should return "none" if parameter is omitted', function() {
            var url = '/hello/start/?utm_source=firefox-browser&utm_medium=firefox-browser&utm_campaign=settings-menu';
            var result = Mozilla.HelloFTU.getParameterByName('utm_content', url);
            expect(result).toEqual('none');
        });
    });

    describe('getTourSource', function () {

        it('should return the supplied parameter value', function() {
            var url = '/hello/start/?utm_source=firefox-browser&utm_medium=firefox-browser&utm_campaign=settings-menu&utm_content=hello-tour_OpenPanel_snippet';
            var result = Mozilla.HelloFTU.getTourSource(url);
            expect(result).toEqual('snippet');
        });
    });

    describe('trackTourSource', function () {

        it('should track tour source in GTM', function() {
            spyOn(Mozilla.HelloFTU, 'getTourSource').and.callFake(function() {
                return 'snippet';
            });
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.trackTourSource('snippet');
            expect(Mozilla.HelloFTU.getTourSource).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.tourSource).toEqual('snippet');
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'hello-interactions-referral',
                'category': '/hello/start interactions',
                'location': 'tour',
                'browserAction': 'GetStarted',
                'helloFTUReferral': 'snippet'
            });
        });
    });

    describe('trackGAConversationConnect', function() {

        it('should should track tour conversion source in GA', function() {
            spyOn(window.dataLayer, 'push');
            spyOn(Mozilla.HelloFTU, 'getTourSourceFromStorage').and.callFake(function() {
                return 'snippet';
            });
            Mozilla.HelloFTU.trackGAConversationConnect();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'hello-interactions',
                'category': '/hello/start interactions',
                'location': 'tour',
                'browserAction': 'TourConnectConversation',
                'helloFTUReferral': 'snippet'
            });
        });
    });
});
