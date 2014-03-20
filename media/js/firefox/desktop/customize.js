/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    // customize icons section
    var $customizer_list = $('#customizer-list');

    // theme thumbnails
    var $themes_thumbs = $('#themes-thumbs');

    // theme preview image
    var $theme_demo = $('#theme-demo');

    // store current customizer
    var current_customizer = 'themes';
    var previous_customizer = '';

    // handle clicking on themes/add-ons/awesome bar icons
    $('.show-customizer').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);

        // make sure action should be taken
        if ($this.attr('href').replace('#', '') !== current_customizer) {
            previous_customizer = current_customizer;
            current_customizer = $this.attr('href').replace('#', '');

            // select correct customizer icon
            $customizer_list.find('a').removeClass('selected');
            $customizer_list.find('a[href="#' + current_customizer + '"]').addClass('selected');

            // apply correct class to icon list for arrow placement
            $customizer_list.removeClass(previous_customizer).addClass(current_customizer);

            var $curr = $('.customizer.active');

            var $next = $($this.attr('href'));

            $curr.fadeOut('fast', function() {
                $curr.removeClass('active');
            });

            // display specified customizer
            $next.fadeIn('fast').addClass('active');
        }
    });

    // handle clicks on theme thumbnails
    $themes_thumbs.on('click', 'a', function(e) {
        e.preventDefault();

        var $this = $(this);

        // de-select all
        $themes_thumbs.find('a').removeClass('selected');

        // select clicked
        $this.addClass('selected');

        // figure out new image src
        var new_src = $theme_demo.attr('src').replace(/(.*)theme-.*\.png/gi, "$1" + $this.attr('id') + '.png');

        // update image with new src
        $theme_demo.attr('src', new_src);
    });
})(window.jQuery);
