/* global define:true */
define([], function () {
    'use strict';

    var Mode = function () {
        Mode.MODES.push(this);
    };

    if (!Mode.MODES) {
        Mode.MODES = [];
        Mode.OPEN_MODE = null;
    }

    Mode.prototype.init = function () {

    };

    Mode.prototype.show = function () {
        // close previous mode and call _onStartShow
        if (Mode.OPEN_MODE) {
            Mode.OPEN_MODE.hide(this._onStartShow.bind(this));
        } else {
            this._onStartShow();
        }
    };

    Mode.prototype._onStartShow = function () {
        this._onShow();
    };

    Mode.prototype._onShow = function () {
        Mode.OPEN_MODE = this;
    };

    Mode.prototype.hide = function (callback) {
        this._hideCallback = callback;
        this._onStartHide();
    };

    Mode.prototype._onStartHide = function () {
        this._onHide();
    };

    Mode.prototype._onHide = function () {
        if (this._hideCallback) {
            this._hideCallback();
            this._hideCallback = null;
        }
    };

    return Mode;
});