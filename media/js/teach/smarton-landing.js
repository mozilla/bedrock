/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global mina, Snap */

(function($) {
    'use strict';

    var hasTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints;

    function smartonShapes() {
        var speed = 450;
        var easing = mina.backout;

        $('.smarton-topics > .topic').each(function() {
            var $this = $(this);
            var shape = new Snap('#' + $this.attr('id') + ' svg.shape');
            var path = shape.select('path');
            var pathConfig = {
                from : $this.data('path-hide'),
                to : $this.data('path-show')
            };

            // Set the shape to the hidden state (it defaults to off state if JS fails)
            path.attr('d', pathConfig.from);

            $this.on('mouseenter', function() {
                path.animate({'path' : pathConfig.to}, speed, easing);
                $(this).addClass('show');
            });

            $this.on('mouseleave', function() {
                path.animate({'path' : pathConfig.from}, speed, easing);
                $(this).removeClass('show');
            });
        });
    }

    if (hasTouch) {
        // No fancy SVG animations for touch devices; avoids the clunky double-tap
        $('.smarton-topics').addClass('has-touch');
    } else {
        smartonShapes();
    }

})(window.jQuery);
