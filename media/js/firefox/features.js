$(document).ready(function() {

    var $current = null;
    var showPeriod = 250;
    var hidePeriod = 200;
    var externalHoverPeriod = 500;
    var internalHoverPeriod = 200;
    var externalHoverTimer = null;
    var internalHoverTimer = null;

    function fadeIn($hover)
    {
        var period = showPeriod;

        $current = $hover;

        if ($hover.is(':animated')) {
            $hover.stop(true, false);
            var startOpacity = parseFloat($hover.css('opacity'));
            period = (1.0 - startOpacity) * showPeriod;
            $hover.animate({ opacity: 1 }, period);
        } else {
            $hover
                .css('opacity', '0')
                .css('display', 'block')
                .animate({ opacity: 1 }, period);
        }
    }

    function fadeOut()
    {
        if ($current) {
            var $that = $current;
            if ($that.is(':animated')) {
                $that.stop(true, false);
            }
            $that.animate(
                { opacity: 0 },
                hidePeriod,
                'linear',
                function() { $that.css('display', 'none'); }
            );
        }
    }

    $('#top-features').hover(
        function () {
            if (externalHoverTimer) {
                clearTimeout(externalHoverTimer);
                externalHoverTimer = null;
            }
        },
        function() {
            if (externalHoverTimer) {
                clearTimeout(externalHoverTimer);
                externalHoverTimer = null;
            }
            if (internalHoverTimer) {
                clearTimeout(internalHoverTimer);
                internalHoverTimer = null;
            }
            externalHoverTimer = setTimeout(
                function() {
                    fadeOut();
                    $current = null;
                },
                externalHoverPeriod
            );
        }
    );

    $features = $('#top-features li');
    $features.each(function(index) {
        var $hover = $('.top-feature-hover', this);
        $(this).hover(
            function() {
                if ($current === null) {
                    fadeIn($hover);
                } else {
                    if (internalHoverTimer) {
                        clearTimeout(internalHoverTimer);
                        internalHoverTimer = null;
                    }
                    internalHoverTimer = setTimeout(function () {
                        if ($current != $hover) {
                            fadeOut();
                            fadeIn($hover);
                        }
                    }, internalHoverPeriod);
                }
            },
            function () {
            }
        );
    });
});
