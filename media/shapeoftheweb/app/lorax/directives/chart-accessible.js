/**
 * @fileOverview Accessible Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
  'use strict';

  /**
   * Accessible Chart directive
   */
  var ChartAccessibleDirective = function () {
    return {
      restrict: 'A',
      replace: true,
      scope: true,
      controller: ChartAccessibleController,
      link: ChartAccessibleLinkFn
    };
  };

  /**
   * Controller for Accessible Chart directive
   * @constructor
   */
  var ChartAccessibleController = function (
    $scope,
    $timeout
    )
  {
    this._$scope = $scope;
    this._$timeout = $timeout;
  };

  /**
   * Array of dependencies to be injected into controller
   * @type {Array}
   */
  ChartAccessibleController.$inject = [
    '$scope',
    '$timeout'
  ];

  /**
   * Link function for Accessible Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartAccessibleLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout( function() {
      var imageUrl = controller._$scope.issue.getInfographic().getDataPoints().url;
      var chart = d3.select("#" + controller._$scope.issue.getId() + " .infographic__wrapper div");

      chart.append("h2")
        .attr("class", "accessibility__header")
        .html("<span>1/9</span> of internet users have a vision impairment.");

      chart.append("img")
        .attr("src", imageUrl)
        .attr("class", "accessibility__img");

      chart.append("h2")
        .attr("class", "accessibility__header")
        .text("How to make content more accessible?");
    }.bind(controller));    
  };

  return ChartAccessibleDirective;
});
