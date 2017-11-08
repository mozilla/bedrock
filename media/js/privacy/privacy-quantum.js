(function() {
    'use strict';

    var strings;
    var mainContent;
    var topicHeaders;
    var topics = [];
    var tabpanelCloseText;
    var tabpanelOpenText;

    /**
     * Check for feature support
     */
    function supportsBaselineJS() {
        return 'querySelectorAll' in document &&
               'addEventListener' in window;
    }

    /**
     * For each main section, this innjects a button to either,
     * show all topics under the section, or collapse all.
     */
    function addMasterToggles() {
        var toggle = document.createElement('button');

        toggle.classList.add('toggle');
        toggle.setAttribute('type', 'button');
        toggle.textContent = tabpanelOpenText;

        dataAttributeHandler({
            elem: toggle,
            property: 'data-is-expanded',
            value: false
        });

        for (var i = 0, l = topicHeaders.length; i < l; i++) {
            var currentHeading = topicHeaders[i].querySelector('h2');

            dataAttributeHandler({
                elem: toggle,
                property: 'data-parent-container',
                value: topicHeaders[i].id
            });

            currentHeading.insertAdjacentHTML('beforeend', toggle.outerHTML);
        }
    }

    /**
     * Collects all of the individual topics(sections) into an Array
     * for use in various other functions.
     */
    function collectAllTopics() {
        for (var i = 0, l = topicHeaders.length; i < l; i++) {
            var nestedTopics = topicHeaders[i].querySelectorAll('section');
            /* nestedTopics is a NodeList which is Array like but,
            not a real array. We therefore need to coherce it into one. */
            topics.push([].slice.call(nestedTopics));
        }

        /* At this point `topics` is a two dimensional array.
        The final step then is to flatten it. */
        topics = topics.reduce(function(a, b) {
            return a.concat(b);
        });
    }

    /**
     * Simple pollyfil for setting and getting data attributes
     * across browsers.
     * @param {Object} data - An object containing the data needed
     * to get or set the data attribute. For example:
     *
     * {
     *     elem: document.getElementById('strings'),
     *     property: 'isExpanded',
     *     value: 'value'
     * }
     *
     * @returns For get operations, it returns the value of the data attribute
     */
    function dataAttributeHandler(data) {
        // if a value is passed, this is a set operation
        if (data.value) {
            if (strings.dataset === undefined) {
                data.elem.setAttribute(data.property, data.value);
            } else {
                data.elem.dataset[formatAsDatasetProperty(data.property)] = data.value;
            }
        } else {
            if (strings.dataset === undefined) {
                /* When using dataset, boolean values are returned as strings.
                When getting the value using `getAttribute` it is returned as a boolean.
                This causes inconsistencies with conditional statements so, explicitly
                convert all return values to a string */
                var propertyValue = data.elem.getAttribute(data.property);
                return propertyValue ? propertyValue.toString() : propertyValue;
            } else {
                return data.elem.dataset[formatAsDatasetProperty(data.property)];
            }
        }
    }

    /**
     * Takes a string in the format `data-tabpanel-open-text` and
     * returns a string formatted such that it can be used as a
     * property accessor on a `dataset`
     * Example:
     * input: data-tabpanel-open-text
     * returns tabpanelOpenText
     *
     * @param {String} property - The property to convert as a string
     * @returns the formatted string
     */
    function formatAsDatasetProperty(property) {
        var formattedProperty = '';
        // first strip of the `data-`
        var stripped = property.substr(property.indexOf('-') + 1);
        // split the result into an array
        var split = stripped.split('-');

        /* start by adding the first item in the array
        to the `formattedProperty` which will be returned */
        formattedProperty = split[0];

        // if the resulting array has more than one item
        if (split.length > 1) {
            // loop over the array, starting at the second item
            for (var i = 1, l = split.length; i < l; i++) {
                var currentString = split[i];
                formattedProperty += currentString.replace(
                    currentString.substr(0,1),
                    currentString.substr(0,1).toUpperCase()
                );
            }
        }
        return formattedProperty;
    }

    /**
     * Hides *all* topics across sections
     */
    function hideAllTopicContent() {
        for (var i = 0, l = topics.length; i < l; i++) {
            var divElem = topics[i].querySelector('div');
            var topicHeading = topics[i].querySelector('h3');

            divElem.classList.add('hidden');
            divElem.setAttribute('aria-hidden', true);

            topicHeading.classList.add('collapsed');
        }
    }

    /**
     * Runs a set of functions on page load.
     */
    function initPage() {
        collectAllTopics();
        hideAllTopicContent();
        addMasterToggles();
        showInitialTopic();
    }

    /**
     * On load, expands the first topic of the first main section. This
     * also calls `addDataChoicesWidget` if on Fx desktop.
     */
    function showInitialTopic() {
        var initialTopic = topicHeaders[0].querySelector('section');
        var initialTopicContent = initialTopic.querySelector('div');
        var initialTopicHeading = initialTopic.querySelector('h3');

        initialTopicContent.classList.remove('hidden');
        initialTopicContent.setAttribute('aria-hidden', false);

        initialTopicHeading.classList.remove('collapsed');
    }

    /**
     * Hide or show all topics for the main section.
     * @param {Object} targetElem - The element that triggered the event
     */
    function toggleMainSectionTopics(targetElem) {
        var targetSectionId = dataAttributeHandler({
            elem: targetElem,
            property: 'data-parent-container'
        });
        var isExpanded = dataAttributeHandler({
            elem: targetElem,
            property: 'data-is-expanded'
        });

        var targetAction = isExpanded === 'true' ? 'add' : 'remove';
        var targetSection = document.getElementById(targetSectionId);
        var subSections = targetSection.querySelectorAll('section');

        for (var i = 0, l = subSections.length; i < l; i++) {
            var divElem = subSections[i].querySelector('div');
            var heading = subSections[i].querySelector('h3');

            divElem.classList[targetAction]('hidden');
            divElem.setAttribute('aria-hidden', isExpanded || 'false');
            heading.classList[targetAction]('collapsed');
        }

        if (isExpanded === 'true') {
            dataAttributeHandler({
                elem: targetElem,
                property: 'data-is-expanded',
                value: 'false'
            });

            targetElem.textContent = tabpanelOpenText;
        } else {
            dataAttributeHandler({
                elem: targetElem,
                property: 'data-is-expanded',
                value: 'true'
            });

            targetElem.textContent = tabpanelCloseText;
        }
    }

    // Don't execute if features aren't supported
    if (supportsBaselineJS()) {
        strings = document.getElementById('strings');
        mainContent = document.querySelector('.privacy-body');
        topicHeaders = document.querySelectorAll('.privacy-body .content-girdle > section');
        tabpanelCloseText = dataAttributeHandler({ elem: strings, property: 'data-tabpanel-close-text' });
        tabpanelOpenText = dataAttributeHandler({ elem: strings, property: 'data-tabpanel-open-text' });

        /* add a class to indicate that js is enabled. This will trigger
        the appropriate styling to be applied */
        mainContent.classList.add('interactive-widget');
        initPage();

        /**
         * Listens for click events on items inside the main content area.
         * It then calls the appropriate function based on the event target.
         * This avoids adding multiple event handlers on individual elements.
         */
        mainContent.addEventListener('click', function(event) {
            // hanle clicks on an individual topic
            if (event.target.tagName === 'H3') {
                var tabContent = event.target.parentElement.nextElementSibling;
                if (tabContent.classList.contains('hidden')) {
                    tabContent.classList.remove('hidden');
                    tabContent.setAttribute('aria-hidden', false);
                    event.target.classList.remove('collapsed');
                } else {
                    tabContent.classList.add('hidden');
                    tabContent.setAttribute('aria-hidden', true);
                    event.target.classList.add('collapsed');
                }
            }

            // handle clicks on the master toggle buttons
            if (event.target.classList.contains('toggle')) {
                toggleMainSectionTopics(event.target);
            }
        });
    }
})();
