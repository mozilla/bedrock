;(function($, Mozilla) {
    'use strict';

    var $window = $(window);
    var $survey = $('#survey-link');
    var pageId = $('body').prop('id');
    var firstTime = 'True';

    // scroll to top of window for mask overlay
    if ($window.scrollTop() > 0) {
        $window.scrollTop(0);
    }

    // Update surver link for visitors who complete the tour
    window.updateTourSurveyLink = function () {
        var surveyId = $survey.data('id');
        $survey.attr('href', 'https://www.surveygizmo.com/s3/1578504/Firefox-Beta-29-Tour-Survey?tour=' + surveyId);
    };

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

    // Open survey link in new window and track click
    function openSurvey (e) {
        e.preventDefault();
        window.open(this.href, '_blank');
        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'survey link', this.href]);
    }

    // Open learn more links in new window and track
    function trackLearnMoreLinks (e) {
        e.preventDefault();
        var url = this.href;
        window.open(url, '_blank');
        gaTrack(['_trackEvent', pageId + ' Page Interactions - New Firefox Tour', 'link click', url]);
    }

    // show sync animation when user scrolls down past header
    $('main > header h1').waypoint(function(direction) {
        if (direction === 'down') {
            syncAnimation();
        }
    }, {
        triggerOnce: true,
        offset: -150
    });

    function syncAnimation () {
        var $syncAnim = $('.sync-anim');
        var $laptop = $syncAnim.find('.laptop');
        var $tablet = $syncAnim.find('.tablet');
        var $cloud = $syncAnim.find('.cloud');
        var $phone = $syncAnim.find('.phone');
        var $arrows = $cloud.find('.sync-arrows');
        var $checkmark = $cloud.find('.checkmark');

        $laptop.addClass('on');

        $laptop.one('animationend', '.passwords', function () {
            $syncAnim.addClass('devices-in');
        });

        $phone.one('animationend', function () {
            $cloud.addClass('up');
        });

        $arrows.one('animationend', function () {
            $tablet.addClass('on');
        });

        $tablet.one('animationend', '.passwords', function () {
            $phone.addClass('on');
        });

        $phone.one('animationend', '.passwords', function () {
            $cloud.addClass('complete');
        });

        $checkmark.one('animationend', function () {
            $syncAnim.addClass('complete');
        });
    }

    //Only highlight sync for Firefox Desktop 29 or greater.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 29) {
        // Highlight sync if the user does not already have it setup
        Mozilla.UITour.getConfiguration('sync', function (config) {
            var $cta = $('.sync-cta');

            if (config.setup === false) {
                // show the sync cta button
                $cta.show();
                // highlight sync in the menu when user clicks cta
                $cta.find('button').on('click', showSyncInMenu);
            }
        });
    }

    // track learn more links on click
    $('.learn-more a').on('click', trackLearnMoreLinks);

    // track survey link on click
    $survey.on('click', openSurvey);

    //track if this is the first time a user has seen any tour (firstrun or whatsnew)
    try {
        if (localStorage.getItem('mozUITourGlobalFlag') === 'taken') {
            firstTime = 'False';
        } else {
            localStorage.setItem('mozUITourGlobalFlag', 'taken');
        }
        gaTrack(['_trackEvent', 'Tour Interaction', 'First Time Seeing Tour', firstTime, 0, true]);
    } catch (e) {}

})(window.jQuery, window.Mozilla);
