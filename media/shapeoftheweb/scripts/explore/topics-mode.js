/* global define:true */
define([
    'pixi',
    'explore/mode',
    'explore/topic',
    'explore/responsive'
], function (
    PIXI,
    Mode,
    Topic,
    Responsive
) {
    'use strict';

    var TopicsMode = function (canvas) {
        TopicsMode.FAKES_PER_TOPIC = 20;

        this._canvas = canvas;

        return this;
    };

    TopicsMode.prototype = new Mode();
    TopicsMode.prototype.constructor = TopicsMode;

    TopicsMode.prototype.setData = function (data) {
        this._topicsData = data;
    };

    TopicsMode.prototype.init = function () {
        this._topics = [];
        this._currentTopic = 0;

        this._topicsContainer = new PIXI.DisplayObjectContainer();
        this._topicsContainer.x = Math.round(this._canvas.canvasSize.x / 2);
        this._topicsContainer.y = Math.round(this._canvas.canvasSize.y / 2);

        var i;
        var j;
        var issue;
        var topic;

        for(i = 0; i < this._topicsData.length; i ++) {
            // get all issues for this topic
            var issues = [];
            for(j = 0; j < this._topicsData[i]._issues.length; j ++) {
                issue = this._canvas.getElementById(this._topicsData[i]._issues[j]._id);
                issues.push(issue);
            }

            // get some random fakes for this topic
            var fakes = [];
            for(j = 0; j < TopicsMode.FAKES_PER_TOPIC; j ++) {
                issue = this._getRandomFake();
                fakes.push(issue);
            }

            // create a new topic
            topic = this._topics[i] = new Topic(this._topicsData[i], i, issues, fakes);
            this._topicsContainer.addChild(topic.elm);

            if (Responsive.IS_LARGE()) {
                topic.elm.x = (this._canvas.canvasSize.x - 400) /
                    (this._topicsData.length - 1) * i;
                topic.elm.x -= ((this._canvas.canvasSize.x - 400) / 2);
            } else if (Responsive.IS_MEDIUM()) {
                topic.elm.x = (this._canvas.canvasSize.x - 500) * (i % 2);
                topic.elm.x -= ((this._canvas.canvasSize.x - 500) / 2);
                topic.elm.y =  (350 * Math.floor(i / 2)) - 350;
            } else {
                topic.elm.x = this._canvas.canvasSize.x * i;
            }

            topic.elm.x = Math.round(topic.elm.x);
            topic.elm.y = Math.round(topic.elm.y);

            topic.setup();
        }
    };

    TopicsMode.prototype._getRandomFake = function () {
        return this._canvas.fakes[Math.floor(Math.random() * this._canvas.fakes.length)];
    };

    TopicsMode.prototype._drawLines = function () {
        var i;
        var j;
        var issue;
        var related;
        var relatedItem;
        var tags;
        var isOver;
        var isSameTopic;

        this._canvas.clearLines();

        for (i = 0; i < this._canvas.issues.length; i ++) {
            issue = this._canvas.issues[i];
            related = issue.data.getRelated();
            tags = issue.data.getTags();

            // draw lines connecting related issues
            for (j = 0; j < related.length; j ++) {
                relatedItem = this._canvas.getElementById(related[j]._id);
                isOver = (issue.isOver || relatedItem.isOver);
                isSameTopic = issue.data._parent._id === relatedItem.data._parent._id;

                if (isSameTopic) {
                    this._canvas.drawLine(issue, relatedItem, 0x0, 0.02);
                }
            }
        }
    };

    TopicsMode.prototype._updateTopics = function () {
        for (var i = 0; i < this._topics.length; i ++) {
            this._topics[i].update(this._canvas.mousePosition);
        }
    };

    TopicsMode.prototype._onStartShow = function () {
        this._canvas.addChild(this._topicsContainer);

        var i;
        for (i = 0; i < this._topics.length; i ++) {
            this._topics[i].show();
        }

        this._drawLinesBind = this._drawLines.bind(this);
        this._updateTopicsBind = this._updateTopics.bind(this);
        this._swipeToNextTopicBind = this._swipeToNextTopic.bind(this);
        this._swipeToPrevTopicBind = this._swipeToPrevTopic.bind(this);
        this._canvas.renderStartS.add(this._drawLinesBind);
        this._canvas.renderStartS.add(this._updateTopicsBind);
        this._canvas.swipeLeftS.add(this._swipeToNextTopicBind);
        this._canvas.swipeRightS.add(this._swipeToPrevTopicBind);

         setTimeout(this._onShow.bind(this), 500);
    };

    TopicsMode.prototype._onStartHide = function () {
        this._canvas.removeChild(this._topicsContainer);

        var i;
        for (i = 0; i < this._topics.length; i ++) {
            this._topics[i].hide();
        }

        this._canvas.renderStartS.remove(this._drawLinesBind);
        this._canvas.renderStartS.remove(this._updateTopicsBind);
        this._canvas.swipeLeftS.remove(this._swipeToNextTopicBind);
        this._canvas.swipeRightS.remove(this._swipeToPrevTopicBind);

        setTimeout(this._onHide.bind(this), 0);
    };

    TopicsMode.prototype._swipeToNextTopic = function () {
        var position = new PIXI.Point();
        this._currentTopic = Math.min(this._currentTopic + 1, 3);

        for(var i = 0; i < this._topics.length; i ++) {
            position.x = this._canvas.canvasSize.x * (i - this._currentTopic);
            this._topics[i].moveTo(position.clone());
        }
    };

    TopicsMode.prototype._swipeToPrevTopic = function () {
        var position = new PIXI.Point();
        this._currentTopic = Math.max(this._currentTopic - 1, 0);

        for(var i = 0; i < this._topics.length; i ++) {
            position.x = this._canvas.canvasSize.x * (i - this._currentTopic);
            this._topics[i].moveTo(position.clone());
        }
    };

    return TopicsMode;
});