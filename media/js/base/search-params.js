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

_SearchParams.prototype.utmParams = function() {
    var utms = {};

    $.each(this.params, function (key, val) {
        if (key.indexOf('utm_') === 0) {
            utms[key] = val;
        }
    });

    return utms;
};

_SearchParams.prototype.utmParamsFxA = function(pathname) {
    pathname = pathname || window.location.pathname || '';

    var utms = this.utmParams();

    /* eslint-disable camelcase */

    // set to default value if not specified in URL
    if (!utms.utm_campaign) {
        // utm_* values will be encoded on the product side, so no need to
        // pre-emptively encode here
        utms.utm_campaign = 'page referral - not part of a campaign';
    }

    // remove locale from pathname and store result in utm_content
    // e.g. https://www.mozilla.org/it/firefox/sync/?foo=bar should
    // have utm_content value of /firefox/sync/.
    var matches = pathname.match(/\/[\w-]+(\/.*)$/);

    if (matches && matches.length > 1) {
        // no need to encode - will be done on product side
        utms.utm_content = matches[1];
    }

    /* eslint-enable camelcase */

    // ensure all values are strings, as no numeric values are allowed
    // into UITour.showFirefoxAccounts
    Object.keys(utms).forEach(function(key) {
        utms[key] = utms[key].toString();
    });

    return utms;
};
