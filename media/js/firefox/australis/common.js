;(function($, Mozilla) {
    'use strict';

    var pageId = $('body').prop('id');
    var $window = $(window);

    var $syncAnim = $('.sync-anim');
    var $laptop = $syncAnim.find('.laptop');
    var $laptopScreen = $laptop.find('.inner');
    var $phone = $syncAnim.find('.phone');
    var $arrows = $laptop.find('.arrows');

    // scroll to top of window for mask overlay
    if ($window.scrollTop() > 0 && (window.location.hash !== '#footer-email-form')) {
        $window.scrollTop(0);
    }

    // start in-page animations when user scrolls down from header
    $('#masthead').waypoint(function(direction) {
        if (direction === 'down') {
            syncAnimation();
            this.destroy(); // execute waypoint once
        }
    }, {
        offset: -20
    });

    function syncAnimation() {
        $syncAnim.addClass('on');

        $arrows.one('animationstart', function () {
            $laptopScreen.addClass('faded');
        });

        $arrows.one('animationend', function () {
            $laptopScreen.removeClass('faded');
        });

        $phone.one('animationend', '.passwords', function () {
            $syncAnim.addClass('complete');
        });
    }

    // link directly to Firefox Accounts when clicking the Sync CTA button
    Mozilla.UITour.getConfiguration('sync', function (config) {
        $('.sync-cta .button').each(function() {
            $(this).attr({
                'data-page-name': pageId,
                'data-interaction': 'button click',
                'data-element-location': 'Get Started with Sync'
            }).on('click', function(e) {
                e.preventDefault();

                // Track sync button clicks

                window.dataLayer.push({
                    'event': 'first-run-sync'
                });

                if (Mozilla.Client.FirefoxMajorVersion >= 31) {
                    Mozilla.UITour.showFirefoxAccounts();
                } else {
                    window.open(this.href, '_blank');
                }
            });
        });
    });

    // track learn more links
    $('.learn-more a').each(function() {
        $(this).attr({
            'data-page-name': pageId,
            'data-interaction': 'button click',
            'data-element-location': 'Get Started with Sync'
        }).on('click', function(e) {
            e.preventDefault();

            // Track sync button clicks

            window.dataLayer.push({
                'event': 'first-run-sync'
            });

            window.open(this.href, '_blank');
        });
    });

})(window.jQuery, window.Mozilla);
