/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {

    // Get the latest version of firefox that is attached as a data
    // attribute. Force a string because jquery sometimes converts it
    // to an integer.
    var latestVersion = ('' + $('#gauge').data('latest-version'));
    latestVersion = parseInt(latestVersion.split('.')[0], 10);

    $('#fx-features').hide();


    if ($(window).width() > 750) { // Only do the slider in wide windows

        // Set up the slider
        var $slides = $('section.slide'),
            isPrevNext = false;

        var getSlideIndex = function(id) {
            var idx = $slides.index($(id + '-slide'));
            return idx == -1 ? 0 : idx;
        };

        // http://jquery.malsup.com/cycle/options.html
        // full list of options
        $('#slider').cycle({
            fx: 'scrollHorz',
            timeout: 0,
            speed: 700, // milliseconds
            nowrap: false,
            prev: '.slider-arrows li.prev a',
            next: '.slider-arrows li.next a',
            onPrevNextEvent: function(isNext, idx, el){
                isPrevNext = true;
                location.hash = el.id.replace('-slide', '');
            }
        });

        $(window).hashchange(function(){
            var sidx = getSlideIndex(location.hash);
            $('.slider-pager').each(function() {
                $(this)
                    .find('li.current')
                    .removeClass('current')
                    .end()
                    .find('li:eq(' + sidx + ')')
                    .addClass('current');
            });
            if (isPrevNext) {
                isPrevNext = false;
            } else {
                $('#slider').cycle(sidx);
            }
            // Track which slides get viewed
            switch (location.hash) {
            case '#speed':
                dcsMultiTrack('WT.z_panel','Desktops & Laptops','WT.dl',98);
                break;
            case '#smartphones':
                dcsMultiTrack('WT.z_panel','Smartphones','WT.dl',98);
                break;
            case '#tablets':
                dcsMultiTrack('WT.z_panel','Tablets','WT.dl',98);
                break;
            case '#addons':
                dcsMultiTrack('WT.z_panel', 'Favorite Add-ons', 'WT.dl', 98);
                break;
            case '#sync':
                dcsMultiTrack('WT.z_panel','Sync Your Gadgets','WT.dl',98);
                break;
            }
        });

        $(window).hashchange();

        // Override clicks on the arrows
        $(".slider-arrows a").click(function(e){
            $(this).blur();
            e.preventDefault();
        });

        // Animate the gauge
        var needle = $('#needle');
        var gauge = $('#gauge');
        var angle = 0;
        var isFirefox = (/\sFirefox/.test(window.navigator.userAgent));

        $.easing.easeInOutSine = function (x, t, b, c, d) {
            return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b;
        };

        $.easing.easeInOutExpo = function (x, t, b, c, d) {
            if (t==0) return b;
            if (t==d) return b+c;
            if ((t/=d/2) < 1) return c/2 * Math.pow(2, 10 * (t - 1)) + b;
            return c/2 * (-Math.pow(2, -10 * --t) + 2) + b;
        };

        function rotate(delta, duration, complete, easing)
        {
            if (!easing) {
                easing = 'swing';
            }
            angle -= delta;
            needle.animate(
                {
                    textIndent: angle
                },
                {
                    'duration' : duration,
                    'easing'   : easing,
                    'complete' : complete,
                    'step'     : function (now, fx) {
                        $(this).css(
                            {
                                '-webkit-transform' : 'rotate(' + now + 'deg)',
                                '-moz-transform' : 'rotate(' + now + 'deg)',
                                '-o-transform' : 'rotate(' + now + 'deg)',
                                'msTransform' : 'rotate(' + now + 'deg)',
                                'transform' : 'rotate(' + now + 'deg)'
                            }
                        );
                    }
                }
            );
        };

        waver = null;
        waverDelta = 1;

        function startWaver()
        {
            if (waver === null) {
                rotate(-waverDelta / 2.0, 280, null, 'easeInOutSine');
                waver = setInterval(function() {
                    rotate(waverDelta, 280, null, 'easeInOutSine');
                    waverDelta *= -1;
                }, 300);
            }
        };

        function stopWaver()
        {
            if (waver) {
                rotate(waverDelta / 2, 1, null, 'linear');
                clearInterval(waver);
                waver = null;
            }
        };

        if (isFirefox) {
            // initial position
            rotate(-1.5, 10, startWaver, 'linear');

            if (latestVersion > getFirefoxMasterVersion()) { // latestVersion is defined inline on the page, fetched from product_details
                // slow
                setTimeout(function() {
                    stopWaver();
                    rotate(-29.5, 1000, startWaver, 'easeInOutExpo');
                }, 1500);
                $('#gauge-slow-note').delay(3000).fadeIn('slow', function(){ $('#fx-upgrade').fadeIn('slow'); });
            } else {
                // fast
                setTimeout(function() {
                    stopWaver();
                    rotate(-168, 1500, startWaver, 'easeInOutExpo');
                }, 1500);
                $('#gauge-fast-note').delay(3000).fadeIn('slow', function(){ $('#fx-features').fadeIn('slow'); });
            }
        } else {
            gauge.hide();

            var $nonfx       = $('#non-fx');
            var $nonfxbtn    = $('#fx-download');
            var $detected    = $('#detected');
            var $notdetected = $('#notdetected');

            var isSafari = /Safari/.test(window.navigator.userAgent);
            var isChrome = /Chrome/.test(window.navigator.userAgent);
            var isIE     = /MSIE/.test(window.navigator.userAgent);
            var isOpera  = /Opera/.test(window.navigator.userAgent);

            if (isChrome) {
                $detected.text(
                    $detected.text().replace(/%BROWSER%/, 'Google Chrome')
                );
                $notdetected.hide();
            } else if (isSafari) {
                $detected.text(
                    $detected.text().replace(/%BROWSER%/, 'Safari')
                );
                $notdetected.hide();
            } else if (isIE) {
                $detected.text(
                    $detected.text().replace(/%BROWSER%/, 'Internet Explorer')
                );
                $notdetected.hide();
            } else if (isOpera) {
                $detected.text(
                    $detected.text().replace(/%BROWSER%/, 'Opera')
                );
                $notdetected.hide();
            } else {
                $detected.hide();
            }

            $nonfx.show();
            $nonfxbtn.show();
        }

    }

});
