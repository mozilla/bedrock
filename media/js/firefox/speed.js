$(function() {
    $('a.close').click(function() {
        $($(this).attr('href')).slideUp();
        return false;
    });
});

$(document).ready(function() {
    var needle = $('#needle');
    var gauge = $('#gauge');
    var angle = 0;
    var latestVersion = parseInt('{{latest_version}}'.split('.')[0], 10);
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

    function getFirefoxVersion()
    {
        var version = 0;

        var matches = /Firefox\/([0-9]+).[0-9]+(?:.[0-9]+)?/.exec(
            navigator.userAgent
        );

        if (matches !== null && matches.length > 0) {
            version = parseInt(matches[1], 10);
        }

        return version;
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

        if (latestVersion > getFirefoxVersion()) {
            // slow
            setTimeout(function() {
                stopWaver();
                rotate(-29.5, 1000, startWaver, 'easeInOutExpo');
            }, 1500);
            $('#gauge-slow-note').delay(3000).fadeIn('slow');
        } else {
            // fast
            setTimeout(function() {
                stopWaver();
                rotate(-168, 1500, startWaver, 'easeInOutExpo');
            }, 1500);
            $('#gauge-fast-note').delay(3000).fadeIn('slow');
        }
    } else {
        gauge.hide();

        var $nonfx       = $('#non-fx');
        var $detected    = $('#detected');
        var $notdetected = $('#notdetected');

        var isSafari = /Safari/.test(window.navigator.userAgent);
        var isChrome = /Chrome/.test(window.navigator.userAgent);
        var isIE     = /MSIE/.test(window.navigator.userAgent);

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
        } else {
            $detected.hide();
        }

        $nonfx.show();
    }
});
