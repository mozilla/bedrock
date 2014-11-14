/* global define:true */
define([
    'pixi',
    'createjs',
    'explore/issue'
], function (
    PIXI,
    createjs,
    Issue
) {
    'use strict';

    var Topic = function (data, index, issues, fakes) {
        this._radius = 70;
        this._linearDist = 40;
        this._linearWidth = 100;
        this.isOver = false;

        this._data = data;
        this._index = index;
        this._issues = issues;
        this._fakes = fakes;

        this.elm = new PIXI.DisplayObjectContainer();

        // this._topicArea;
        // this._linearArea;
        // this._topicTitle;
        // this._topicDesc;

        Topic.TOPICS.push(this);
    };

    Topic.TOPICS = [];

    Topic.prototype.setup = function () {
        // topic mouse over
        this._topicArea = new PIXI.Graphics();
        this._topicArea.i = this._index;
        this._topicArea.hitArea = new PIXI.Rectangle(
            -this._radius,
            -this._radius,
            this._radius * 2,
            this._radius * 2);
        this._topicArea.interactive = true;
        this._topicArea.buttonMode = true;
        this.elm.addChild(this._topicArea);
        this._topicArea.mouseover = this._mouseOver.bind(this);
        this._topicArea.touchstart = this._delayTouchOver.bind(this);

        // topic mouse out area
        var aMargin = 20;
        this._linearArea = new PIXI.Graphics();
        this._linearArea.i = this._index;
        this._linearArea.x = - 100 - aMargin / 2;
        this._linearArea.interactive = true;
        this._linearArea.buttonMode = true;
        this._linearArea.hitArea = new PIXI.Rectangle(
            -this._linearWidth / 2,
            -(this._linearDist * this._issues.length / 2) - aMargin,
            this._linearWidth + 100 + aMargin,
            (this._linearDist * this._issues.length) + aMargin);

        // title
        this._topicTitle = new PIXI.Text(this._data.getName().toUpperCase(),
            {font: '300 22px "Fira Sans", sans-serif', fill: '#222222'});
        this.elm.addChild(this._topicTitle);
        this._topicTitle.x = Math.round(-this._topicTitle.width / 2);
        this._topicTitle.y = Math.round(-this._topicTitle.height / 2);

        // description
        this._topicDesc = new PIXI.Text(this._data.getTagline(),
            {
                font: '300 14px "Fira Sans", sans-serif',
                fill: '#666666',
                wordWrap: true,
                wordWrapWidth: 200,
                align: 'center'
        });
        this.elm.addChild(this._topicDesc);
        this._topicDesc.x = Math.round(-this._topicDesc.width / 2);
        this._topicDesc.y = Math.round(this._radius + 50);

        // topic issue elements
        var issue;
        var i;
        var tH = (this._topicTitle.height / 2) + 5; // half title height
        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.setTextAlwaysVisible(false);
            issue.setIsInteractive(false);

            issue.topicX = (Math.random() * this._radius * 2) - this._radius;
             // from -(radius - tH / 2) to (radius - tH / 2)
            issue.topicY = (Math.random() * (this._radius - tH) * 2) - (this._radius - tH);
            // dont go between -tH/2 and tH/2 (the title area)
            issue.topicY += tH * (issue.topicY > 0 ? 1 : -1);
        }

        for(i = 0; i < this._fakes.length; i ++) {
            issue = this._fakes[i];
            issue.topicX = (Math.random() * this._radius * 2) - this._radius;
            issue.topicY = (Math.random() * this._radius * 2) - this._radius;
        }

        return this;
    };

    Topic.prototype.show = function () {
        var issue;
        var i;
        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.setMode(Issue.MODE_TOPICS);
            issue.moveTo(this.elm.x + issue.topicX, this.elm.y + issue.topicY)
                .call(issue._resumeStaticAnimation.bind(issue));
            issue.topicMouseOver = this._mouseOverIssue.bind(this);
            issue.topicMouseOut = this._mouseOutIssue.bind(this);
            issue.mouseOverS.add(issue.topicMouseOver);
            issue.mouseOutS.add(issue.topicMouseOut);
        }

        for(i = 0; i < this._fakes.length; i ++) {
            issue = this._fakes[i];
            createjs.Tween.get(issue.elm, {override: true})
                .to({
                    alpha: issue.implodeAlpha,
                    x: this.elm.x + issue.topicX,
                    y: this.elm.y + issue.topicY
                }, 300, createjs.Ease.easeIn);
        }
    };

    Topic.prototype.hide = function () {
        var issue;
        var i;

        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            createjs.Tween.get(issue.elm, {override: true})
                .to({alpha: 1}, 300, createjs.Ease.quartIn);
            issue.mouseOverS.remove(issue.topicMouseOver);
            issue.mouseOutS.remove(issue.topicMouseOut);
        }

        for(i = 0; i < this._fakes.length; i ++) {
            this._fakes[i].explode();
        }
    };

    Topic.prototype._mouseOverIssue = function (issue) {
        issue.mouseOver();
    };

    Topic.prototype._mouseOutIssue = function (issue) {
        issue.mouseOut();
    };

    Topic.prototype._delayTouchOver = function () {
        this._timeoutTouchOver = setTimeout(function () {
            this._mouseOver();
        }.bind(this), 1500);
    };

    /**
    * When hovering a topic
    */
    Topic.prototype._mouseOver = function () {
        this.isOver = true;

        this.elm.removeChild(this._topicArea);

        var i;
        var j;
        var topic;
        var issue;

        // move issues to a linear position
        var posX;
        var posY;
        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.setTextAlwaysVisible(true);
            issue.stopMoving();
            posX = this.elm.x + this._linearArea.x;
            posY = this.elm.y + this._linearArea.y;
            posY += (((this._linearDist * i) - this._linearDist * this._issues.length / 2));
            issue.moveTo(Math.round(posX), Math.round(posY));
        }

        // hide fakes
        for(i = 0; i < this._fakes.length; i ++) {
            issue = this._fakes[i];
            issue.implodeAlpha = issue.elm.alpha;
            createjs.Tween.get(issue.elm, {override: true})
                .to({alpha: 0}, 300, createjs.Ease.easeIn);
        }

        // move selected title and desc
        posY = -this._linearDist * this._issues.length / 2;
        posY -= this._topicTitle.height + 50;
        createjs.Tween.get(this._topicTitle, {override: true})
            .to({y: posY}, 300, createjs.Ease.easeIn);
        createjs.Tween.get(this._topicDesc, {override: true})
            .to({alpha: 0}, 300, createjs.Ease.easeIn);

        // tone down other topics
        for(i = 0; i < Topic.TOPICS.length; i ++) {
            topic = Topic.TOPICS[i];
            if (topic._index !== this._index) {
                createjs.Tween.get(topic._topicTitle, {override: true})
                    .to({alpha: 0.5}, 300, createjs.Ease.easeIn);
                createjs.Tween.get(topic._topicDesc, {override: true})
                    .to({alpha: 0.5}, 300, createjs.Ease.easeIn);

                for(j = 0; j < topic._issues.length; j ++) {
                    createjs.Tween.get(topic._issues[j].elm, {override: true})
                        .to({alpha: 0.5}, 300, createjs.Ease.easeIn);
                }
            }
        }
        // this._linearArea.mouseout = this._linearArea.touchend = this._mouseOut.bind(this);
    };

    /**
    * When the mouse leaves a topic
    */
    Topic.prototype._mouseOut = function () {
        this.isOver = false;

        this.elm.addChild(this._topicArea);

        var i;
        var j;
        var topic;
        var issue;

        // move selected title and desc
        createjs.Tween.get(this._topicTitle, {override: true})
            .to({y: -this._topicTitle.height / 2, tint: 0xFFFFFF}, 300, createjs.Ease.easeOut);
        createjs.Tween.get(this._topicDesc, {override: true})
            .to({alpha: 1}, 300, createjs.Ease.easeOut);

        // show fakes
        for(i = 0; i < this._fakes.length; i ++) {
            issue = this._fakes[i];
            createjs.Tween.get(issue.elm, {override: true})
                .to({alpha: issue.implodeAlpha}, 300, createjs.Ease.easeOut);
        }

        // tone down other topics
        for(i = 0; i < Topic.TOPICS.length; i ++) {
            topic = Topic.TOPICS[i];
            if (topic._index !== this._index) {
                createjs.Tween.get(topic._topicTitle, {override: true})
                    .to({alpha: 1}, 300, createjs.Ease.easeIn);
                createjs.Tween.get(topic._topicDesc, {override: true})
                    .to({alpha: 1}, 300, createjs.Ease.easeIn);

                for(j = 0; j < topic._issues.length; j ++) {
                    createjs.Tween.get(topic._issues[j].elm, {override: true})
                        .to({alpha: 1}, 300, createjs.Ease.easeIn);
                }
            }
        }

        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.setTextAlwaysVisible(false);
            issue.moveTo(this.elm.x + issue.topicX, this.elm.y + issue.topicY)
                .call(issue._resumeStaticAnimation.bind(issue));
        }
    };

    Topic.prototype.moveTo = function (position) {
        var i;
        var issue;

        clearTimeout(this._timeoutTouchOver);
        this._topicArea.mouseover = this._topicArea.touchstart = null;

        createjs.Tween.get(this.elm, {override: true})
            .to({x:position.x, y:position.y}, 300, createjs.Ease.getBackOut(1.5));

        for(i = 0; i < this._issues.length; i ++) {
            issue = this._issues[i];
            issue.moveTo(position.x + issue.topicX, position.y + issue.topicY)
                .call(issue._resumeStaticAnimation.bind(issue));
        }

        for(i = 0; i < this._fakes.length; i ++) {
            issue = this._fakes[i];
            createjs.Tween.get(issue.elm, {override: true})
                .to({
                    alpha: issue.implodeAlpha,
                    x: position.x + issue.topicX,
                    y: position.y + issue.topicY
                }, 300, createjs.Ease.easeIn);
        }

        setTimeout(function resumeEvents () {
            this._topicArea.mouseover = this._topicArea.touchstart = this._mouseOver.bind(this);
        }.bind(this), 5000);
    };

    Topic.prototype.update = function (mousePosition) {
        if (this.isOver) {
            // check for mouse out
            var x0 = this.elm.x + this._linearArea.x + this._linearArea.hitArea.x;
            var x1 = x0 + this._linearArea.hitArea.width;
            var y0 = this.elm.y + this._linearArea.y + this._linearArea.hitArea.y;
            var y1 = y0 + this._linearArea.hitArea.height;

            if (mousePosition.x < x0 || mousePosition.x > x1 ||
                mousePosition.y < y0 || mousePosition.y > y1) {
                this._mouseOut();
            }
        }
    };

    return Topic;
});