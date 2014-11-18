/* global define:true */
define([
    'explore/circle',
    'pixi',
    'createjs',
    'signals'
], function (
    Circle,
    PIXI,
    createjs,
    signals
) {
    'use strict';

    var Issue = function (index, canvasSize) {
        this._index = index;
        this._canvasSize = canvasSize;
        this.elm = new PIXI.DisplayObjectContainer();

        this.mouseOverS = new signals.Signal();
        this.mouseOutS = new signals.Signal();
        this.pressS = new signals.Signal();

        this._titleOverStyle = {font: '600 14px "Fira Sans", sans-serif', fill: '#222222'};
        this._topicStyle = {font: '200 12px "Fira Sans", sans-serif', fill: '#222222'};

        return this;
    };

    Issue.prototype = new Circle();
    Issue.prototype.constructor = Issue;

    Issue.MODE_EXPLORE = 'explore';
    Issue.MODE_TOPICS = 'topics';
    Issue.MODE_ISSUES = 'issues';
    Issue.MODE_DETAIL = 'detail';
    Issue.MODES = [
        Issue.MODE_EXPLORE,
        Issue.MODE_TOPICS,
        Issue.MODE_ISSUES,
        Issue.MODE_DETAIL
    ];

    Issue.prototype.setData = function (data) {
        this.mode = Issue.MODE_EXPLORE;
        Circle.prototype.setData.call(this, data);

        var colors = [0x6bb94e, 0xf6c925, 0xdb3f33];
        this.color = colors[this.data._status];

        this._textAlwaysVisible = false;
    };

    /**
     * Draws an issue circle
     * @param  {number} radius desired radius
     * @param  {number} x x position
     * @param  {number} y y position
     */
    Issue.prototype.draw = function (radius, x, y) {
        x = Math.round(x);
        y = Math.round(y);

        Circle.prototype.draw.call(this, radius, x, y);
        this.elm.interactive = true;
        this.elm.buttonMode = true;
        this.isInteractive = true;
        this.elm.index = this._index;

        this.elm.mouseover = this.elm.touchstart = this._onMouseOver.bind(this);
        this.elm.mouseout = this._onMouseOut.bind(this);
        this.elm.mousedown = this._onPress.bind(this);

        // create issue mode specific code
        this._drawIssueMode();
    };

    Issue.prototype._onMouseOver = function () {
        this.mouseOverS.dispatch(this);
    };

    Issue.prototype._onMouseOut = function () {
        this.mouseOutS.dispatch(this);
    };

    Issue.prototype._onPress = function () {
        this.pressS.dispatch(this);
    };

    Issue.prototype._drawIssueMode = function () {
        // bigger, rectangular mask
        this._issueModeMask = new PIXI.Graphics();
        this._issueModeMask.beginFill(0x000000);
        this._issueModeMask.alpha = 0.5;
        this._issueModeMask.drawRect(0, 0, this.elm.stage.width + 300, 80);
        this._issueModeMask.y = -40;

        // container for whats masked by _issueModeMask
        this._issueModeContainer = new PIXI.DisplayObjectContainer();
        this._issueModeContainer.mask = this._issueModeMask;

        // circular mask
        this._issueModeFillMask = new PIXI.Graphics();
        this._issueModeFillMask.beginFill(0xFF0000);
        this._issueModeFillMask.alpha = 0.1;
        this._issueModeFillMask.drawCircle(0, 0, this._canvasSize.x);
        this._issueModeFillMask.endFill();
        this._issueModeFillMask.scale = {x:0, y:0};
        this._issueModeContainer.addChild(this._issueModeFillMask);

        // container for whats masked by _issueModeFillMask
        this._issueModeOverContainer = new PIXI.DisplayObjectContainer();
        this._issueModeOverContainer.mask = this._issueModeFillMask;
        this._issueModeContainer.addChild(this._issueModeOverContainer);

        // color fill
        this._issueModeFiller = new PIXI.Graphics();
        this._issueModeFiller.beginFill(this.color);
        this._issueModeFiller.drawRect(0, 0, this._canvasSize.x, this._canvasSize.y);
        this._issueModeFiller.endFill();
        this._issueModeOverContainer.addChild(this._issueModeFiller);

        // white title
        var style = {font: '200 20px "Fira Sans", sans-serif', fill: '#FFFFFF'};
        this._issueModeTitle = new PIXI.Text(this.data.getName().toUpperCase(), style);
        this._issueModeOverContainer.addChild(this._issueModeTitle);
        this._issueModeTitle.x = this._title.x;
        this._issueModeTitle.y = -10; // -this._issueModeTitle.height / 2
    };

    Issue.prototype.setMode = function (mode) {
        var lastMode = this.mode;
        this.mode = mode;

        if (mode === Issue.MODE_EXPLORE) {
            this.setTextAlwaysVisible(false);
            this.setIsInteractive(true);
        } else if (mode === Issue.MODE_TOPICS) {
            this.setTextAlwaysVisible(false);
            this.setIsInteractive(false);
            this._title.setStyle(this._topicStyle);
            this._title.y = Math.round(-this._title.height / 2);
        } else if (mode === Issue.MODE_ISSUES) {
            this.stopMoving();
            this.setTextAlwaysVisible(true);
            this.setIsInteractive(false);
            this._title.setStyle(this._titleStyle);
            this._title.y = Math.round(-this._title.height / 2);
            if (!this._issueModeArea) {
                this._issueModeArea = new PIXI.Rectangle(0, -40, this.elm.width, 80);
            }
            this.elm.hitArea = this._issueModeArea;
        } else if (mode === Issue.MODE_DETAIL) {
            this.stopMoving();
            this.setTextAlwaysVisible(true);
            this.setIsInteractive(false);
            var style = {font: '300 12px "Fira Sans", sans-serif', fill: '#FFFFFF'};
            this._issueModeTitle.setStyle(style);
            this._issueModeTitle.y = Math.round(-this._title.height / 2);
            // if (!this._issueModeArea) {
            //     this._issueModeArea = new PIXI.Rectangle(0, -40, this.elm.width, 80);
            // }
            // this.elm.hitArea = this._issueModeArea;
        }

        if (lastMode === Issue.MODE_ISSUES) {
            this._title.setStyle(this._titleStyle);
            this._title.y = Math.round(-this._title.height / 2);
            this.elm.hitArea = null;
            this.elm.alpha = 1;
        }
    };

    Issue.prototype.setTextAlwaysVisible = function (isVisible) {
        this._textAlwaysVisible = isVisible;

        if (isVisible && this._title.alpha !== 1) {
            this.elm.addChild(this._title);
            this._title.alpha = 0;
            createjs.Tween.get(this._title, {override: true})
                .to({alpha: 1}, 200, createjs.Ease.quartIn);
        } else if(!this.isOver) {
            createjs.Tween.get(this._title, {override: true})
                .to({alpha: 0}, 200, createjs.Ease.quartOut)
                .call(function () {
                    if (this._title.parent) {
                        this.elm.removeChild(this._title);
                    }
                }.bind(this));
        }
    };

    Issue.prototype.setIsInteractive = function (value) {
        this.isInteractive = value;
    };

    Issue.prototype._superMouseOver = Issue.prototype.mouseOver;
    /**
     * Sets mouse over
     */
    Issue.prototype.mouseOver = function () {
        Issue.prototype._superMouseOver.bind(this)();

        this.stopMoving();
        this.lightUp();

        var totalHeight = this._title.height;

        if (this.mode === Issue.MODE_EXPLORE && this._subtitle) {
            totalHeight += this._subtitle.height + 2;
            this._title.setStyle(this._titleOverStyle);
        }

        this._title.y = Math.round(-totalHeight / 2);

        if (this.mode === Issue.MODE_EXPLORE && this._subtitle) {
            this.elm.addChild(this._subtitle);
            this._subtitle.y = Math.round(this._title.y + this._title.height + 2);
            createjs.Tween.get(this._subtitle, {override: true})
            .to({alpha: 1}, 200, createjs.Ease.quartIn);
        }
    };

    Issue.prototype.issueModeMouseOver = function () {
        Issue.prototype._superMouseOver.bind(this)();

        var globalOrigin = this.elm.toGlobal(new PIXI.Point());

        this.elm.addChild(this._issueModeContainer);
        this.elm.addChild(this._issueModeMask);

        this._issueModeMask.x = -globalOrigin.x;
        // this._issueModeMask.width = this._canvasSize.x - globalOrigin.x;
        this._issueModeFiller.x = -globalOrigin.x;
        this._issueModeFiller.y = -globalOrigin.y;
        this._issueModeFiller.width = this._canvasSize.x + globalOrigin.x;
        this._issueModeFiller.height = this._canvasSize.y + globalOrigin.y;

        createjs.Tween.get(this._issueModeFillMask.scale, {override: true}).to(
            {x:1, y:1},
            200,
            createjs.Ease.sineOut
        );
    };

    Issue.prototype._superMouseOut = Issue.prototype.mouseOut;
    /**
     * Sets mouse out
     */
    Issue.prototype.mouseOut = function () {
        Issue.prototype._superMouseOut.bind(this)();

        var tweenBack = createjs.Tween.get(this.elm, {override: true})
            .to({x: this._x0, y: this._y0}, 500, createjs.Ease.getBackOut(2.5));

        if (this.mode === Issue.MODE_EXPLORE && this._subtitle) {
            tweenBack.call(this._resumeStaticAnimation.bind(this));
            this._title.setStyle(this._titleStyle);
            this._title.y = Math.round(-this._title.height / 2);

            createjs.Tween.get(this._subtitle, {override: true})
                .to({alpha: 0}, 200, createjs.Ease.quartOut)
                .call(function () {
                    if (this._subtitle.parent) {
                        this.elm.removeChild(this._subtitle);
                    }
                }.bind(this));
        }

        this.lightDown();
    };

    Issue.prototype.issueModeMouseOut = function () {
        Issue.prototype._superMouseOut.bind(this)();

        createjs.Tween.get(this._issueModeFillMask.scale, {override: true}).to(
            {x:0, y:0},
            200,
            createjs.Ease.sineIn)
            .call(function () {
                this.elm.removeChild(this._issueModeContainer);
                this.elm.removeChild(this._issueModeMask);
            }.bind(this));
    };

    Issue.prototype.openIssue = function () {
        this.setMode(Issue.MODE_DETAIL);

        var globalOrigin = this.elm.toGlobal(new PIXI.Point());

        this.elm.addChild(this._issueModeContainer);
        this.elm.addChild(this._issueModeMask);

        this._issueModeMask.x = -globalOrigin.x;
        this._issueModeFiller.x = -globalOrigin.x;
        this._issueModeFiller.y = -globalOrigin.y;
        this._issueModeFiller.width = this._canvasSize.x + globalOrigin.x;
        this._issueModeFiller.height = this._canvasSize.y + globalOrigin.y;

        // this._issueModeFillMask.scale = {x:1, y:1};
        this._issueModeMask.y = -globalOrigin.y;
        this._issueModeMask.height = this._canvasSize.y;

        createjs.Tween.get(this._issueModeFillMask.scale, {override: true}).to(
            {x:1, y:1},
            300,
            createjs.Ease.sineOut
        );
    };

    Issue.prototype.closeIssue = function () {
        this.elm.removeChild(this._issueModeContainer);
        this.elm.removeChild(this._issueModeMask);

        this._issueModeFiller.x = 0;
        this._issueModeFiller.y = 0;

        this._issueModeFillMask.scale = {x:0, y:0};
        this._issueModeMask.y = 0;
    };

    /**
     * animation tick
     * @param  {Point} mousePosition current mouse position
     */
    Issue.prototype.update = function (mousePosition) {
        if (this.isOver && this.isInteractive) {
            this.elm.x = Math.round(mousePosition.x);
            this.elm.y = Math.round(mousePosition.y);

            var stickyRadius = 30;
            if (Math.abs(this.elm.x - this._x0) > stickyRadius ||
                    Math.abs(this.elm.y - this._y0) > stickyRadius) {
                this.mouseOut();
            }
        }
        // this.elm.aplha = isOver && !circle.isOver ? 0.5 : 1;
    };

    return Issue;
});