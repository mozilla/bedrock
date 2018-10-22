(function() {
    'use strict';

    var strings;
    var topicHeaders;
    var initialTopic;
    var initialTopicContent;

    /**
     * Check for feature support
     */
    function supportsBaselineJS() {
        return 'querySelectorAll' in document &&
               'addEventListener' in window;
    }

    /**
     * Adds the data choices widget(Firefox only) to the first sub-section under
     * "Firefox by default shares data to".
     * @param {Object} section - The section to which the widget
     * will be added
     */
    function addDataChoicesWidget(section) {
        var container = document.createElement('div');
        var copyContainer = document.createElement('p');
        var button = document.createElement('button');

        container.setAttribute('class', 'data-choices');

        copyContainer.textContent = strings.dataset.choicesCopy;

        button.textContent = strings.dataset.choicesButton;
        button.setAttribute('id', 'choose');
        button.setAttribute('type', 'button');
        button.className = 'mzp-c-button';

        container.appendChild(copyContainer);
        container.appendChild(button);

        section.appendChild(container);

        // handle clicks on the data choices "Choose" button
        $('#choose').on('click', function() {
            // if the uitour did not load, just return
            if (Mozilla.UITour === undefined) {
                return;
            }

            Mozilla.UITour.openPreferences('privacy-reports');
        });
    }

    // Don't execute if features aren't supported and client isn't desktop Firefox
    if (supportsBaselineJS() && Mozilla.Client.isFirefoxDesktop) {
        strings = document.getElementById('strings');
        topicHeaders = document.querySelectorAll('.privacy-body .l-narrow > section');
        initialTopic = topicHeaders[0].querySelector('section');
        initialTopicContent = initialTopic.querySelector('div');

        // and that the UITour works (requires base/uitour-lib.js)
        Mozilla.UITour.ping(function() {
            addDataChoicesWidget(initialTopicContent);
        });
    }

})();
