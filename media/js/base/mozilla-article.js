/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mzp) {
    'use strict';

    var _mqWide = matchMedia('(max-width: 767px)');

    if (_mqWide.matches) {
        Mzp.Details.init('.side-reference > h4');
    }
    _mqWide.addListener(function(mq) {
        if (mq.matches) {
            Mzp.Details.init('.side-reference > h4');
        } else {
            Mzp.Details.destroy('.side-reference > h4');
        }
    });

})(window.Mzp);
