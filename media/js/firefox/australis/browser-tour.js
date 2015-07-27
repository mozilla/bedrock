/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

;(function($, Mozilla) {
    'use strict';

    function BrowserTour (options) {

        this.options = {
            id: null,
            helloPageId: null,
            onTourComplete: null
        };

        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty(i)) {
                    this.options[i] = options[i];
                }
            }
        }

        // use all the flags!
        this.tourHasStarted = false;
        this.tourHasFinished = false;
        this.tourIsVisible = false;
        this.tourIsPostponed = false;
        this.tourIsAnimating = false;
        this.onTourCompleteHasFired = false;

        // flag when hello panel is showing
        this.helloPanelVisible = false;

        // set timeout for highlights
        this.highlightTimer = null;

        this.isLargeViewport = matchMedia('(min-width: 800px)');

        this.$window = $(window);
        this.$body = $('body');
        this.$doc = $(document);
        this.$tour = $('#ui-tour').detach().show();
        this.$mask = $('#ui-tour-mask').detach().show();
        this.$maskInner = this.$mask.find('.mask-inner');

        this.$body.append(this.$mask).append(this.$tour);

        if (!this.options.allowScroll) {
            this.$body.addClass('noscroll');
        }

        this.$mask.focus();

        this.$tourList = $('.ui-tour-list');
        this.$prevButton = $('button.prev');
        this.$nextButton = $('button.next');
        this.$closeButton = $('button.close');
        this.$progress = $('.progress-step');
        this.$progressStep = this.$progress.find('.step');
        this.$progressMeter = this.$progress.find('.progress');
        this.$compactTitle = $('.compact-title');
        this.$tourTip = $('.tour-tip');
        this.$tourControls = $('.ui-tour-controls');
        this.$cta = $('.cta');
        this.$inTourLinks = this.$tourList.find('a.more');

        // quick ref elem for door-hanger icons
        this.$iconElem = $('.tour-init');

        // bind UITour event listeners
        this.bindEvents();

        // bind resize handler to hide highlights at smaller viewports
        // as positioning can sometimes be incorrect (Bug 1091785)
        this.bindResize();
    }

    /*
     * Show the initial door-hanger menu that begins the tour
     * and display the 'splash screen' animation.
     */
    BrowserTour.prototype.init = function () {
        var that = this;
        var $p = this.$maskInner.find('p');
        var $main = this.$maskInner.find('.main');
        var words = $p.text().split(' ');
        var delay = $('body').hasClass('html-ltr') ? 100 : 0;
        var $tempEl = $('<div>');

        // wrap each word in a <span> with an incremental
        // transition-delay value.
        $p.empty().show();
        $.each(words, function(i, word) {
            var $span = $('<span>').text(word + ' ');
            $span.css({
                'transition-delay': (i * delay) + 'ms'
            });
            $tempEl.append($span);
        });
        $p.html($tempEl.html());

        setTimeout(function () {
            // animate the mask welcome message
            that.$maskInner.addClass('in');

            setTimeout(function () {
                $p.addClass('in');
            }, 1000);

            // show the door hanger if the tab is visible
            if (!document.hidden) {
                // trigger the door hanger for whatsnew
                $('.tour-init').trigger('tour-step');
            }

        }, 1000);

        // Register page id for Telemetry
        Mozilla.UITour.registerPageID(this.options.id);
    };

    /*
     * Bind custom events to handle calls to Mozilla.UITour
     * as well as regular event listeners for UI interaction
     */
    BrowserTour.prototype.bindEvents = function () {
        // door-hanger menu buttons
        var buttons = [
            {
                label: this.getText(window.trans('later')),
                style: 'link',
                callback: this.postponeTour.bind(this)
            },
            {
                label: this.getText(window.trans('start')),
                style: 'primary',
                callback: this.startTour.bind(this)
            }
        ];

        // callback to postpone tour if user clicks the (x) button
        var options = {
            closeButtonCallback: this.postponeTour.bind(this)
        };

        var doorHangerTitle = this.getText(window.trans('title'));
        var doorHangerText = this.getText(window.trans('text'));

        // show the door-hanger info panel
        $('.tour-init').on('tour-step', function () {
            var icon = Mozilla.ImageHelper.isHighDpi() ? this.dataset.iconHighRes : this.dataset.icon;

            Mozilla.UITour.showInfo(
                this.dataset.target,
                doorHangerTitle,
                doorHangerText,
                icon,
                buttons,
                options
            );

            // temp fix for Bug 1049130
            Mozilla.UITour.showHighlight(this.dataset.target, 'wobble');
            Mozilla.UITour.showHighlight(this.dataset.target, 'wobble');
        });

        // show a hightlighted target feature in the browser UI
        $('.tour-highlight').on('tour-step', function () {
            Mozilla.UITour.showHighlight(this.dataset.target, this.dataset.effect);
        });

        // show a targeted menu panel in the browser UI
        $('.tour-menu').on('tour-step', function () {
            Mozilla.UITour.showMenu(this.dataset.target);
        });

        // 36.0 show hello menu panel
        $('.tour-show-hello-panel').on('tour-step', this.showHelloPanel.bind(this));
        $('.hello-reminder-door-hanger').on('tour-step', this.reminderHelloButton.bind(this));

        // handle page visibility changes to show the appropriate tour step
        this.$doc.on('visibilitychange.ui-tour', this.handleVisibilityChange.bind(this));

        // carousel event handlers
        this.$tour.on('transitionend', '.ui-tour-list li.current', this.onTourStep.bind(this));
        this.$closeButton.on('click', this.closeTour.bind(this));
        this.$mask.on('click', this.closeTour.bind(this));
        $('.cta button').on('click', this.startBrowsing.bind(this));
        $('button.step').on('click', this.onStepClick.bind(this));

        // show tooltips on prev/next buttons
        this.$tourControls.on('mouseenter focus', 'button.step', this.onStepHover.bind(this));
        this.$tourControls.on('mouseleave blur', 'button.step', this.offStepHover.bind(this));

        // alternate tour has in-step links to advance section
        this.$inTourLinks.on('click', this.onTourLinkClick.bind(this));

        // prevent focusing out of mask while initially visible
        this.$doc.on('focus.ui-tour', 'body', $.proxy(function(e) {
            if (!this.tourHasStarted && !this.$mask[0].contains(e.target)) {
                e.stopPropagation();
                this.$mask.focus();
            }
        }, this));
    };

    /*
     * Unbinds events on document and body. Mainly used for testing purposes where
     * multiple prototype instances may be created.
     */
    BrowserTour.prototype.unbindDocument = function() {
        this.$body.removeClass('noscroll');
        this.$body.off('.ui-tour');
        this.$doc.off('.ui-tour');
    };

    /*
     * Hide UITour highlights if browser is resized < 900px as
     * a temp workaround for Bug 1091785
     */
    BrowserTour.prototype.bindResize = function () {
        var that = this;
        this.isLargeViewport.addListener(function (mq) {
            if (!mq.matches && that.tourIsVisible) {
                Mozilla.UITour.hideHighlight();
                Mozilla.UITour.hideInfo();
                Mozilla.UITour.hideMenu('appMenu');
            } else if (mq.matches && that.tourIsVisible) {
                clearInterval(that.highlightTimer);
                that.highlightTimer = setTimeout(function () {
                    that.showHighlight();
                }, 900);
            }
        });
    };

    /*
     * Strips HTML from string to make sure markup
     * does not get injected in any UITour door-hangers.
     * @param string (data attribute string)
     */
    BrowserTour.prototype.getText = function (string) {
        return $('<div/>').html(string).text();
    };

    /*
     *Alternate version of the tour has in-step links to advance sections
     */
    BrowserTour.prototype.onTourLinkClick = function (e) {
        var $current = this.$tourList.find('li.current');
        var step = $current.data('step');
        e.preventDefault();

        if (this.tourIsAnimating || !this.tourIsVisible) {
            return;
        }

        this.$tour.focus();

        if ($current.is(':last-child')) {
            this.doCloseTour();
        } else {
            this.goToTourStep('next');
            step += 1;

            window.dataLayer.push({
                'event': 'first-run-tour',
                'interaction': 'link click to',
                'browserAction': 'Step' + step
            });

        }
    };

    /*
     * Shows tooltips for next/prev steps when mouseenter or focus is applied to button
    */
    BrowserTour.prototype.onStepHover = function (e) {
        e.preventDefault();
        var $button = $(e.target);
        var $current = this.$tourList.find('li.current');
        var tipText;

        // if the tour is compact do nothing
        if ($button.hasClass('up')) {
            return;
        }

        tipText = $button.hasClass('prev') ? $current.data('tipPrev') : $current.data('tipNext');

        if (tipText) {
            this.$tourTip.html(tipText).addClass('show-tip');
        }
    };

    /*
     * Hide tooltips on mouseleave or blur
     */
    BrowserTour.prototype.offStepHover = function (e) {
        e.preventDefault();
        this.$tourTip.removeClass('show-tip');
    };

    /*
     * Postpone the tour until later.
     * Close the tour and display sign-post cta top right corner.
     */
    BrowserTour.prototype.postponeTour = function () {
        var firstTime;
        this.tourIsPostponed = true;
        var $cta = $('<button class="floating-cta"></button>');
        $cta.html(window.trans('laterCta'));
        this.$body.append($cta);
        $('.floating-cta').one('click', $.proxy(function (e) {
            e.preventDefault();
            this.restartTour();
            firstTime = this.checkFirstTime();

            window.dataLayer.push({
                'event': 'first-run-tour',
                'interaction': 'click',
                'browserAction': 'Signpost CTA',
                'firstTime': firstTime
            });

        }, this));

        this.doCloseTour();

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'click',
            'browserAction': 'Not now'
        });
    };

    /*
     * Restarts the tour once postponed.
     * This can be called by an in-page cta or floating signpost cta
     */
    BrowserTour.prototype.restartTour = function () {
        var that = this;
        $('.floating-cta').fadeOut(function () {
            $(this).remove();
        });
        if (!this.tourHasStarted) {
            if (!this.options.allowScroll) {
                this.$body.addClass('noscroll');
            }

            this.$mask.show();
            setTimeout(function () {
                that.$mask.removeClass('out');
                that.startTour();
            }, 50);
        } else {
            this.expandTour();
        }

        if (typeof this.options.onRestartTour === 'function') {
            this.options.onRestartTour();
        }
    };

    /*
     * Toggles floating signpost cta visibility
     * Needed when Tabzilla opens/closes
     */
    BrowserTour.prototype.toggleSignPost = function () {
        var $cta = $('.floating-cta');
        if (this.tourIsPostponed) {
            if ($cta.is(':visible')) {
                $cta.fadeOut();
            } else if (!$cta.is(':visible')) {
                $cta.fadeIn();
            }
        }
    };

    /*
     * Updates the tour UI controls buttons to reflect the current step
     */
    BrowserTour.prototype.updateControls = function () {
        var $current = this.$tourList.find('li.current');

        this.$closeButton.removeAttr('disabled', 'disabled');

        // update prev/next button states
        if ($current.is(':first-child')) {
            this.$prevButton.attr('disabled', 'disabled').addClass('faded');
            this.$nextButton.removeAttr('disabled').removeClass('faded');
        } else if ($current.is(':last-child')) {
            this.$nextButton.attr('disabled', 'disabled').addClass('faded');
            this.$prevButton.removeAttr('disabled').removeClass('faded');
        } else {
            $('.ui-tour-controls button').removeAttr('disabled').removeClass('faded');
        }
    };

    /*
     * Open hello menu panel
     */
    BrowserTour.prototype.showHelloPanel = function () {
        var target = 'loop';
        var that = this;
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets) {
                if ($.inArray(target, config.targets) !== -1) {
                    that.helloPanelVisible = true;
                    Mozilla.UITour.showMenu(target, function () {
                        Mozilla.UITour.registerPageID(that.options.helloPageId);
                        that.$window.one('resize.hello', that.hideHelloPanel.bind(that));
                    });
                } else {
                    that.promptAddHelloButton();
                }
            }

        });
    };

    /*
     * Hide Hello menu panel
     */
    BrowserTour.prototype.hideHelloPanel = function () {
        Mozilla.UITour.hideHighlight();
        Mozilla.UITour.hideMenu('loop');
        this.$window.off('resize.hello');
        this.helloPanelVisible = false;
    };

    /*
     * Show door-hanger prompting user to add the Hello button
     */
    BrowserTour.prototype.promptAddHelloButton = function () {
        var $dataElm = $('.hello-prompt-door-hanger');
        var icon = Mozilla.ImageHelper.isHighDpi() ? this.$iconElem.data('iconHighRes') : this.$iconElem.data('icon');

        var buttons = [
            {
                label: this.getText($dataElm.data('buttonLater')),
                style: 'link',
                callback: this.laterHelloButton.bind(this)
            },
            {
                label: this.getText($dataElm.data('buttonAdd')),
                style: 'primary',
                callback: this.addHelloButton.bind(this)
            }
        ];

        var options = {
            closeButtonCallback: this.closeHelloDoorhanger.bind(this),
            targetCallback: this.closeHelloDoorhanger.bind(this)
        };

        Mozilla.UITour.showHighlight('appMenu', 'wobble');

        Mozilla.UITour.showInfo(
            'appMenu',
            this.getText($dataElm.data('title')),
            this.getText($dataElm.data('text')),
            icon,
            buttons,
            options
        );
    };

    /*
     * Add the Hello icon to the toolbar
     */
    BrowserTour.prototype.addHelloButton = function () {
        var that = this;
        Mozilla.UITour.addNavBarWidget('loop', function() {
            that.highlightHelloButton();

            window.dataLayer.push({
                'event': 'first-run-tour',
                'interaction': 'Add it now',
                'browserAction': 'The Hello icon'
            });

        });
    };

    /*
     * Highlight Hello icon once added to the toolbar
     */
    BrowserTour.prototype.highlightHelloButton = function () {
        var $dataElm = $('.hello-added-door-hanger');
        var icon = Mozilla.ImageHelper.isHighDpi() ? this.$iconElem.data('iconHighRes') : this.$iconElem.data('icon');
        var target = 'loop';

        Mozilla.UITour.showHighlight(target, 'wobble');

        var buttons = [];

        var options = {
            closeButtonCallback: this.closeHelloDoorhanger.bind(this)
        };

        Mozilla.UITour.showInfo(
            target,
            this.getText($dataElm.data('title')),
            this.getText($dataElm.data('text')),
            icon,
            buttons,
            options
        );

        this.$window.one('resize.hello', this.closeHelloDoorhanger.bind(this));
    };

    /*
     * Remind user they can add Hello button later
     */
    BrowserTour.prototype.laterHelloButton = function () {
        var $dataElm = $('.hello-later-door-hanger');
        var icon = Mozilla.ImageHelper.isHighDpi() ? this.$iconElem.data('iconHighRes') : this.$iconElem.data('icon');

        var buttons = [];

        var options = {
            closeButtonCallback: this.closeHelloDoorhanger.bind(this),
            targetCallback: this.closeHelloDoorhanger.bind(this)
        };

        Mozilla.UITour.showInfo(
            'appMenu',
            this.getText($dataElm.data('title')),
            this.getText($dataElm.data('text')),
            icon,
            buttons,
            options
        );

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'Later',
            'browserAction': 'The Hello icon'
        });
    };

    /*
     * Remind user where the Hello icon is
     */
    BrowserTour.prototype.reminderHelloButton = function () {
        var $dataElm = $('.hello-reminder-door-hanger');
        var icon = Mozilla.ImageHelper.isHighDpi() ? this.$iconElem.data('iconHighRes') : this.$iconElem.data('icon');
        var target = 'loop';
        var that = this;

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            var buttons = [];
            var options = {};

            if (config.targets) {
                if ($.inArray(target, config.targets) !== -1) {

                    options = {
                        closeButtonCallback: that.closeHelloDoorhanger.bind(that)
                    };

                    Mozilla.UITour.showHighlight(target, 'wobble');

                    Mozilla.UITour.showInfo(
                        target,
                        that.getText($dataElm.data('title')),
                        that.getText($dataElm.data('text')),
                        icon,
                        buttons,
                        options
                    );

                    that.$window.one('resize.hello', that.closeHelloDoorhanger.bind(that));
                }
            }
        });
    };

    /*
     * Closes Hello door-hanger / highlight
     */
    BrowserTour.prototype.closeHelloDoorhanger = function () {
        Mozilla.UITour.hideHighlight();
        Mozilla.UITour.hideInfo();
        this.$window.off('resize.hello');
    };

    /*
     * Shows current tour step highlight item
     */
    BrowserTour.prototype.showHighlight = function (show) {
        var $current = this.$tourList.find('li.current');
        var $stepTarget = $current.find('.step-target');
        var that = this;
        var target;
        var showHighlight = show || (!document.hidden && this.isLargeViewport.matches);

        // if the tab is not visible when event fires or viewport is too small
        // don't show the highlight step
        if (!showHighlight) {
            return;
        }

        // if we're simply highlighting a target,
        // check it's availability in the UI first
        if ($stepTarget.hasClass('tour-highlight')) {

            Mozilla.UITour.getConfiguration('availableTargets', function (config) {

                target = $stepTarget.data('target');

                if (target && config.targets && $.inArray(target, config.targets) !== -1) {

                    // tour can force sticky menu between steps
                    // using conditional 'app-menu' class
                    if ($current.hasClass('app-menu')) {
                        Mozilla.UITour.showMenu('appMenu');
                    } else {
                        Mozilla.UITour.hideMenu('appMenu');
                    }

                    clearInterval(that.highlightTimer);
                    that.highlightTimer = setTimeout(function () {
                        $stepTarget.trigger('tour-step');
                    }, 200);
                }
            });
        // other UITour actions handle target availability checking
        // in their own 'tour-step' event handlers.
        // So just trigger the event.
        } else {
            clearInterval(this.highlightTimer);
            this.highlightTimer = setTimeout(function () {
                $stepTarget.trigger('tour-step');
            }, 200);
        }
    };

    /*
     * Triggers the current step tour highlight / interaction
     * Called on `transitionend` event after carousel item animates
     */
    BrowserTour.prototype.onTourStep = function (e) {
        if (e.originalEvent.propertyName === 'transform') {
            var $current = this.$tourList.find('li.current');
            var step = $current.data('step');
            var tipText;

            this.tourIsAnimating = false;
            this.showHighlight();

            this.$progressStep.html(window.trans('step' + step));
            this.$progressMeter.attr('aria-valuenow', step);
            this.$tourList.find('.tour-step').not('.current').removeClass('visible');

            // update the button states
            this.updateControls();

            // set focus on the header of current slide
            $current.find('h2').focus();

            if ($current.is(':last-child')) {
                // fire callback when reaching the last tour step.
                this.onTourComplete();
                // show green cta for the last step
                this.$cta.removeAttr('disabled').fadeIn();
            }

            // if user still has hover/focus over a button show the tooltip
            if ($('button.next:hover').length) {
                tipText = $current.data('tipNext');
                if (tipText) {
                    this.$tourTip.html(tipText);
                    this.$tourTip.addClass('show-tip');
                }
            } else if ($('button.prev:hover').length) {
                tipText = $current.data('tipPrev');
                if (tipText) {
                    this.$tourTip.html(tipText);
                    this.$tourTip.addClass('show-tip');
                }
            }
        }
    };

    /*
     * Tour navigation click handler
     */
    BrowserTour.prototype.onStepClick = function (e) {
        e.preventDefault();
        var $button = $(e.target);
        var $current = this.$tourList.find('li.current');
        var step = $current.data('step');
        // if the tour is compact do nothing
        // as uses it's own handler
        if ($button.hasClass('up')) {
            return;
        }

        var trans = $button.hasClass('prev') ? 'prev' : 'next';
        this.goToTourStep(trans);

        if (trans === 'prev') {
            step -= 1;
        } else {
            step += 1;
        }

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'arrow click to',
            'browserAction': 'Step ' + step
        });
    };

    /*
     * Transitions carousel animation to the next/prev step of the tour
     */
    BrowserTour.prototype.goToTourStep = function (trans) {
        var $current = this.$tourList.find('li.current');
        var $prev;
        var $next;

        if (!trans) {
            return;
        }

        this.tourIsAnimating = true;

        // hide any current highlights
        // or info panels
        clearInterval(this.highlightTimer);

        Mozilla.UITour.hideMenu('appMenu');
        Mozilla.UITour.hideInfo();
        Mozilla.UITour.hideHighlight();

        if (this.helloPanelVisible) {
            this.hideHelloPanel();
        }

        this.$tourTip.removeClass('show-tip');

        // disable tour control buttons while animating
        $('.ui-tour-controls button').attr('disabled', 'disabled');

        // if we're moving back from the last step, hide green cta
        if ($current.is(':last-child')) {
            this.$cta.attr('disabled', 'disabled').fadeOut();
        }

        // animate in/out the correct tour panel
        if (trans === 'prev') {
            $current.removeClass('current next-out').addClass('prev-out');
            $prev = $current.prev().addClass('visible');
            // slight delay is needed when animating an element
            // after applying display: block;
            setTimeout(function () {
                $prev.addClass('current');
            }, 50);

        } else if (trans === 'next') {
            $current.removeClass('current prev-out').addClass('next-out');
            $next = $current.next().addClass('visible');
            setTimeout(function () {
                $next.addClass('current');
            }, 50);
        }
    };

    /*
     * Go directly to a specific step in the tour. This can be called from
     * within the web page to go directly to a specific tour step.
     */
    BrowserTour.prototype.goToStep = function (step) {
        var $current = $('.ui-tour-list .tour-step[data-step="' + step + '"]');

        $('.ui-tour-list .tour-step.current').removeClass('current visible');
        $('.ui-tour-list .tour-step').removeClass('prev-out next-out');
        $current.addClass('current visible');
        $('.ui-tour-list .tour-step:gt(' + step + ')').addClass('prev-out');
        $('.ui-tour-list .tour-step:lt(' + step + ')').addClass('next-out');
        this.$progressStep.html(window.trans('step' + step));
        this.$progressMeter.attr('aria-valuenow', step);

        this.updateControls();
    };

    /*
     * Closes the browser tour when user clicks green cta button
     */
    BrowserTour.prototype.startBrowsing = function () {
        if (this.tourIsAnimating || !this.tourIsVisible) {
            return;
        }
        this.doCloseTour();

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'button click',
            'browserAction': 'Start Browsing'
        });
    };

    /*
     * Determines whether tour should be minimized or closed completely
     */
    BrowserTour.prototype.closeTour = function () {
        var $current = this.$tourList.find('li.current');

        if (this.tourIsAnimating || !this.tourIsVisible) {
            return;
        }

        if ($current.is(':last-child')) {
            this.doCloseTour();
        } else {
            this.doCompactTour();
        }
    };

    /*
     * Closes the tour completely
     * Triggered on last step or if user presses esc key
     */
    BrowserTour.prototype.doCloseTour = function () {
        this.tourIsVisible = false;
        this.tourHasStarted = false;
        this.tourHasFinished = true;

        this.hideAnnotations();
        if (this.tourHasStarted) {

            window.dataLayer.push({
                'event': 'first-run-tour',
                'interaction': 'click',
                'browserAction': 'Close tour'
            });

        }

        this.$cta.fadeOut('fast', $.proxy(function () {
            this.$tour.removeClass('in');
            this.$mask.addClass('out');
            setTimeout(this.onCloseTour.bind(this), 600);
        }, this));
    };

    BrowserTour.prototype.onCloseTour = function () {
        this.$mask.find('.mask-inner').addClass('out');
        this.$mask.hide();
        this.$body.removeClass('noscroll');
        // unbind ui-tour focus and keyboard event listeners
        this.$doc.off('.ui-tour').focus();
        this.$tour.off('.ui-tour');

        if (typeof this.options.onCloseTour === 'function') {
            this.options.onCloseTour();
        }
    };

    /*
     * Minimize the tour to compact state
     * Called when pressing the close button mid-way through the tour
     */
    BrowserTour.prototype.doCompactTour = function () {
        this.tourIsVisible = false;
        this.tourIsAnimating = true;

        this.hideAnnotations();

        this.$tour.removeClass('in').addClass('compact');
        this.$tour.attr('aria-expanded', false);

        // fade out the main modal content
        this.$tourList.fadeOut('fast');
        this.$progress.fadeOut('fast');
        this.$prevButton.fadeOut('fast');
        this.$closeButton.fadeOut('fast');

        // apply focus to the 'open' button once tour is compact.
        this.$nextButton.addClass('up').text(window.trans('open')).focus();
        this.$nextButton.off().on('click', this.expandTour.bind(this));

        // fade out the mask so user can interact with the page
        this.$mask.addClass('out');

        setTimeout(this.onCompactTour.bind(this), 600);

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'click',
            'browserAction': 'Compact tour'
        });
    };

    BrowserTour.prototype.onCompactTour = function () {
        var title;
        title = this.$tourList.find('li.current h2').text();
        this.$mask.hide();
        this.$body.removeClass('noscroll');

        // fade in the compact modal content
        this.$compactTitle.html('<h2>' + title + '</h2>').fadeIn();
        this.$progress.addClass('compact').fadeIn($.proxy(function () {
            this.tourIsAnimating = false;
        }, this));

        if (typeof this.options.onCompactTour === 'function') {
            this.options.onCompactTour();
        }
    };

    /*
     * Expand tour from compact state and go back to the step
     * user was on on prior to minimizing the tour.
     */
    BrowserTour.prototype.expandTour = function () {
        var that = this;

        if (this.tourIsAnimating) {
            return;
        }

        this.tourIsVisible = true;
        this.tourIsAnimating = true;

        this.$tour.removeClass('compact').addClass('in').focus();
        this.$tour.attr('aria-expanded', true);
        this.$compactTitle.fadeOut('fast');
        this.$progress.fadeOut('fast');
        this.$prevButton.fadeIn('fast');
        this.$nextButton.off().on('click', this.onStepClick.bind(this));
        this.$nextButton.removeClass('up').text(window.trans('next'));
        this.$closeButton.fadeIn('fast');

        this.$mask.show();

        setTimeout(this.onTourExpand.bind(this), 600);

        setTimeout(function () {
            that.$mask.removeClass('out');
        }, 50);

        window.dataLayer.push({
            'event': 'first-run-tour',
            'interaction': 'click',
            'browserAction': 'Expand tour'
        });
    };

    BrowserTour.prototype.onTourExpand = function () {
        if (!this.options.allowScroll) {
            this.$body.addClass('noscroll');
        }

        this.showHighlight();
        this.$progress.removeClass('compact').fadeIn('slow');
        this.$tourList.find('li.current').find('h2').focus();
        this.$tourList.fadeIn('slow', $.proxy(function () {
            this.tourIsAnimating = false;
        }, this));

        if (typeof this.options.onExpandTour === 'function') {
            this.options.onExpandTour();
        }
    };

    /*
     * Minimizes / closes the tour based on current step
     * Triggered when user presses the esc key
     */
    BrowserTour.prototype.onKeyUp = function (e) {
        var $current = this.$tourList.find('li.current');

        if (this.tourIsVisible && !this.tourIsAnimating) {

            switch (e.which) {
            // esc minimizes the tour
            case 27:
                this.closeTour();
                break;
            // left arrow key to previous step
            case 37:
                if (!$current.is(':first-child')) {
                    this.goToTourStep('prev');
                }
                break;
            // right arrow key to previous step
            case 39:
                if (!$current.is(':last-child')) {
                    this.goToTourStep('next');
                }
                break;
            }
        }
    };

    /*
     * Finds if the tour is taken for the first time
     * for custom dimension
     */
    BrowserTour.prototype.checkFirstTime = function () {
        var firstTime = 'True';
        try {
            if (localStorage.getItem(this.options.id) === 'taken') {
                firstTime = 'False';
            } else {
                localStorage.setItem(this.options.id, 'taken');
            }
            return firstTime;
        } catch (e) {
            return 'False';
        }
    };

    /*
     * Starts the tour and animates the carousel up from bottom of viewport
     */
    BrowserTour.prototype.startTour = function () {
        this.updateControls();

        var that = this;
        var $current = this.$tourList.find('li.current');
        var step = $current.data('step');
        var firstTime;

        this.$progressStep.html(window.trans('step' + step));

        // fade out the inner mask messaging that's shown the the page loads
        this.$maskInner.addClass('out');

        this.$tour.addClass('in').focus();
        this.$tour.attr('aria-expanded', true);
        this.tourIsVisible = true;
        this.tourHasStarted = true;
        this.tourIsAnimating = true;

        Mozilla.UITour.hideHighlight();
        Mozilla.UITour.hideInfo();

        // toggle/close with escape key
        this.$body.on('keyup.ui-tour', this.onKeyUp.bind(this));

        // prevent focusing out of modal while open
        this.$doc.off('focus.ui-tour', 'body').on('focus.ui-tour', 'body', function(e) {
            if (that.tourIsVisible && !that.$tour[0].contains(e.target)) {
                e.stopPropagation();
                that.$tour.focus();
            }
        });

        setTimeout(this.onStartTour.bind(this), 600);

        if (!this.tourIsPostponed) {
            firstTime = this.checkFirstTime();

            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'first-run-start-tour',
                'firstTime': firstTime,
                'browserAction': 'Lets go'
            });
        } else {
            this.tourIsPostponed = false;
        }

    };

    /*
     * When the tour finishes animating in from bottom, trigger the tour step
     */
    BrowserTour.prototype.onStartTour = function () {
        var $current = this.$tourList.find('li.current');
        var that = this;
        $current.find('h2').focus();
        this.tourIsAnimating = false;
        this.highlightTimer = setTimeout(function () {
            that.showHighlight();
        }, 100);
    };

    /*
     * Fire an optional callback when the user reaches last step in the tour
     */
    BrowserTour.prototype.onTourComplete = function () {
        if (typeof this.options.onTourComplete === 'function' && !this.onTourCompleteHasFired) {
            this.options.onTourComplete();
            this.onTourCompleteHasFired = true;
        }
    };

    /*
     * Helper method to hide currently visible highlight annotations
     */
    BrowserTour.prototype.hideAnnotations = function () {
        clearInterval(this.highlightTimer);
        Mozilla.UITour.hideMenu('appMenu');
        Mozilla.UITour.hideHighlight();
        Mozilla.UITour.hideInfo();

        if (this.helloPanelVisible) {
            this.hideHelloPanel();
        }
    };

    /*
     * Handles page visibility changes if user leaves/returns to current tab.
     * Tour step UI highlights should hide when user leaves the tab, and appear
     * again when the user returns to the tab.
     */
    BrowserTour.prototype.handleVisibilityChange = function () {
        var $current = this.$tourList.find('li.current');
        var step = $current.data('step');
        var that = this;

        // if tab is hidden then hide all the UITour things.
        if (document.hidden) {
            this.hideAnnotations();

            if (this.tourIsVisible) {

                window.dataLayer.push({
                    'event': 'first-run-tour-visibility',
                    'browserAction': 'Leave tour'
                });

            }
        } else {
            // if tab is visible and tour is open, show the current step.
            if (this.tourIsVisible) {
                this.highlightTimer = setTimeout(function () {
                    if (that.tourIsVisible) {
                        that.showHighlight();
                        that.$progress.find('.step').html(window.trans('step' + step));
                        that.$progress.find('.progress').attr('aria-valuenow', step);
                    }
                }, 900);

                window.dataLayer.push({
                    'event': 'first-run-tour-visibility',
                    'browserAction': 'Return to tour'
                });

                // Update page id for Telemetry when returning to tab
                Mozilla.UITour.registerPageID(this.options.id);
            } else if (!this.tourHasStarted && !this.tourIsPostponed && !this.tourHasFinished) {
                // if tab is visible and tour has not yet started, show the door hanger.
                $('.tour-init').trigger('tour-step');
                // Register page id for Telemetry
                Mozilla.UITour.registerPageID(this.options.id);
            }
        }
    };

    window.Mozilla.BrowserTour = BrowserTour;

})(window.jQuery, window.Mozilla);
