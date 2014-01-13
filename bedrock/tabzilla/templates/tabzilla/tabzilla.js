/**
 * Tabzilla global navigation for Mozilla projects
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
 *   Media query matchMedia polyfill implementation from Paul Irish
 *   (https://github.com/paulirish/matchMedia.js/) used under the following
 *   license (MIT):
 *
 *   Copyright (c) 2012 Scott Jehl
 *
 *   Permission is hereby granted, free of charge, to any person obtaining a copy
 *   of this software and associated documentation files (the "Software"), to
 *   deal in the Software without restriction, including without limitation the
 *   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 *   sell copies of the Software, and to permit persons to whom the Software is
 *   furnished to do so, subject to the following conditions:
 *
 *   The above copyright notice and this permission notice shall be included in
 *   all copies or substantial portions of the Software.
 *
 *   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 *   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 *   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 *   DEALINGS IN THE SOFTWARE.
 *
 *
 * @copyright 2012-2013 silverorange Inc.
 * @license   http://www.mozilla.org/MPL/MPL-1.1.html Mozilla Public License 1.1
 * @author    Michael Gauthier <mike@silverorange.com>
 * @author    Steven Garrity <steven@silverorange.com>
 * @author    Isac Lagerblad <icaaaq@gmail.com>
 * @author    Kohei Yoshino <kohei.yoshino@gmail.com>
 */

