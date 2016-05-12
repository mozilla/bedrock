/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $window = $(window);
    var $document = $(document);
    var $body = $('body');
    var $navList = $('#contribute-nav-menu');
    var hasMediaQueries = (typeof matchMedia !== 'undefined');

    // If the browser supports media queries, check the width onload and onresize.
    // If not, just lock it in permanent wideMode.
    if (hasMediaQueries) {
        checkWidth();
        $window.on('resize', function() {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(checkWidth, 200);
        });
    } else {
        $body.removeClass('thin').addClass('wide');
    }

    function checkWidth() {
        if (window.matchMedia('screen and (min-width: 761px)').matches) {
            $body.removeClass('thin').addClass('wide');
            $navList.removeAttr('aria-hidden').show();
        } else {
            $body.removeClass('wide').addClass('thin');
            $navList.attr('aria-hidden', 'true').hide();
        }
    }

    // Show/hide the navigation in small viewports
    $document.on('click', 'body.thin .contribute-nav .toggle', expandPageNav);
    $document.on('click', 'body.thin .contribute-nav .toggle.open', collapsePageNav);
    $document.on('mouseleave', 'body.thin .contribute-nav', collapsePageNav);

    function expandPageNav() {
        $navList.slideDown('fast').removeAttr('aria-hidden').attr('aria-expanded', 'true');
        $('.contribute-nav .toggle').addClass('open');
    }

    function collapsePageNav() {
        $navList.slideUp('fast').attr('aria-hidden', 'true').removeAttr('aria-expanded');
        $('.contribute-nav .toggle').removeClass('open');
    }

})(window.jQuery);
