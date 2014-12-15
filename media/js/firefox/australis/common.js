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

    // track Sync CTA click and link to about:accounts where posiible
    function trackSyncClick(e) {
        e.preventDefault();
        var url = this.href;
        var goToAccounts = function () {
            // available on Firefox 31 and greater
            Mozilla.UITour.showFirefoxAccounts();
        };

        if (window.getFirefoxMasterVersion() >= 31) {
            gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'button click', 'Get Started with Sync'], goToAccounts);
        } else {
            window.open(url, '_blank');
            gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'button click', 'Get Started with Sync']);
        }
    }

    // Open learn more links in new window and track
    function trackLearnMoreLinks(e) {
        e.preventDefault();
        var url = this.href;
        window.open(url, '_blank');
        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'link click', url]);
    }

    // start in-page animations when user scrolls down from header
    $('#masthead').waypoint(function(direction) {
        if (direction === 'down') {
            syncAnimation();
        }
    }, {
        triggerOnce: true,
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
        $('.sync-cta').on('click', '.button', trackSyncClick);
    });

    // track learn more links on click
    $('.learn-more a').on('click', trackLearnMoreLinks);

})(window.jQuery, window.Mozilla);
