/**
 * @fileOverview Window directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['angular', 'jquery'], function (angular, $) {
    'use strict';

    var BREAKPOINTS = {
        0: 'small',
        560: 'medium',
        960: 'large',
        1360: 'xlarge'
    };

    var Window = function () {
        return {
            restrict: 'A',
            controller: WindowController,
            link: WindowLinkFn
        };
    };

    Window.$inject = ['$rootScope'];

    var WindowController = function (
        $scope,
        $rootScope,
        $compile,
        $timeout,
        windowService,
        pubSubService
    ) {

        /**
         * Reference to controller $scope
         * @type {Object}
         */
        this.$scope = $scope;

        /**
         * Reference to application rootScope
         * @type {Object}
         */
        this.$rootScope = $rootScope;

        /**
         * Reference to Angular's compile function
         * @type {Function}
         */
        this.$compile = $compile;

        /**
         * Reference to Angular's timeout function
         * @type {Function}
         */
        this.$timeout = $timeout;

        /**
         * Reference to window service
         * @type {Object}
         */
        this.windowService = windowService;

        /**
         * Reference to pubSub service
         * @type {Object}
         */
        this.pubSubService = pubSubService;

        this._hasPageYOffset = window.pageYOffset !== undefined;
    };

    WindowController.$inject = [
        '$scope',
        '$rootScope',
        '$compile',
        '$timeout',
        'windowService',
        'pubSubService'
    ];

    WindowController.prototype.evaluateBreakpoint = function () {
        var currentBreakpoint = BREAKPOINTS[Object.keys(BREAKPOINTS)[0]];

        // Loop over breakpoints
        for (var breakpoint in BREAKPOINTS) {
            if (breakpoint < this.windowDims.width) {
                currentBreakpoint = BREAKPOINTS[breakpoint];
            }
        }

        if (currentBreakpoint !== this.latestBreakpoint) {
            this.latestBreakpoint = currentBreakpoint;
            this.windowService.setBreakpoint(this.latestBreakpoint);

            // Inform Angular of breakpoint change
            this.$timeout(function () {
                this.$scope.$apply();
            }.bind(this));
        }
    };

    WindowController.prototype.onResize = function () {
        this.windowService.setDimensions(this.windowDims);
        this.evaluateBreakpoint();
    };

    WindowController.prototype.onScroll = function (e) {
        var offset = this._hasPageYOffset ?
            e.originalEvent.currentTarget.pageYOffset :
            (document.documentElement || document.body).scrollTop;

        this.windowService.setScrollTop(offset);
    };

    WindowController.prototype.getBreakpoint = function () {
        return this.windowService.breakpoint;
    };

    WindowController.prototype.setBreakpoint = function (newBreakpoint) {
        this.windowService.setBreakpoint(newBreakpoint);
    };

    var WindowLinkFn = function WindowLinkFn(scope, iElem, iAttrs, controller) {
        var windowEl = $(window);

        var onResize = angular.bind(controller, function () {
            this.windowDims = {
                height: windowEl.innerHeight(),
                width: windowEl.innerWidth()
            };

            // Inform controller and apply scope
            this.onResize();
        });

        function onBreakpointChange(newBreakpoint) {
            iElem
                .removeClass(function (index, css) {
                    return (css.match(/bp-\S+/g) || []).join(' ');
                })
                .addClass('bp-' + newBreakpoint);
        }

        function onDetailModeChange(isDetail) {
            var classMethod = (isDetail === true) ? 'addClass' : 'removeClass';
            iElem[classMethod]('is-detail');
        }

        windowEl
            .on('scroll', controller.onScroll.bind(controller))
            .on('resize', onResize).trigger('resize');

        // init
        onBreakpointChange(
            controller.windowService.breakpoint()
        );

        controller.pubSubService.subscribe(
            'windowService.breakpoint',
            onBreakpointChange
        );

        controller.pubSubService.subscribe(
            'windowService.detailMode',
            onDetailModeChange
        );
    };

    return Window;

});
