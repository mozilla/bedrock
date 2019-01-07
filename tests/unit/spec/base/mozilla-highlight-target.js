/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, it, expect, sinon, spyOn, jasmine */

describe('mozilla-highlight-target.js', function() {

    'use strict';

    beforeEach(function () {
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.ping = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();
        Mozilla.UITour.showHighlight = sinon.stub();
        Mozilla.UITour.hideHighlight = sinon.stub();
    });

    describe('isTargetAvailable', function() {

        it('should throw an error if callback is not supplied', function() {
            spyOn(Mozilla.UITour, 'getConfiguration');
            expect(function() {
                Mozilla.HighlightTarget.isTargetAvailable('foo');
            }).toThrowError('isTargetAvailable: second argument is not a function');
        });

        it('should return true if target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['privateWindow']
                });
            });
            Mozilla.HighlightTarget.isTargetAvailable('privateWindow', function(result) {
                expect(result).toBeTruthy();
                expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            });
        });

        it('should return false if target is not available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            });
            Mozilla.HighlightTarget.isTargetAvailable('privateWindow', function(result) {
                expect(result).toBeFalsy();
                expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            });
        });
    });

    describe('bindEvents', function() {

        it('should bind events correctly', function() {
            spyOn(Mozilla.HighlightTarget, 'unbindEvents');
            spyOn($.fn, 'one');
            Mozilla.HighlightTarget.bindEvents();
            expect(Mozilla.HighlightTarget.unbindEvents).toHaveBeenCalled();
            expect($.fn.one).toHaveBeenCalledWith('click.highlight-target', Mozilla.HighlightTarget.hideHighlight);
            expect($.fn.one).toHaveBeenCalledWith('resize.highlight-target', Mozilla.HighlightTarget.hideHighlight);
            expect($.fn.one).toHaveBeenCalledWith('visibilitychange.highlight-target', Mozilla.HighlightTarget.handleVisibilityChange);
        });
    });

    describe('unbindEvents', function() {

        it('should unbind events correctly', function() {
            spyOn($.fn, 'off');
            Mozilla.HighlightTarget.unbindEvents();
            expect($.fn.off).toHaveBeenCalledWith('click.highlight-target');
            expect($.fn.off).toHaveBeenCalledWith('resize.highlight-target');
            expect($.fn.off).toHaveBeenCalledWith('visibilitychange.highlight-target');
        });
    });

    describe('handleVisibilityChange', function() {

        it('should hide highlight if the document is hidden', function() {
            spyOn(Mozilla.HighlightTarget, 'hideHighlight');
            Mozilla.HighlightTarget.handleVisibilityChange(true);
            expect(Mozilla.HighlightTarget.hideHighlight).toHaveBeenCalled();
        });
    });

    describe('hideHighlight', function() {

        it('should hide highlight', function() {
            spyOn(Mozilla.UITour, 'hideHighlight');
            spyOn(Mozilla.HighlightTarget, 'unbindEvents');
            Mozilla.HighlightTarget.hideHighlight();
            expect(Mozilla.UITour.hideHighlight).toHaveBeenCalled();
            expect(Mozilla.HighlightTarget.unbindEvents).toHaveBeenCalled();
        });
    });

    describe('showHighlight', function() {

        it('should show highlight and bind events', function() {
            spyOn(Mozilla.UITour, 'showHighlight');
            spyOn(Mozilla.HighlightTarget, 'bindEvents');
            Mozilla.HighlightTarget.showHighlight('privateWindow');
            expect(Mozilla.UITour.showHighlight).toHaveBeenCalledWith('privateWindow', 'wobble');
            expect(Mozilla.HighlightTarget.bindEvents).toHaveBeenCalled();
        });
    });

    describe('fireCustomEvent', function() {

        it('should trigger a custom event correctly', function() {
            var id = 'privateWindow';
            spyOn($.fn, 'trigger');
            Mozilla.HighlightTarget.fireCustomEvent('.foo', id);
            expect($.fn.trigger).toHaveBeenCalledWith('highlight-target', id);
        });
    });

    describe('tryHighlight', function() {

        beforeEach(function() {
            spyOn(Mozilla.HighlightTarget, 'showHighlight');
            spyOn(Mozilla.HighlightTarget, 'fireCustomEvent');
            spyOn(Mozilla.HighlightTarget, 'doRedirect');
        });

        it('should throw an error arguments are not valid', function() {
            spyOn(Mozilla.HighlightTarget, 'isTargetAvailable');
            expect(function() {
                Mozilla.HighlightTarget.tryHighlight(undefined, 'foo', 'https://www.mozilla.org/');
            }).toThrowError('tryHighlight: first argument target should be a DOM element');
            expect(function() {
                Mozilla.HighlightTarget.tryHighlight({}, undefined, 'https://www.mozilla.org/');
            }).toThrowError('tryHighlight: second argument target should be a string');
            expect(function() {
                Mozilla.HighlightTarget.tryHighlight({}, 'privateWindow', undefined);
            }).toThrowError('tryHighlight: third argument href should be a string');
        });

        it('should show highlight if target is available', function() {
            var elm = {};
            spyOn(Mozilla.HighlightTarget, 'isTargetAvailable').and.callFake(function(_target, callback) {
                callback(true);
            });
            Mozilla.HighlightTarget.tryHighlight(elm, 'privateWindow', 'https://www.mozilla.org/');
            expect(Mozilla.HighlightTarget.fireCustomEvent).toHaveBeenCalledWith(elm, 'privateWindow');
            expect(Mozilla.HighlightTarget.showHighlight).toHaveBeenCalledWith('privateWindow');
        });

        it('should follow link if target is not available', function() {
            spyOn(Mozilla.HighlightTarget, 'isTargetAvailable').and.callFake(function(_target, callback) {
                callback(false);
            });
            Mozilla.HighlightTarget.tryHighlight({}, 'privateWindow', 'https://www.mozilla.org/');
            expect(Mozilla.HighlightTarget.doRedirect).toHaveBeenCalledWith('https://www.mozilla.org/');
        });


    });

    describe('bindCTA', function() {

        it('should bind CTA click', function() {
            spyOn($.fn, 'on');
            Mozilla.HighlightTarget.bindCTA('.foo');
            expect($.fn.on).toHaveBeenCalledWith('click.highlight-target', Mozilla.HighlightTarget.handleCTAClick);
        });
    });

    describe('unbindCTA', function() {

        it('should unbind CTA click', function() {
            spyOn($.fn, 'off');
            Mozilla.HighlightTarget.unbindCTA('.foo');
            expect($.fn.off).toHaveBeenCalledWith('click.highlight-target');
        });
    });

    describe('init', function() {

        it('should thrown an error is selector is not supplied', function() {
            expect(function() {
                Mozilla.HighlightTarget.init();
            }).toThrowError('init: first argument selector is undefined');
        });

        it('should bind CTA if UITour ping is received', function() {
            spyOn(Mozilla.UITour, 'ping').and.callFake(function(callback) {
                callback();
            });
            spyOn(Mozilla.HighlightTarget, 'bindCTA');
            Mozilla.HighlightTarget.init('.foo');
            expect(Mozilla.HighlightTarget.bindCTA).toHaveBeenCalledWith('.foo');
        });

        it('should not bind CTA if UITour ping is not received', function() {
            spyOn(Mozilla.UITour, 'ping');
            spyOn(Mozilla.HighlightTarget, 'bindCTA');
            Mozilla.HighlightTarget.init('.foo');
            expect(Mozilla.HighlightTarget.bindCTA).not.toHaveBeenCalled();
        });
    });
});
