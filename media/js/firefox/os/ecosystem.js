/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $window = $(window);

    var pager;

    var $pageSections = $('.pager-page');
    var $mainContent = $('#main-content');
    var $phone = $('#phone');
    var $icons = $('#phone li');
    var $iconLinks = $icons.find('a');
    var $navButtons = $('#nav-button-wrapper');
    var $next = $('#next');
    var $logoWrapper = $('#page-header');
    var $copyHeadings = $('.pager-page:not(:first-child) h2');
    var $copyBodies = $('.copy-body');
    var $videos = $('video');

    var queryIsDesktop = matchMedia('(min-width: 1000px)');
    var desktopInitialized = false;

    // set up backgrounds
    var $wrapper = $('#wrapper');
    var $bgBlue = $('<div class="bg" id="bg-blue"></div>');
    var $bgWhite = $('<div class="bg" id="bg-white"></div>');
    var $foxTail = $('<div id="fox-tail" class="unloaded"></div>');

    $wrapper.prepend($foxTail).prepend($bgBlue).prepend($bgWhite);

    // un-hide pager pages (called after pager is initialized)
    // prevents sub page flicker just prior to pager initialization
    var showPagerPages = function() {
        $pageSections.css('opacity', 1);
    };

    // first view of desktop UI - only fires once per page load
    var initializeDesktop = function() {
        $phone.removeClass('unloaded');
        $foxTail.removeClass('unloaded');

        setTimeout(function() {
            initIconDazzle();
        }, 600);

        desktopInitialized = true;
    };

    // set all moving assets to default state
    // called on page load (if desktop width), when queryIsDesktop matches,
    // and when close button/icon is clicked
    var resetDesktopState = function() {
        $phone.removeClass('offset');
        $foxTail.removeClass('offset');
        $navButtons.fadeOut();
        $logoWrapper.removeClass('light');
        $bgBlue.removeClass('active');

        // allow icons to be keyboard navigated
        $iconLinks.removeAttr('tabindex');
    };

    // callback for pager
    // sets focus to next button (to get focus off hidden phone)
    var afterPageChangedCallback = function() {
        if (pager.currentPage.id !== 'intro') {
            $next.focus();
        }
    };

    // disable/enable desktop features
    var toggleDesktop = function(enable) {
        if (enable) {
            // keep window scrolled to the top if loading with hash
            if (window.location.hash !== '') {
                window.scrollTo(0, 0);
            }

            if (!desktopInitialized) {
                initializeDesktop();
            }

            // activate pager
            pager = new Mozilla.Pager($mainContent, {
                onCreate: showPagerPages,
                afterPageChanged: afterPageChangedCallback
            });

            // add phone/nav event listeners
            enablePhoneClicks();
            enableNavButtonClicks();

            // remove copy heading event listeners
            disableCopyHeaderClicks();

            // disallow keyboard access to headings
            $copyHeadings.removeAttr('tabindex');

            resetDesktopState();

            // listen for hash changes
            $window.on('hashchange.anniversary', function() {
                setPage();
            });
        } else {
            Mozilla.Pager.destroyPagers();
            pager = null;

            // make sure dark logo is showing
            $logoWrapper.removeClass('light');

            // remove phone/nav event listeners
            $phone.off('click.anniversary');
            $navButtons.off('click.anniversary').hide();

            // add copy heading event listeners
            enableCopyHeaderClicks();

            // allow keyboard access to headings
            $copyHeadings.attr('tabindex', 0);

            // stop listening for hash changes
            $window.off('hashchange.anniversary');
        }
    };

    // add listener to media query to load/unload desktop UI
    queryIsDesktop.addListener(function(mq) {
        if (mq.matches) {
            window.location.hash = '';

            // enable desktop features
            toggleDesktop(true);
        } else {
            // remove desktop features
            toggleDesktop(false);
        }
    });

    // initialize fancy fading in of phone icons
    var initIconDazzle = function() {
        var iconIds = [];

        $icons.each(function(i, li) {
            iconIds.push(li.id);
        });

        iconDazzle(iconIds);
    };

    // actually fade in phone icons
    var iconDazzle = function(iconIds) {
        var theIcon = iconIds.pop();

        $('#phone li#' + theIcon).addClass('loaded');

        if (iconIds.length > 0) {
            setTimeout(function(){
                iconDazzle(iconIds);
            }, 60);
        }
    };

    // sets pager page based on URL hash
    var setPage = function() {
        pauseVideos();

        var currentHash = window.location.hash.replace(/#/, '');

        // default to first page
        var page = pager.pages[0];

        // if hashchange fired from a button/icon click, page will already be set
        if (pager.currentPage.id === currentHash || (pager.currentPage.id === 'intro' && currentHash === '')) {
            return;
        }

        // if we have a hash, find the corresponding page
        if (window.location.hash !== '') {
            page = pager.findPageById(currentHash);
        }

        // if not on the intro page, set blue UI
        if (page.id !== 'intro') {
            $bgBlue.addClass('active'); // show blue bg
            $phone.addClass('offset'); // slide phone off to the right
            $foxTail.addClass('offset'); // slide fox tail off to the right
            $navButtons.fadeIn(); // fade in nav buttons
            $logoWrapper.addClass('light'); // set logo to light version

            // disallow icons to be keyboard navigated
            $iconLinks.attr('tabindex', -1);
        } else {
            resetDesktopState();
        }

        pager.setPageWithAnimation(page);
    };

    // add event listeners to phone icons
    var enablePhoneClicks = function() {
        // handle clicks on icons
        $phone.on('click.anniversary', 'a', function(e) {
            e.preventDefault();

            // disallow clicks if phone is offset
            if (!$phone.hasClass('offset')) {
                var href = $(this).attr('href');

                gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', 'Icon Click', href]);

                // updating the hash will fire the onhashchange listener, which
                // will display the requested page
                window.location.hash = href.replace(/#/, '');
            }
        });
    };

    // add event listeners to nav buttons (next/prev/close)
    var enableNavButtonClicks = function() {
        $navButtons.on('click.anniversary', 'button', function(e) {
            var button = $(e.target).attr('id');

            switch (button) {
                case 'close':
                    resetDesktopState();

                    // show intro section
                    var page = pager.findPageById('intro');
                    pager.setPageWithAnimation(page);

                    window.location.hash = 'intro';

                    break;
                case 'prev':
                    // make sure we don't display the intro page
                    if (pager.currentPage.index === 1) {
                        // jump to the last page
                        pager.setPageWithAnimation(pager.pages[pager.pages.length - 1]);
                    } else {
                        pager.prevPageWithAnimation();
                    }

                    window.location.hash = '#' + pager.currentPage.id;

                    break;
                case 'next':
                    if (pager.currentPage.index === pager.pages.length - 1) {
                        // jump to the second (first blue) page
                        pager.setPageWithAnimation(pager.pages[1]);
                    } else {
                        pager.nextPageWithAnimation();
                    }

                    window.location.hash = '#' + pager.currentPage.id;

                    break;
            }

            gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', button, '#' + pager.currentPage.id]);
        });
    };

    // add event listeners to page headings (used in < desktop sizes)
    var enableCopyHeaderClicks = function() {
        // make sure all copy-body's are hidden
        $copyBodies.hide();

        $copyHeadings.attr('role', 'button').on('click.anniversary keypress.anniversary', function(e) {
            var keyCode = e.keyCode || e.which;

            if (e.type === 'click' || (e.type === 'keypress' && keyCode === 13)) {
                var $this = $(this);
                var $copyBody = $this.siblings('.copy-body');
                var toggleState;

                if ($copyBody.is(':visible')) {
                    toggleState = 'close slider';
                    $copyBody.slideUp();
                    $this.attr('aria-expanded', false);

                    pauseVideos();
                } else {
                    toggleState = 'open slider';
                    $copyBody.slideDown();
                    $this.attr('aria-expanded', true);
                }

                gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', toggleState, '#' + $this.parents('.pager-page').attr('id')]);
            }
        });
    };

    // remove event listeners from page headings
    var disableCopyHeaderClicks = function() {
        $copyHeadings.removeAttr('role').off('.anniversary');

        // make sure any hidden copy-body's are visible
        $copyBodies.show();
    };

    var pauseVideos = function() {
        // stop all videos
        $videos.each(function(i, video) {
            video.pause();
        });
    };

    // GA tracking on videos
    $videos.on('play', function() {
        var $this = $(this);

        // get rid of focus style
        $this.blur();
        gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', $(this).attr('id'), 'Play']);

        // fix for odd Fx behavior/bug - controls do not fade out when clicking play and
        // *quickly* moving mouse off video
        setTimeout(function() {
            $this.removeAttr('controls');

            setTimeout(function() {
                $this.attr('controls', 'controls');
            }, 100);
        }, 100);
    }).on('pause', function() {
        // get rid of focus style
        this.blur();

        // is video over?
        // 'pause' event fires just before 'ended', so
        // using 'ended' results in extra pause tracking.
        var action = (this.currentTime === this.duration) ? 'Complete' : 'Pause';

        gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', $(this).attr('id'), action]);
    });

    // STARTUP ROUTINE
    // after a short wait, see if we should set up desktop UI
    setTimeout(function() {
        // are we at a desktop-y resolution?
        if (queryIsDesktop.matches) {
            // set up desktop stuff
            toggleDesktop(true);

            // present initial content
            setTimeout(function() {
                // if no URL hash, slide phone down and fox tail in, then start icon snazziness
                if (window.location.hash === '' || window.location.hash === '#intro') {
                    initializeDesktop();
                // if URL hash present, show that sub page
                } else {
                    // put phone & tail in the correct place
                    $phone.removeClass('unloaded').addClass('offset');
                    $foxTail.removeClass('unloaded').addClass('offset');

                    // quick display all phone icons
                    $('#phone li').addClass('loaded');

                    // show the requested page
                    setPage();
                }
            }, 300);
        // if less than desktop width, just enable page header listeners
        } else {
            // add copy heading event listeners
            enableCopyHeaderClicks();

            // allow keyboard access to headings
            $copyHeadings.attr('tabindex', 0);
        }
    }, 500);
})(window.jQuery);
