/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var $statusUnknown = $('.status-unknown');
    var $tab = $('caption', $statusUnknown);
    var $tabPanels = $('thead, tbody', $statusUnknown);
    var expandedState;

    $tab.on('click', function() {

        expandedState = $tab.attr('aria-expanded') === 'false' ? true : false;

        $tab.attr('aria-expanded', expandedState);
        $tabPanels.toggleClass('hidden')
                  .attr('aria-hidden', !expandedState);
    });
})();
