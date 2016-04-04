/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var $document = $(document);
    var $taskSteps = $('.task-steps');
    var $thankYou = $('#thankyou');
    var $getFirefox = $('.get-firefox');
    var $actionButton = $('.action');
    var $signupTweetForm = $('#signup-tweet');
    var $downloadDevTools = $('.dev-edition');
    var $tryAnotherTask = $('.try-another');
    var visibilityChange = getVisibilityStateEventKeyword();

    // some tasks, like installing Whimsy, required the user to be using Firefox
    if ($getFirefox.length > -1 && !Mozilla.Client.isFirefox) {
        $getFirefox.toggleClass('hidden');
        // hide any action buttons that forms part of the task.
        $actionButton.addClass('hidden');
    }

    /**
     * Determines the visibilitychange event name based on the current browser
     * and returns the appropriate keyword. Based on code from:
     * https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
     */
    function getVisibilityStateEventKeyword() {
        // for browser that support the event unprefixed
        if (typeof document.hidden !== 'undefined') {
            return 'visibilitychange';
        }

        // for Chrome 13 and lower
        if (typeof document.webkitHidden !== 'undefined') {
            return 'webkitvisibilitychange';
        }

        // for older versions of IE
        if (typeof document.msHidden !== 'undefined') {
            return 'msvisibilitychange';
        }
    }

    /**
     * Toggles the completed class on the relevant step, and calls
     * taskComplete() if this was the final step of the task.
     */
    function completeStep($step) {
        var $stepOne = $('#step_one');
        var $stepTwo = $('#step_two');

        if ($step.data('step') === 'one') {
            $stepOne.toggleClass('completed');
        } else if ($step.data('step') === 'two') {
            $stepTwo.toggleClass('completed');
        }

        if ($step.data('complete') === true) {
            taskComplete();
        }
    }

    /**
     * Called once all steps of the task has been completed. This will
     * show the thank message and scroll it into view.
     */
    function taskComplete() {
        $thankYou.removeClass('visibly-hidden');
        $thankYou.attr('aria-hidden', 'false');
        $thankYou[0].scrollIntoView();
        $thankYou.focus();
    }

    /**
     * Waits for the initial tab/window to become visible, and then
     * proceeds to complete the relevant task step.
     */
    function handleVisibilityChange($step) {
        // to be sure we do not queue a bunch of visibilityChange events,
        // because the browser did not fire the event, and thus `.off`
        // was never called, we first ensue no events are currently bound,
        // before binding a new one.
        $document.off(visibilityChange + '.taskview');

        $document.on(visibilityChange + '.taskview', function() {
            // we wait until our current tab is visible before
            // showing the thank you message.
            if (document.visibilityState === 'visible') {
                completeStep($step);
                $document.off(visibilityChange + '.taskview');
            }
        });
    }

    /**
     * Handles blur and focus events on the main window, and completes
     * the task step once the main window receives focus.
     */
    function handleFocusChange($step) {
        $(window).one('focus', function() {
            completeStep($step);
        });
    }

    /**
     * Sends data to GA about the interaction steps a user has taken.
     * @param {string} interaction - The kind of interaction
     * @param {int} variation - Whether it is a v1 or v2 task.
     */
    function trackInteraction(interaction, variation) {
        window.dataLayer.push({
            event: 'get-involved-task-interaction',
            interaction: interaction,
            variation: variation
        });
    }

    /**
     * Initializes the tweet form, set's up the character counter and binds
     * the submit event handler.
     */
    function initTweetForm() {
        var $tweetField = $('#tweet_txt');
        var $charCount = $('.char-count');
        var maxLength = 140;
        var tweetLength = $tweetField.val().length;

        // get and show the initial number of characters
        $charCount.text(maxLength - tweetLength);

        $tweetField.on('keyup', function() {
            tweetLength = $tweetField.val().length;
            $charCount.text(maxLength - tweetLength);
        });

        $signupTweetForm.on('submit', function(event) {
            event.preventDefault();

            var $submitButton = $('input[type="submit"]');
            var tweetIntentURL = $signupTweetForm.attr('action');
            var tweetContent = $tweetField.val();
            var hashTag = $('#hashtag').attr('value');
            var tweet = encodeURI(tweetIntentURL + '?text=' + tweetContent + '&hashtags=' + hashTag);

            window.open(tweet, 'twitter', 'width=550,height=480,scrollbars');

            // only v2 tasks has Tweet forms.
            trackInteraction('share on twitter', '2');
            handleFocusChange($submitButton);
        });
    }

    /**
     * Handles completion of Whimsy interaction steps.
     */
    function whimsy(event) {

        var $this = $(event.target);

        if ($this.data('action') === 'install') {
            handleVisibilityChange($this);
            trackInteraction('install whimsy', $this.data('variation'));
        } else if ($this.data('action') === 'rate') {
            handleVisibilityChange($this);
            trackInteraction('AMO exit link', $this.data('variation'));
        }
    }

    /**
     * Handles completion of Firefox Mobile interaction steps.
     */
    function installFirefox(event) {
        var $this = $(event.target);

        if ($this.data('action') === 'install') {
            handleVisibilityChange($this);
        }
    }

    /**
     * Handles completion of Follow Mozilla interaction steps.
     */
    function followMozilla(event) {
        var $this = $(event.target);
        var intentURL = $this.attr('href');
        var screenName;

        if ($this.data('action') === 'follow') {
            event.preventDefault();
            screenName = intentURL.substr(intentURL.indexOf('=') + 1);
            window.open(intentURL, 'twitter', 'width=550,height=480,scrollbars');
            handleFocusChange($this);
            trackInteraction('follow ' + screenName, $this.data('variation'));
        }
    }

    /**
     * Called by joyOfCoding, monitors video playback and marks the video step
     * as watched once we reach the 40sec mark.
     * @param {object} $video - The video element as a jQuery object.
     */
    function markAsWatched($video) {
        var videoElement = $video[0];

        // a user can click play again after having watched the video the
        // first time. Clicking on pause, for example, will also trigger the
        // click event so, we need to ensure we only run the below on the
        // first interaction.
        if ($video.data('watched') !== true) {
            $video.on('timeupdate.taskview', function() {
                // user needs to watch at least 40 seconds before we mark
                // this step as complete.
                if (videoElement.currentTime >= 40) {
                    completeStep($video);
                    // once the step has been completed,
                    // remove the event listener.
                    $video.off('timeupdate.taskview');
                    $video.data('watched', true);
                    trackInteraction('completed joy of coding', $video.data('variation'));
                }
            });
        }
    }

    /**
     * Handles completion of Joy of Coding interaction steps.
     */
    function joyOfCoding(event) {
        var $this = $(event.target);

        // to avoid sending multiple pings to GA as a user pauses and plays the video,
        // we check whether the data-ga attribute exists. If it does, there is nothing
        // to do here, so just return.
        if ($this.data('ga')) {
            return;
        }

        var $jocVideo = $('#joc');
        var videoElement = $jocVideo[0];
        var $playButton = $('.watch');

        // If the interaction happened on the video element itself, simply track
        // the event and call markAsWatched. Let the video element do it's thing.
        if ($this[0].id === 'joc' && $this[0].paused) {
            // we need to set the ga data attribute on both the video element
            // and the button, because we do not know where the next interaction
            // will be triggered from.
            $this.attr('data-ga', true);
            $playButton.attr('data-ga', true);

            trackInteraction('play joy of coding', $this.data('variation'));
            markAsWatched($this);
        } else  if ($this.data('action') === 'play' && videoElement.paused) {
            videoElement.play();

            $this.attr('data-ga', true);
            $jocVideo.attr('data-ga', true);

            trackInteraction('play joy of coding', $this.data('variation'));
            markAsWatched($jocVideo);
        } else if ($this.data('action') === 'discuss') {
            handleVisibilityChange($this);
            trackInteraction('joy of coding exit link', $this.data('variation'));
        }
    }

    /**
     * Handles completion of FoxFooding interaction steps.
     */
    function startFoxFooding(event) {
        var $this = $(event.target);
        var intentURL = $this.attr('href');

        if ($this.data('action') === 'join') {
            handleVisibilityChange($this);
            trackInteraction('foxfooding exit link', $this.data('variation'));
        } else if ($this.data('action') === 'follow') {
            event.preventDefault();
            window.open(intentURL, 'twitter', 'width=550,height=480,scrollbars');
            handleFocusChange($this);
            trackInteraction('Follow foxfooding on Twiiter', $this.data('variation'));
        }
    }

    /**
     * Handles completion of DevTools interaction steps.
     */
    function learnDevTools(event) {
        var $this = $(event.target);

        if ($this.data('action') === 'challenger') {
            handleVisibilityChange($this);
            trackInteraction('devtools challenger exit link', $this.data('variation'));
        }
    }

    // send GA events for clicks on the dev edition download button
    if ($downloadDevTools.length > 0) {
        $downloadDevTools.on('click', function() {
            trackInteraction('download firefox dev edition', $downloadDevTools.data('variation'));
        });
    }

    // only bind the handler when the form exists
    if ($signupTweetForm.length > 0) {
        initTweetForm();
    }

    // send GA events for clicks on the back and try another task links
    $tryAnotherTask.on('click', function() {
        var $this = $(this);
        trackInteraction($this.text(), $this.data('variation'));
    });

    $taskSteps.on('click', function(event) {

        var $target = $(event.target);
        var currentTask = $target.data('task');

        if (currentTask === 'whimsy') {
            whimsy(event);
        } else if (currentTask === 'firefox-mobile') {
            installFirefox(event);
        } else if (currentTask === 'follow-mozilla') {
            followMozilla(event);
        } else if (currentTask === 'joyofcoding') {
            joyOfCoding(event);
        } else if (currentTask === 'foxfooding') {
            startFoxFooding(event);
        } else if (currentTask === 'devtools') {
            learnDevTools(event);
        }
    });
})();
