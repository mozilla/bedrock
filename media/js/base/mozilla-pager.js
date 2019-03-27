/**
 * Animated pagination widget
 *
 * Initializes all elements of a specific class as a pages section. Does so
 * in accessible way with options for next/prev arrows or tabbed navigation.
 *
 * This code is licensed under the Mozilla Public License 1.1.
 *
 * Portions adapted from the jQuery Easing plugin written by Robert Penner and
 * used under the following license:
 *
 *   Copyright 2001 Robert Penner
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions are
 *   met:
 *
 *   - Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   - Neither the name of the author nor the names of contributors may be
 *     used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 *   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 *   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 *   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 *   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 *   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 *   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * @copyright 2007-2010 Mozilla Foundation, 2007-2010 silverorange Inc.
 * @license   https://www.mozilla.org/MPL/1.1/ Mozilla Public License 1.1
 * @author    Michael Gauthier <mike@silverorange.com>
 *
 */

/**
 * Updated 2014-06
 * @author Jon Petto <jon@equalparts.io>
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

// {{{ Mozilla.Pager

/**
 * Pager widget
 *
 * @param jQuery Object $container - jQuery representation of element
 *          containing the pager.
 */
Mozilla.Pager = function($container) {
    'use strict';

    this.$container = $container;

    // If the potential pager has already been initialized, just return
    // a reference to the existing pager object.
    if (this.$container.hasClass('pager-initialized')) {
        return Mozilla.Pager.findPagerById(this.$container.prop('id'));
    }

    // Store reference to page container.
    this.$pageContainer = this.$container.find('.pager-content:first');

    // If the potential pager does not have content, it's invalid.
    if (!this.$pageContainer.length) {
        return null;
    }

    // Make sure the container has an ID.
    if (!this.$container.prop('id')) {
        this.$container.prop('id', 'mozilla-pager-' + Mozilla.Pager.currentId);
        Mozilla.Pager.currentId++;
    }

    // Make sure the page container has an ID.
    if (!this.$pageContainer.prop('id')) {
        this.$pageContainer.prop('id', this.$container.prop('id') + '-pages');
    }

    // Mark pager as initialized.
    this.$container.addClass('pager-initialized');

    this.id           = this.$container.prop('id');
    this.pagesById    = {};
    this.pages        = [];
    this.previousPage = null;
    this.currentPage  = null;
    this.animatingOut = false;

    this.randomStartPage = this.$container.hasClass('pager-random');

    // add pages
    var page;
    var pageNodes = this.$pageContainer.children('.pager-page');

    if (this.$container.hasClass('pager-with-tabs')) {
        // Should be either a <ol> or <ul>. Tab links must be contained
        // in a wrapper, e.g. <li><a href="#sometab"></a></li>.
        var $tabs = this.$container.find('.pager-tabs:first');

        this.$tabs = ($tabs.length) ? $tabs : null;
    } else {
        this.$tabs = null;
    }

    var i;
    if (this.$tabs) {
        this.$tabNodes = this.$tabs.children().not('.pager-not-tab');

        // initialize pages with tabs
        var index = 0;

        for (i = 0; i < pageNodes.length; i++) {
            if (i < this.$tabNodes.length) {
                var tabAnchorNode = $(this.$tabNodes[i]).children('a:first');

                if (tabAnchorNode.length) {
                    page = new Mozilla.Page(
                        pageNodes[i],
                        index,
                        tabAnchorNode[0]
                    );

                    this.addPage(page);

                    index++;
                }
            }
        }

        // Add WAI-ARIA support.
        this.$tabs.attr('role', 'tablist');
        this.$tabNodes.attr('role', 'presentation');
        this.$tabNodes.find('a').each(function(index, anchor) {
            var $anchor = $(anchor);

            $anchor.attr({
                'role': 'tab',
                'aria-controls': $anchor.attr('href').replace(/#/, ''),
                'aria-selected': 'false'
            });
        });
    } else {
        // initialize pages without tabs
        for (i = 0; i < pageNodes.length; i++) {
            page = new Mozilla.Page(pageNodes[i], i, false);
            this.addPage(page);
        }
    }

    if (this.$container.hasClass('pager-with-nav')) {
        this.drawNav();
    } else {
        this.$nav = null;
    }

    this.history = !this.$container.hasClass('pager-no-history');

    // initialize current page
    var currentPage;

    if (this.history) {
        var hash = location.hash;
        hash = (hash.substring(0, 1) === '#') ? hash.substring(1) : hash;

        // trim leading and tailing slash
        hash = hash.replace(/(^\/|\/$)/g, '');

        if (hash.length) {
            this.setStateFromPath(hash, false, false);
            currentPage = this.currentPage;
        }
    }

    if (!currentPage && this.pages.length > 0) {
        if (this.randomStartPage) {
            this.setPage(this.getPseudoRandomPage());
        } else {
            var defPage = this.$pageContainer.children('.default-page:first');

            if (defPage.length) {
                var defId;

                if (defPage[0].id.substring(0, 5) === 'page-') {
                    defId = defPage[0].id.substring(5);
                } else {
                    defId = defPage[0].id;
                }

                this.setPage(this.pagesById[defId]);
            } else {
                this.setPage(this.pages[0]);
            }
        }
    }

    // initialize auto-rotation of pages
    if (this.$container.hasClass('pager-auto-rotate')) {
        var that = this;
        this.autoRotate = true;
        this.startAutoRotate();

        // prevent auto-rotate when hovering over container
        this.$container.on('mouseenter.' + Mozilla.Pager.EVENT_NAMESPACE,
            function() {
                that.stopAutoRotate();
            }
        ).on('mouseleave.' + Mozilla.Pager.EVENT_NAMESPACE,
            function() {
                if (that.autoRotate) { that.startAutoRotate(); }
            }
        );

        // prevent auto-rotate when focused on container
        this.$container.on('focusin.' + Mozilla.Pager.EVENT_NAMESPACE,
            function() {
                that.stopAutoRotate();
            }
        ).on('focusout.' + Mozilla.Pager.EVENT_NAMESPACE,
            function() {
                if (that.autoRotate) {
                    that.startAutoRotate();
                }
            }
        );
    } else {
        this.autoRotate = false;
    }

    // Make pagers accessible from other scripts.
    Mozilla.Pager.pagers.push(this);

    // Make sure hash monitoring is active (if needed).
    if (this.history) {
        Mozilla.Pager.initHashMonitor();
    }

    return this;
};

// }}}

Mozilla.Pager.currentId  = 1;
Mozilla.Pager.pagers = [];
Mozilla.Pager.monitoringHash = false;

// Time taken for page to fade in/out from tab/nav interaction.
Mozilla.Pager.PAGE_DURATION = Mozilla.Pager.PAGE_DURATION || 150;    // milliseconds
// Time taken for page to fade in/out during auto rotate.
Mozilla.Pager.PAGE_AUTO_DURATION = Mozilla.Pager.PAGE_AUTO_DURATION || 850;    // milliseconds
// Time page is visible during auto rotate.
Mozilla.Pager.AUTO_ROTATE_INTERVAL = Mozilla.Pager.AUTO_ROTATE_INTERVAL || 7000;  // milliseconds
Mozilla.Pager.NEXT_TEXT = Mozilla.Pager.NEXT_TEXT || Mozilla.Utils.trans('global-next');
Mozilla.Pager.PREV_TEXT = Mozilla.Pager.PREV_TEXT || Mozilla.Utils.trans('global-previous');
Mozilla.Pager.HIDDEN_CLASS = 'hidden'; // sets display: none;

// Should not be overridden by implementing script.
Mozilla.Pager.PAGE_NUMBER_TEXT = '%s / %s';
Mozilla.Pager.EVENT_NAMESPACE = 'mozpager'; // targeted event (un)binding

// {{{ createPagers()

/**
 * Initializes pagers.
 *
 * @param Boolean autoOnly - If true, only initializes pagers with
 *     'pager-auto-init' class.
 */
Mozilla.Pager.createPagers = function(autoOnly) {
    'use strict';

    // Find all pagers that have not been initialized.
    $('.pager').not('.pager-initialized').each(function(i, pagerNode) {
        var $pagerNode = $(pagerNode);

        if ((autoOnly && $pagerNode.hasClass('pager-auto-init')) || !autoOnly) {
            new Mozilla.Pager($pagerNode);
        }
    });
};

// }}}
// {{{ findPager()

Mozilla.Pager.findPagerById = function(pagerId) {
    'use strict';

    var pager = $.grep(Mozilla.Pager.pagers, function(elem) {
        return elem.id === pagerId;
    });

    return pager.length > 0 ? pager[0] : null;
};

// }}}
// {{{ destroyPagers()

Mozilla.Pager.destroyPagers = function() {
    'use strict';

    var pagerIds = [];
    var i;

    for (i = 0; i < Mozilla.Pager.pagers.length; i++) {
        pagerIds.push(Mozilla.Pager.pagers[i].id);
    }

    for (i = 0; i < pagerIds.length; i++) {
        Mozilla.Pager.destroyPagerById(pagerIds[i]);
    }
};

// }}}
// {{{ destroyPagerById()

Mozilla.Pager.destroyPagerById = function(pagerId) {
    'use strict';

    var pager = Mozilla.Pager.findPagerById(pagerId);

    // If no pager is found, we're done here.
    if (!pager) {
        return false;
    }

    // Stop auto-rotate.
    if (pager.autoRotate) {
        pager.stopAutoRotate();
    }

    // Remove generated nav markup.
    if (pager.$nav) {
        pager.$nav.remove();
    }

    // Remove event listeners from container.
    pager.$container.off('.' + Mozilla.Pager.EVENT_NAMESPACE);

    if (pager.$tabs) {
        // Remove 'selected' class from tab links.
        pager.$tabNodes.find('a').removeClass('selected');

        // Remove 'pager-selected-?' class from tab links container.
        pager.$tabs[0].className = Mozilla.Pager.removePagerSelectedClass(pager.$tabs[0].className);
    }

    for (var i = 0; i < pager.pages.length; i++) {
        // Remove hidden classes/ARIA states from pages
        pager.pages[i].$el.removeClass(Mozilla.Pager.HIDDEN_CLASS).attr('aria-hidden', 'false');

        // Revert page ID and remove data.
        pager.pages[i].$el.prop('id', pager.pages[i].$el.data('orig-id'));
        pager.pages[i].$el.data('orig-id', undefined);

        // Remove event listeners on tabs.
        if (pager.pages[i].tab) {
            pager.pages[i].$tab.off('.' + Mozilla.Pager.EVENT_NAMESPACE).attr('aria-selected', 'false');
        }

        // Remove event listeners on page children.
        pager.pages[i].$el.find('*').off('.' + Mozilla.Pager.EVENT_NAMESPACE);
    }

    // Remove from array
    var pagerIndex = $.inArray(pager, Mozilla.Pager.pagers);
    Mozilla.Pager.pagers.splice(pagerIndex, 1);

    // Remove initialized class
    pager.$container.removeClass('pager-initialized');

    // Update hash monitoring
    Mozilla.Pager.updateHashMonitor();

    return true;
};

// }}}
// {{{ initHashMonitor()

Mozilla.Pager.initHashMonitor = function() {
    'use strict';

    if (!Mozilla.Pager.monitoringHash) {
        // If one or more root pagers have history enabled, check if window
        // location changes from back/forward button use.
        for (var i = 0; i < Mozilla.Pager.pagers.length; i++) {
            if (Mozilla.Pager.pagers[i].history) {
                $(window).on('hashchange.' + Mozilla.Pager.EVENT_NAMESPACE, Mozilla.Pager.checkLocation);
                Mozilla.Pager.monitoringHash = true;

                break;
            }
        }
    }
};

// }}}
// {{{ updateHashMonitor()

Mozilla.Pager.updateHashMonitor = function() {
    'use strict';

    // Only proceed if hash is currently being monitored.
    if (Mozilla.Pager.monitoringHash) {
        var shouldMonitor = false;

        // Make sure a pager with history still exists.
        for (var i = 0; i < Mozilla.Pager.pagers.length; i++) {
            if (Mozilla.Pager.pagers[i].history) {
                shouldMonitor = true;
                break;
            }
        }

        // If no pager with history exists, stop hash monitoring.
        if (!shouldMonitor) {
            $(window).off('hashchange.' + Mozilla.Pager.EVENT_NAMESPACE);
            Mozilla.Pager.monitoringHash = false;
        }
    }
};

// }}}
// {{{ checkLocation()

Mozilla.Pager.checkLocation = function() {
    'use strict';

    var hash = location.hash;
    hash = (hash.substring(0, 1) === '#') ? hash.substring(1) : hash;

    // trim leading and tailing slash
    hash = hash.replace(/(^\/|\/$)/g, '');

    var pager;

    for (var i = 0; i < Mozilla.Pager.pagers.length; i++) {
        pager = Mozilla.Pager.pagers[i];

        if (pager.history) {
            pager.setStateFromPath(hash, true, true);
        }
    }
};

// }}}
// {{{ getPseudoRandomPage()

Mozilla.Pager.prototype.getPseudoRandomPage = function() {
    'use strict';

    var page = null;

    if (this.pages.length > 0) {
        var now = new Date();
        page = this.pages[now.getSeconds() % this.pages.length];
    }

    return page;
};

// }}}
// {{{ setStateFromPath()

Mozilla.Pager.prototype.setStateFromPath = function(path, animate, focus) {
    'use strict';

    var base = path;
    var pos = base.indexOf('/');

    if (pos !== -1) {
        base = base.substr(0, pos);
        path = path.substr(pos + 1);
    }

    var baseParts = base.split('+');
    var updateSelf;
    var page;

    for (var i = 0; i < baseParts.length; i++) {
        base = baseParts[i];
        page = this.pagesById[base];
        updateSelf = (this.currentPage === null || base !== this.currentPage.id);

        if (page) {
            if (updateSelf) {
                if (animate) {
                    this.setPageWithAnimation(
                        page,
                        Mozilla.Pager.PAGE_DURATION
                    );
                } else {
                    this.setPage(page);
                }
            }

            if (updateSelf && focus) {
                this.currentPage.focusTab(); // for accessibility
            }

            break;
        }
    }

};

// }}}
// {{{ prevPageWithAnimation()

Mozilla.Pager.prototype.prevPageWithAnimation = function(duration) {
    'use strict';

    var index = this.currentPage.index - 1;
    if (index < 0) {
        index = this.pages.length - 1;
    }

    this.setPageWithAnimation(this.pages[index], duration);
};

// }}}
// {{{ nextPageWithAnimation()

Mozilla.Pager.prototype.nextPageWithAnimation = function(duration) {
    'use strict';

    var index = this.currentPage.index + 1;
    if (index >= this.pages.length) {
        index = 0;
    }

    this.setPageWithAnimation(this.pages[index], duration);
};

// }}}
// {{{ drawNav()

Mozilla.Pager.prototype.drawNav = function() {
    'use strict';

    var that = this;

    this.$nav = $('<div>').attr({
        'class': 'pager-nav'
    });

    // page numbers
    this.$pageNumber = $('<span>').attr('class', 'pager-nav-page-number');
    this.$pageNumber.appendTo(this.$nav);

    this.$navLinksWrapper = $('<fieldset>').attr({
        'class': 'pager-nav-links-wrapper'
    });
    this.$navLinksWrapper.appendTo(this.$nav);

    // create previous link
    this.$prev = $('<button>').attr({
        'type': 'button',
        'class': 'pager-prev',
        'aria-controls': this.$pageContainer.prop('id')
    }).text(Mozilla.Pager.PREV_TEXT);

    this.$prev.on('click.' + Mozilla.Pager.EVENT_NAMESPACE, function(e) {
        e.preventDefault();
        that.prevPageWithAnimation(Mozilla.Pager.PAGE_DURATION);
        that.autoRotate = false;
        that.stopAutoRotate();
    }).appendTo(this.$navLinksWrapper);

    // divider
    var $divider = $('<span>').attr('class', 'pager-nav-divider');
    $divider.appendTo(this.$navLinksWrapper);

    // create next link
    this.$next = $('<button>').attr({
        'type': 'button',
        'class': 'pager-next',
        'aria-controls': this.$pageContainer.prop('id')
    }).text(Mozilla.Pager.NEXT_TEXT);

    this.$next.on('click.' + Mozilla.Pager.EVENT_NAMESPACE, function(e) {
        e.preventDefault();
        that.nextPageWithAnimation(Mozilla.Pager.PAGE_DURATION);
        that.autoRotate = false;
        that.stopAutoRotate();
    }).appendTo(this.$navLinksWrapper);

    // add nav to the DOM
    this.$nav.insertBefore(this.$pageContainer);
};

// }}}
// {{{ updateLocation()

Mozilla.Pager.prototype.updateLocation = function(page) {
    'use strict';

    if (!this.history) {
        return;
    }

    // set address bar to current page
    var baseLocation = location.href.split('#')[0];

    var hash = page.id;

    location.href = baseLocation + '#' + hash;
};

// }}}
// {{{ addPage()

Mozilla.Pager.prototype.addPage = function(page) {
    'use strict';

    var that = this;

    this.pagesById[page.id] = page;
    this.pages.push(page);

    if (page.tab) {
        page.$tab.on('click.' + Mozilla.Pager.EVENT_NAMESPACE, function(e) {
            e.preventDefault();
            that.setPageWithAnimation(page, Mozilla.Pager.PAGE_DURATION);
            that.autoRotate = false;
            that.stopAutoRotate();
        });
    }

    page.$el.find('*').on('focus.' + Mozilla.Pager.EVENT_NAMESPACE, function() {
        if (page.$el.hasClass(Mozilla.Pager.HIDDEN_CLASS)) {
            that.setPage(page);
            that.autoRotate = false;
            that.stopAutoRotate();
        }
    });
};

// }}}
// {{{ update()

Mozilla.Pager.prototype.update = function() {
    'use strict';

    if (this.$tabs) {
        this.updateTabs();
    }

    if (this.$nav) {
        this.updateNav();
    }

    var el = this.$pageContainer.get(0);

    el.className = Mozilla.Pager.removePagerSelectedClass(el.className);

    this.$pageContainer.addClass('pager-selected-' + this.currentPage.id);
};

// }}}
// {{{ updateTabs()

Mozilla.Pager.prototype.updateTabs = function() {
    'use strict';

    var el = this.$tabs.get(0);

    el.className = Mozilla.Pager.removePagerSelectedClass(el.className);

    this.currentPage.selectTab();
    this.$container.trigger('changePage', [this.currentPage.tab]);
    this.$tabs.addClass('pager-selected-' + this.currentPage.id);
};

Mozilla.Pager.removePagerSelectedClass = function(className) {
    'use strict';

    className = className.replace(/pager-selected-[\w-]+/g, '');
    className = className.replace(/^\s+|\s+$/g,'');

    return className;
};

// }}}
// {{{ updateNav()

Mozilla.Pager.prototype.updateNav = function() {
    'use strict';

    // update page number
    var pageNumber = this.currentPage.index + 1;
    var pageCount  = this.pages.length;

    var text = Mozilla.Pager.PAGE_NUMBER_TEXT.replace(/%s/, pageNumber);
    text     = text.replace(/%s/, pageCount);

    this.$pageNumber.text(text);

    // update previous link
    this.updateNavPrevLink(this.currentPage.index === 0);

    // update next link
    this.updateNavNextLink(this.currentPage.index === this.pages.length - 1);
};

// }}}
// {{{ updateNavPrevLink()

Mozilla.Pager.prototype.updateNavPrevLink = function(disable) {
    'use strict';

    this.$prev.prop('disabled', disable);
};

// }}}
// {{{ updateNavNextLink()

Mozilla.Pager.prototype.updateNavNextLink = function(disable) {
    'use strict';

    this.$next.prop('disabled', disable);
};

// }}}
// {{{ setPage()

Mozilla.Pager.prototype.setPage = function(page) {
    'use strict';

    if (this.currentPage !== page) {
        if (this.currentPage) {
            this.currentPage.deselectTab();
            this.currentPage.hide();
        }

        if (this.previousPage) {
            this.previousPage.hide();
        }

        this.previousPage = this.currentPage;

        this.currentPage = page;
        this.currentPage.show();
        this.update();
    }
};

// }}}
// {{{ setPageWithAnimation()

Mozilla.Pager.prototype.setPageWithAnimation = function(page, duration) {
    'use strict';

    if (this.currentPage !== page) {

        this.updateLocation(page);

        // deselect last selected page (not necessarily previous page)
        if (this.currentPage) {
            this.currentPage.deselectTab();
        }

        // fade out if we are not already fading out
        if (!this.animatingOut) {
            // if we were fading in, don't take as long to fade out
            if (this.$pageContainer.is(':animated')) {
                var startOpacity = parseFloat(this.$pageContainer.css('opacity'));
                duration = startOpacity * Mozilla.Pager.PAGE_DURATION;
                this.$pageContainer.stop(true, false);
            }

            // only set previous page if we are not already fading out
            this.previousPage = this.currentPage;
            this.animatingOut = true;

            // Set the current page before the animation starts to prevent
            // race conditions if the duration is super low or 0. With low
            // durations, the complete handler function will run before this
            // function finishes.
            this.currentPage = page;

            var that = this;

            this.$pageContainer.animate(
                { opacity: 0 },
                duration,
                'pagerFadeOut',
                function() {
                    that.fadeInPage(duration);
                }
            );

        } else {
            // always set current page so the correct page fades in
            this.currentPage = page;
        }

        this.update();
    }

    // for Safari 1.5.x bug setting window.location.
    return false;
};

// }}}
// {{{ fadeInPage()

Mozilla.Pager.prototype.fadeInPage = function(duration) {
    'use strict';

    if (this.previousPage) {
        this.previousPage.hide();
    }

    this.currentPage.show();

    this.animatingOut = false;

    this.$pageContainer.animate({ opacity: 1 }, duration, 'pagerFadeOut');
};

// }}}
// {{{ stopAutoRotate()

Mozilla.Pager.prototype.stopAutoRotate = function() {
    'use strict';

    if (this.autoRotateInterval) {
        clearInterval(this.autoRotateInterval);
        this.autoRotateInterval = null;
    }
};

// }}}
// {{{ startAutoRotate()

Mozilla.Pager.prototype.startAutoRotate = function() {
    'use strict';

    var setupInterval = function(pager) {
        var intervalFunction = function() {
            pager.nextPageWithAnimation(Mozilla.Pager.PAGE_AUTO_DURATION);
        };

        pager.autoRotateInterval = setInterval(intervalFunction,
            Mozilla.Pager.AUTO_ROTATE_INTERVAL, pager);
    };

    if (!this.autoRotateInterval) {
        setupInterval(this);
    }
};

// }}}
// {{{ Mozilla.Page

/**
 * Page in a pager
 *
 * @param DOMElement el
 * @param Number index
 * @param DOMElement tab
 */
Mozilla.Page = function(el, index, tab) {
    'use strict';

    this.el = el;
    this.$el = $(this.el);

    // Make sure the Page has an ID.
    if (!this.$el.prop('id')) {
        this.$el.prop('id', 'mozilla-pager-page-' + Mozilla.Page.currentId);
        Mozilla.Page.currentId++;
    }

    // Change element id so updating the window.location does not navigate to
    // the page. This is mostly for IE.
    if (this.el.id.substring(0, 5) === 'page-') {
        this.id = this.el.id.substring(5);
    } else {
        this.id = this.el.id;
    }

    // Store original ID for revert when destroyed.
    this.$el.data('orig-id', this.el.id);

    this.el.id = 'page-' + this.id;
    this.index = index;

    if (tab) {
        this.tab = tab;
        this.$tab = $(this.tab);

        // Make sure the tab has an ID (for WAI-ARIA).
        if (!this.$tab.prop('id')) {
            this.$tab.prop('id', this.id + '-tab');
        }

        // Add WAI-ARIA support.
        this.$el.attr({
            'aria-labelledby': this.$tab.prop('id'),
            'role': 'tabpanel'
        });
    } else {
        this.tab = null;
    }

    this.hide();
};

// }}}

Mozilla.Page.currentId = 1;

// {{{ selectTab()

Mozilla.Page.prototype.selectTab = function() {
    'use strict';

    if (this.tab) {
        this.$tab.addClass('selected').attr('aria-selected', 'true');
    }
};

// }}}
// {{{ deselectTab()

Mozilla.Page.prototype.deselectTab = function() {
    'use strict';

    if (this.tab) {
        this.$tab.removeClass('selected').attr('aria-selected', 'false');
    }
};

// }}}
// {{{ focusTab()

Mozilla.Page.prototype.focusTab = function() {
    'use strict';

    if (this.tab) {
        this.tab.focus();
    }
};

// }}}
// {{{ hide()

Mozilla.Page.prototype.hide = function() {
    'use strict';

    this.$el.addClass(Mozilla.Pager.HIDDEN_CLASS).attr('aria-hidden', 'true');
};

// }}}
// {{{ show()

Mozilla.Page.prototype.show = function() {
    'use strict';

    this.$el.removeClass(Mozilla.Pager.HIDDEN_CLASS).attr('aria-hidden', 'false');
};

// }}}

$(document).ready(function() {
    'use strict';

    // add easing functions
    $.extend($.easing, {
        'pagerFadeIn':  function (x, t, b, c, d) {
            return c * (t /= d) * t + b;
        },
        'pagerFadeOut': function (x, t, b, c, d) {
            return -c * (t /= d) * (t - 2) + b;
        }
    });

    Mozilla.Pager.createPagers(true);
});
