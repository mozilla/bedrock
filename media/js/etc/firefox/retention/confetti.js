/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) { descriptor.writable = true; } Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) { defineProperties(Constructor.prototype, protoProps); } if (staticProps) { defineProperties(Constructor, staticProps); } return Constructor; }; }();

    function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

    var animation = '';
    var search = window.location.search;
    if (search.indexOf('animation=static') >= 0) {
        animation = 'static';
    }

    var requestAnimFrame = function () {
        return window.requestAnimationFrame || window.mozRequestAnimationFrame || function (callback) {
            window.setTimeout(callback, 1000 / 60);
        };
    }();

    // Returns a random number between a range.
    function range(a, b) {
        return (b - a) * Math.random() + a;
    }

    var NUM_CONFETTI = 425;
    var COLORS = ['rgb(255,255,255)', 'rgb(255,112,87)', 'rgb(244,239,50)', 'rgb(23,137,147)'];
    function setupConfetti(id) {
        var canvas = document.getElementById(id);
        var context = canvas.getContext('2d');
        var width = 0;
        var height = 0;

        function resizeWindow() {
            width = canvas.width = canvas.clientWidth;
            height = canvas.height = canvas.clientHeight;
        }
        resizeWindow();

        var defaultOpacity = 0;
        if (animation === 'static') {
            defaultOpacity = 1;
        } else {
            window.addEventListener('resize', resizeWindow, false);
            window.addEventListener('focus', resizeWindow, false);
        }

        var confettiSize = 6;

        var xpos = 0;
        document.addEventListener('mousemove', function (e) {
            xpos = e.pageX / window.innerWidth - 0.5;
        });

        // Initial code thanks to https://codepen.io/linrock/pen/Amdhr
        var Confetti = function () {
            function Confetti() {
                _classCallCheck(this, Confetti);

                this.rgb = COLORS[~~range(0, 4)];
                this.replace();
                this.start = Date.now() / 1000;
                this.now = this.start;
                this.diff = 0;
            }

            _createClass(Confetti, [{
                key: 'replace',
                value: function replace() {
                    this.opacity = defaultOpacity;
                    this.x = range(-100, width - confettiSize + 100);
                    this.y = range(-100, height - confettiSize);
                    this.xmax = width - confettiSize;
                    this.ymax = height - confettiSize;

                    this.dop = range(4, 6);
                    this.vx = (range(-0.2, 0.2) + xpos) * 200;
                    this.vy = confettiSize + range(1, 2) * 150;
                    this.start = Date.now() / 1000;
                    this.now = this.start;
                    this.diff = 0;
                }
            }, {
                key: 'draw',
                value: function draw() {
                    this.now = Date.now() / 1000;
                    this.diff = this.now - this.start;

                    this.x += this.vx * this.diff;
                    this.y += this.vy * this.diff;
                    this.opacity += this.dop * this.diff;

                    if (this.opacity > 1) {
                        this.opacity = 1;
                        this.dop *= -1;
                    }
                    if (this.opacity < 0 || this.y > this.ymax) {
                        this.replace();
                    }
                    if (!(0 < this.x < this.xmax)) {
                        this.x = (this.x + this.xmax) % this.xmax;
                    }
                    context.beginPath();
                    context.rect(~~this.x, ~~this.y, confettiSize, confettiSize);
                    context.globalAlpha = this.opacity;
                    context.fillStyle = this.rgb;
                    context.fill();
                    this.start = Date.now() / 1000;
                }
            }]);

            return Confetti;
        }();

        var confetti = [];
        var pushConfetti = function pushConfetti() {
            confetti.push(new Confetti());
            if (confetti.length < NUM_CONFETTI) {
                requestAnimFrame(pushConfetti);
            }
        };
        if (animation === 'static') {
            pushConfetti = function pushConfetti() {
                confetti.push(new Confetti());
                if (confetti.length < NUM_CONFETTI) {
                    pushConfetti();
                }
            };
        }
        pushConfetti();

        function step() {
            context.clearRect(0, 0, width, height);
            confetti.forEach(function (c) {
                c.draw();
            });
        }

        return step;
    }

    var canvasStep = setupConfetti('confetti-canvas');
    var _step = function step() {
        canvasStep();
        requestAnimFrame(_step);
    };
    if (animation === 'static') {
        _step = function _step() {
            canvasStep();
        };
    }
    _step();
})();
