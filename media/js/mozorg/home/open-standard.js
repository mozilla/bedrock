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

    function showFeedCategory($target) {
        if ($target && $target.length > 0 && !$target.hasClass('selected')) {
            $os.find('.os-container.selected').removeClass('selected');
            $target.addClass('selected');
        }
    }

    function onCategoryClick(e) {
        e.preventDefault();

        var $button = $(this);
        var id = $button.attr('aria-controls');
        var $target = $('#' + id);

        if ($target && $target.length > 0) {
            $buttonsContainer.find('.selected').removeClass('selected');
            $button.addClass('selected');
            showFeedCategory($target);
        }
    }

    function onCategorySelect(e) {
        e.preventDefault();

        var $target = $('#' + e.target.value);

        showFeedCategory($target);
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
        $select.on('change.os', onCategorySelect);
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
    }

    initOpenStandard();

});
