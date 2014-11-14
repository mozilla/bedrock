define([
    'angular',
    'jquery'
], function (angular, $) {

    'use strict';

    var scrollService = function (
        $q,
        $timeout,
        windowService
    ) {

        this.$timeout = $timeout;
        this.windowService = windowService;
        this.$q = $q;

        this._elements = {};

        this._scrollElems = {
            all: $('body, html'),
            body: $('body')
        };

        this._scrollOffset = 0;

        this.SCROLL_DEFAULTS = {
            animate: true,
            delay: 0,
            easing: 'easeInOut',
            duration: 1000
        };

        /**
         * Micro "stop the propagation" method.
         * @param {Object} e
         * @returns {boolean}
         */
        this.stopEventPropagation = function (e) {
            e.preventDefault();
            e.stopPropagation(true);
            return false;
        };

        return {
            go: this.go.bind(this),
            setOffset: this.setOffset.bind(this)
        };
    };

    scrollService.$inject = [
        '$q',
        '$timeout',
        'windowService',
        'pubSubService'
    ];

    scrollService.prototype.setOffset = function (forcedOffset) {
        // if offset is passed to .go() method as an option,
        // we force offset to that value
        if (typeof forcedOffset !== 'undefined') {
            this._scrollOffset = forcedOffset;
            return;
        }

        this._scrollOffset = 0;
    };

    scrollService.prototype.go = function (scrollId, opts) {
        var deferred = this.$q.defer();

        var o = $.extend({}, this.SCROLL_DEFAULTS, opts);

        var scrollTop, scrollObj, self = this;

        this.setOffset(o.offset);

        switch (scrollId) {
        case 'top':
            scrollTop = 0;
            break;
        case 'bottom':
            scrollTop = this._scrollElems.body.height();
            break;
        default:
            // Fire initial callback for scroll start
            o.callback && o.callback('start');
            scrollTop = null;
            break;
        }

        function animate() {

            var scrollEvents = 'mousewheel DOMMouseScroll touchmove';

            $(window).bind(scrollEvents, self.stopEventPropagation.bind(self));

            var isCompleted = false;

            // If there is a specific element to scroll to,
            // now is the time to find it. Object selection
            // and offset getting was moved here because if done
            // earlier, the object might not have rendered on its spot
            // and the offset value might be a false one.
            if (scrollTop === null) {
                var elemFromId = (typeof scrollId === 'object') ?
                    scrollId : $('#' + scrollId);

                if (elemFromId.length) {
                    scrollTop = elemFromId.offset().top;
                }
            }

            self._scrollElems.all.animate(
                {
                    scrollTop: scrollTop + self._scrollOffset
                },
                o.duration,
                o.easing,
                function () {
                    // Resolve $q
                    deferred.resolve();

                    if (!isCompleted) {

                        $(window).unbind(scrollEvents);

                        isCompleted = true;
                        scrollObj &&
                            typeof o.callback === 'function' &&
                            o.callback('end');
                    }
                });
        }

        this.$timeout(animate, o.delay);

        return deferred.promise;
    };

    return scrollService;
});
