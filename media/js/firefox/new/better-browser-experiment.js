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
        'A144_A203_A008845',
        'A144_A203_C002355',
        'A144_A203_C003768',
        'A144_A203_A008874',
        'A144_A203_C002358',
        'A144_A203_C003770',
        'A144_A203_C001006',
        'A144_A203_C003771',
        'A144_A634_A008782',
        'A144_A634_C002349',
        'A144_A634_C003778',
        'A144_A634_A008816',
        'A144_A634_C002352',
        'A144_A634_C003781'
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
            id: 'experiment_firefox_new_betterbrowser',
            variations: {
                'xv=betterbrowser&v=a': 16,
                'xv=betterbrowser&v=b': 16,
                'xv=betterbrowser&v=c': 16,
                'xv=betterbrowser&v=d': 16,
                'xv=betterbrowser&v=e': 16,
                'xv=betterbrowser&v=f': 16
            }
        });

        cop.init();
    }
})(window.Mozilla);
