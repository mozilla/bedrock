/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, site) {
    'use strict';

    var $html = $('html');
    var $shield = $('#tracking-protection-animation');
    var panels = ['tracking-protection', 'when-to-use', 'control-center', 'cta'];

    $.each(panels, function(index, value) {
        new Waypoint({
            element: document.getElementById(value),
            handler: function(direction) {
                if(direction == 'down') {
                    registerGA(value);
                }
            },
            offset: 'bottom-in-view'
        });
    }); 

    function registerGA(section) {
        window.dataLayer.push({
            event: 'private-browsing-page-interactions',
            interaction: 'scroll',
            section: section        
        });
    }

    Mozilla.HighlightTarget.init('.button-flat-dark');

    if (window.isFirefox()) {
        if (window.getFirefoxMasterVersion() >= 42)  {
            $html.addClass('firefox-up-to-date');
            $('.button-flat-dark').on('highlight-target', function() {
                $shield.addClass('blocked');
            });
        } else {
            $html.addClass('firefox-old');
        }
    } else {
        $html.addClass('non-firefox');
    }

})(window.jQuery, window.site);
