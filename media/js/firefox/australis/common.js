;(function($, Mozilla) {
    'use strict';

    var pageId = $('body').prop('id');
    var $window = $(window);

    var $rays = $('.share .rays');
    var $syncAnim = $('.sync-anim');
    var $laptop = $syncAnim.find('.laptop');
    var $laptopScreen = $laptop.find('.inner');
    var $phone = $syncAnim.find('.phone');
    var $arrows = $laptop.find('.arrows');

    // scroll to top of window for mask overlay
    if ($window.scrollTop() > 0 && (window.location.hash !== '#footer-email-form')) {
        $window.scrollTop(0);
    }

    function trackGlowClick (e) {
        e.preventDefault();
        var url = this.href;
        window.open(url, '_blank');
        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'button click', 'Share Your Vision CTA']);
    }

    // Highlight sync in the app menu and track cta click
    function showSyncInMenu (e) {
        e.preventDefault();
        e.stopPropagation();
        Mozilla.UITour.showHighlight('accountStatus', 'wobble');

        // hide app menu when user clicks anywhere on the page
        $(document.body).one('click', function () {
            Mozilla.UITour.hideHighlight();
        });

        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'button click', 'Get Started with Sync']);
    }

    // Open learn more links in new window and track
    function trackLearnMoreLinks (e) {
        e.preventDefault();
        var url = this.href;
        window.open(url, '_blank');
        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'link click', url]);
    }

    // start in-page animations when user scrolls down from header
    $('#masthead').waypoint(function(direction) {
        if (direction === 'down') {
            syncAnimation();
            $rays.addClass('on');
        }
    }, {
        triggerOnce: true,
        offset: -20
    });

    function syncAnimation () {
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

    // show sync in menu when user clicks cta
    $('.sync-cta button').on('click', showSyncInMenu);

    // track learn more links on click
    $('.learn-more a').on('click', trackLearnMoreLinks);

    // track Glow CTA button click
    $('.share-cta .button').on('click', trackGlowClick);

})(window.jQuery, window.Mozilla);
