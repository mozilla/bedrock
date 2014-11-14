define(function () {
    'use strict';

    var ExploreService = function ($location, $timeout) {
        this._$location = $location;
        this._$timeout = $timeout;
    };

    ExploreService.prototype.setCanvas = function (canvas) {
        this._canvas = canvas;
        this._canvas.init();
        this._canvas.setEnterIssueCallback(this._onPressIssue.bind(this));
    };

    ExploreService.prototype.switchView = function (view) {
        if (view === 'explore') {
            this._canvas.showExplore();
        } else if (view === 'topics') {
            this._canvas.showTopics();
        } else if (view === 'issues') {
            this._canvas.showIssues();
        } else if (view === 'detail') {
            this._canvas.showDetail();
        }
    };

    ExploreService.prototype._onPressIssue = function (topic, issue) {
        this._$timeout(function () {
            this._$location.url('/en-US/shapeoftheweb/detail/?topic=' + topic + '&issue=' + issue);
        }.bind(this));
    };

    ExploreService.$inject = [
        '$location',
        '$timeout'
    ];

    return ExploreService;
});
