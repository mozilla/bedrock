/**
 * @fileOverview Terms & Conditions Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
    'use strict';

    /**
     * Terms & Conditions Chart directive
     */
    var ChartTermsAndConditionsDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            scope: true,
            controller: ChartTermsAndConditionsController,
            link: ChartTermsAndConditionsLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/chart-terms-and-conditions.tpl.html'
        };
    };

    /**
     * Controller for Terms & Conditions Chart directive
     * @constructor
     */
    var ChartTermsAndConditionsController = function (
        $scope,
        $timeout,
        pubSubService,
        windowService
        )
    {
        this._$scope = $scope;
        this._$timeout = $timeout;
        this._pubSubService = pubSubService;
        this._windowService = windowService;

        this._data = $scope.issue.getInfographic().getDataPoints().termsAndConditions;

        $scope.tAndC = {
            data: this._data,
            minutesToString: this.minutesToString.bind(this)
        };

        this._stackMultipliers = {
            'small': 0.85,
            'medium': 1.65,
            'large': 1.65,
            'xlarge': 1.65
        };
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    ChartTermsAndConditionsController.$inject = [
        '$scope',
        '$timeout',
        'pubSubService',
        'windowService'
    ];

    ChartTermsAndConditionsController.prototype.minutesToString = function (mins) {
        var hours = Math.floor(mins / 60);
        var minutes = mins % 60;

        if (hours === 0) {
            return minutes + 'min';
        } else if (hours === 1) {
            return '1 hour ' + minutes + ' min';
        } else {
            return hours + ' hours ' + minutes + ' min';
        }
    };

    /**
     * Link function for Terms and Conditions Chart directive
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      jQuery element.
     * @param {object} iAttrs     Directive attributes.
     * @param {object} controller Controller reference.
     */
    var ChartTermsAndConditionsLinkFn = function (scope, iElem, iAttrs, controller) {
        var createStacks = function () {
            console.log('create');
            var $stacks = $('.terms-company__stacks');

            // clear stacks
            $stacks.html('');

            $stacks.each(function (idx) {
                var $this = $(this);
                var length = controller._data[idx].length;
                var numBars = Math.round(length / 1000) *
                    controller._stackMultipliers[controller._windowService.breakpoint()];

                for (var i = 0; i < numBars; i++) {
                    $this.append('<div class="stacks-item"></div>');
                }
            });
        };

        // init stacks
        controller._$timeout(createStacks);

        // reinit on breakpoint change
        controller._pubSubService.subscribe(
            'windowService.breakpoint',
            createStacks
        );
    };

    return ChartTermsAndConditionsDirective;
});
