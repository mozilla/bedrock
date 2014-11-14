/**
 * @fileOverview Data Portability Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
    'use strict';

    /**
     * Terms & Conditions Chart directive
     */
    var ChartDataPortabilityDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            scope: true,
            controller: ChartDataPortabilityController,
            link: ChartDataPortabilityLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/chart-data-portability.tpl.html'
        };
    };

    /**
     * Controller for Data Portability Chart directive
     * @constructor
     */
    var ChartDataPortabilityController = function (
        $scope,
        $timeout
        )
    {
        this._$scope = $scope;
        this._$timeout = $timeout;

        this._data = $scope.issue.getInfographic().getDataPoints().dataStandards;

        $scope.dataStandards = {
            data: this._data
        };
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    ChartDataPortabilityController.$inject = [
        '$scope',
        '$timeout'
    ];

    /**
     * Link function for Data Portability Chart directive
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      jQuery element.
     * @param {object} iAttrs     Directive attributes.
     * @param {object} controller Controller reference.
     */
    var ChartDataPortabilityLinkFn = function (scope, iElem, iAttrs, controller) {
        controller._$timeout(function() {
            var chart = d3.select("#" + controller._$scope.issue.getId() + " .infographic__wrapper div");
            var divs = d3.selectAll(".data-portability__symbol")
                .append("div")
                    .attr("class", function(d, i) {
                        var answer = controller._$scope.dataStandards.data[i].answer;
                        if (answer === "Yes") {
                            return "data-portability__symbol-yes";
                        } else if (answer === "Partial") {
                            return "data-portability__symbol-partial";
                        } else if (answer === "No") {
                            return "data-portability__symbol-no";
                        }
                    });
        }.bind(controller))
    };

    return ChartDataPortabilityDirective;
});
