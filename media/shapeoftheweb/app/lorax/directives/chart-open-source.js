/**
 * @fileOverview Open Source Chart directive
 * @author <a href='mailto:chris@work.co'>Chris James</a>
 */
define(['jquery', 'd3'], function ($, d3) {
    'use strict';

    /**
     * Open Source Chart directive
     */
    var ChartOpenSourceDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            scope: true,
            controller: ChartOpenSourceController,
            link: ChartOpenSourceLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/chart-open-source.tpl.html'
        };
    };

    /**
     * Controller for Open Source Chart directive
     * @constructor
     */
    var ChartOpenSourceController = function (
        $scope,
        $timeout
        )
    {
        this._$scope = $scope;
        this._$timeout = $timeout;

        $scope.lineGraph = {
          data: $scope.issue.getInfographic().getDataPoints(),
          dataLabels: $scope.issue.getInfographic().getDataPoints().dataLabels
        }
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    ChartOpenSourceController.$inject = [
        '$scope',
        '$timeout'
    ];

  /**
   * Link function for Open Source Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartOpenSourceLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._$timeout( function() {
      var data = controller._$scope.lineGraph.data;
      var lineData = data.lineGraphData;
      var id = controller._$scope.issue.getId();
      var lineGraph = d3.select("#" + id + " .infographic__wrapper div");

      var numDatasets = lineData[0].data.length;

      var dollarFormat = d3.format(".3s");

      var graphWidth = $("#" + id + " .infographic__wrapper div").width();

      var margin = {top: 20, right: 20, bottom: 50, left: 10};
      var width = graphWidth/2.25;
      var height = graphWidth/2.0;

      var svg = lineGraph.append("svg")
        .attr("class", "opensource__svg")
        .attr("width", width)
        .attr("height", height);
        // .style("position", "absolute")
        // .style("left", (graphWidth/2-width/2) + "px")
        // .style("top", height/2 + "px");

      drawPattern();
      //drawFirstAndLast();
      drawData();

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
          .attr("transform", "translate(0," + (height-margin.bottom+10) + ")")
          .call(xAxis);

          return x;
      }

      function drawData() {
        var x = drawLabel();

        for ( var i = 0; i < numDatasets; i++ ) {
          var y = d3.scale.linear()
          .range([height-margin.bottom, margin.top])
          .domain([
            d3.min( lineData, function(d) { return (d.data[i] * 0.50); }),
            d3.max( lineData, function(d) { return (d.data[i] * 1.25); })
          ]);

          var line = d3.svg.line()
            .x(function(d) { return x(d.label); })
            .y(function(d) { return y(d.data[i]) });

          var datasetGroup = svg.append("g")
            .attr("class", function() {
              if ( i < 3 ) {
                return "opensource__dataset-os";
              }
              else {
                return "opensource__dataset-browser"
              }
            });

          datasetGroup.append("path")
            .datum(lineData)
            .attr("class", "linegraph__line opensource__line_" + i)
            .attr("d", line);

          var point = datasetGroup.selectAll(".point__" + i)
            .data(lineData)
            .enter()
            .append("g")
            .attr("class", "opensource__point_" + i)
            .append("circle")
              .attr("class", "opensource__point_" + i + "_circle")
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

        var diff = Math.floor(Math.abs(x(lineData[0].label) - x(lineData[1].label)))/2;

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

    return ChartOpenSourceDirective;
});
