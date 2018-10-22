/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    var contentValues = [
        'A144_A203_C001036',
        'A144_A203_C001056',
        'A144_A203_C001046',
        'A144_A634_C001304',
        'A144_A634_C001285',
        'A144_A203_A008847',
        'A144_A203_A008876',
        'A144_A203_C001008',
        'A144_A634_A008784',
        'A144_A634_A008818'
    ];

    var source = getUrlParam('utm_source');
    var content = getUrlParam('utm_content');

    var mediumOk = getUrlParam('utm_medium') === 'cpc';
    var sourceOk = source === 'google' || source === 'bing';
    var contentOk;

    // adcontent value in querystring must match a pre-defined value
    for (var i = contentValues.length - 1; i > -1; i--) {
        if (contentValues[i] === content) {
            contentOk = true;
            break;
        }
    }

    // only initialize experiment if all query params are as required
    if (mediumOk && sourceOk && contentOk) {
        var cop = new Mozilla.TrafficCop({
            id: 'experiment_firefox_new_opera',
            variations: {
                'v=a': 33, // control
                'v=1': 33,
                'v=2': 33
            }
        });

        cop.init();
    }
})(window.Mozilla);