var Tabzilla = (function (Tabzilla) {
    'use strict';
    var minimumJQuery = '1.7.1';
    var panel;
    var nav;
    var headlines;
    var tab;
    var opened = false;
    var hasMediaQueries = ('matchMedia' in window);
    var isIE9 = (document.documentMode === 9);
    var mode = 'wide';
    var negativeTabIndex = '-1';
    var $ = null; // non-version-conflicting jQuery alias for tabzilla
    var jQuery;
    var checkMode = function () {
        var currentMode = getMode();
        if (mode !== currentMode) {
            mode = currentMode;
            setMode();
        }
    };
    var getMode = function() {
        if (hasMediaQueries && matchMedia('(max-width: 719px)').matches) {
            return 'compact';
        }
        return 'wide';
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
        nav.find('>ul').attr('role', 'presentation');

        headlines.each(function (i) {
            $(this).attr({
                'id': 'tab-' + i,
                'aria-controls': 'panel-' + i,
                'tabindex': negativeTabIndex,
                'role': 'tab',
                'aria-expanded': false
            });
        });
        if (!nav.find('h2[tabindex=0]').length) {
            nav.find('h2:first').attr('tabindex', 0);
        }
        nav.find('div').each(function (i) {
            $(this).attr({
                'id': 'panel-' + i,
                'aria-labeledby': 'tab-' + i,
                'role': 'tabpanel'
            }).css('display','none');
        });
    };
    var removeCompactModeAttributes = function () {
        nav.find('>ul').removeAttr('role');
        headlines.removeAttr('id aria-controls tabindex role aria-expanded');
        nav.find('div').removeAttr('id aria-labeledby role style');
    };
    var addCompactModeEvents = function () {
        nav.on('click.submenu', 'h2', function (event) {
            event.preventDefault();
            var div = $(event.target).next('div');
            $(event.target).attr('aria-expanded', div.is(':hidden'));
            div.toggle();
        });
        nav.on('keydown.submenu', function (event) {
            var which = event.which;
            var target = $(event.target);
            // search
            if (target.is('input')) {
                return true;
            }
            // enter or space
            if (which === 13 || which === 32) {
                event.preventDefault();
                target.trigger('click');
            }
            // up or left
            if (which === 37 || which === 38) {
                event.preventDefault();
                headlines.each(function (i) {
                    if (i > 0 && $(this).attr('tabindex') === 0) {
                        $(this).attr('tabindex', negativeTabIndex);
                        $(headlines[i - 1]).attr('tabindex', 0).focus();
                        return false;
                    }
                });
            }
            // down or right
            if (which === 40 || which === 39) {
                event.preventDefault();
                headlines.each(function (i) {
                    if (i < (headlines.length - 1) && $(this).attr('tabindex') === 0) {
                        $(this).attr('tabindex', negativeTabIndex);
                        $(headlines[i + 1]).attr('tabindex', 0).focus();
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
        nav.off('.submenu');
    };
    Tabzilla.open = function () {
        opened = true;
        panel.toggleClass('open');
        var height = $('#tabzilla-contents').height();
        panel.animate({'height': height}, 200, function () {
            panel.css('height', 'auto');
        });
        tab
            .attr({'aria-expanded' : 'true'})
            .addClass('tabzilla-opened')
            .removeClass('tabzilla-closed');

        panel.focus();

        if (typeof(_gaq) == 'object') {
            window._gaq.push(['_trackEvent', 'Tabzilla', 'click', 'Open Tabzilla']);
        }

        return panel;
    };
    Tabzilla.close = function () {
        opened = false;
        panel.animate({height: 0}, 200, function () {
            panel.toggleClass('open');
        });

        tab
            .attr({'aria-expanded' : 'false'})
            .addClass('tabzilla-closed')
            .removeClass('tabzilla-opened');

        if (typeof(_gaq) == 'object') {
            window._gaq.push(['_trackEvent', 'Tabzilla', 'click', 'Close Tabzilla']);
        }

        return tab;
    };
    Tabzilla.compareVersion = function (a, b) {
        var num1, num2;
        a = ('' + a).split('.');
        b = ('' + b).split('.');
        while (a.length < b.length) { a.push('0'); }
        while (b.length < a.length) { b.push('0'); }
        for (var i = 0; i < a.length; i++) {
            num1 = parseInt(a[i], 10);
            num2 = parseInt(b[i], 10);
            if (num1 > num2) { return 1; }
            if (num1 < num2) { return -1; }
        }
        return 0;
    };
    var Infobar = function (id, name) {
        this.id = id;
        this.name = name;
        this.disabled = false;
        this.prefName = 'tabzilla.infobar.' + id + '.disabled';

        // Read the preference
        try {
            if (sessionStorage.getItem(this.prefName) === 'true') {
                this.disabled = true;
            }
        } catch (ex) {}

        // If there is already another infobar, don't show this
        if ($('#tabzilla-infobar').length) {
            this.disabled = true;
        }
    };
    Infobar.prototype.show = function (str) {
        // A infobar can be disabled by pref.
        // And check the existence of another infobar again
        if (this.disabled || $('#tabzilla-infobar').length) {
            return;
        }

        var self = this;
        var bar = self.element = $(
          '<div id="tabzilla-infobar" class="' + self.id + '" role="dialog"><div>'
        + '<p>' + str.message + '</p><ul>'
        + '<li><button class="btn-accept" type="button">' + str.accept + '</button></li>'
        + '<li><button class="btn-cancel" type="button">' + str.cancel + '</button></li>'
        + '</ul></div></div>').prependTo(panel);

        bar.find('.btn-accept').click(function (event) {
            event.preventDefault();
            self.trackEvent(self.onaccept.trackAction || 'accept',
                            self.onaccept.trackLabel,
                            undefined,
                            self.onaccept.callback);
            self.hide();
        });

        bar.find('.btn-cancel').click(function (event) {
            event.preventDefault();
            self.trackEvent(self.oncancel.trackAction || 'cancel',
                            self.oncancel.trackLabel,
                            undefined,
                            self.oncancel.callback);
            self.hide();
            try {
                sessionStorage.setItem(self.prefName, 'true');
            } catch (ex) {}
        });

        panel.trigger('infobar-showing');
        self.trackEvent(self.onshow.trackAction || 'show',
                        self.onshow.trackLabel,
                        true,
                        self.onshow.callback);

        if (opened) {
            bar.css('height', 0)
               .animate({'height': bar.find('div').outerHeight()}, 200,
                        function () { panel.trigger('infobar-shown'); });
        } else {
            panel.animate({'height': bar.height()}, 200,
                          function () { panel.trigger('infobar-shown'); });
        }

        return bar;
    };
    Infobar.prototype.hide = function () {
        var self = this;
        var target = (opened) ? self.element : panel;

        panel.trigger('infobar-hiding');

        target.animate({'height': 0}, 200, function () {
            self.element.remove();
            panel.trigger('infobar-hidden');
        });
    };
    Infobar.prototype.trackEvent = function (action, label, value, callback) {
        if (typeof(_gaq) !== 'object') {
            return;
        }

        var cmd = ['_trackEvent', 'Tabzilla - ' + this.name, action, label];

        // The optional value will be used to detect if the event is a real
        // user interaction. Set true for a non-interaction event.
        if (value !== undefined) {
            cmd.push(value);
        }

        window._gaq.push(cmd);

        if (callback) {
            var timer = null;
            var _callback = function () {
                clearTimeout(timer);
                callback();
            };
            timer = setTimeout(_callback, 500);
            window._gaq.push(_callback);
        }
    };
    Infobar.prototype.onshow = {};
    Infobar.prototype.onaccept = {};
    Infobar.prototype.oncancel = {};
    Tabzilla.setupTransbar = function (userLang, pageLang) {
        var transbar = new Infobar('transbar', 'Translation Bar');
        userLang = userLang || navigator.language || navigator.browserLanguage;
        pageLang = pageLang || document.documentElement.lang;

        if (transbar.disabled || !userLang || !pageLang) {
            return false;
        }

        var userLangLower = userLang.toLowerCase();
        var userLangShort = userLangLower.split('-')[0];
        var pageLangLower = pageLang.toLowerCase();

        // Compare the user's language and the page's language
        if (userLangLower === pageLangLower ||
                // Consider some legacy locales like fr-FR, it-IT or el-GR
                userLangShort === pageLangLower) {
            return false;
        }

        // Normalize the user language in the form of ab or ab-CD
        userLang = userLang.replace(/^(\w+)(?:-(\w+))?$/, function (m, p1, p2) {
            return p1.toLowerCase() + ((p2) ? '-' + p2.toUpperCase() : '');
        });

        // Check the availability of the translated page for the user.
        // Use an alternate URL in <head> or a language option in <form>
        var langLink = $([
            'link[hreflang="' + userLang + '"]',
            // The user language can be ab-CD while the page language is ab
            // (Example: fr-FR vs fr, ja-JP vs ja)
            'link[hreflang="' + userLangShort + '"]'
            ].join(','));
        var langOption = $([
            '#language [value="' + userLang + '"]',
            // Languages in the language switcher are uncapitalized on some
            // sites (AMO, Firefox Flicks)
            '#language [value="' + userLangLower + '"]',
            // The user language can be ab-CD while the page language is ab
            // (Example: fr-FR vs fr, ja-JP vs ja)
            '#language [value="' + userLangShort + '"]',
            // Sometimes the value of a language switcher option is the path of
            // a localized page on some sites (MDN)
            '#language [value^="/' + userLang + '/"]',
            '#language [value^="/' + userLangShort + '/"]'
            ].join(','));

        if (!langLink.length && !langOption.length) {
            return false;
        }

        // Normalize the user language again, based on the language of the site
        userLang = (langLink.length) ? langLink.attr('hreflang')
                                     : langOption.val();

        // Log the language of the current page
        transbar.onshow.trackLabel = transbar.oncancel.trackLabel = userLang;
        transbar.oncancel.trackAction = 'hide';

        // If the user selects Yes, show the translated page
        transbar.onaccept = {
            trackAction: 'change',
            trackLabel: userLang,
            callback: function () {
                if (langLink.length) {
                    location.href = langLink.attr('href');
                } else {
                    langOption.attr('selected', 'selected').get(0).form.submit();
                }
            }
        };

        // Fetch the localized strings and show the Translation Bar
        $.ajax({ url: '{{ settings.CDN_BASE_URL }}/' + userLang + '/tabzilla/transbar.jsonp',
                 cache: true, crossDomain: true, dataType: 'jsonp',
                 jsonpCallback: "_", success: function (str) {
            transbar.show(str).attr('lang', userLang);
        }});

        return true;
    };
    var setupGATracking = function () {
        // track tabzilla links in GA
        $('#tabzilla-contents').on('click', 'a', function (e) {
            var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
            var href = this.href;
            var timer = null;
            var callback = function () {
                clearTimeout(timer);
                window.location = href;
            };

            if (typeof(_gaq) == 'object') {
                if (newTab) {
                    window._gaq.push(['_trackEvent', 'Tabzilla', 'click', href]);
                } else {
                    e.preventDefault();
                    timer = setTimeout(callback, 500);
                    window._gaq.push(['_trackEvent', 'Tabzilla', 'click', href], callback);
                }
            }
        });
        // track search keywords in GA
        $('#tabzilla-search form').on('submit', function (e) {
            e.preventDefault();

            var $form = $(this);
            var keyword = $form.find('#q').val();
            var timer = null;
            var callback = function () {
                clearTimeout(timer);
                $form.submit();
            };

            $form.unbind('submit');

            if (typeof(_gaq) == 'object' && keyword !== '') {
                timer = setTimeout(callback, 500);
                window._gaq.push(['_trackEvent', 'Tabzilla', 'search', keyword], callback);
            } else {
                $form.submit();
            }
        });
    };
    var addEaseInOut = function () {
        $.extend($.easing, {
            'easeInOut':  function (x, t, b, c, d) {
                if (( t /= d / 2) < 1) {
                    return c / 2 * t * t + b;
                }
                return -c / 2 * ((--t) * (t - 2) - 1) + b;
            }
        });
    };
    var addMatchMediaPolyfill = function () {
        window.matchMedia = window.matchMedia || (function( doc, undefined ) {
            var bool;
            var docElem = doc.documentElement;
            var refNode = docElem.firstElementChild || docElem.firstChild;
            // fakeBody required for <FF4 when executed in <head>
            var fakeBody = doc.createElement( "body" );
            var div = doc.createElement( "div" );

            div.id = "mq-test-1";
            div.style.cssText = "position:absolute;top:-100em";
            fakeBody.style.background = "none";
            fakeBody.appendChild(div);

            return function(q){
                div.innerHTML = "&shy;<style media=\"" + q + "\"> #mq-test-1 { width: 42px; }</style>";
                docElem.insertBefore( fakeBody, refNode );
                bool = div.offsetWidth === 42;
                docElem.removeChild( fakeBody );
                return {
                    matches: bool,
                    media: q
                };
            };
        }( document ));
    };
    var init = function () {
        $('body').prepend(content);
        tab = $('#tabzilla');
        panel = $('#tabzilla-panel');
        nav = $('#tabzilla-nav');
        headlines = nav.find('h2');

        if (isIE9 && !hasMediaQueries) {
            addMatchMediaPolyfill();
            hasMediaQueries = true;
        }

        addEaseInOut();

        checkMode();
        $(window).on('resize', function () {
            checkMode();
        });

        panel.on('keydown', function (event) {
            if (event.which === 27) {
                event.preventDefault();
                Tabzilla.close();
            }
        });

        tab.attr('aria-label', '{{ _('Mozilla links')|js_escape }}');

        tab.on('click', function (event) {
            event.preventDefault();
            if (opened) {
                Tabzilla.close();
            } else {
                Tabzilla.open();
            }
        });

        // Information Bars in order of priority
        var infobars = {
            translation: Tabzilla.setupTransbar
        };
        $.each((tab.data('infobar') || '').split(' '), function (index, value) {
            var setup = infobars[value];
            if (setup) {
                setup.call();
            }
        });

        setupGATracking();

        // Careers teaser in error console.
        $(window).load(function() {
            try {
                // Try to only show on stage and production environments.
                if (/mozill|webmaker|allizom|firefox/.exec(location.hostname)) {
                    console.log("{% filter js_escape|safe %}{% include "includes/careers-teaser.html" %}{% endfilter %}");
                }
            } catch(e) {}
        });
    };
    var loadJQuery = function (callback) {
        var noConflictCallback = function() {
            // set non-conflicting version local aliases
            jQuery = window.jQuery.noConflict(true);
            $ = jQuery;
            callback.call();
        };
        var script = document.createElement("script");
        if (script.readyState) {
            script.onreadystatechange = function () {
                if (script.readyState === "loaded" || script.readyState === "complete") {
                    script.onreadystatechange = null;
                    noConflictCallback.call();
                }
            };
        } else {
            script.onload = noConflictCallback;
        }
        script.src = '//mozorg.cdn.mozilla.net/media/js/libs/jquery-' + minimumJQuery + '.min.js';
        document.getElementsByTagName('head')[0].appendChild(script);
    };
    // icn=tabz appended to links for Google Analytics purposes
    var content =
      '<div id="tabzilla-panel" class="tabzilla-closed" tabindex="-1">'
    + '  <div id="tabzilla-contents">'
    + '    <div id="tabzilla-promo">'
    +'      <div class="snippet" id="tabzilla-promo-fxos">'
    + '        <a href="https://www.mozilla.org/firefox/os/?icn=tabz">'
    + '          <h4>{{ _('Look ahead')|js_escape }}</h4>'
    + '          <p>{{ _('Learn all about Firefox OS')|js_escape }} »</p>'
    + '        </a>'
    + '      </div>'
    + '    </div>'
    + '    <div id="tabzilla-nav">'
    + '      <ul>'
    + '        <li><h2>Mozilla</h2>'
    + '          <div>'
    + '            <ul>'
    + '              <li><a href="https://www.mozilla.org/mission/?icn=tabz">{{ _('Mission')|js_escape }}</a></li>'
    + '              <li><a href="https://www.mozilla.org/about/?icn=tabz">{{ _('About')|js_escape }}</a></li>'
    + '              <li><a href="https://www.mozilla.org/projects/?icn=tabz">{{ _('Projects')|js_escape }}</a></li>'
    + '              <li><a href="https://support.mozilla.org/?icn=tabz">{{ _('Support')|js_escape }}</a></li>'
    + '              <li><a href="https://developer.mozilla.org/?icn=tabz">{{ _('Developer Network')|js_escape }}</a></li>'
    + '            </ul>'
    + '          </div>'
    + '        </li>'
    + '        <li><h2>{{ _('Products')|js_escape }}</h2>'
    + '          <div>'
    + '            <ul>'
    + '              <li><a href="https://www.mozilla.org/firefox/?icn=tabz">Firefox</a></li>'
    + '              <li><a href="https://www.mozilla.org/thunderbird/?icn=tabz">Thunderbird</a></li>'
    + '              <li><a href="https://www.mozilla.org/firefox/os/?icn=tabz">Firefox OS</a></li>'
    + '            </ul>'
    + '          </div>'
    + '        </li>'
    + '        <li><h2>{{ _('Innovations')|js_escape }}</h2>'
    + '          <div>'
    + '            <ul>'
    + '              <li><a href="https://webfwd.org/?icn=tabz">WebFWD</a></li>'
    + '              <li><a href="https://mozillalabs.com/?icn=tabz">Labs</a></li>'
    + '              <li><a href="https://webmaker.org/?icn=tabz">Webmaker</a></li>'
    + '              <li><a href="https://www.mozilla.org/research/?icn=tabz">Research</a></li>'
    + '            </ul>'
    + '          </div>'
    + '        </li>'
    + '        <li><h2>{{ _('Get Involved')|js_escape }}</h2>'
    + '          <div>'
    + '            <ul>'
    + '              <li><a href="https://www.mozilla.org/contribute/?icn=tabz">{{ _('Volunteer')|js_escape }}</a></li>'
    + '              <li><a href="https://www.mozilla.org/en-US/about/careers.html?icn=tabz">{{ _('Careers')|js_escape }}</a></li>'
    + '              <li><a href="https://www.mozilla.org/en-US/about/mozilla-spaces/?icn=tabz">{{ _('Find us')|js_escape }}</a></li>'
    + '              <li><a href="{{ donate_url() }}?icn=tabz&amp;source=tabzilla_donate&amp;amount=20" class="donate">{{ _('Donate')|js_escape }}</a></li>'
    + '              <li><a href="https://www.mozilla.org/about/partnerships/?icn=tabz">{{ _('Partner')|js_escape }}</a></li>'
    + '            </ul>'
    + '          </div>'
    + '        </li>'
    + '        <li id="tabzilla-search">'
    + '          <a href="https://www.mozilla.org/community/directory.html?icn=tabz">{{ _('Website Directory')|js_escape }}</a>'
    + '          <form title="{{ _('Search Mozilla sites')|js_escape }}" role="search" action="https://www.google.com/cse">'
    + '            <input type="hidden" value="002443141534113389537:ysdmevkkknw" name="cx">'
    + '            <input type="hidden" value="FORID:0" name="cof">'
    + '            <label for="q">{{ _('Search')|js_escape }}</label>'
    + '            <input type="search" placeholder="{{ _('Search')|js_escape }}" id="q" name="q">'
    + '          </form>'
    + '        </li>'
    + '      </ul>'
    + '    </div>'
    + '  </div>';
    + '</div>';

    // Self-executing function must be after all vars have been initialized
    (function () {
        if (window.jQuery !== undefined &&
            Tabzilla.compareVersion(window.jQuery.fn.jquery, minimumJQuery) !== -1
        ) {
            // set up local jQuery aliases
            jQuery = window.jQuery;
            $ = jQuery;
            $(document).ready(init);
        } else {
            // no jQuery or older than minimum required jQuery
            loadJQuery(init);
        }
    })();

    return Tabzilla;

})(Tabzilla || {});
