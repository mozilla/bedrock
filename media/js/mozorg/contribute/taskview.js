$(function() {
    'use strict';

    var $stepOne = $('#step_one');
    var $thankYou = $('#thankyou');
    var $getFirefox = $('.get-firefox');
    var $downloadButton = $('.download-link');

    var $followButton = $('.follow-mozilla')
    var intentURL = $followButton.attr('href');

    // some tasks, like install Whimsy, required the user to be using Firefox
    if ($getFirefox.length > -1 && !isFirefox()) {
        $getFirefox.toggleClass('hidden');
    }

    /**
     *
     */
    function handleVisibilityChange() {
        document.addEventListener('visibilitychange', function() {
            // we wait until our current tab is visible before
            // showing the thank you message.
            if (document.visibilityState === 'visible') {
                // toggles number to check mark display
                $stepOne.addClass('completed');
                taskComplete();

                document.removeEventListener('visibilitychange');
            }
        });
    }

    /**
     * Called once all steps of the task has been completed. This will
     * then show the thank message and scroll it into view.
     */
    function taskComplete() {
        $thankYou.removeClass('visibly-hidden');
        $thankYou.attr('aria-hidden', 'false');
        $thankYou[0].scrollIntoView();
        $thankYou.focus();
    }

    /**
     * Completions steps after the install buttons was clicked
     */
    function installWhimsey() {
        // toggles number to check mark display
        $stepOne.toggleClass('completed');
        taskComplete();
    }

    /**
     * Opens a new scaled window that allows a user to follow
     * @StartMozilla on Twitter.
     */
    function followMozilla() {
        var taskCompleted = false;

        window.open(intentURL, 'twitter', 'width=550,height=480,scrollbars');

        if (!taskCompleted) {
            // once our original window recieves focus again, complete the task.
            window.onfocus = taskComplete;
            $stepOne.addClass('completed');
            // ensure this only happens the first time.
            taskCompleted = true;
        }
    }

    $downloadButton.on('click', function(event) {
        // the above will open one of the app stores in a new tab
        // we only want to check the step and show the thank you
        // message once our tab is visible again.
        handleVisibilityChange();
    });

    $stepOne.on('click', function(event) {

        var className = event.target.className;

        if (className === 'install-whimsey') {
            event.preventDefault();
            installWhimsey();
        } else if (className === 'watch-joc') {
            event.preventDefault();
            playJOC();
        }  else if (className === 'follow-mozilla') {
            event.preventDefault();
            followMozilla();
        } else if (className === 'build-firefox' || className === 'devtools') {
            handleVisibilityChange();
        }
    });

});
