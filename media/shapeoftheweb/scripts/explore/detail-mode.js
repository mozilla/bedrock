/* global define:true */
define([
    'pixi',
    'explore/mode',
    'explore/issue'
], function (
    PIXI,
    Mode,
    Issue
) {
    'use strict';

    var DetailMode = function (canvas) {
        this._canvas = canvas;

        return this;
    };

    DetailMode.prototype = new Mode();
    DetailMode.prototype.constructor = DetailMode;

    DetailMode.prototype.init = function () {

    };

    DetailMode.prototype._onStartShow = function () {
        var i;
        var issue;

        for (i = 0; i < this._canvas.issues.length; i ++) {
            issue = this._canvas.issues[i];
            issue.setMode(Issue.MODE_DETAIL);
        }

        for (i = 0; i < this._canvas.tags.length; i ++) {
            issue = this._canvas.tags[i];
            issue.explode();
        }

        for (i = 0; i < this._canvas.fakes.length; i ++) {
            issue = this._canvas.fakes[i];
            issue.explode();
        }

        this._canvas.clearLines();

        setTimeout(this._onShow.bind(this), 500);
    };

    DetailMode.prototype._onStartHide = function () {
        var i;
        var issue;

        for (i = 0; i < this._canvas.issues.length; i ++) {
            issue = this._canvas.issues[i];
            issue.implode();
        }

        for (i = 0; i < this._canvas.tags.length; i ++) {
            issue = this._canvas.tags[i];
            issue.implode();
        }

        for (i = 0; i < this._canvas.fakes.length; i ++) {
            issue = this._canvas.fakes[i];
            issue.implode();
        }

        setTimeout(this._onHide.bind(this), 0);
    };

    return DetailMode;
});