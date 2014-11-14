define(['d3'], function (d3) {
    'use strict';

    var InfographicModel = function (id, type, data) {
        this._id = id;
        this._type = type;
        this._header = data.header;
        this._subheader = data.subheader;
        this._dataPoints = data.dataPoints;
        this._source = data.source;
    };

    InfographicModel.prototype.getId = function () {
        return this._id;
    };

    InfographicModel.prototype.getType = function () {
        return this._type;
    };

    InfographicModel.prototype.getHeader = function () {
        return this._header;
    };

    InfographicModel.prototype.getSubheader = function () {
        return this._subheader;
    };

    InfographicModel.prototype.getDataPoints = function () {
        return this._dataPoints;
    };

    InfographicModel.prototype.getSourceName = function () {
        return this._source.name;
    };

    InfographicModel.prototype.getSourceLocation = function () {
        return this._source.src;
    };

    InfographicModel.prototype.drawInfographic = function () {
        // console.log(this._id);
        switch ( this._type ) {
        case 'line-graph':
            this.drawLineGraph();
            break;

        case 'bar-graph':
            this.drawBarGraph();
            break;

        case 'map':
            this.drawMap();
            break;

        case 'static-image':
            this.drawStaticImage();
            break;
        }
        // console.log(this._drawingFunctions[this._type]);
        // var draw = {
        //   "line-graph": function () {
        //     return this.drawLineGraph();
        //   },
        //   "bar-graph": function () {
        //     return this.drawBarGraph();
        //   }
        // }


    };

    return InfographicModel;
});

