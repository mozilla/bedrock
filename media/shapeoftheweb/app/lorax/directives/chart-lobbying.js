/**
 * @fileOverview Lobbying Chart directive
 * @author <a href='mailto:chris@work.co'>Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
    'use strict';

    /**
     * Line Graph Chart directive
     */
    var ChartLobbyingDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            scope: true,
            controller: ChartLobbyingController,
            link: ChartLobbyingLinkFn
        };
    };

    /**
     * Controller for Lobbying Chart directive
     * @constructor
     */
    var ChartLobbyingController = function (
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
    ChartLobbyingController.$inject = [
        '$scope',
        '$timeout'
    ];

  /**
   * Link function for Lobbying Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartLobbyingLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout( function() {
      var data = controller._$scope.issue.getInfographic().getDataPoints();
      var lineData = data.lineGraphData;
      var id = controller._$scope.issue.getId();
      var lineGraph = d3.select("#" + id + " .infographic__wrapper div");

      var numDatasets = lineData[0].data.length;

      var dollarFormat = d3.format(".3s");

      var graphWidth = $("#" + id + " .infographic__wrapper div").width();

      var margin = {top: 20, right: 20, bottom: 50, left: 10};
      var width = graphWidth;
      var height = graphWidth * .7;

      var svg = lineGraph.append("svg")
        .attr("class", "linegraph__svg")
        .attr("width", width)
        .attr("height", height);
      
      drawPattern();
      drawLegend();
      drawFirstAndLast();
      drawData();

      lineGraph.append("div")
        .attr("class", "linegraph__revolvers")
        .html("* Revolvers are former members of Congress, congressional staffers, or executive branch officials.");

      function drawFirstAndLast() {
        var first = svg.append("g")

        first.append("text")
          .attr("class", "linegraph__firstlast")
          .attr("x", margin.left)
          .attr("y", height - 120)
          .text( function(d) { return dollarFormat(lineData[0].data[0]).replace("G","M")});

        first.append("text")
          .attr("class", "linegraph__firstlast")
          .attr("x", margin.left)
          .attr("y", height - 190)
          .text( function(d) { return lineData[0].data[1]});

        var last = svg.append("g")
          .attr("class", "linegraph__firstlast")

        last.append("text")
          .attr("class", "linegraph__firstlast")
          .attr("x", width - margin.right*2)
          .attr("y", 115)
          .text( function(d) { return dollarFormat(lineData[lineData.length-1].data[0]).replace("G","M")});

        last.append("text")
          .attr("class", "linegraph__firstlast")
          .attr("x", width - margin.right*2)
          .attr("y", 55)
          .text( function(d) { return lineData[lineData.length-1].data[1]});
      }


      function drawLegend() {
        var legend = svg.append("g")
          .attr("class", "linegraph__legend")
          .attr("x", width-margin.right)
          .attr("y", margin.top/3)
          .attr("height", 100)
          .attr("width", 300);

        legend.selectAll("g")
          .data(data.dataLabels)
          .enter()
          .append("g")
            .attr("class", "linegraph__legendLabel");

        var legendLabel = legend.selectAll(".linegraph__legendLabel");

        legendLabel.selectAll("circle")
          .data(data.dataLabels)
          .enter()
          .append("circle")
            .attr("class", function(d, i) { return "linegraph__point_" + i + "_circle"})
            .attr("cx", function(d, i) {return width - margin.right - i*80 - (margin.right*5)})
            .attr("cy", margin.top/3)
            .attr("r", 3);

        legendLabel.selectAll("text")
          .data(data.dataLabels)
          .enter()
          .append("text")
              .attr("class", "linegraph__legendtext")
              .attr("x", function(d, i) {return width - margin.right - i*80 - (margin.right*5) + 10})
              .attr("y", margin.top/3+4)
              .text(function(d) { return d; })
      }

      function drawLabel() {
        var x = d3.scale.linear()
          .range([margin.left, width-margin.right])
          .domain([
            d3.min( lineData, function(d) { return d.label }),
            d3.max( lineData, function(d) { return d.label })
          ]);

        var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .tickFormat( function(d) { return d.toString(); })
          .tickValues( lineData.map( function (d) { return d.label; }) )
          .tickSize(0);

        svg.append("g")
          .attr("class", "linegraph__xaxis_year")
          .attr("transform", "translate(0," + (height-margin.bottom) + ")")
          .call(xAxis);

          return x;
      }

      function drawData() {
        var x = drawLabel();

        for ( var i = 0; i < numDatasets; i++ ) {
          var y = d3.scale.linear()
          .range([height-margin.top, -margin.bottom])
          .domain([
            d3.min( lineData, function(d) { return (d.data[i] * 0.50); }),
            d3.max( lineData, function(d) { return (d.data[i] * 1.25); })
          ]);

          var line = d3.svg.line()    
            .x(function(d) { return x(d.label); })
            .y(function(d) { return y(d.data[i]) }); 

          var datasetGroup = svg.append("g");

          datasetGroup.append("path")
            .datum(lineData)
            .attr("class", "linegraph__line")
            .attr("d", line);

          var point = datasetGroup.selectAll(".point__" + i)
            .data(lineData)
            .enter()
            .append("g")
            .attr("class", function() { return "linegraph__point_" + i; })
            .append("circle")
              .attr("class", function() { return "linegraph__point_" + i + "_circle"})
              .attr("cx", function(d) { return x(d.label); })
              .attr("cy", function(d) { return y(+d.data[i]); })
              .attr("r", 3);
        }
      }      

      function drawPattern() {
        var x = d3.scale.linear()
          .range([margin.left, width-margin.right])
          .domain([
            d3.min( lineData, function(d) { return d.label }),
            d3.max( lineData, function(d) { return d.label })
          ]);

        var diff = Math.floor(Math.abs(x(lineData[0].label) - x(lineData[1].label)));

        var pattern = svg.append("g")
          .attr("class", "linegraph__pattern");

        var years = lineData.map( function(d) { return d.label; });
        years.forEach( function(val) {

          for ( var i = margin.top+15; i < height-margin.bottom; i+=diff ) {
            var xPos = x(val);
            pattern.append("line")
              .attr("x1", xPos+2.5)
              .attr("y1", i)
              .attr("x2", xPos+2.5)
              .attr("y2", i+5);

            pattern.append("line")
              .attr("x1", xPos)
              .attr("y1", i+2.5)
              .attr("x2", xPos+5)
              .attr("y2", i+2.5);              
          }
        });

      }

    }.bind(controller));
  };

    return ChartLobbyingDirective;
});
