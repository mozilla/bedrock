/**
 * @fileOverview Data Tracking Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
    'use strict';

    /**
     * Terms & Conditions Chart directive
     */
    var ChartDataTrackingDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            scope: true,
            controller: ChartDataTrackingController,
            link: ChartDataTrackingLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/chart-data-tracking.tpl.html'
        };
    };

    /**
     * Controller for Data Tracking Chart directive
     * @constructor
     */
    var ChartDataTrackingController = function (
        $scope,
        $timeout
        )
    {
        this._$scope = $scope;
        this._$timeout = $timeout;

        this._data = $scope.issue.getInfographic().getDataPoints().tracking;

        $scope.tracking = {
            data: this._data
        };
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    ChartDataTrackingController.$inject = [
        '$scope',
        '$timeout'
    ];

    /**
     * Link function for Data Tracking Chart directive
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      jQuery element.
     * @param {object} iAttrs     Directive attributes.
     * @param {object} controller Controller reference.
     */
    var ChartDataTrackingLinkFn = function (scope, iElem, iAttrs, controller) {
        var createBars = function () {
            var $bars = $('.data-tracking__tracker-bar');
            var maxHeight = 200;

            $bars.each(function(idx) {
                var $this = $(this);
                var length = controller._data[idx].percent;
                var percentBar = document.createElement("div");
                percentBar.style.height = ((length * maxHeight)/100) + "px";
                console.log(percentBar.style.height);
                percentBar.classList.add("data-tracking__tracker-bar-percent");

                $this.append(percentBar);
            });
        };

        controller._$timeout(createBars);
    };

    return ChartDataTrackingDirective;
});
