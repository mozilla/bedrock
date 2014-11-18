/**
 * @fileOverview Cyber Threats Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
  'use strict';

  /**
   * Cyber Threats Chart directive
   */
  var ChartCyberThreatsDirective = function () {
    return {
      restrict: 'A',
      replace: true,
      scope: true,
      controller: ChartCyberThreatsController,
      link: ChartCyberThreatsLinkFn
    };
  };

  /**
   * Controller for Cyber Threats Chart directive
   * @constructor
   */
  var ChartCyberThreatsController = function (
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
  ChartCyberThreatsController.$inject = [
    '$scope',
    '$timeout'
  ];

  /**
   * Link function for Cyber Threats Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartCyberThreatsLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout(function() {
      var circleData = controller._$scope.issue.getInfographic().getDataPoints().cyberThreats;
      var id = controller._$scope.issue.getId();
      var circleChart = d3.select("#" + id + " .infographic__wrapper div");

      var graphWidth = $("#" + id + " .infographic__wrapper div").width();
      var width = graphWidth;
      var height = graphWidth;

      var circleSize = width/5.5;
      var circleFromCenter = height/2.6;
      var twoPi = (Math.PI*2);

      var threatData = {};

      $.each(circleData, function(key, data) {
        var id = "cyberthreat__name-" + data.name.toLowerCase().replace(/[^A-Z0-9]/ig, "_");
        var description = data.description;

        threatData[id] = {
          "description": description
        }
      });

      var background = circleChart.append("div")
        .attr("class","cyberthreat__background")
        .style("width", width + "px")
        .style("height", height + "px");

      drawLegend();

      var descriptionBox = background.append("div")
        .attr("class", "cyberthreat__descriptionbox")
        .style("left", width/2 - (circleFromCenter - circleFromCenter/5)/2 - circleSize/2 + "px")
        .style("top", height/2 - circleFromCenter/5 + "px");

      var circleContainer = background.append("div")
        .attr("class", "cyberthreat__circlecontainer")
        .style("left", width/2 - (circleFromCenter - circleFromCenter/5)/2 + "px")
        .style("top", height/2 - circleFromCenter/5 + "px");  

      var labels = circleContainer.selectAll("div")
        .data(circleData)
        .enter()
        .append("div")
          .attr("class", "cyberthreat__label")
          .attr("id", function(d) { return "cyberthreat__name-" + d.name.toLowerCase().replace(/[^A-Z0-9]/ig, "_"); })
          .style("left", function(d, i) { return Math.cos( twoPi * i/circleData.length) * circleFromCenter + "px"; })
          .style("top", function(d, i) { return Math.sin( twoPi * i/circleData.length) * circleFromCenter + "px"; })
          .style("width", circleSize + "px")
          .style("height", circleSize + "px")
          .style("border-radius", circleSize + "px")
          .style("background", function(d) { 
            if( d.category === "Vulnerabilities")
              return "rgba(0,0,0,0.7)";
            else if( d.category === "Malware")
              return "rgba(0,0,0,0.45)";
            else( d.category === "Exploits")
              return "rgba(0,0,0,0.2)";
          })
          .on("mouseover", addDescription)
          .append("div")
            .text( function(d) { return d.name; });

      d3.select("#cyberthreat__name-spyware")
        .style("border", "3px solid #fff");

      d3.select(".cyberthreat__descriptionbox")
        .text( threatData["cyberthreat__name-spyware"].description);



      function addDescription() {
        d3.select(".cyberthreat__descriptionbox")
          .text( threatData[this.id].description );

        d3.selectAll(".cyberthreat__label")
          .style("border", "none");

        d3.select(this)
          .style("border", "3px solid #fff");
      }

      function drawLegend() {
        var legend = background.append("div")
          .attr("class", "cyberthreat__legend");

        legend.append("div")
          .text("Vulnerabilities")
          .style("border-left", "15px solid rgba(0,0,0,0.7)");

        legend.append("div")
          .text("Malware")
          .style("border-left", "15px solid rgba(0,0,0,0.45)");

        legend.append("div")
          .text("Exploits")
          .style("border-left", "15px solid rgba(0,0,0,0.2)");

      }

    }.bind(controller));
  }

  return ChartCyberThreatsDirective;
});
