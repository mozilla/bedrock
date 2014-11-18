/* global define:true */
define([
    'stats',
    'explore/explore-canvas',
    'explore/explore-mode',
    'explore/topics-mode',
    'explore/issues-mode',
    'explore/detail-mode',
    'explore/issue',
    'jquery-mobile'
], function (
    Stats,
    ExploreCanvas,
    ExploreMode,
    TopicsMode,
    IssuesMode,
    DetailMode,
    Issue
) {
    'use strict';

    var Explore = function () {
        this._canvas = new ExploreCanvas();
        this._explore = new ExploreMode(this._canvas);
        this._topics = new TopicsMode(this._canvas);
        this._issues = new IssuesMode(this._canvas);
        this._detail = new DetailMode(this._canvas);
    };

    Explore.prototype.init = function (isDebug) {
        this._canvas.drawIssues(this._issueData);
        this._canvas.drawTags(this._tagData);
        this._canvas.pressIssueS.add(this._openIssue.bind(this));

        this._explore.init();
        this._topics.init();
        this._issues.init();
        this._detail.init();

        // FPS count for debugging
        if (isDebug) {
            this._stats = new Stats();
            this._showStats();
        }

        this.showExplore();
    };

    Explore.prototype.setData = function (data) {
        this._issueData = data.getIssues();
        this._tagData = data.getTags();
        this._topicsData = data.getTopics();

        this._topics.setData(this._topicsData);
    };

    Explore.prototype.setContainer = function (container) {
        this._canvas.init(container);
    };

    Explore.prototype.setEnterIssueCallback = function (enterIssueCallback) {
        this.enterIssueCallback = enterIssueCallback;
    };

    /**
    * Shows FPS count
    */
    Explore.prototype._showStats = function () {
        this._stats.setMode(0);
        this._stats.domElement.style.position = 'absolute';
        this._stats.domElement.style.left = '0px';
        this._stats.domElement.style.top = '0px';
        document.body.appendChild(this._stats.domElement);
    };

    /**
    * Go to explore mode
    */
    Explore.prototype.showExplore = function () {
        this._explore.show();
    };

    /**
    * Go to issues mode
    */
    Explore.prototype.showIssues = function () {
        this._issues.show();
    };

    /**
    * Go to topics mode
    */
    Explore.prototype.showTopics = function () {
        this._topics.show();
    };

    Explore.prototype.showDetail = function () {
        this._detail.show();
    };

    Explore.prototype._openIssue = function (issue) {
        this._mode = Issue.MODE_DETAIL;

        if (this.enterIssueCallback) {
            var issueData = issue.data;
            issue.openIssue();
            setTimeout(function () {
                this.enterIssueCallback(issueData.getParent().getId(), issueData.getId());
                this._detail.show();
                issue.closeIssue();
            }.bind(this), 300);
        }
    };

    Explore.prototype._updateScroller = function (mousePosition) {
        // no movement if mouse is out of the canvas
        if (mousePosition.y > this._canvasSize.y ||
            mousePosition.y < -this._canvasSize.y) {
            mousePosition.y = 0;
        }

        // using tan so the movement is smoother
        var tanMouse = Math.tan(mousePosition.y / this._canvasSize.y * Math.PI / 2);

        // no movement if mouse is near the center
        if (Math.abs(tanMouse) < 0.5) {
            tanMouse = 0;
        }

        this._scrollFinalPosition -= tanMouse * 8;

        this._scrollFinalPosition = Math.max(
            Math.min(this._scrollFinalPosition, 0),
            (-(this._scrollArea.y + (this._issueMargin * this._issues.length)) +
            this._scrollArea.height - 200)
        );

        this._scrollPosition += (this._scrollFinalPosition - this._scrollPosition) / 5;

        var i;
        var issue;
        for (i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.elm.y = issue.issueY + this._scrollPosition;
            // issue.elm.alpha = ((1 - Math.abs(issue.elm.y / this._scrollArea.height))) + 0.3;
        }
    };

    return Explore;
});