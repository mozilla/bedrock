/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $window = $(window);
    var $os = $('#open-standard');
    var $buttonsContainer = $('.os-category-buttons');
    var $buttons = $buttonsContainer.find('button');
    var $select = $os.find('#os-category-select');
    var $container = $os.find('.os-container');

    var isSmallViewport = $('#masthead .container').width() < 941;
    var queryIsMobile;

    if (window.matchMedia) {
        queryIsMobile = matchMedia('(max-width: 1139px)');
    }

    function showFeedCategory($target, name) {
        if ($target && $target.length > 0 && !$target.hasClass('selected')) {
            $os.find('.os-container.selected').removeClass('selected');
            $target.addClass('selected');

            gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: View articles by topic', name]);
        }
    }

    function onCategoryClick(e) {
        e.preventDefault();

        var $button = $(this);
        var id = $button.attr('aria-controls');
        var name = $button.data('name');
        var $target = $('#' + id);

        if ($target && $target.length > 0 && !$button.hasClass('selected')) {
            $buttonsContainer.find('.selected').removeClass('selected');
            $button.addClass('selected');
            showFeedCategory($target, name);
        }
    }

    function onCategorySelect(e) {
        e.preventDefault();

        var $target = $('#' + e.target.value);
        var name = $(e.target).find(':selected').data('name');

        showFeedCategory($target, name);
    }

    function showFeedArticle(e) {
        e.preventDefault();

        var $headline = $(this);
        var $headlineList = $headline.closest('.os-headlines');
        var id = $headline.attr('aria-controls');
        var $target = $('#' + id);

        if ($target.length > 0 && !$target.hasClass('selected')) {
            $headlineList.find('li .selected').removeClass('selected').attr('aria-selected', false);
            $headline.addClass('selected').attr('aria-selected', true);
            $target.siblings('.selected').removeClass('selected').attr('aria-hidden', true);
            $target.addClass('selected').attr('aria-hidden', false);

            gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: Article Link Click', this.href]);
        }
    }

    /*
     * Desktop users get article previews in the form of a tablist.
     * Clicking a category headline displays the corresponding article.
     */
    function initWideScreen() {
        $container.first().addClass('selected');
        $buttons.first().addClass('selected');

        $container.each(function() {
            var $category = $(this);
            var $headlineLists = $category.find('.os-headlines');
            var $headlines = $headlineLists.find('a');
            var $articles = $category.find('.os-article-container article');

            $headlineLists.attr('role', 'tablist');

            $headlines.attr('role', 'tab');
            $headlines.first().addClass('selected').attr('aria-selected', true);
            $headlines.siblings(':first').attr('aria-selected', false);

            $articles.attr('role', 'tabpanel');
            $articles.first().addClass('selected').attr('aria-hidden', false);
            $articles.siblings(':first').attr('aria-hidden', true);

            $headlines.on('click.os', showFeedArticle);
        });
    }

    /*
     * Unbinds events and resets aria associated with desktop tablist
     */
    function removeWideScreen() {
        $container.each(function() {
            var $category = $(this);
            var $headlineLists = $category.find('.os-headlines');
            var $headlines = $headlineLists.find('a');
            var $articles = $category.find('.os-article-container article');

            $category.removeClass('selected');

            $headlineLists.removeAttr('role');
            $headlines.removeAttr('role');
            $headlines.removeAttr('aria-selected');
            $headlines.removeClass('selected');

            $articles.removeAttr('role');
            $articles.removeAttr('aria-hidden');
            $articles.removeClass('selected');

            $headlines.off('click.os', showFeedArticle);
        });

        $buttonsContainer.find('.selected').removeClass('selected');
    }

    /*
     * Mobile users get a <select> input for category selection
     */
    function initSmallScreen() {
        $select[0].selectedIndex = 0;
        $container.first().addClass('selected');
        $buttons.first().addClass('selected');
    }

    function removeSmallScreen() {
        $container.each(function() {
            var $category = $(this);
            var $headlineLists = $category.find('.os-headlines');
            var $headlines = $headlineLists.find('a');
            var $articles = $category.find('.os-article-container article');

            $category.removeClass('selected');
            $headlines.removeClass('selected');
            $articles.removeClass('selected');
        });
    }

    function trackReadMoreButton() {
        $os.find('a.more-large').on('click', function (e) {
            var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
            var href = this.href;
            var callback = function() {
                window.location = href;
            }

            if (newTab) {
                gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: Article Link Click', 'Read More Articles']);
            } else {
                e.preventDefault();
                gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: Article Link Click', 'Read More Articles'], callback);
            }

        });
    }

    /*
     * Desktop viewports get article preview tablist
     * Mobile viewports get category headlines only
     */
    function initOpenStandard() {
        // if we support matchmedia, let's use it
        if (window.matchMedia) {

            if (queryIsMobile.matches) {
                initSmallScreen();
            } else {
                initWideScreen();
            }

            queryIsMobile.addListener(function(mq) {
                if (mq.matches) {
                    removeWideScreen();
                    initSmallScreen();
                } else {
                    removeSmallScreen();
                    initWideScreen();
                }
            });
        } else {
            // else let's just check window width
            if (isSmallViewport) {
                initSmallScreen();
            } else {
                initWideScreen();
            }
        }

        $select.on('change.os', onCategorySelect);
        $buttons.on('click.os', onCategoryClick);
        trackReadMoreButton();
    }

    initOpenStandard();

});
