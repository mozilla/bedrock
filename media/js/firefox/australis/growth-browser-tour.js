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
            onTourComplete: null,
            suppressDoorhanger: false
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
        this.tourHasFinished = this.options.suppressDoorhanger;
        this.tourIsVisible = false;
        this.tourIsAnimating = false;
        this.onTourCompleteHasFired = false;

        // set timeout for highlights
        this.highlightTimer = null;

        this.isLargeViewport = matchMedia('(min-width: 800px)');

        this.$body = $('body');
        this.$doc = $(document);
        this.$mask = $('#ui-tour-mask').detach().show();
        this.$maskInner = this.$mask.find('.mask-inner');

        this.$body.append(this.$mask);

        if (!this.options.allowScroll) {
            this.$body.addClass('noscroll');
        }

        this.$mask.focus();

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
        var $p = this.$maskInner.find('.stage p');
        var words = $p.text().split(' ');
        var delay = 80;
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

            // fade in secondary headline
            setTimeout(function () {
                $p.addClass('in');
            }, 1000);

            // show the door hanger if the tab is visible & not suppressing
            if (!document.hidden && !that.options.suppressDoorhanger) {
                // trigger the door hanger
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
                label: window.trans('later'),
                style: 'link',
                callback: this.options.cancelTour.bind(this, 'Not Now')
            },
            {
                label: window.trans('start'),
                style: 'primary',
                callback: this.options.startTour.bind(this, "Let's Go")
            }
        ];

        // callback to postpone tour if user clicks the (x) button
        var options = {
            closeButtonCallback: this.options.cancelTour.bind(this, 'Close')
        };

        // show the door-hanger info panel
        $('.tour-init').on('tour-step', function () {
            var icon = Mozilla.ImageHelper.isHighDpi() ? this.dataset.iconHighRes : this.dataset.icon;

            Mozilla.UITour.showInfo(
                this.dataset.target,
                window.trans('title'),
                window.trans('text'),
                icon,
                buttons,
                options
            );
        });

        // handle page visibility changes to show the appropriate tour step
        this.$doc.on('visibilitychange', this.handleVisibilityChange.bind(this));

        // prevent focusing out of mask while initially visible
        this.$doc.on('focus.ui-tour', 'body', $.proxy(function(e) {
            if (!this.tourHasStarted && !this.$mask[0].contains(e.target)) {
                e.stopPropagation();
                this.$mask.focus();
            }
        }, this));
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
            } else if (mq.matches && that.tourIsVisible) {
                clearInterval(that.highlightTimer);
                that.highlightTimer = setTimeout(function () {
                    that.showHighlight();
                }, 900);
            }
        });
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

        this.$mask.addClass('out');
        setTimeout(this.onCloseTour.bind(this), 600);
    };

    BrowserTour.prototype.onCloseTour = function () {
        this.$maskInner.addClass('out');
        this.$mask.hide();
        this.$body.removeClass('noscroll');

        if (typeof this.options.onCloseTour === 'function') {
            this.options.onCloseTour();
        }
    };

    /*
     * Minimizes / closes the tour based on current step
     * Triggered when user presses the esc key
     */
    BrowserTour.prototype.onKeyUp = function (e) {
        if (this.tourIsVisible && !this.tourIsAnimating) {
            switch (e.which) {
            // esc minimizes the tour
            case 27:
                this.closeTour();
                break;
            }
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
    };

    /*
     * Handles page visibility changes if user leaves/returns to current tab.
     * Tour step UI highlights should hide when user leaves the tab, and appear
     * again when the user returns to the tab.
     */
    BrowserTour.prototype.handleVisibilityChange = function () {
        var that = this;

        // if tab is hidden then hide all the UITour things.
        if (document.hidden) {
            this.hideAnnotations();
        } else {
            // if tab is visible and tour is open, show the current step.
            if (this.tourIsVisible) {
                this.highlightTimer = setTimeout(function () {
                    if (that.tourIsVisible) {
                        that.showHighlight();
                    }
                }, 900);
                // Update page id for Telemetry when returning to tab
                Mozilla.UITour.registerPageID(this.options.id);
            } else if (!this.tourHasStarted && !this.tourHasFinished) {
                // if tab is visible and tour has not yet started, show the door hanger.
                $('.tour-init').trigger('tour-step');
                // Register page id for Telemetry
                Mozilla.UITour.registerPageID(this.options.id);
            }
        }
    };

    window.Mozilla.BrowserTour = BrowserTour;

})(window.jQuery, window.Mozilla);
