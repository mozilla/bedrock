/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var ltr = document.dir === 'ltr';
    var historyEnabled = typeof history.replaceState === 'function';
    var utils = Mozilla.Utils;

    // Use the History API to update location.hash
    var updateHistory = function (sectionId) {
        if (historyEnabled) {
            history.replaceState({}, document.title, sectionId ? '#' + sectionId : '.');
        }
    };

    // Set up the modal navigation
    var navModal = function (direction) {
        var $origin = $('.modal-origin').removeClass('modal-origin');
        var action;

        if (direction === 1) {
            action = 'modal next';
            $origin = $origin.next().length ? $origin.next()
                                            : $origin.siblings(':first');
        } else {
            action = 'modal prev';
            $origin = $origin.prev().length ? $origin.prev()
                                            : $origin.siblings(':last');
        }

        // Get the new section ID
        var sectionId = $origin.attr('id');

        $('#modal').attr('aria-labelledby', sectionId).focus();
        $('#modal .inner').attr('id', sectionId + '-overlay');
        $('#modal .overlay-contents').replaceWith($origin.clone()
            .attr('tabindex', '0').addClass('overlay-contents'));

        $origin.addClass('modal-origin');

        window.dataLayer.push({
            'event': 'manifesto-interaction',
            'browserAction': action,
            'section': sectionId.match(/\d+/)[0]
        });

        updateHistory(sectionId);
    };

    // Set up the modal
    $('[id^="principle-"]').each(function () {
        var $this = $(this);
        var sectionId = $this.attr('id');

        $this.attr({
            'tabindex': '0'
        }).on('click', function () {

            Mozilla.Modal.createModal(this, $this.clone().removeAttr('id'), {
                'title': '',
                'onCreate': function () {
                    $('#modal .inner').attr('id', sectionId + '-overlay');
                    var $nav = $('<nav role="presentation"></nav>').insertBefore('#modal-close');

                    $('<button class="next" aria-controls="modal"></button>')
                        .text(utils.trans('principle-nav-next')).appendTo($nav);
                    $('<button class="prev" aria-controls="modal"></button>')
                        .text(utils.trans('principle-nav-prev')).appendTo($nav);

                    $nav.on('click', 'button', function () {
                        var $this = $(this);
                        var $section = $('#modal section');

                        // Track arrow clicks on Manifesto quote popup
                        window.dataLayer.push({
                            'event': 'manifesto-quote-click-arrow',
                            'direction': ($this.attr('class') === 'prev') ? 'previous' : 'next',
                            'quote': $section.attr('data-ga-quote'),
                            'quoteNumber': $section.attr('data-ga-quote-number')
                        });

                        navModal($this.hasClass('prev') ? -1 : 1);
                    });

                    updateHistory(sectionId);
                },
                'onDestroy': function () {
                    updateHistory();
                }
            });

            // Track Manifesto quote clicks

            window.dataLayer.push({
                'event': 'manifesto-quote-click',
                'quote': $this.attr('data-ga-quote'),
                'quoteNumber': $this.attr('data-ga-quote-number')
            });

        }).on('keydown', function (event) {
            if (event.keyCode === 13) {
                $this.trigger('click');
            }
        });

        $('<p class="more"></p>').text(utils.trans('principle-read-more').replace('…', ''))
            .appendTo($this.find('header'));
    });

    // Set up keyboard shortcuts for the modal
    $(document).on('keydown', '#modal', function (event) {
        var direction = 0;

        switch (event.keyCode) {
        case 37: // Left arrow
            direction = ltr ? -1 : 1;
            break;
        case 38: // Up arrow
            direction = -1;
            break;
        case 39: // Right arrow
            direction = ltr ? 1 : -1;
            break;
        case 40: // Down arrow
            direction = 1;
            break;
        }

        if (direction) {
            event.preventDefault();
            navModal(direction);
        }
    });

    // Open Twitter in a sub window
    // https://dev.twitter.com/docs/intents
    var openTwitterSubwin = function (section, url) {


        window.dataLayer.push({
            'event': 'manifesto-quote-share',
            'quote': $('#modal section').data('ga-quote')
        });

        // Check if the official Twitter widget is activated. If so, we don't
        // have to open a popup window ourselves as it will be opened by the
        // widget code.
        if (window.__twitterIntentHandler) {
            return;
        }

        var width = 550;
        var height = 420;
        var options = {
            'scrollbars': 'yes',
            'resizable': 'yes',
            'toolbar': 'no',
            'location': 'yes',
            'width': width,
            'height': height,
            'top': screen.height > height ? Math.round((screen.height / 2) - (height / 2)) : 0,
            'left': Math.round((screen.width / 2) - (width / 2))
        };

        window.open(url, 'twitter_share', $.param(options).replace(/&/g, ',')).focus();
    };

    // Set up modal link handler
    $(document).on('click', '#modal .principle a', function (event) {
        var $this = $(this);
        var section = $('#modal .inner').attr('id').match(/\d+/)[0];
        var href = $this.attr('href');
        var action;

        if ($this.hasClass('tweet')) {
            // Open Twitter in a sub window
            event.preventDefault();
            openTwitterSubwin(section, href);
        } else {
            // Open the link in a new tab
            $this.attr({
                'target': '_blank',
                'rel': 'noopener noreferrer'
            });

            action = href.match(/youtube/) ? 'modal video link click'
                                           : 'modal link click';

            window.dataLayer.push({
                'event': 'manifesto-interaction',
                'browserAction': action,
                'section': $('#modal section').data('ga-quote')
            });
        }
    });

    var tellLink = $('#sec-tell .share .tweet');

    // Update the tweet link when the custom text is modifled
    $('#sec-tell textarea').on('input', function () {
        tellLink.attr('href', tellLink.attr('href')
            .replace(/&text=.*/, '&text=' + encodeURIComponent($(this).val())));
    });

    // Set up content link handler
    $('#main-content a').each(function() {
        var $this = $(this);

        if (!$this.hasClass('share-button')) {
            $this.attr({
                'data-element-action': 'content link click',
                'data-element-section': $this.text()
            });
        }
    });

    $('#main-content a').on('click', function (event) {
        var $this = $(this);
        var href = $this.attr('href');

        event.preventDefault();

        if ($this.hasClass('tweet')) {
            // Open Twitter in a sub window
            openTwitterSubwin('custom', href);
        } else if (!$this.hasClass('share-button')) {
            // Open the link in the current tab
            location.href = href;

        }
    });

    // Open the modal automatically if valid location.hash is given
    if (location.hash.match(/^#principle\-\d+$/) && $(location.hash).length) {
        $(location.hash).click();
    }
});
