/* Base JS unit test spec for bedrock tabzilla.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('browser-tour.js', function() {

    var windowTransStub;
    var tour;
    var onCloseTourCallback;
    var onCompactTourCallback;
    var onExpandTourCallback;
    var onRestartTourCallback;
    var onTourCompleteCallback;
    var clock;

    beforeEach(function() {

        // turn off animation effects so we don't have to wait for async
        jQuery.fx.off = true;

        // example tour template markup
        var tourMarkup = [
          '<div id="ui-tour" tabindex="-1" aria-expanded="false">',
            '<div class="cta">',
              '<button type="button" aria-controls="ui-tour">Start browsing</button>',
            '</div>',
            '<div class="tour-tip"></div>',
            '<div class="ui-tour-controls">',
              '<button class="step prev" aria-controls="tour-steps tour-progress">Previous</button>',
              '<button class="step next" aria-controls="tour-steps tour-progress">Next</button>',
              '<button class="close" aria-controls="tour-steps tour-progress">Close</button>',
            '</div>',
            '<div class="tour-background">',
              '<div class="tour-inner">',
                '<div id="tour-progress" class="progress-step">',
                  '<div class="logo"></div>',
                  '<span class="step"></span>',
                  '<div class="progress" role="progressbar" aria-valuenow="1" aria-valuemin="1" aria-valuemax="4">',
                    '<span class="indicator"></span>',
                  '</div>',
                '</div>',
                '<ul id="tour-steps" class="ui-tour-list">',
                  '<li class="tour-step current app-menu visible" data-step="1" data-tip-next="Next">',
                    '<div class="tour-item">',
                      '<h2 class="tour-highlight step-target" data-target="appMenu" data-effect="wobble">',
                        'Title text',
                      '</h2>',
                      '<ul class="tour-menu step-target" data-target="appMenu">',
                        '<li><a href="#" role="button" class="more">Link text</a></li>',
                      '</ul>',
                    '</div>',
                  '</li>',
                  '<li class="tour-step" data-step="2" data-tip-prev="Previous" data-tip-next="Next">',
                    '<div class="tour-item">',
                      '<h2 class="tour-highlight step-target" data-target="customize" data-effect="wobble">',
                        'Title text',
                      '</h2>',
                      '<ul class="tour-forget-widget step-target">',
                        '<li><a href="#" role="button" class="more">Link text</a></li>',
                      '</ul>',
                    '</div>',
                  '</li>',
                  '<li class="tour-step" data-step="3" data-tip-prev="Previous">',
                    '<div class="tour-item">',
                      '<h2 class="tour-search-engine step-target" data-target="searchEngine-google">',
                        'Title text',
                      '</h2>',
                      '<ul>',
                        '<li><a href="#" role="button" class="more">Link text</a></li>',
                      '</ul>',
                    '</div>',
                  '</li>',
                  '<li class="tour-step" data-step="4" data-tip-prev="Previous">',
                    '<div class="tour-item">',
                      '<h2 class="tour-show-hello-panel step-target">',
                        'Title text',
                      '</h2>',
                      '<ul>',
                        '<li><a href="#" role="button" class="more">Link text</a></li>',
                      '</ul>',
                    '</div>',
                  '</li>',
                '</ul>',
                '<div class="compact-title"></div>',
                '<div class="tour-init" data-target="appMenu" data-icon="logo.png" data-icon-high-res="logo-high-res.png"></div>',
              '</div>',
            '</div>',
          '</div>',
          '<div id="ui-tour-mask" tabindex="-1">',
            '<div class="mask-inner">',
              '<div class="logo"></div>',
              '<div class="stage">',
                '<h1>Mask title</h1>',
                '<p>Mask sub heading</p>',
              '</div>',
            '</div>',
          '</div>',
        ].join();

        $(tourMarkup).appendTo('body');

        // always set the first tour step to current
        $('.ui-tour-list li.current').removeClass('current');
        $('.ui-tour-list li:first').addClass('current');

        windowTransStub = sinon.stub(window, 'trans').returns('Foo bar');

        // use fake timers to make tests easier
        clock = sinon.useFakeTimers();

        // stub out Mozilla.UITour
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.registerPageID = sinon.stub();
        Mozilla.UITour.showInfo = sinon.stub();
        Mozilla.UITour.showHighlight = sinon.stub();
        Mozilla.UITour.hideHighlight = sinon.stub();
        Mozilla.UITour.showMenu = sinon.stub();
        Mozilla.UITour.hideInfo = sinon.stub();
        Mozilla.UITour.hideMenu = sinon.stub();
        Mozilla.UITour.addNavBarWidget = sinon.stub();

        // stub out Mozilla.ImageHelper.isHighDpi
        Mozilla.ImageHelper.isHighDpi = sinon.stub();

        // spy on BrowserTour prototype methods
        spyOn(Mozilla.BrowserTour.prototype, 'bindEvents').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'bindResize').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'handleVisibilityChange').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onStartTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'showHighlight').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onStepClick').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'closeTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'doCloseTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onCloseTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onCompactTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onTourExpand').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'doCompactTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'restartTour').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'startBrowsing').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onStepHover').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'offStepHover').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onTourLinkClick').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'goToTourStep').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'hideAnnotations').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'updateControls').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onTourComplete').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'onTourStep').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'showHelloPanel').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'hideHelloPanel').andCallThrough();
        spyOn(Mozilla.BrowserTour.prototype, 'promptAddHelloButton').andCallThrough();

        // custom callback stubs
        onCloseTourCallback = sinon.stub();
        onCompactTourCallback = sinon.stub();
        onExpandTourCallback = sinon.stub();
        onRestartTourCallback = sinon.stub();
        onTourCompleteCallback = sinon.stub();

        // create tour & init
        tour = new Mozilla.BrowserTour({
            id: 'test-id',
            onCloseTour: onCloseTourCallback,
            onCompactTour: onCompactTourCallback,
            onExpandTour: onExpandTourCallback,
            onRestartTour: onRestartTourCallback,
            onTourComplete: onTourCompleteCallback
        });

        tour.init();
    });

    afterEach(function() {
        // turn animations back on
        jQuery.fx.off = false;
        windowTransStub.restore();

        // remove tour after each test
        $('#ui-tour').remove();
        $('#ui-tour-mask').remove();
        tour = null;

        //restore timers
        clock.restore();
    });

    describe('instantiation', function () {

        it('should create a new instance', function() {
            expect(tour instanceof Mozilla.BrowserTour).toBeTruthy();
        });

        it('should call bindEvents', function() {
            expect(Mozilla.BrowserTour.prototype.bindEvents).toHaveBeenCalled();
        });

        it('should call bindResize', function() {
            expect(Mozilla.BrowserTour.prototype.bindResize).toHaveBeenCalled();
        });

        it('should register a telemetry ID using the option supplied', function() {
            expect(Mozilla.UITour.registerPageID.calledWith('test-id')).toBeTruthy();
        });
    });

    describe('startTour', function() {

        it('should start the first step of the tour correctly', function() {
            Mozilla.UITour.getConfiguration = sinon.stub();
            tour.startTour();
            clock.tick(1000);
            expect(Mozilla.BrowserTour.prototype.updateControls).toHaveBeenCalled();
            expect(Mozilla.BrowserTour.prototype.showHighlight).toHaveBeenCalled();
            expect(Mozilla.BrowserTour.prototype.onStartTour).toHaveBeenCalled();
        });
    });

    describe('bindEvents', function() {

        it('should show a door-hanger on tour-init event', function() {
            $('.tour-init').trigger('tour-step');
            expect(Mozilla.UITour.showInfo.called).toBeTruthy();
        });

        it('should show a highlight on tour-step event', function() {
            $('.tour-highlight').trigger('tour-step');
            expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
        });

        it('should open a menu on tour-step event', function() {
            $('.tour-menu').trigger('tour-step');
            expect(Mozilla.UITour.showMenu.called).toBeTruthy();
        });

        it('should should handle visibilitychange events', function() {
            $(document).trigger('visibilitychange');
            expect(Mozilla.BrowserTour.prototype.handleVisibilityChange).toHaveBeenCalled();
        });
    });

    describe('postponeTour, restartTour', function () {

        afterEach(function() {
            $('button.floating-cta').remove();
        });

        it('should close the tour and show resume cta button', function() {
            tour.postponeTour();
            expect($('button.floating-cta').length === 1).toBeTruthy();
            expect(Mozilla.BrowserTour.prototype.doCloseTour).toHaveBeenCalled();
        });

        it('should restart the tour once postponed', function() {
            tour.postponeTour();
            $('button.floating-cta').trigger('click');
            expect(Mozilla.BrowserTour.prototype.restartTour).toHaveBeenCalled();
        });

        it('should excecute callback when tour restarts if passed as an option', function() {
            tour.restartTour();
            expect(onRestartTourCallback.called).toBeTruthy();
        });
    });

    describe('updateControls', function () {

        it('should disable prev button on first step', function() {
            tour.updateControls();
            expect($('.ui-tour-controls button.step.prev').attr('disabled')).toEqual('disabled');
            expect($('.ui-tour-controls button.step.next').attr('disabled')).not.toEqual('disabled');
        });

        it('should disable next button on last step', function() {
            $('.ui-tour-list > li.current').removeClass('current');
            $('.ui-tour-list > li:last').addClass('current');
            tour.updateControls();
            expect($('.ui-tour-controls button.step.prev').attr('disabled')).not.toEqual('disabled');
            expect($('.ui-tour-controls button.step.next').attr('disabled')).toEqual('disabled');
        });

        it('buttons should not be disabled on other steps', function() {
            $('.ui-tour-list > li.current').removeClass('current');
            $('.ui-tour-list > li:nth-of-type(2)').addClass('current');
            tour.updateControls();
            expect($('.ui-tour-controls button.step.prev').attr('disabled')).not.toEqual('disabled');
            expect($('.ui-tour-controls button.step.next').attr('disabled')).not.toEqual('disabled');
        });
    });

    describe('onStepHover, offStepHover', function () {

        it('hovering over button should show a tooltip', function() {
            $('.ui-tour-controls button.step.next').trigger('mouseenter');
            expect(Mozilla.BrowserTour.prototype.onStepHover).toHaveBeenCalled();
            expect($('.tour-tip').hasClass('show-tip')).toBeTruthy();
        });

        it('hovering off button should hide a tooltip', function() {
            $('.ui-tour-controls button.step.next').trigger('mouseleave');
            expect(Mozilla.BrowserTour.prototype.offStepHover).toHaveBeenCalled();
            expect($('.tour-tip').hasClass('show-tip')).toBeFalsy();
        });
    });

    describe('onTourStep', function () {

        beforeEach(function() {
            Mozilla.UITour.getConfiguration = sinon.stub();
        });

        it('should show the current step correctly', function() {
            var event = {
                originalEvent: {
                    propertyName:'transform'
                }
            };
            tour.onTourStep(event);
            expect(Mozilla.BrowserTour.prototype.showHighlight).toHaveBeenCalled();
            expect(Mozilla.BrowserTour.prototype.updateControls).toHaveBeenCalled();
        });

        it('should call onTourComplete on the last step of the tour', function() {
            var event = {
                originalEvent: {
                    propertyName:'transform'
                }
            };
            $('.ui-tour-list > li.current').removeClass('current');
            $('.ui-tour-list > li:last').addClass('current');
            tour.onTourStep(event);
            expect(Mozilla.BrowserTour.prototype.onTourComplete).toHaveBeenCalled();
        });
    });

    describe('onTourComplete', function () {

        it('should excecute callback when passed as an option', function() {
            tour.onTourComplete();
            expect(onTourCompleteCallback.called).toBeTruthy();
        });

        it('should only excecute callback once', function() {
            tour.onTourComplete();
            tour.onTourComplete();
            expect(onTourCompleteCallback.calledOnce).toBeTruthy();
        });
    });

    describe('showHighlight', function() {

        beforeEach(function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['appMenu']
                });
            };
        });

        it('should query availableTargets', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
            tour.showHighlight();
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
        });

        it('should trigger a highlight if target is available', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
            tour.showHighlight();
            clock.tick(300);
            expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
        });

        it('if target is not available it should not trigger a highlight', function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['foo']
                });
            };
            spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
            tour.showHighlight();
            clock.tick(300);
            expect(Mozilla.UITour.showHighlight.called).toBeFalsy();
        });
    });

    describe('Forget button', function() {

        describe('highlightForgetButton', function() {

            beforeEach(function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['forget']
                    });
                };
            });

            it('should query availableTargets', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-forget-widget').trigger('tour-step');
                expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            });

            it('should trigger a highlight if target is available', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-forget-widget').trigger('tour-step');
                expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
            });

            it('should show a door-hanger if not available', function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['foo']
                    });
                };
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-forget-widget').trigger('tour-step');
                expect(Mozilla.UITour.showInfo.called).toBeTruthy();
                expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
            });
        });

        describe('addForgetButton', function() {

            it('should add the icon using addNavBarWidget', function() {
                tour.addForgetButton();
                expect(Mozilla.UITour.addNavBarWidget.calledWith('forget')).toBeTruthy();
                expect(Mozilla.UITour.hideHighlight.called).toBeTruthy();
            });
        });

        describe('laterForgetButton', function() {

            it('should show a reminder door-hanger', function() {
                tour.laterForgetButton();
                expect(Mozilla.UITour.showInfo.called).toBeTruthy();
                expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
            });
        });

        describe('closeForgetDoorhanger', function() {

            it('should should hide info panel and highlight', function() {
                tour.closeForgetDoorhanger();
                expect(Mozilla.UITour.hideInfo.called).toBeTruthy();
                expect(Mozilla.UITour.hideHighlight.called).toBeTruthy();
            });
        });
    });

    describe('highlightSearchEngine', function () {

        beforeEach(function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['searchProvider', 'searchEngine-google']
                });
            };
        });

        it('should query availableTargets', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
            $('.tour-search-engine').trigger('tour-step');
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
        });

        it('should open the menu if search engine is available', function() {
            $('.tour-search-engine').trigger('tour-step');
            expect(Mozilla.UITour.showMenu.calledWith('searchEngines')).toBeTruthy();
        });

        it('should highlight if search engine is not available', function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['searchProvider', 'searchEngine-foo']
                });
            };
            $('.tour-search-engine').trigger('tour-step');
            expect(Mozilla.UITour.showMenu.calledWith('searchEngines')).toBeFalsy();
            expect(Mozilla.UITour.showHighlight.called).toBeTruthy();
        });

        it('should do nothing if search bar is not available', function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['foo', 'searchEngine-foo']
                });
            };
            $('.tour-search-engine').trigger('tour-step');
            expect(Mozilla.UITour.showMenu.called).toBeFalsy();
            expect(Mozilla.UITour.showHighlight.called).toBeFalsy();
        });
    });

    describe('Hello panel', function() {

        describe('showHelloPanel', function() {

            beforeEach(function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['loop']
                    });
                };
            });

            it('should query availableTargets', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-show-hello-panel').trigger('tour-step');
                expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            });

            it('should open the hello panel if available', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-show-hello-panel').trigger('tour-step');
                expect(Mozilla.BrowserTour.prototype.showHelloPanel).toHaveBeenCalled();
                expect(Mozilla.UITour.showMenu.calledWith('loop')).toBeTruthy();
            });

            it('should call promptAddHelloButton if target is not available', function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['foo']
                    });
                };
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                $('.tour-show-hello-panel').trigger('tour-step');
                expect(Mozilla.BrowserTour.prototype.showHelloPanel).toHaveBeenCalled();
                expect(Mozilla.UITour.showMenu.called).toBeFalsy();
                expect(Mozilla.BrowserTour.prototype.promptAddHelloButton).toHaveBeenCalled();
            });

        });

        describe('hideHelloPanel', function () {

            it('should hide the Hello panel', function() {
                tour.hideHelloPanel();
                expect(Mozilla.UITour.hideMenu.calledWith('loop')).toBeTruthy();
                expect(Mozilla.UITour.hideHighlight.called).toBeTruthy();
            });
        });

        describe('promptAddHelloButton', function () {

            it('should show a door-hanger on appMenu target', function() {
                tour.promptAddHelloButton();
                expect(Mozilla.UITour.showHighlight.calledWith('appMenu')).toBeTruthy();
                expect(Mozilla.UITour.showInfo.calledWith('appMenu')).toBeTruthy();
            });
        });

        describe('addHelloButton', function () {

            it('should add the icon using addNavBarWidget', function() {
                tour.addHelloButton();
                expect(Mozilla.UITour.addNavBarWidget.calledWith('loop')).toBeTruthy();
            });
        });

        describe('highlightHelloButton', function () {

            it('should show a door-hanger on loop target', function() {
                tour.highlightHelloButton();
                expect(Mozilla.UITour.showHighlight.calledWith('loop')).toBeTruthy();
                expect(Mozilla.UITour.showInfo.calledWith('loop')).toBeTruthy();
            });
        });

        describe('laterHelloButton', function () {

            it('should show a door-hanger on appMenu target', function() {
                tour.laterHelloButton();
                expect(Mozilla.UITour.showInfo.calledWith('appMenu')).toBeTruthy();
            });
        });

        describe('reminderHelloButton', function() {

            beforeEach(function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['loop']
                    });
                };
            });

            it('should query availableTargets', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                tour.reminderHelloButton();
                expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('availableTargets', jasmine.any(Function));
            });

            it('should show a door-hanger on loop target available', function() {
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                tour.reminderHelloButton();
                expect(Mozilla.UITour.showHighlight.calledWith('loop')).toBeTruthy();
                expect(Mozilla.UITour.showInfo.calledWith('loop')).toBeTruthy();
            });

            it('should do nothing if loop target is not available', function() {
                Mozilla.UITour.getConfiguration = function(configName, callback) {
                    callback({
                        targets: ['foo']
                    });
                };
                spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
                tour.reminderHelloButton();
                expect(Mozilla.UITour.showHighlight.called).toBeFalsy();
                expect(Mozilla.UITour.showInfo.called).toBeFalsy();
            });

        });

    });

    describe('hideAnnotations', function () {

        it('should hide UITour annotations', function() {
            tour.hideAnnotations();
            expect(Mozilla.UITour.hideMenu.calledWith('appMenu')).toBeTruthy();
            expect(Mozilla.UITour.hideHighlight.called).toBeTruthy();
            expect(Mozilla.UITour.hideInfo.called).toBeTruthy();
        });

        it('should hide Hello panel if it is open', function() {
            Mozilla.UITour.getConfiguration = function(configName, callback) {
                callback({
                    targets: ['loop']
                });
            };
            spyOn(Mozilla.UITour, 'getConfiguration').andCallThrough();
            tour.showHelloPanel();
            tour.hideAnnotations();
            expect(Mozilla.BrowserTour.prototype.hideHelloPanel).toHaveBeenCalled();
        });
    });

    describe('getText', function () {

        it('should string HTML from a string', function() {
            var text = tour.getText('Some <strong>text</strong>')
            expect(text).toEqual('Some text');
        });
    });

    describe('Tour interactions', function() {

        beforeEach(function() {
            Mozilla.UITour.getConfiguration = sinon.stub();
            tour.startTour();
            clock.tick(1000);
        });

        describe('Button navigation', function() {

            it('should advance the tour when clicking step button', function() {
                $('button.step').trigger('click');
                expect(Mozilla.BrowserTour.prototype.onStepClick).toHaveBeenCalled();
            });

            it('should go to forwards when clicking next step', function() {
                $('button.step.next').trigger('click');
                expect(Mozilla.BrowserTour.prototype.goToTourStep).toHaveBeenCalledWith('next');
            });

            it('should go to back when clicking previous step', function() {
                $('button.step.prev').trigger('click');
                expect(Mozilla.BrowserTour.prototype.goToTourStep).toHaveBeenCalledWith('prev');
            });

            it('should hide UITour annotations before advancing tour step', function() {
                $('button.step').trigger('click');
                expect(Mozilla.UITour.hideHighlight.called).toBeTruthy();
                expect(Mozilla.UITour.hideInfo.called).toBeTruthy();
                expect(Mozilla.UITour.hideMenu.called).toBeTruthy();
            });

            it('clicking the tour mask should close the tour', function() {
                $('#ui-tour-mask').trigger('click');
                expect(Mozilla.BrowserTour.prototype.closeTour).toHaveBeenCalled();
            });

            it('clicking primary cta button should call close the tour', function() {
                $('.cta button').trigger('click');
                expect(Mozilla.BrowserTour.prototype.startBrowsing).toHaveBeenCalled();
                expect(Mozilla.BrowserTour.prototype.doCloseTour).toHaveBeenCalled();
            });
        });

        describe('Keyboard navigation', function() {

            it('should close the tour when pressing esc', function() {
                var e = jQuery.Event('keyup');
                e.which = 27;
                $('body').trigger(e);
                expect(Mozilla.BrowserTour.prototype.closeTour).toHaveBeenCalled();
            });

            it('should go to the previous step on left arrow press', function() {
                var e = jQuery.Event('keyup');
                e.which = 37;
                $('.ui-tour-list > li.current').removeClass('current');
                $('.ui-tour-list > li:last').addClass('current');
                $('body').trigger(e);
                expect(Mozilla.BrowserTour.prototype.goToTourStep).toHaveBeenCalledWith('prev');
            });

            it('should go to the next step on right arrow press', function() {
                var e = jQuery.Event('keyup');
                e.which = 39;
                $('body').trigger(e);
                expect(Mozilla.BrowserTour.prototype.goToTourStep).toHaveBeenCalledWith('next');
            });
        });

        describe('onTourLinkClick', function () {

            it('should go to the next step if available', function() {
                $('.ui-tour-list > li.current a.more').trigger('click');
                expect(Mozilla.BrowserTour.prototype.onTourLinkClick).toHaveBeenCalled();
                expect(Mozilla.BrowserTour.prototype.goToTourStep).toHaveBeenCalledWith('next');
            });

            it('should close the tour if on last step', function() {
                $('.ui-tour-list > li.current').removeClass('current');
                $('.ui-tour-list > li:last').addClass('current');
                $('.ui-tour-list > li.current a.more').trigger('click');
                expect(Mozilla.BrowserTour.prototype.onTourLinkClick).toHaveBeenCalled();
                expect(Mozilla.BrowserTour.prototype.doCloseTour).toHaveBeenCalled();
            });
        });

        describe('closeTour', function () {

            it('clicking close button should close the tour', function() {
                $('button.close').trigger('click');
                expect(Mozilla.BrowserTour.prototype.closeTour).toHaveBeenCalled();
            });

            it('should minimize the tour if not on last step', function() {
                $('button.close').trigger('click');
                expect(Mozilla.BrowserTour.prototype.doCompactTour).toHaveBeenCalled();
            });

            it('should close the tour if on last step', function() {
                $('.ui-tour-list > li.current').removeClass('current');
                $('.ui-tour-list > li:last').addClass('current');
                $('button.close').trigger('click');
                expect(Mozilla.BrowserTour.prototype.doCloseTour).toHaveBeenCalled();
            });
        });

        describe('doCloseTour', function () {

            it('should call hide annotations before closing', function() {
                tour.doCloseTour();
                expect(Mozilla.BrowserTour.prototype.hideAnnotations).toHaveBeenCalled();
            });

            it('should call onCloseTour after closing', function() {
                tour.doCloseTour();
                clock.tick(700);
                expect(Mozilla.BrowserTour.prototype.onCloseTour).toHaveBeenCalled();
            });
        });

        describe('onCloseTour', function () {

            it('should excecute callback when passed as an option', function() {
                tour.onCloseTour();
                expect(onCloseTourCallback.called).toBeTruthy();
            });
        });

        describe('doCompactTour', function () {

            it('should call hide annotations before closing', function() {
                tour.doCompactTour();
                expect(Mozilla.BrowserTour.prototype.hideAnnotations).toHaveBeenCalled();
            });

            it('should call onCompactTour after closing', function() {
                tour.doCompactTour();
                clock.tick(700);
                expect(Mozilla.BrowserTour.prototype.onCompactTour).toHaveBeenCalled();
            });
        });

        describe('onCompactTour', function () {

            it('should excecute callback when passed as an option', function() {
                tour.onCompactTour();
                expect(onCompactTourCallback.called).toBeTruthy();
            });
        });

        describe('expandTour', function () {

            it('should call onTourExpand after expanding', function() {
                tour.expandTour();
                clock.tick(700);
                expect(Mozilla.BrowserTour.prototype.onTourExpand).toHaveBeenCalled();
            });
        });

        describe('onTourExpand', function () {

            it('should show the current step highlights', function() {
                tour.onTourExpand();
                expect(Mozilla.BrowserTour.prototype.showHighlight).toBeTruthy();
            });

            it('should excecute callback when passed as an option', function() {
                tour.onTourExpand();
                expect(onExpandTourCallback.called).toBeTruthy();
            });
        });
    });
});
