/* global define:true */
define([
    'jquery',
    'pixi',
    'createjs',
    'signals',
    'explore/issue',
    'explore/circle',
    'explore/responsive',
    'jquery-mobile'
], function (
    $,
    PIXI,
    createjs,
    signals,
    Issue,
    Circle,
    Responsive
) {
    'use strict';

    var ExploreCanvas = function () {
        this.issues = [];
        this.tags = [];
        this.fakes = [];

        this.canvasSize = new PIXI.Point();

        this.renderStartS = new signals.Signal();
        this.renderEndS = new signals.Signal();

        this.swipeLeftS = new signals.Signal();
        this.swipeRightS = new signals.Signal();
        this.pressIssueS = new signals.Signal();

        return this;
    };

    /**
    * Sets HTML element for PIXI container
    * @param  {object} DOM object
    */
    ExploreCanvas.prototype.init = function (container) {
        this._lastTick = 0;
        this.canvasSize.x = container.width();
        this.canvasSize.y = container.height();

        Responsive.SIZE = this.canvasSize;

        // create pixijs renderer and stage
        this._renderer = new PIXI.CanvasRenderer(
            this.canvasSize.x,
            this.canvasSize.y,
            {transparent: true, antialias: true});
        this._stage = new PIXI.Stage();
        this._stage.interactive = true;
        container.append(this._renderer.view);

        // lines
        this._linesContainer = new PIXI.Graphics();
        this._linesContainer.x = Math.round(this._renderer.width / 2);
        this._linesContainer.y = Math.round(this._renderer.height / 2);
        this._stage.addChild(this._linesContainer);

        // particles
        this._particlesContainer = new PIXI.DisplayObjectContainer();
        this._particlesContainer.interactive = true;
        this._particlesContainer.x = this._linesContainer.x;
        this._particlesContainer.y = this._linesContainer.y;
        this._stage.addChild(this._particlesContainer);

        // start rendering
        requestAnimationFrame(this._render.bind(this));

        this._drawFakes();

        // touch events
        this._stage.touchstart = this._onTouchStart.bind(this);
        $(document).on('swipeleft', container, this._onSwipeLeft.bind(this));
        $(document).on('swiperight', container, this._onSwipeRight.bind(this));
    };

    /**
    * Draw fake circles on canvas
    */
    ExploreCanvas.prototype._drawFakes = function () {
        var seed;
        var rSeed;
        var circle;
        for (var i = 0; i < 200; i ++) {
            seed = Math.random() * Math.PI * 2;
            rSeed = Math.pow(Math.random(), 1/3) * (this._exploreRadius - 20);

            circle = new Circle();

            this.fakes.push(circle);
            this._particlesContainer.addChild(circle.elm);

            circle.draw(1, Math.sin(seed) * rSeed, Math.cos(seed) * rSeed);
            circle.elm.alpha = 0.1 + (0.3 * rSeed / this._exploreRadius);
        }
    };

    /**
    * Draw tags on canvas
    */
    ExploreCanvas.prototype.drawTags = function (tagData) {
        this._tagData = tagData;

        var tag;
        var i;
        var j;
        for (i = 0; i < this._tagData.length; i ++) {
            for (j = 0; j < 5; j ++) { // to add some volume
                tag = new Issue(i, this.canvasSize);
                tag.setIsInteractive(false);

                this.tags.push(tag);
                this._particlesContainer.addChild(tag.elm);

                tag.setData(this._tagData[i]);
                tag.draw(2);
                tag.pressS.add(this._onPressIssue.bind(this));
            }
        }
    };

    /**
    * Draw issues on canvas
    */
    ExploreCanvas.prototype.drawIssues = function (issueData) {
        this._issueData = issueData;

        var issue;
        for (var i = 0; i < this._issueData.length; i ++) {
            issue = new Issue(i, this.canvasSize);

            this.issues.push(issue);
            this._particlesContainer.addChild(issue.elm);

            issue.setData(this._issueData[i]);
            issue.draw(3 + Math.random() * 5);
            issue.pressS.add(this._onPressIssue.bind(this));
        }
    };

    ExploreCanvas.prototype._onPressIssue = function (issue) {
        this.pressIssueS.dispatch(issue);
    };

    ExploreCanvas.prototype.addChild = function (child) {
        this._stage.addChild(child);
    };

    ExploreCanvas.prototype.removeChild = function (child) {
        this._stage.removeChild(child);
    };

    /**
     * update particle positions
     */
    ExploreCanvas.prototype._updateParticles = function () {
        var i;

        for (i = 0; i < this.issues.length; i ++) {
            this.issues[i].update(this.mousePosition);
        }

        for (i = 0; i < this.tags.length; i ++) {
            this.tags[i].update(this.mousePosition);
        }
    };

    /**
     * Clear lines from canvas
     */
    ExploreCanvas.prototype.clearLines = function () {
        this._linesContainer.clear();
    };

    /**
     * Hide lines container
     */
    ExploreCanvas.prototype.hideLines = function () {
        createjs.Tween.get(this._linesContainer).to({alpha:0}, 300, createjs.Ease.quartOut);
    };

    /**
     * Show lines container
     */
    ExploreCanvas.prototype.showLines = function () {
        createjs.Tween.get(this._linesContainer).to({alpha:1}, 300, createjs.Ease.quartIn);
    };

    /**
     * Draw a line on canvas
     * @param  {Circle} issue origin particle
     * @param  {Circle} related destination particle
     * @param  {Number} color line color
     * @param  {Number} alpha line alpha
     */
    ExploreCanvas.prototype.drawLine = function (issue, related, color, alpha) {
        this._linesContainer.lineStyle(1, color,  alpha);
        this._linesContainer.moveTo(issue.elm.x, issue.elm.y);
        this._linesContainer.lineTo(related.elm.x, related.elm.y);
    };

    /**
    * Get visual element from id
    */
    ExploreCanvas.prototype.getElementById = function (id) {
        var i;

        for (i = 0; i < this.issues.length; i ++) {
            if (this.issues[i].data._id === id) {
                return this.issues[i];
            }
        }

        for (i = 0; i < this.tags.length; i ++) {
            if (this.tags[i].data._id === id) {
                return this.tags[i];
            }
        }
    };

    ExploreCanvas.prototype._onTouchStart = function (event) {
        this._touchPosition = event.global;
    };

    ExploreCanvas.prototype._onSwipeLeft = function () {
        this.swipeLeftS.dispatch();
    };

    ExploreCanvas.prototype._onSwipeRight = function () {
        this.swipeRightS.dispatch();
    };

    /**
     * Updates _mousePosition
     */
    ExploreCanvas.prototype._updateMousePosition = function () {
        // mouse position
        var mousePosition = this._stage.getMousePosition().clone();

        // get position from touch if theres one
        if (this._touchPosition) {
            mousePosition = this._touchPosition.clone();
        }

        // make it relative to container
        mousePosition.x -= this._particlesContainer.x;
        mousePosition.y -= this._particlesContainer.y;

        if (this.autoModePosition) {
            mousePosition = this.autoModePosition.clone();
        }

        this.mousePosition = mousePosition.clone();
    };

    /**
     * do render cycle
     */
    ExploreCanvas.prototype._render = function (tick) {
        this.renderStartS.dispatch();

        // update elements
        this._updateMousePosition();
        this._updateParticles();

        // update tween tick
        createjs.Tween.tick(tick - this._lastTick);
        this._lastTick = tick;

        // render canvas
        this._renderer.render(this._stage);
        requestAnimationFrame(this._render.bind(this));

        this.renderEndS.dispatch();
    };

    return ExploreCanvas;
});