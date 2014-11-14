/**
 * @fileOverview Static Image Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
  'use strict';

  /**
   * Static Image Chart directive
   */
  var ChartStaticImageDirective = function () {
    return {
      restrict: 'A',
      replace: true,
      scope: true,
      controller: ChartStaticImageController,
      link: ChartStaticImageLinkFn
    };
  };

  /**
   * Controller for Static Image Chart directive
   * @constructor
   */
  var ChartStaticImageController = function (
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
  ChartStaticImageController.$inject = [
    '$scope',
    '$timeout'
  ];

  /**
   * Link function for Static Image Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartStaticImageLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout( function() {
      var imageUrl = controller._$scope.issue.getInfographic().getDataPoints().url;
      var chart = d3.select("#" + controller._$scope.issue.getId() + " .infographic__wrapper div");
      chart.append("img")
        .attr("src", imageUrl);
    }.bind(controller));    
  };

  return ChartStaticImageDirective;
});
