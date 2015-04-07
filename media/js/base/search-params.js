/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Retrieve search params as a object for easier access
// This is a simple version of https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams
var _SearchParams = function (search) {
    var params = this.params = {};

    search = search || location.search || '';
    search = search.match(/^\??(.*)/)[1];
    search = search ? search.split(/[&;]/m) : [];

    $.each(search, function (index, param) {
        param = param.split('=');

        var key = param[0];
        var value = param[1];

        params[key] = !isNaN(value) ? parseFloat(value) : value;
    });
};

_SearchParams.prototype.get = function (key) {
    return this.params[key];
};

_SearchParams.prototype.set = function (key, value) {
    this.params[key] = !isNaN(value) ? parseFloat(value) : value;
};

_SearchParams.prototype.has = function (key) {
    return key in this.params;
};

_SearchParams.prototype.remove = function (key) {
    delete this.params[key];
};

_SearchParams.prototype.toString = function () {
    return $.map(this.params, function (value, key) {
        return [encodeURIComponent(key), encodeURIComponent(value)].join('=');
    }).join('&');
};
