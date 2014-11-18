/**
 * @fileOverview Platform Neutrality Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
  'use strict';

  /**
   * Platform Neutrality Chart directive
   */
  var ChartPlatformNeutralityDirective = function () {
    return {
      restrict: 'A',
      replace: true,
      scope: true,
      controller: ChartPlatformNeutralityController,
      link: ChartPlatformNeutralityLinkFn
    };
  };

  /**
   * Controller for Platform Neutrality Chart directive
   * @constructor
   */
  var ChartPlatformNeutralityController = function (
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
  ChartPlatformNeutralityController.$inject = [
    '$scope',
    '$timeout'
  ];

  /**
   * Link function for Platform Neutrality Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartPlatformNeutralityLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout(function() {
      var pieData = controller._$scope.issue.getInfographic().getDataPoints().percentOfUsers;
      var id = controller._$scope.issue.getId();
      var pieChart = d3.select("#" + id + " .infographic__wrapper div");

      var graphWidth = $("#" + id + " .infographic__wrapper div").width();
      var width = graphWidth;
      var height = graphWidth * .4;

      var innerR = 72;
      var outerR = 80;
      var spacing = 200;
      
      var svg = pieChart.append("svg")
        .attr("id", "platformneutrality__svg")
        .attr("width", width)
        .attr("height", height);
        
      var cScale = d3.scale.linear()
        .domain([0,100])
        .range([0, -2*Math.PI]);

      for (var i = 0; i < pieData.length; i++) {
        var userPercent = d3.svg.arc()
          .innerRadius(innerR)
          .outerRadius(outerR)
          .startAngle(0)
          .endAngle(cScale(pieData[i].value));

        var userPercentWedge = d3.svg.arc()
          .innerRadius(0)
          .outerRadius(outerR)
          .startAngle(0)
          .endAngle(cScale(pieData[i].value));

        var restOfUsers = d3.svg.arc()
          .innerRadius(innerR)
          .outerRadius(outerR)
          .startAngle(cScale(pieData[i].value))
          .endAngle(cScale(100));

        svg.append("path")
          .attr("class", "platformneutrality__users")
          .attr("d", userPercent)
          .attr("transform", "translate(" + (i*spacing + outerR) + ",100)");

        svg.append("path")
          .attr("class", "platformneutrality__wedge")
          .attr("d", userPercentWedge)
          .attr("transform", "translate(" + (i*spacing + outerR) + ",100)"); 

        svg.append("path")
          .attr("class", "platformneutrality__others")
          .attr("d", restOfUsers)
          .attr("transform", "translate(" + (i*spacing + outerR) + ",100)");

        svg.append("text")
          .attr("class", "platformneutrality__label")
          .attr("text-anchor", "middle")
          .attr("x", (i*spacing + outerR))
          .attr("y", 210)
          .text(pieData[i].type.toUpperCase());
      }

      svg.append("text")
        .attr("class", "platformneutrality__value")
        .attr("x", outerR - 30)
        .attr("y", 60)
        .text(pieData[0].value + "%");

      svg.append("text")
        .attr("class", "platformneutrality__value")
        .attr("x", spacing + outerR - 45)
        .attr("y", 85)
        .text(pieData[1].value + "%");

      svg.append("text")
        .attr("class", "platformneutrality__value")
        .attr("x", spacing*2 + outerR - 55)
        .attr("y", 105)
        .text(pieData[2].value + "%");

      var legend = pieChart.append("div")
        .attr("class", "platformneutrality__legend");

      var mobile = legend.append("div")
        .attr("class", "platformneutrality__legendbox");

      mobile.append("div")
        .text("Mobile Web");

      mobile.append("div")
        .attr("class", "mobile-web");

      var nativeApp = legend.append("div")
        .attr("class", "platformneutrality__legendbox");

      nativeApp.append("div")
        .text("Native App");

      nativeApp.append("div")
        .attr("class", "native-app")

    }.bind(controller));

  }

  return ChartPlatformNeutralityDirective;
});
