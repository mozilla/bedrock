/* global define:true */
define([], function () {
    'use strict';

    var Responsive = {};

    Responsive.AT_LARGE = 960;
    Responsive.AT_MEDIUM = 560;
    Responsive.SIZE = {x:0, y:0};

    Responsive.IS_LARGE = function () {
        return Responsive.SIZE.x > Responsive.AT_LARGE;
    };

    Responsive.IS_MEDIUM = function () {
        return Responsive.SIZE.x > Responsive.AT_MEDIUM;
    };

    Responsive.IS_SMALL = function () {
        return Responsive.SIZE.x <= Responsive.AT_MEDIUM;
    };

    return Responsive;
});