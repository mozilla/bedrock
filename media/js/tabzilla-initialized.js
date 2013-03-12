;(function($,sr){
    'use strict';
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
        var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap) {
                    func.apply(obj, args);
                }
                timeout = null;
            }
            if (timeout) {
                clearTimeout(timeout);
            }
            else if (execAsap){
                func.apply(obj, args);
            }
            timeout = setTimeout(delayed, threshold || 100);
        };
    };
    // smartresize
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };
})(jQuery,'smartresize');

var moz = (function (parent, $) {
    'use strict';
    var tabzilla = parent.tabzilla = parent.tabzilla || {};

    // private variables
    var hasMediaQueries = ('matchMedia' in window);
    var isGT_IE8 = function() {
        return !(/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
    };

    var tab = $('#tabzilla');
    var opened = false;

    var panel;
    var tabzillaNav;
    var headlines;

    var mode = 'wide';
    var checkMode = function () {
        var currentMode = getMode();
        if (mode !== currentMode) {
            mode = currentMode;
            setMode();
        }
    };
    var getMode = function() {
        if ((isGT_IE8() || hasMediaQueries) && ($(window).outerWidth() <= 719)) {
            return 'compact';
        } else {
            return 'wide';
        }
    };
    var setMode = function () {
        if (mode === 'wide') {
            leaveCompactMode();
        } else {
            enterCompactMode();
        }
    };
    var leaveCompactMode = function () {
        removeCompactModeAttributes();
        removeCompactModeEvents();
        panel.focus();
    };
    var enterCompactMode = function () {
        addCompactModeAttributes();
        addCompactModeEvents();
    };

    var addCompactModeAttributes = function () {
        tabzillaNav.find('>ul').attr('role', 'presentation');

        headlines.each(function(i) {
            $(this).attr({
                'id': 'tab-'+i,
                'aria-controls': 'panel-'+0,
                'tabindex': '-1',
                'role': 'tab',
                'aria-expanded': false
            });
        });
        if (!tabzillaNav.find('h2[tabindex=0]').length) {
            tabzillaNav.find('h2:first').attr('tabindex', 0);
        }

        tabzillaNav.find('div').each(function(i) {
            $(this).attr({
                'id': 'panel-'+i,
                'aria-labeledby': 'tab-'+i,
                'role': 'tabpanel'
            }).css('display','none');
        });
    };
    var removeCompactModeAttributes = function () {
        headlines.removeAttr('id aria-controls tabindex role aria-expanded');
        tabzillaNav.find('div').removeAttr('id aria-labeledby role style');
    };
    var addCompactModeEvents = function () {
        tabzillaNav.on('click.submenu', 'h2', function (event){
            event.preventDefault();
            var div = $(event.target).next('div');
            $(event.target).attr('aria-expanded', div.is(':hidden'));
            div.toggle();
        });
        tabzillaNav.on('keydown.submenu', function (event){
            var which = event.which;
            var target = $(event.target);
            // enter or space
            if (which === 13 || which === 32) {
                event.preventDefault();
                target.trigger('click');
            }
            // up or left
            if (which === 37 || which === 38) {
                event.preventDefault();
                headlines.each(function(i) {
                    if (i > 0 && $(this).attr('tabindex') === 0) {
                        $(this).attr('tabindex', '-1');
                        $(headlines[i-1]).attr('tabindex', 0).focus();
                        return false;
                    }
                });
            }
            // down or right
            if (which === 40 || which === 39) {
                event.preventDefault();
                headlines.each(function(i) {
                    if (i < (headlines.length - 1) && $(this).attr('tabindex') === 0) {
                        $(this).attr('tabindex', '-1');
                        $(headlines[i+1]).attr('tabindex', 0).focus();
                        return false;
                    }
                });
            }
            // esc
            if (which === 27 && target.is('a')) {
                event.preventDefault();
                event.stopPropagation();
                target.parents('div').prev('h2').trigger('click').focus();
            }
        });
    };
    var removeCompactModeEvents = function () {
        tabzillaNav.off('.submenu');
    };
    var removeClickEvent = function (tab) {
        if (typeof tab.detachEvent != 'undefined') {
            tab.detachEvent('onclick', tabzilla.loadAssets);
        } else {
            tab.removeEventListener('click', tabzilla.loadAssets, false);
        }
    };

    tabzilla.open = function () {
        opened = true;
        panel.toggleClass('open');
        var height = $('#tabzilla-contents').height();
        panel.animate({ 'height' : height }, 200, function() {
            panel.css('height', 'auto');
        });
        tab
            .attr({'aria-expanded' : 'true'})
            .addClass('tabzilla-opened')
            .removeClass('tabzilla-closed');

        panel.focus();
    };

    tabzilla.close = function () {
        opened = false;
        panel.animate({ height: 0 }, 200, function() {
            panel.toggleClass('open');
        });

        tab
            .attr({'aria-expanded' : 'false'})
            .addClass('tabzilla-closed')
            .removeClass('tabzilla-opened');
    };

    tabzilla.init = function () {
        $('body').prepend(content);
        panel = $('#tabzilla-panel');
        tabzillaNav = $('#tabzilla-nav');
        headlines = tabzillaNav.find('h2');

        checkMode();
        $(window).smartresize(function () {
            checkMode();
        });

        panel.on('keydown', function(event) {
            if (event.which === 27) {
                event.preventDefault();
                tabzilla.close();
            }
        });

        tab.on('click', function(event) {
            event.preventDefault();
            if (opened) {
                tabzilla.close();
            } else {
                tabzilla.open();
            }
        });

        if (tab.hasClass('tabzilla-loading')) {
            removeClickEvent($(tab)[0]);
            tab.removeClass('tabzilla-loading');
            tabzilla.open();
        }
    };

    var content =
        '<div id="tabzilla-panel" class="tabzilla-closed" tabindex="-1">' +
        '  <div id="tabzilla-contents">' +
        '    <div id="tabzilla-promo">' +
        '      <div class="snippet" id="tabzilla-promo-mwc">' +
        '      <a href="https://www.mozilla.org/firefox/partners/">' +
        '       <h4>Firefox OS debuts</h4>' +
        '       <p>at Mobile World Congress!</p>' +
        '       <p>Learn more »</p></a>' +
        '      </div>' +
        '    </div>' +
        '    <div id="tabzilla-nav">' +
        '      <ul>' +
        '        <li><h2>Mozilla</h2>' +
        '          <div>' +
        '            <ul>' +
        '              <li><a href="https://www.mozilla.org/mission/">Mission</a></li>' +
        '              <li><a href="https://www.mozilla.org/about/">About</a></li>' +
        '              <li><a href="https://www.mozilla.org/projects/">Projects</a></li>' +
        '              <li><a href="https://support.mozilla.org/">Support</a></li>' +
        '              <li><a href="https://developer.mozilla.org">Developer Network</a></li>' +
        '            </ul>' +
        '          </div>' +
        '        </li>' +
        '        <li><h2>Products</h2>' +
        '          <div>' +
        '            <ul>' +
        '              <li><a href="https://www.mozilla.org/firefox">Firefox</a></li>' +
        '              <li><a href="https://www.mozilla.org/thunderbird">Thunderbird</a></li>' +
        '              <li><a href="https://www.mozilla.org/firefoxos">Firefox OS</a></li>' +
        '            </ul>' +
        '          </div>' +
        '        </li>' +
        '        <li><h2>Innovations</h2>' +
        '          <div>' +
        '            <ul>' +
        '              <li><a href="https://webfwd.org/">WebFWD</a></li>' +
        '              <li><a href="https://mozillalabs.com/">Labs</a></li>' +
        '              <li><a href="https://webmaker.org/">Webmaker</a></li>' +
        '              <li><a href="https://www.mozilla.org/research/">Research</a></li>' +
        '            </ul>' +
        '          </div>' +
        '        </li>' +
        '        <li><h2>Get Involved</h2>' +
        '          <div>' +
        '            <ul>' +
        '              <li><a href="https://www.mozilla.org/contribute/">Volunteer</a></li>' +
        '              <li><a href="https://www.mozilla.org/en-US/about/careers.html">Careers</a></li>' +
        '              <li><a href="https://www.mozilla.org/en-US/about/mozilla-spaces/">Find us</a></li>' +
        '              <li><a href="https://join.mozilla.org/">Join us</a></li>' +
        '            </ul>' +
        '          </div>' +
        '        </li>' +
        '        <li id="tabzilla-search">' +
        '          <a href="https://www.mozilla.org/community/directory.html">Website Directory</a>' +
        '          <form title="Search Mozilla sites" role="search" action="http://www.google.com/cse">' +
        '            <input type="hidden" value="002443141534113389537:ysdmevkkknw" name="cx">' +
        '            <input type="hidden" value="FORID:0" name="cof">' +
        '            <label for="q">Search</label>' +
        '            <input type="search" placeholder="Search" id="q" name="q">' +
        '          </form>' +
        '        </li>' +
        '      </ul>' +
        '    </div>' +
        '  </div>' +
        '</div>';

    return parent;
}(moz || {}, jQuery));