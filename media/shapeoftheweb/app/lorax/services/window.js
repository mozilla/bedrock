/**
 * Manages sizing and breakpoints.
 *
 * @class core/services/windowService
 */
define(['jquery', 'modernizr', 'pubsub'], function ($, Modernizr) {
    'use strict';

    var windowService = function (pubSubService) {
        var _window = {
            breakpoint: 'small',
            dimensions: {}
        };

        /**
         * Reference to pubSubService
         */
        this.pubSubService = pubSubService;

        /**
         * @method core/services/windowService~getCurrentBreakpoint
         */
        function getCurrentBreakpoint() {
            return _window.breakpoint;
        }

        /**
         * @method core/services/windowService~setBreakpoint
         * @param newBreakpoint {String} Current breakpoint after change.
         */
        function setBreakpoint(newBreakpoint) {
            _window.breakpoint = newBreakpoint;
            pubSubService.publish('windowService.breakpoint', [newBreakpoint]);
        }

        /**
         * @method core/services/windowService~setDimensions
         * @param windowObj
         */
        function setDimensions(windowObj) {
            _window.dimensions = windowObj;
            $.publish('windowService.resize', [windowObj]);
        }

        /**
         * @method core/services/windowService~getWindowDims
         */
        function getWindowDims() {
            return _window.dimensions;
        }

        /**
         * @method core/services/windowService~getScrollPos
         */
        function getScrollTop() {
            return _window.scrollTop;
        }

        /**
         * @method core/services/windowService~setScrollPos
         */
        function setScrollTop(scrollTop) {
            _window.scrollTop = scrollTop;
            $.publish('windowService.scroll', [scrollTop]);
        }

        function subscribe(eventType, callback) {
            $.subscribe('windowService.' + eventType, function (e, res) {
                callback(res);
            });
        }

        function unsubscribe(eventType, callback) {
            $.unsubscribe('windowService.' + eventType, callback);
        }

        function matchMedia(query) {
            return Modernizr.mq(query);
        }

        function getDeviceWindowHeight() {
            // Get zoom level of mobile Safari
            // We use width, instead of height, because there are no vertical toolbars :)
            var zoomLevel = document.documentElement.clientWidth / window.innerWidth;

            // window.innerHeight returns height of the visible area.
            // We multiply it by zoom and get out real height.
            return window.innerHeight * zoomLevel;
        }

        /**
         * @method core/services/windowService~setDetailMode
         * @param detailMode {Bool} Detail mode on/off
         */
        function setDetailMode(detailMode) {
            pubSubService.publish('windowService.detailMode', [detailMode]);
        }

        return {
            setBreakpoint: setBreakpoint,
            breakpoint: getCurrentBreakpoint,
            setDimensions: setDimensions,
            dimensions: getWindowDims,
            setScrollTop: setScrollTop,
            scrollTop: getScrollTop,
            subscribe: subscribe,
            unsubscribe: unsubscribe,
            mq: matchMedia,
            getDeviceWindowHeight: getDeviceWindowHeight,
            setDetailMode: setDetailMode
        };
    };

    windowService.$inject = ['pubSubService'];

    return windowService;
});
