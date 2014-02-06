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

        // set timeout for highlights
        this.highlightTimer = null;

        this.$body = $('body');
        this.$doc = $(document);
        this.$tour = $('#ui-tour').detach().show();
        this.$mask = $('<div id="ui-tour-mask"><div class="mask-inner"></div></div>');

        // clone the page header and show the mask
        this.$mask.find('.mask-inner').html($('header h1').clone());
        this.$body.append(this.$mask).append(this.$tour).addClass('noscroll');

        this.$tourList = $('.ui-tour-list');
        this.$prevButton = $('button.prev');
        this.$nextButton = $('button.next');
        this.$closeButton = $('button.close');
        this.$progress = $('.progress-step');
        this.$compactTitle = $('.compact-title');

        // bind UITour event listeners
        this.bindEvents();
    }

    /*
     * Show the initial door-hanger menu that begins the tour
     */
    BrowserTour.prototype.init = function () {
        // show the door hanger if the tab is visible
        if (!document.hidden) {
            $('.tour-init').trigger('tour-step');
            // temp workaround if bug 968039 does not make it into Aurora 29
            // fixes highlight position first time browser is opened.
            Mozilla.UITour.showHighlight("appMenu");
        }
    };

    /*
     * Bind custom events to handle calls to Mozilla.UITour
     * as well as regular event listeners for UI interaction
     */
    BrowserTour.prototype.bindEvents = function () {
        // door-hanger menu buttons
        var buttons = [
            {
                label: window.trans('later'),
                style: 'link',
                callback: this.postponeTour.bind(this)
            },
            {
                label: window.trans('start'),
                callback: this.startTour.bind(this)
            }
        ];

        // show the door-hanger info panel
        $('.tour-init').on('tour-step', function () {
            var icon = Mozilla.ImageHelper.isHighDpi() ? this.dataset.iconHighRes : this.dataset.icon;

            Mozilla.UITour.showInfo(
                this.dataset.target,
                window.trans('title'),
                window.trans('text'),
                icon,
                buttons
            );
        });

        // show a hightlighted target feature in the browser UI
        $('.tour-highlight').on('tour-step', function () {
            Mozilla.UITour.showHighlight(this.dataset.target);
        });

        // show a targeted menu panel in the browser UI
        $('.tour-menu').on('tour-step', function () {
            Mozilla.UITour.showMenu(this.dataset.target);
        });

        // handle page visibility changes to show the appropriate tour step
        this.$doc.on('visibilitychange', this.handleVisibilityChange.bind(this));

        // carousel event handlers
        this.$doc.on('transitionend', '.ui-tour-list li.current', this.onTourStep.bind(this));
        this.$closeButton.on('click', this.closeTour.bind(this));
        this.$mask.on('click', this.closeTour.bind(this));
        $('.cta button').on('click', this.closeTour.bind(this));
        $('button.step').on('click', this.onStepClick.bind(this));

        // prevent focusing out of mask while initially visible
        this.$doc.on('focus.ui-tour', 'body', $.proxy(function(e) {
            if (!this.tourHasStarted && !this.$mask[0].contains(e.target)) {
                e.stopPropagation();
                this.$mask.focus();
            }
        }, this));

        // toggle floating signpost visibility when tabzilla opens / closes
        $('#tabzilla').on('click', this.toggleSignPost.bind(this));
        $(document).on('keydown', '#tabzilla-panel', $.proxy(function (event) {
            if (event.which === 27 && this.tourIsPostponed) {
                $('.floating-cta').fadeIn();
            }
        }, this));
    };

    /*
     * Postpone the tour until later.
     * Close the tour and display sign-post cta top right corner.
     */
    BrowserTour.prototype.postponeTour = function () {
        this.tourIsPostponed = true;
        var $cta = $('<button class="floating-cta"></button>');
        $cta.text(window.trans('laterCta'));
        this.$body.append($cta);
        $('.floating-cta').one('click', $.proxy(function (e) {
            e.preventDefault();
            this.restartTour();
            gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Signpost CTA']);
        }, this));

        this.doCloseTour();
        gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Not now']);
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
            this.$body.addClass('noscroll');
            this.$mask.show();
            setTimeout(function () {
                that.$mask.removeClass('out');
                that.startTour();
            }, 50);

        } else {
            this.expandTour();
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
     * Triggers the current step tour highlight / interaction
     * Called on `transitionend` event after carousel item animates
     */
    BrowserTour.prototype.onTourStep = function (e) {
        if (e.originalEvent.propertyName === 'transform') {
            var $current = this.$tourList.find('li.current');
            var step = $current.data('step');
            this.tourIsAnimating = false;
            Mozilla.UITour.hideInfo();
            Mozilla.UITour.hideHighlight();
            $current.find('.step-target').delay(100).trigger('tour-step');
            this.$progress.find('.step').text(window.trans('step' + step));
            this.$progress.find('.progress').attr('aria-valuenow', step);
            this.$tourList.find('.tour-step').not('.current').removeClass('visible');

            // hide menu panel when not needed as it has super-sticky special powers
            if (!$current.hasClass('app-menu')) {
                Mozilla.UITour.hideMenu('appMenu');
            }

            // update the button states
            this.updateControls();

            // set focus on the header of current slide
            $current.find('h2').focus();

            // fire callback when reaching the last tour step.
            if ($current.is(':last-child')) {
                this.onTourComplete();
            }

            gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Step ' + step]);
        }
    };

    /*
     * Tour navigation click handler
     */
    BrowserTour.prototype.onStepClick = function (e) {
        e.preventDefault();
        var $button = $(e.target);

        // if the tour is compact do nothing
        // as uses it's own handler
        if ($button.hasClass('up')) {
            return;
        }

        var trans = $button.hasClass('prev') ? 'prev' : 'next';
        this.goToTourStep(trans);
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

        // disable tour control buttons while animating
        $('.ui-tour-controls button').attr('disabled', 'disabled');

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
        this.$progress.find('.step').text(window.trans('step' + step));
        this.$progress.find('.progress').attr('aria-valuenow', step);

        this.updateControls();
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
        Mozilla.UITour.hideHighlight();

        if (this.tourHasStarted) {
            gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Close tour']);
        }

        this.tourIsVisible = false;
        this.tourHasStarted = false;
        this.tourHasFinished = true;

        this.$tour.removeClass('in');
        this.$mask.find('.mask-inner').addClass('out');
        this.$mask.addClass('out');
        this.$mask.one('transitionend', this.onCloseTour.bind(this));
    };

    BrowserTour.prototype.onCloseTour = function () {
        this.$mask.hide();
        this.$body.removeClass('noscroll');
        // unbind ui-tour focus and keyboard event listeners
        this.$doc.off('.ui-tour').focus();
        this.$tour.off('.ui-tour');
    };

    /*
     * Minimize the tour to compact state
     * Called when pressing the close button mid-way through the tour
     */
    BrowserTour.prototype.doCompactTour = function () {
        this.tourIsVisible = false;
        this.tourIsAnimating = true;
        Mozilla.UITour.hideHighlight();
        Mozilla.UITour.hideMenu('appMenu');
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
        this.$mask.one('transitionend', this.onCompactTour.bind(this));

        gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Compact tour']);
    };

    BrowserTour.prototype.onCompactTour = function (e) {
        var title;
        if (e.originalEvent.propertyName === 'opacity') {
            title = this.$tourList.find('li.current h2').text();
            this.$mask.hide();
            this.$body.removeClass('noscroll');

            // fade in the compact modal content
            this.$compactTitle.html('<h2>' + title + '</h2>').fadeIn();
            this.$progress.addClass('compact').fadeIn($.proxy(function () {
                this.tourIsAnimating = false;
            }, this));
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
        setTimeout(function () {
            that.$mask.removeClass('out');
        }, 50);

        this.$mask.one('transitionend', this.onTourExpand.bind(this));

        gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Expand tour']);
    };

    BrowserTour.prototype.onTourExpand = function (e) {
        if (e.originalEvent.propertyName === 'opacity') {
            this.$body.addClass('noscroll');
            this.$tourList.find('li.current .step-target').trigger('tour-step');
            this.$progress.removeClass('compact').fadeIn('slow');
            this.$tourList.find('li.current').find('h2').focus();
            this.$tourList.fadeIn('slow', $.proxy(function () {
                this.tourIsAnimating = false;
            }, this));
        }
    };

    /*
     * Minimizes / closes the tour based on current step
     * Triggered when user presses the esc key
     */
    BrowserTour.prototype.onKeyUp = function (e) {
        var $current = this.$tourList.find('li.current');

        if (this.tourIsVisible && !this.tourIsAnimating) {

            switch (e.keyCode) {
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
     * Starts the tour and animates the carousel up from bottom of viewport
     */
    BrowserTour.prototype.startTour = function () {
        this.updateControls();

        var that = this;
        var $current = this.$tourList.find('li.current');
        var step = $current.data('step');

        this.$progress.find('.step').text(window.trans('step' + step));
        this.$tour.addClass('in').focus();
        this.$tour.attr('aria-expanded', true);
        this.tourIsVisible = true;
        this.tourHasStarted = true;

        // fade out the inner mask messaging that's shown the the page loads
        this.$mask.find('.mask-inner').addClass('out');

        Mozilla.UITour.hideInfo();

        // toggle/close with escape key
        this.$tour.on('keyup.ui-tour', this.onKeyUp.bind(this));

        // prevent focusing out of modal while open
        this.$doc.off('focus.ui-tour').on('focus.ui-tour', 'body', function(e) {
            if (that.tourIsVisible && !that.$tour[0].contains(e.target)) {
                e.stopPropagation();
                that.$tour.focus();
            }
        });

        // show the first tour step
        setTimeout(function () {
            that.$tourList.find('li.current .step-target').trigger('tour-step');
            $current.find('h2').focus();
        }, 500);

        if (!this.tourIsPostponed) {
            gaTrack(['_trackEvent', 'Tour Interaction', 'click', 'Lets go']);
        } else {
            this.tourIsPostponed = false;
        }

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
            clearInterval(this.highlightTimer);
            Mozilla.UITour.hideHighlight();
            Mozilla.UITour.hideInfo();
            Mozilla.UITour.hideMenu('appMenu');

            if (this.tourIsVisible) {
                gaTrack(['_trackEvent', 'Tour Interaction', 'visibility', 'Leave tour']);
            }
        } else {
            // if tab is visible and tour is open, show the current step.
            if (this.tourIsVisible) {
                this.highlightTimer = setTimeout(function () {
                    $current.find('.step-target').trigger('tour-step');
                    that.$progress.find('.step').text(window.trans('step' + step));
                    that.$progress.find('.progress').attr('aria-valuenow', step);
                }, 900);
                gaTrack(['_trackEvent', 'Tour Interaction', 'visibility', 'Return to tour']);
            } else if (!this.tourHasStarted && !this.tourIsPostponed && !this.tourHasFinished) {
                // if tab is visible and tour has not yet started, show the door hanger.
                $('.tour-init').trigger('tour-step');
            }
        }
    };

    window.Mozilla.BrowserTour = BrowserTour;

})(window.jQuery, window.Mozilla);
