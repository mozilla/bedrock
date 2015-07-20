/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, jasmine */

describe('hello-ftu-minimal.js', function() {

    'use strict';

    var clock;

    beforeEach(function() {
        // use fake timers to make tests easier
        clock = sinon.useFakeTimers();

        // stub out Mozilla.UITour
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.showMenu = sinon.stub();
        Mozilla.UITour.hideMenu = sinon.stub();
        Mozilla.UITour.observe = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();

        Mozilla.HelloFTU.documentHidden = null;
        Mozilla.HelloFTU.getStartedClicked = false;
        Mozilla.HelloFTU.helloPanelVisible = false;

        spyOn(Mozilla.UITour, 'showMenu').and.callFake(function(target, callback) {
            callback();
        });
    });

    afterEach(function() {
        Mozilla.HelloFTU.unbindHelloEvents();

        Mozilla.HelloFTU.documentHidden = null;
        Mozilla.HelloFTU.getStartedClicked = false;
        Mozilla.HelloFTU.helloPanelVisible = false;

        //restore timers
        clock.restore();
    });

    describe('init', function () {

        beforeEach(function() {
            spyOn(Mozilla.UITour, 'observe').and.callThrough();
            spyOn(Mozilla.HelloFTU, 'showHelloPanel');
            spyOn(Mozilla.HelloFTU, 'bindPageEvents');
            spyOn(Mozilla.HelloFTU, 'trackTourSource');
        });

        it('should initialize if loop target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            });
            Mozilla.HelloFTU.init();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.observe).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showHelloPanel).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindPageEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.trackTourSource).toHaveBeenCalled();
        });

        it('should not initialize if loop target unavailable', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HelloFTU.init();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.observe).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showHelloPanel).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindPageEvents).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.trackTourSource).not.toHaveBeenCalled();
        });
    });

    describe('showHelloPanel', function () {

        it('should show panel if loop target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            });
            spyOn(Mozilla.HelloFTU, 'bindHelloPanelEvents');
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.helloPanelVisible).toBeTruthy();
            expect(Mozilla.HelloFTU.bindHelloPanelEvents).toHaveBeenCalled();
        });

        it('should not show panel if loop target unavailable', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.helloPanelVisible).toBeFalsy();
        });

        it('should not show panel if document is hidden', function() {
            Mozilla.HelloFTU.documentHidden = true;
            spyOn(Mozilla.UITour, 'getConfiguration').and.callThrough();
            Mozilla.HelloFTU.showHelloPanel();
            expect(Mozilla.UITour.getConfiguration).not.toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showMenu).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.helloPanelVisible).toBeFalsy();
        });
    });

    describe('hideHelloPanel', function () {

        it('should hide panel if visible', function() {
            Mozilla.HelloFTU.helloPanelVisible = true;
            spyOn(Mozilla.UITour, 'hideMenu');
            spyOn(Mozilla.HelloFTU, 'unbindHelloPanelEvents');
            Mozilla.HelloFTU.hideHelloPanel();
            expect(Mozilla.UITour.hideMenu).toHaveBeenCalledWith('loop');
            expect(Mozilla.HelloFTU.unbindHelloPanelEvents).toHaveBeenCalled();
        });

        it('should not hide panel if not visible', function() {
            spyOn(Mozilla.UITour, 'hideMenu');
            spyOn(Mozilla.HelloFTU, 'unbindHelloPanelEvents');
            Mozilla.HelloFTU.hideHelloPanel();
            expect(Mozilla.UITour.hideMenu).not.toHaveBeenCalledWith('loop');
            expect(Mozilla.HelloFTU.unbindHelloPanelEvents).not.toHaveBeenCalled();
        });
    });

    describe('handleVisibilityChange', function() {

        beforeEach(function() {
            spyOn(Mozilla.HelloFTU, 'showHelloPanel');
            spyOn(Mozilla.HelloFTU, 'hideHelloPanel');
            spyOn(Mozilla.HelloFTU, 'bindHelloEvents');
            spyOn(Mozilla.HelloFTU, 'unbindHelloEvents');
        });

        it('should hide panel when document is hidden', function() {
            Mozilla.HelloFTU.documentHidden = true;
            Mozilla.HelloFTU.handleVisibilityChange();
            expect(Mozilla.HelloFTU.hideHelloPanel).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.unbindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.showHelloPanel).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).not.toHaveBeenCalled();
        });

        it('should show panel when document is visible', function() {
            Mozilla.HelloFTU.documentHidden = false;
            Mozilla.HelloFTU.handleVisibilityChange();
            clock.tick(1000);
            expect(Mozilla.HelloFTU.showHelloPanel).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.hideHelloPanel).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.unbindHelloEvents).not.toHaveBeenCalled();
        });

        it('should not show panel if "get started" has been clicked', function() {
            Mozilla.HelloFTU.documentHidden = false;
            Mozilla.HelloFTU.getStartedClicked = true;
            Mozilla.HelloFTU.handleVisibilityChange();
            clock.tick(1000);
            expect(Mozilla.HelloFTU.showHelloPanel).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.bindHelloEvents).toHaveBeenCalled();
            expect(Mozilla.HelloFTU.hideHelloPanel).not.toHaveBeenCalled();
            expect(Mozilla.HelloFTU.unbindHelloEvents).not.toHaveBeenCalled();
        });
    });

    describe('handleResize', function () {

        it('should hide Hello panel', function() {
            spyOn(Mozilla.HelloFTU, 'hideHelloPanel');
            Mozilla.HelloFTU.handleResize();
            expect(Mozilla.HelloFTU.hideHelloPanel).toHaveBeenCalled();
        });
    });

    describe('trackRoomShareButton', function () {

        it('should track in GTM when a button was clicked', function() {
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.trackRoomShareButton('foo');
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
            expect($.fn.on).toHaveBeenCalledWith('visibilitychange.hello', jasmine.any(Function));
        });
    });

    describe('bindHelloEvents', function () {

        it('should bind UITour observe event listener', function() {
            spyOn(Mozilla.UITour, 'observe');
            Mozilla.HelloFTU.bindHelloEvents();
            expect(Mozilla.UITour.observe).toHaveBeenCalled();
        });
    });

    describe('handleHelloEvents', function () {

        it('should handle opening chat window', function() {
            spyOn(Mozilla.HelloFTU, 'onChatWindowOpened');
            Mozilla.HelloFTU.handleHelloEvents('Loop:ChatWindowOpened');
            expect(Mozilla.HelloFTU.onChatWindowOpened).toHaveBeenCalled();
        });

        it('should handle copy button press', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLCopied');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLCopied-Tour');
        });

        it('should handle email button press', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLEmailed');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLEmailed-Tour');
        });

        it('should handle share button press', function() {
            spyOn(Mozilla.HelloFTU, 'trackRoomShareButton');
            Mozilla.HelloFTU.handleHelloEvents('Loop:RoomURLShared');
            expect(Mozilla.HelloFTU.trackRoomShareButton).toHaveBeenCalledWith('URLShared-Tour');
        });
    });

    describe('unbindHelloEvents', function () {

        it('should unbind UITour observe event listener', function() {
            spyOn(Mozilla.UITour, 'observe');
            Mozilla.HelloFTU.unbindHelloEvents();
            expect(Mozilla.UITour.observe).toHaveBeenCalledWith(null);
        });
    });

    describe('onChatWindowOpened', function () {

        it('should track the event in GTM', function() {
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.onChatWindowOpened();
            expect(window.dataLayer.push).toHaveBeenCalled();
        });

        it('should only track the event once', function() {
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.onChatWindowOpened();
            Mozilla.HelloFTU.onChatWindowOpened();
            expect(window.dataLayer.push.calls.count()).toEqual(1);
        });

        it('should register that "Get Started" was clicked', function() {
            expect(Mozilla.HelloFTU.getStartedClicked).toBeFalsy();
            Mozilla.HelloFTU.onChatWindowOpened();
            expect(Mozilla.HelloFTU.getStartedClicked).toBeTruthy();
        });

        it('should unbind Hello panel events', function() {
            spyOn(Mozilla.HelloFTU, 'unbindHelloPanelEvents');
            Mozilla.HelloFTU.onChatWindowOpened();
            expect(Mozilla.HelloFTU.unbindHelloPanelEvents).toHaveBeenCalled();
        });
    });

    describe('bindHelloPanelEvents', function () {

        it('should bind events correctly', function() {
            spyOn($.fn, 'one');
            Mozilla.HelloFTU.bindHelloPanelEvents();
            expect($.fn.one).toHaveBeenCalledWith('click.hello', Mozilla.HelloFTU.hideHelloPanel);
            expect($.fn.one).toHaveBeenCalledWith('resize.hello', Mozilla.HelloFTU.handleResize);
        });
    });

    describe('unbindHelloPanelEvents', function () {

        it('should unbind events correctly', function() {
            spyOn($.fn, 'off');
            Mozilla.HelloFTU.unbindHelloPanelEvents();
            expect($.fn.off).toHaveBeenCalledWith('click.hello', Mozilla.HelloFTU.hideHelloPanel);
            expect($.fn.off).toHaveBeenCalledWith('resize.hello', Mozilla.HelloFTU.handleResize);
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
            spyOn(window.dataLayer, 'push');
            Mozilla.HelloFTU.trackTourSource('snippet');
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'hello-interactions-referral',
                'category': '/hello/start interactions',
                'location': 'tour',
                'browserAction': 'GetStarted',
                'helloFTUReferral': 'snippet'
            });
        });
    });
});
