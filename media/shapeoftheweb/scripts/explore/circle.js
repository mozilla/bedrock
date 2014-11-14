/* global define:true */
define(['pixi', 'createjs'], function (PIXI, createjs) {
    'use strict';

    var Circle = function () {
        this.elm = new PIXI.DisplayObjectContainer();

        return this;
    };

    Circle.prototype.draw = function (radius) {
        this.radius = radius;

        this._circle = new PIXI.Graphics();
        this.elm.addChild(this._circle);
        this._drawCircle();
        this._circle.hitArea = new PIXI.Rectangle(-radius, -radius, radius * 2, radius * 2);

        if (this.data) {
            this._drawTitle();
        }

        this._resumeStaticAnimation();
    };

    /**
     * setup data
     * @param {object} data
     */
    Circle.prototype.setData = function (data) {
        this.data = data;
    };

    /**
     * Enables static (explore) animation mode
     */
    Circle.prototype._resumeStaticAnimation = function () {
        var d = this.radius / 10; // displace quocient

        if (this._staticScaleTween) {
            createjs.Tween.removeTweens(this._circle.scale);
        }
        this._staticScaleTween = createjs.Tween.get(
            this._circle.scale,
            {loop: true, override: true})
            .to(
                {x:1.2 + (0.2 * d), y:1.2 + (0.2 * d)},
                600 + Math.random() * 500,
                createjs.Ease.sineInOut
            )
            .to(
                {x:1, y:1},
                600 + Math.random() * 500,
                createjs.Ease.sineInOut
            );

        if (this._staticPositionTween) {
            this._staticPositionTween.setPaused(true);
        }
        this._staticPositionTween = createjs.Tween.get(this.elm, {loop: true, override: true})
            .to({
                    x: this._x0 + (-10 + Math.random() * 20) * d,
                    y: this._y0 + (-10 + Math.random() * 20) * d
                },
                1000 + Math.random() * 500,
                createjs.sineInOut)
            .to({
                    x: this._x0 + (-10 + Math.random() * 20) * d,
                    y: this._y0 + (-10 + Math.random() * 20) * d
                },
                1000 + Math.random() * 500,
                createjs.sineInOut)
            .to({
                    x: this._x0 + (-10 + Math.random() * 20) * d,
                    y: this._y0 + (-10 + Math.random() * 20) * d
                },
                1000 + Math.random() * 500,
                createjs.sineInOut)
            .to({
                    x: this._x0 + (-10 + Math.random() * 20) * d,
                    y: this._y0 + (-10 + Math.random() * 20) * d
                },
                1000 + Math.random() * 500,
                createjs.sineInOut)
            .to({x: this._x0, y: this._y0}, 1000 + Math.random() * 500, createjs.sineInOut);
    };

    /**
    * Draws a single circle
    * @param  {number} radius circle radius
    * @param  {number} x initial position on x axis
    * @param  {number} y initial position on y axis
    * @return {DisplayObject} actual element
    */
    Circle.prototype._drawCircle = function (color) {
        if (!color) {
            color = 0x222222;
        }

        this._circle.clear();
        this._circle.beginFill(color);
        this._circle.drawCircle(0, 0, this.radius);
        this._circle.endFill();
    };

    Circle.prototype._drawTitle = function () {
        this._titleStyle = {font: '600 10px "Fira Sans", sans-serif', fill: '#222222'};

        //.split('').join(String.fromCharCode(8202))
        this._title = new PIXI.Text(this.data.getName().toUpperCase(), this._titleStyle);
        this._title.x = 20;
        this._title.y = -this._title.height / 2;
        this._title.alpha = 0;

        if (this.data.getParent) {
            this._subtitleStyle = {font: '800 10px "Fira Sans", sans-serif', fill: '#AAAAAA'}
            this._subtitle = new PIXI.Text(
                this.data.getParent().getName().toUpperCase(),
                this._subtitleStyle
            );
            this._subtitle.x = this._title.x;
            this._subtitle.y = -this._subtitle.height / 2;
            this._subtitle.alpha = 0;
        }
    };

    /**
     * Moves elements away from center
     */
    Circle.prototype.explode = function (radius, center) {
        if (this.elm.alpha === 0) {
            return;
        }
        if (!center) {
            center = {x:0, y:0};
        }

        this.implodeAlpha = this.elm.alpha;

        var angle = Math.atan2(this._y0, this._x0);
        angle += (Math.random() * Math.PI / 16) - (Math.PI / 32);

        this.stopMoving();
        createjs.Tween.get(this.elm, {override: true})
            .wait(Math.random() * 100)
            .to(
                {
                    alpha: 0,
                    x: center.x + Math.cos(angle) * (radius + 200),
                    y: center.y + Math.sin(angle) * (radius + 200)
                },
                (Math.random() * 150) + 200,
                createjs.quartOut);
    };

    /**
     * Recovers from explode()
     */
    Circle.prototype.implode = function () {
        this._staticPositionTween.setPaused(true);
        createjs.Tween.get(this.elm, {override: true})
            .to({alpha: this.implodeAlpha, x: this._x0, y: this._y0},
                (Math.random() * 100) + 200,
                createjs.quartIn)
            .call(this._resumeStaticAnimation.bind(this));
    };

    /**
     * Sets mouse over
     */
    Circle.prototype.mouseOver = function () {
        this.isOver = true;
        if (this.mouseOverCallback) {
            this.mouseOverCallback(this);
        }
    };

    /**
     * Sets mouse out
     */
    Circle.prototype.mouseOut = function () {
        this.isOver = false;
        if (this.mouseOutCallback) {
            this.mouseOutCallback(this);
        }
    };

    Circle.prototype.lightUp = function () {
        this._drawCircle(this.color);

        this.elm.addChild(this._title);
        createjs.Tween.get(this._title, {override: true})
            .to({alpha: 1}, 200, createjs.Ease.quartIn);
    };

    Circle.prototype.lightDown = function () {
        this._drawCircle();

        if (!this._textAlwaysVisible) {
            createjs.Tween.get(this._title, {override: true})
                .to({alpha: 0}, 200, createjs.Ease.quartOut)
                .call(function () {
                    if (this._title.parent) {
                        this.elm.removeChild(this._title);
                    }
                }.bind(this));
        }
    };

    /**
     * Stops static animation and moves element with a bouncy effect
     * @param  {number} x desired x position
     * @param  {number} y desired y position
     * @return {object} Tween for chaining
     */
    Circle.prototype.moveTo = function (x, y) {
        this._x0 = x;
        this._y0 = y;

        this._staticPositionTween.setPaused(true);

        return createjs.Tween.get(this.elm, {override: true})
            .to({x:x, y:y}, (Math.random() * 100) + 400, createjs.Ease.getBackOut(1.5));
    };

    /**
     * Stops static movement
     */
    Circle.prototype.stopMoving = function () {
        this._staticScaleTween.setPaused(true);
        this._staticPositionTween.setPaused(true);
        this.elm.x = Math.round(this.elm.x);
        this.elm.y = Math.round(this.elm.y);
    };

    return Circle;
});