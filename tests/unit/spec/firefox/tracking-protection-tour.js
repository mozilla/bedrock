/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, jasmine */

describe('tracking-protection-tour.js', function() {

    'use strict';

    var clock;

    beforeEach(function() {
        // use fake timers to make tests easier
        clock = sinon.useFakeTimers();

        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();
        Mozilla.UITour.showInfo = sinon.stub();
        Mozilla.UITour.hideInfo = sinon.stub();
        Mozilla.UITour.showMenu = sinon.stub();
        Mozilla.UITour.hideMenu = sinon.stub();
        Mozilla.UITour.openPreferences = sinon.stub();
        Mozilla.UITour.closeTab = sinon.stub();

        spyOn(Mozilla.UITour, 'showMenu').and.callFake(function(target, callback) {
            callback();
        });

        spyOn(Mozilla.TPTour, 'getStep1Strings').and.callFake(function() {
            return {
                titleText: 'Step 1 title',
                panelText: 'Step 1 text',
                stepText: '1/3',
                buttonText: 'Next'
            };
        });

        spyOn(Mozilla.TPTour, 'getStep3Strings').and.callFake(function() {
            return {
                titleText: 'Step 3 title',
                panelText: 'Step 3 text',
                panelTextNewTab: 'Step 3 new tab text',
                panelTextAlt: 'Step 3 alt text',
                stepText: '3/3',
                buttonText: 'Got it!'
            };
        });
    });

    afterEach(function() {
        clock.restore();
        Mozilla.TPTour.state = 'step1';
        Mozilla.TPTour.highlightSupressed = false;
    });

    describe('init', function() {

        beforeEach(function() {
            spyOn(Mozilla.TPTour, 'getStrings');
            spyOn(Mozilla.TPTour, 'bindEvents');
        });

        it('shoud show the first tour step', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'none';
            });
            spyOn(Mozilla.TPTour, 'step1');
            Mozilla.TPTour.init();
            expect(Mozilla.TPTour.getStrings).toHaveBeenCalled();
            expect(Mozilla.TPTour.bindEvents).toHaveBeenCalled();
            clock.tick(600);
            expect(Mozilla.TPTour.step1).toHaveBeenCalled();
        });

        it('shoud show the second tour step when needed', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return '2';
            });
            spyOn(Mozilla.TPTour, 'step2');
            Mozilla.TPTour.init();
            expect(Mozilla.TPTour.getStrings).toHaveBeenCalled();
            expect(Mozilla.TPTour.bindEvents).toHaveBeenCalled();
            clock.tick(600);
            expect(Mozilla.TPTour.step2).toHaveBeenCalled();
        });

        it('shoud show the third tour step when needed', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return '3';
            });
            spyOn(Mozilla.TPTour, 'step3');
            Mozilla.TPTour.init();
            expect(Mozilla.TPTour.getStrings).toHaveBeenCalled();
            expect(Mozilla.TPTour.bindEvents).toHaveBeenCalled();
            clock.tick(600);
            expect(Mozilla.TPTour.step3).toHaveBeenCalled();
        });
    });

    describe('step1', function() {

        beforeEach(function() {
            Mozilla.TPTour.getStrings();
        });

        it('shoud show an info panel if "trackingProtection" target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['trackingProtection']
                });
            });
            spyOn(Mozilla.UITour, 'showInfo');
            Mozilla.TPTour.step1();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));

            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('trackingProtection',
                'Step 1 title', 'Step 1 text', undefined,
                [
                    { label: '1/3', style: 'text' },
                    { callback: Mozilla.TPTour.step2, label: 'Next', style: 'primary' }
                ],
                {
                    closeButtonCallback: Mozilla.TPTour.shouldCloseTab
                }
            );

            expect(Mozilla.TPTour.state).toEqual('step1');
        });

        it('shoud not show an info panel if "trackingProtection" target is unavailable', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            spyOn(Mozilla.UITour, 'showInfo');
            Mozilla.TPTour.step1();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            expect(Mozilla.UITour.showInfo).not.toHaveBeenCalled();
            expect(Mozilla.TPTour.state).toEqual('step1');
        });
    });

    describe('step2', function() {

        it('shoud update state correctly', function() {
            Mozilla.TPTour.step2();
            expect(Mozilla.TPTour.state).toEqual('step2');
        });
    });

    describe('step3', function() {

        beforeEach(function() {
            Mozilla.TPTour.getStrings();
            spyOn(Mozilla.UITour, 'showInfo');
            spyOn(Mozilla.TPTour, 'replaceURLState');
        });

        describe('shoud open "controlCenter" and highlight "trackingUnblock" if target is available', function() {

            beforeEach(function() {            
                spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                    callback({
                        targets: ['controlCenter-trackingUnblock']
                    });
                });
            });

            it('should show the correct string for private window', function() {
                spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                    return 'none';
                });

                Mozilla.TPTour.step3();

                expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('controlCenter-trackingUnblock',
                    'Step 3 title', 'Step 3 text', undefined,
                    [
                        { label: '3/3', style: 'text' },
                        { callback: Mozilla.TPTour.shouldCloseTab, label: 'Got it!', style: 'primary' }
                    ],
                    {
                        closeButtonCallback: Mozilla.TPTour.shouldCloseTab
                    }
                );

                expect(Mozilla.TPTour.replaceURLState).toHaveBeenCalledWith('3');
                expect(Mozilla.TPTour.state).toEqual('step3');
            });

            it('should show the correct string for non-private window', function() {
                spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                    return 'true';
                });

                Mozilla.TPTour.step3();

                expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('controlCenter-trackingUnblock',
                    'Step 3 title', 'Step 3 new tab text', undefined,
                    [
                        { label: '3/3', style: 'text' },
                        { callback: Mozilla.TPTour.shouldCloseTab, label: 'Got it!', style: 'primary' }
                    ],
                    {
                        closeButtonCallback: Mozilla.TPTour.shouldCloseTab
                    }
                );

                expect(Mozilla.TPTour.replaceURLState).toHaveBeenCalledWith('3');
                expect(Mozilla.TPTour.state).toEqual('step3');
            });
        });

        it('shoud open "controlCenter" and highlight "trackingBlock" if target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['controlCenter-trackingBlock']
                });
            });

            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'none';
            });

            Mozilla.TPTour.step3();

            expect(Mozilla.UITour.showInfo).toHaveBeenCalledWith('controlCenter-trackingBlock',
                'Step 3 title', 'Step 3 alt text', undefined,
                [
                    { label: '3/3', style: 'text' },
                    { callback: Mozilla.TPTour.shouldCloseTab, label: 'Got it!', style: 'primary' }
                ],
                {
                    closeButtonCallback: Mozilla.TPTour.shouldCloseTab
                }
            );

            expect(Mozilla.TPTour.replaceURLState).toHaveBeenCalledWith('3');
            expect(Mozilla.TPTour.state).toEqual('step3');
        });
    });

    describe('shouldCloseTab', function() {

        beforeEach(function() {
            spyOn(Mozilla.TPTour, 'tryCloseTab');
            spyOn(Mozilla.TPTour, 'step4');
        });

        it('should try and close the tour if in a new tab', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'true';
            });
            Mozilla.TPTour.shouldCloseTab();
            expect(Mozilla.TPTour.tryCloseTab).toHaveBeenCalled();
        });

        it('should show step 4 if tour is not in a new tab', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'none';
            });
            Mozilla.TPTour.shouldCloseTab();
            expect(Mozilla.TPTour.step4).toHaveBeenCalled();
        });
    });

    describe('tryCloseTab', function() {

        it('should try and close the tab as expected', function() {
            spyOn(Mozilla.TPTour, 'step4');
            spyOn(Mozilla.TPTour, 'hidePanels');
            spyOn(Mozilla.UITour, 'closeTab');
            Mozilla.TPTour.tryCloseTab();
            expect(Mozilla.TPTour.hidePanels).toHaveBeenCalled();
            expect(Mozilla.UITour.closeTab).toHaveBeenCalled();
            clock.tick(500);
            expect(Mozilla.TPTour.step4).toHaveBeenCalled();
        });
    });

    describe('step4', function() {

        it('shoud update state correctly', function() {
            spyOn(Mozilla.TPTour, 'hidePanels');
            spyOn($.fn, 'one');
            Mozilla.TPTour.step4();
            expect(Mozilla.TPTour.hidePanels).toHaveBeenCalled();
            expect($.fn.one).toHaveBeenCalledWith('animationend', Mozilla.TPTour.showEndState);
            expect(Mozilla.TPTour.state).toEqual('step4');
        });
    });

    describe('showEndState', function() {

        it('shoud update state correctly', function() {
            spyOn(Mozilla.TPTour, 'replaceURLState');
            Mozilla.TPTour.showEndState();
            expect(Mozilla.TPTour.replaceURLState).toHaveBeenCalledWith('done');
        });
    });

    describe('_getText', function() {

        it('should strip HTML from the queried string', function() {
            spyOn(Mozilla.TPTour, '_trans').and.callFake(function() {
                return 'I\'m <strong>The Dude</strong>, so that\'s what you call me, <em>man</em>.';
            });
            var result = Mozilla.TPTour._getText('someId');
            expect(result).toEqual('I\'m The Dude, so that\'s what you call me, man.');
        });
    });

    describe('openPrivacyPrefs', function() {

        it('should open preferences and pass the privacy tab ID', function() {
            spyOn(Mozilla.UITour, 'openPreferences');
            Mozilla.TPTour.openPrivacyPrefs();
            expect(Mozilla.UITour.openPreferences).toHaveBeenCalledWith('privacy');
        });
    });

    describe('bindEvents', function() {

        it('should bind events correctly', function() {
            spyOn($.fn, 'on');
            Mozilla.TPTour.bindEvents();
            expect($.fn.on).toHaveBeenCalledWith('click.tp-tour', Mozilla.TPTour.handlePrefsLinkClick);
            expect($.fn.on).toHaveBeenCalledWith('click.tp-tour', Mozilla.TPTour.step3);
            expect($.fn.on).toHaveBeenCalledWith('click.tp-tour', Mozilla.TPTour.shouldCloseTab);
            expect($.fn.on).toHaveBeenCalledWith('visibilitychange.tp-tour', Mozilla.TPTour.handleVisibilityChange);
            expect($.fn.on).toHaveBeenCalledWith('resize.tp-tour', Mozilla.TPTour.handleResize);
            expect($.fn.on).toHaveBeenCalledWith('click.tp-tour', Mozilla.TPTour.restartTour);
        });
    });

    describe('handleResize', function() {

        beforeEach(function() {
            spyOn(Mozilla.UITour, 'hideInfo');
            spyOn(Mozilla.TPTour, 'showTourStep');
        });

        it('should hide and reshow info panel if on tour step 1', function() {
            Mozilla.TPTour.handleResize();
            expect(Mozilla.UITour.hideInfo).toHaveBeenCalled();
            expect(Mozilla.TPTour.highlightSupressed).toBeTruthy();
            clock.tick(400);
            expect(Mozilla.TPTour.highlightSupressed).toBeFalsy();
            expect(Mozilla.TPTour.showTourStep).toHaveBeenCalled();
        });

        it('should not hide info panels on other steps', function() {
            Mozilla.TPTour.state = 'step2';
            Mozilla.TPTour.handleResize();
            expect(Mozilla.UITour.hideInfo).not.toHaveBeenCalled();
        });
    });

    describe('handleVisibilityChange', function() {

        it('should hide UITour highlights when document is hidden', function() {
            Mozilla.TPTour.documentHidden = true;
            spyOn(Mozilla.TPTour, 'hidePanels');
            Mozilla.TPTour.handleVisibilityChange();
            expect(Mozilla.TPTour.hidePanels).toHaveBeenCalled();
        });

        it('should show tour step when document is visible', function() {
            Mozilla.TPTour.documentHidden = false;
            spyOn(Mozilla.TPTour, 'showTourStep');
            Mozilla.TPTour.handleVisibilityChange();
            clock.tick(400);
            expect(Mozilla.TPTour.showTourStep).toHaveBeenCalled();
        });
    });

    describe('showTourStep', function() {

        it('should show the appropriate tour step', function() {
            spyOn(Mozilla.TPTour, 'step1');
            spyOn(Mozilla.TPTour, 'step2');
            spyOn(Mozilla.TPTour, 'step3');

            Mozilla.TPTour.state = 'step1';
            Mozilla.TPTour.showTourStep();
            expect(Mozilla.TPTour.step1).toHaveBeenCalled();

            Mozilla.TPTour.state = 'step2';
            Mozilla.TPTour.showTourStep();
            expect(Mozilla.TPTour.step2).toHaveBeenCalled();

            Mozilla.TPTour.state = 'step3';
            Mozilla.TPTour.showTourStep();
            expect(Mozilla.TPTour.step3).toHaveBeenCalled();
        });
    });

    describe('getStrings', function() {

        it('should get translated strings for steps 1 and 3', function() {
            Mozilla.TPTour.getStrings();
            expect(Mozilla.TPTour.getStep1Strings).toHaveBeenCalled();
            expect(Mozilla.TPTour.getStep3Strings).toHaveBeenCalled();
        });
    });

    describe('hidePanels', function() {

        it('should hide all info panels and menus', function() {
            spyOn(Mozilla.UITour, 'hideInfo');
            spyOn(Mozilla.UITour, 'hideMenu');
            spyOn(Mozilla.TPTour, 'hideStep2Panel');
            Mozilla.TPTour.hidePanels();
            expect(Mozilla.UITour.hideInfo).toHaveBeenCalled();
            expect(Mozilla.UITour.hideMenu).toHaveBeenCalledWith('controlCenter');
            expect(Mozilla.TPTour.hideStep2Panel).toHaveBeenCalled();
        });
    });

    describe('restartTour', function() {

        it('should reset tour back to step1', function() {
            spyOn(Mozilla.TPTour, 'resetPageState');
            spyOn(Mozilla.TPTour, 'hideStep2Panel');
            spyOn(Mozilla.TPTour, 'showTourStep');
            Mozilla.TPTour.state = 'step3';
            Mozilla.TPTour.restartTour();
            expect(Mozilla.TPTour.resetPageState).toHaveBeenCalled();
            expect(Mozilla.TPTour.hideStep2Panel).toHaveBeenCalled();
            expect(Mozilla.TPTour.showTourStep).toHaveBeenCalled();
            expect(Mozilla.TPTour.state).toEqual('step1');
        });
    });

    describe('getParameterByName', function () {

        it('should return the supplied parameter value', function() {
            var url = '/start/?step=3';
            var result = Mozilla.TPTour.getParameterByName('step', url);
            expect(result).toEqual('3');
        });

        it('should return "none" if parameter is omitted', function() {
            var url = '/start/';
            var result = Mozilla.TPTour.getParameterByName('step', url);
            expect(result).toEqual('none');
        });
    });

    describe('replaceURLState', function() {

        it('should update URL with query param if not present', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'none';
            });
            spyOn(window.history, 'replaceState');
            Mozilla.TPTour.replaceURLState('3', '/start/');
            expect(window.history.replaceState).toHaveBeenCalledWith({}, '', '/start/?step=3');

            Mozilla.TPTour.replaceURLState('3', '/start/?foo=bar');
            expect(window.history.replaceState).toHaveBeenCalledWith({}, '', '/start/?foo=bar&step=3');
        });

        it('should not change URL if supplied parameter value is already present', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return '3';
            });
            spyOn(window.history, 'replaceState');
            Mozilla.TPTour.replaceURLState('3', '/start/?step=3');
            expect(window.history.replaceState).not.toHaveBeenCalled();
        });

        it('should update query parameter with the value supplied', function() {
            spyOn(Mozilla.TPTour, 'getParameterByName').and.callFake(function() {
                return 'done';
            });
            spyOn(window.history, 'replaceState');
            Mozilla.TPTour.replaceURLState('3', '/start/?step=done');
            expect(window.history.replaceState).toHaveBeenCalledWith({}, '', '/start/?step=3');

            Mozilla.TPTour.replaceURLState('3', '/start/?bar=foo&step=done');
            expect(window.history.replaceState).toHaveBeenCalledWith({}, '', '/start/?bar=foo&step=3');
        });
    });
});
