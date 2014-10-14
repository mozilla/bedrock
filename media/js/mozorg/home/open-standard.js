/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $os = $('#open-standard');
    var $buttonsContainer = $('.os-category-buttons');
    var $buttons = $buttonsContainer.find('button');
    var $select = $os.find('#os-category-select');
    var $container = $os.find('.os-container');
    var $imgContainers = $os.find('.os-article .article-img');
    var $headlines = $os.find('.os-headlines a');
    var $headlineLists = $os.find('.os-headlines');
    var $articles = $os.find('.os-article-container article');

    var isSmallViewport = $('#masthead .container').width() < 941;
    var queryIsMobile;

    if (window.matchMedia) {
        queryIsMobile = matchMedia('(max-width: 1139px)');
    }

    /*
     * Shows the given feed category
     * @param $target (jQuery object), name (strong category name)
     */
    function showFeedCategory($target, name) {
        var $current;
        if ($target && $target.length > 0 && !$target.hasClass('selected')) {
            $current = $os.find('.os-container.selected');
            $current.removeClass('selected').attr('aria-expanded', 'false');
            $target.addClass('selected').attr('aria-expanded', 'true');

            gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: View articles by topic', name]);
        }
    }

    /*
     * Show feed category when buttons are clicked
     */
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

            // update select input when button changes
            $select.off('change.os', onCategorySelect);
            $select.find('option[value="' + id + '"]').prop('selected', 'selected');
            $select.on('change.os', onCategorySelect);
        }
    }

    /*
     * Show feed category when select input changes
     */
    function onCategorySelect(e) {
        e.preventDefault();

        var $target = $('#' + e.target.value);
        var name = $(e.target).find(':selected').data('name');

        // update button when selected option changes
        $buttonsContainer.find('.selected').removeClass('selected');
        $buttonsContainer.find('#' + e.target.value + '-btn').addClass('selected');

        showFeedCategory($target, name);
    }

    /*
     * Show article preview for wider screens when headline is clicked
     */
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
     * Track headline link clicks in GA for small screens
     */
    function trackArticleLink(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: Article Link Click', href]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Homepage Interactions', 'OS: Article Link Click', href], callback);
        }
    }

    /*
     * Article preview images are created from a placeholder to prevent smaller viewports
     * downloading images which are not needed
     */
    function initArticleImages() {
        $imgContainers.each(function () {
            var $placeholder = $(this).find('.img-placeholder');
            if ($placeholder.length > 0) {
                $placeholder.replaceWith('<img src="' + $placeholder.data('src') + '" alt="' + $placeholder.data('alt') + '">');
            }
        });
    }

    /*
     * Desktop users get article previews in the form of a tablist.
     * Clicking a category headline displays the corresponding article.
     */
    function initWideScreen() {
        $headlineLists.attr('role', 'tablist');
        $headlineLists.find('a.selected').attr('aria-selected', true);

        $headlines.each(function() {
            var $headline = $(this);
            $headline.attr('role', 'tab');
            $headline.attr('aria-controls', $headline.data('ariaControls'));
        });

        $articles.attr('role', 'tabpanel');
        $articles.not('.selected').attr('aria-hidden', true);
        $os.find('.os-article-container article.selected').attr('aria-hidden', false);
        $headlines.on('click.os', showFeedArticle);

        initArticleImages();
    }

    /*
     * Unbinds events and resets aria associated with desktop tablist
     */
    function removeWideScreen() {
        $headlines.removeAttr('role aria-selected aria-controls');
        $articles.removeAttr('role aria-hidden');
        $headlines.off('click.os', showFeedArticle);
    }

    /*
     * Bind link tracking clicks on headlines
     */
    function initSmallScreen() {
        $headlines.on('click.os', trackArticleLink);
    }

    /*
     * Unbind link tracking clicks on headlines
     */
    function removeSmallScreen() {
        $headlines.off('click.os', trackArticleLink);
    }

    /*
     * Track read more cta button click in GA
     */
    function trackReadMoreButton() {
        $os.find('a.more-large').on('click', function (e) {
            var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
            var href = this.href;
            var callback = function() {
                window.location = href;
            };

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

        // first category is initially selected
        $select[0].selectedIndex = 0;
        $container.first().addClass('selected');
        $buttons.first().addClass('selected');

        // for each category container add selected class to first
        // headline and article preview
        $container.each(function() {
            var $category = $(this);
            var $headline = $category.find('.os-headlines a:first');
            var $article = $category.find('.os-article-container article:first');

            $category.attr({
                'aria-role': 'region',
                'aria-expanded': 'false'
            });
            $category.first().attr('aria-expanded', 'true');

            $article.addClass('selected');
            $headline.addClass('selected');
        });

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

        // bind events
        $select.on('change.os', onCategorySelect);
        $buttons.on('click.os', onCategoryClick);

        // add ga tracking on read more button cta
        trackReadMoreButton();
    }

    initOpenStandard();
});
