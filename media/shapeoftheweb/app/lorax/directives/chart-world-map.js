/**
 * @fileOverview World Map Chart directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'd3', 'topojson', 'jquery-selectric'], function ($, d3, topojson) {
  'use strict';

  /**
   * World Map Chart directive
   */
  var ChartWorldMapDirective = function () {
    return {
      restrict: 'A',
      replace: true,
      scope: true,
      controller: ChartWorldMapController,
      link: ChartWorldMapLinkFn
    };
  };

  /**
   * Controller for World Map Chart directive
   * @constructor
   */
  var ChartWorldMapController = function (
    $scope,
    $timeout,
    dataService
    )
  {
    this._$scope = $scope;
    this._$timeout = $timeout;
    this._getMap = dataService.getMap();
  };

  /**
   * Array of dependencies to be injected into controller
   * @type {Array}
   */
  ChartWorldMapController.$inject = [
    '$scope',
    '$timeout',
    'dataService'
  ];

  /**
   * Link function for World Map Chart directive
   * @param {object} scope      Angular scope.
   * @param {JQuery} iElem      jQuery element.
   * @param {object} iAttrs     Directive attributes.
   * @param {object} controller Controller reference.
   */
  var ChartWorldMapLinkFn = function (scope, iElem, iAttrs, controller) {
    controller._getMap.then(function (model) {
      var issueId = controller._$scope.issue.getId();

      var mapData = model.geoData;
      var countryData = model.countryData;

      var shadeName = controller._$scope.issue.getInfographic().getDataPoints().countryData.shading.name;
      var shadeValues = controller._$scope.issue.getInfographic().getDataPoints().countryData.shading.values;
      var shadeLegend = controller._$scope.issue.getInfographic().getDataPoints().countryData.shading.legend;
      var displayDataset = controller._$scope.issue.getInfographic().getDataPoints().countryData.display.name;
      var displayUnits = controller._$scope.issue.getInfographic().getDataPoints().countryData.display.units;
      var colorScale = setShading(shadeValues);

      var infographicData = {};
      $.each(countryData, function(key, data) {
        var id = data.id;
        var displayName = data.displayName;
        var shadeData = data[shadeName];
        var displayData = data[displayDataset];

        infographicData[id] = {
          "displayName": displayName,
          "shadeData": shadeData,
          "displayData": displayData,
          "displayUnits": displayUnits
        }
      });
      
      var map = d3.select("#" + issueId + " .infographic__wrapper div")
        .attr("class", "map");
      var mapWidth = $("#" + issueId + " .infographic__wrapper div").width();
      var width = 650;
      var height = 500;

      var defaultCountry = "USA";
      var labelX = 385;
      var labelY = 385;

      var projection = d3.geo.mercator()
          .scale(100)
          .translate([width / 2, height / 1.75]);   
          
      var path = d3.geo.path()
        .projection(projection);   

      var svg = map.append("svg")
        .attr("preserveAspectRatio", "xMidYMid")
        .attr("width", mapWidth)
        .attr("height", mapWidth * height / width);

      svg.append("rect")
        .attr("class", "worldmap__background")
        .attr("width", mapWidth)
        .attr("height", mapWidth * height / width);
      
      var g = svg.append("g");
       
      g.append("g")
        .attr("id", "countries")
        .selectAll("path")
        .data(topojson.feature(mapData, mapData.objects.countries).features) 
        .enter()
        .append("path")
          .attr("id", function(d) { return d.id; })
          .style("fill", function(d) { 
            if (infographicData[d.id] && infographicData[d.id].displayData) {
              return colorScale(infographicData[d.id].shadeData);
            } else {
              return "rgba(0,0,0,0.15)";
            }
          })
          .attr("d", path)
          .style("mask", "url(#maskStripe)")
          .on("mouseover", country_over);

      svg.append("text")
        .attr("class", "worldmap__label worldmap__label-country")
        .attr("x", function() { return labelX;})
        .attr("y", function() { return labelY;})
        .attr("text-anchor", "middle")
        .text(infographicData[defaultCountry].displayName);

      svg.append("text")
        .attr("class", "worldmap__label worldmap__label-data")
        .attr("x", function() { return labelX; })
        .attr("y", function() { return labelY+20; })
        .attr("text-anchor", "middle")
        .text(infographicData["USA"].displayData + infographicData["USA"].displayUnits);  

      g.select("#" + defaultCountry).style("mask","");
      g.select("#" + defaultCountry).style("fill", "#fff");

      initializeSvgFilters(svg);
      drawLegend();
      drawDropdown();

      $("#" + issueId + " .infographic__wrapper div select").selectric('init'); 

      function country_over (d) {
        if (d) {
          if ( infographicData[d.id] && infographicData[d.id].displayData ) {
            selectCountry(d.id);
          }
        }
      }

      function drawLegend() {
        var legend = svg.selectAll(".worldmap__legend")
          .data(shadeLegend)
          .enter()
          .append("g")
            .attr("class", "worldmap__legend")
            .attr("transform", function(d, i) { return "translate(0," + (i*20 + (mapWidth * height / width)/2) + ")";});

        legend.append("rect")
          .attr("x", 0)
          .attr("width", 15)
          .attr("height", 15)
          .style("mask", "url(#maskStripe)")
          .style("fill", function(d, i) { return colorScale(shadeValues[i]-0.01);}); // subtract 0.01 to take scale offset into consideration

        legend.append("text")
          .attr("x", 20)
          .attr("y", 7.5)
          .attr("dy", ".35em")
          .text(function(d) { return d; });
      }

    function drawDropdown() {
      var dropDown = map.append("select")
        .attr("class", "worldmap__dropdown");

      dropDown.append("option")
        .attr("value", "Find a country")
        .text("Find a country");

      $.each(countryData, function(key, data) {
        if (infographicData[data.id] && infographicData[data.id].displayData) {
          dropDown.append("option")
            .attr("value", data.id)
            .text(data.displayName);
        }
      });

      
      $("#" + issueId + " .infographic__wrapper div select").change( function() {
        if ( infographicData[this.value] && infographicData[this.value].displayData ) {
          selectCountry(this.value);
        }
      });
    }

    function selectCountry(countryId) {
      var country = g.select("#" + countryId);

      svg.select(".worldmap__label-country")
        .text("");
      svg.select(".worldmap__label-data")
        .text("");
      g.selectAll("path")
        .style("mask", "url(#maskStripe)")
        .style("fill", function(d) { 
          if (infographicData[d.id] && infographicData[d.id].displayData) {
            return colorScale(infographicData[d.id].shadeData);
          } else {
            return "rgba(0,0,0,0.15)";
          }
        });

      country.style("mask","");
      country.style("fill", "#fff");

      svg.select(".worldmap__label-country")
        .text(infographicData[countryId].displayName);
      svg.select(".worldmap__label-data")
        .text(infographicData[countryId].displayData + infographicData[countryId].displayUnits);
    }

    }.bind(controller));
  };

  function setShading(shadeValues) {
    var opacity = 1.0;
    var minOpacity = 1.0;
    var opacityMod = minOpacity/(shadeValues.length);
    var countryColors = [];
    for (var i = 0; i < shadeValues.length; i++) {
      countryColors.push("rgba(0,0,0," + (opacity-i*opacityMod) + ")");
    }

    var colorScale = d3.scale.threshold()
      .domain(shadeValues)
      .range(countryColors);
    return colorScale;
  }

  function initializeSvgFilters(svg) {
    var defs = svg.append("defs");

    var patternStripe = defs.append("pattern")
      .attr("id", "patternStripe")
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", "100%")
      .attr("height", "100%")
      .append("image")
        .attr("xlink:href", "../images/map_stripe.png")
        .attr("width", "100%")
        .attr("height", "100%");

    var maskStripe = defs.append("mask")
      .attr("id", "maskStripe")
      .append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("fill", "url(#patternStripe)");

  }

  return ChartWorldMapDirective;
});
