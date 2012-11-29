/* vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4: */

/**
 * Tabzilla global navigation for Mozilla projects
 *
 * This code is licensed under the Mozilla Public License 1.1.
 *
 * Event handling portions adapted from the YUI Event component used under
 * the following license:
 *
 *   Copyright © 2012 Yahoo! Inc. All rights reserved.
 *
 *   Redistribution and use of this software in source and binary forms,
 *   with or without modification, are permitted provided that the following conditions
 *   are met:
 *
 *   - Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   - Neither the name of Yahoo! Inc. nor the names of YUI's contributors may
 *     be used to endorse or promote products derived from this software
 *     without specific prior written permission of Yahoo! Inc.
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
 *
 * @copyright 2012 silverorange Inc.
 * @license   http://www.mozilla.org/MPL/MPL-1.1.html Mozilla Public License 1.1
 * @author    Michael Gauthier <mike@silverorange.com>
 * @author    Steven Garrity <steven@silverorange.com>
 */

function Tabzilla()
{
    if (typeof jQuery != 'undefined' && jQuery) {
        jQuery(document).ready(Tabzilla.init);
    } else {
        Tabzilla.run();
    }
}

Tabzilla.READY_POLL_INTERVAL = 40;
Tabzilla.readyInterval = null;
Tabzilla.jQueryCDNSrc =
    '//www.mozilla.org/media/js/libs/jquery-1.7.1.min.js';

Tabzilla.LINK_TITLE = {
    CLOSED: '{{ _('Mozilla links')|js_escape }}',
    OPENED: '{{ _('Close (Esc)')|js_escape }}'
}

/**
 * Whether or not Tabzilla is in small mode
 *
 * @var Boolean
 */
Tabzilla.smallMode = false;

/**
 * Whether or not min/max width media queries are supported in CSS
 *
 * If not supported, the small mode is never triggered.
 *
 * @var Boolean
 */
Tabzilla.hasMediaQueryWidths = (function(){
    return !(/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
})();

/**
 * Sets up the DOMReady event for Tabzilla
 *
 * Adapted from the YUI Event component. Defined in Tabzilla so we do not
 * depend on YUI or jQuery. The YUI DOMReady implementation is based on work
 * Dean Edwards, John Resig, Matthias Miller and Diego Perini.
 */
Tabzilla.run = function()
{
    var webkit = 0, isIE = false, ua = navigator.userAgent;
    var m = ua.match(/AppleWebKit\/([^\s]*)/);

    if (m && m[1]) {
        webkit = parseInt(m[1], 10);
    } else {
        m = ua.match(/Opera[\s\/]([^\s]*)/);
        if (!m || !m[1]) {
            m = ua.match(/MSIE\s([^;]*)/);
            if (m && m[1]) {
                isIE = true;
            }
        }
    }

    // Internet Explorer: use the readyState of a defered script.
    // This isolates what appears to be a safe moment to manipulate
    // the DOM prior to when the document's readyState suggests
    // it is safe to do so.
    if (isIE) {
        if (self !== self.top) {
            document.onreadystatechange = function() {
                if (document.readyState == 'complete') {
                    document.onreadystatechange = null;
                    Tabzilla.ready();
                }
            };
        } else {
            var n = document.createElement('p');
            Tabzilla.readyInterval = setInterval(function() {
                try {
                    // throws an error if doc is not ready
                    n.doScroll('left');
                    clearInterval(Tabzilla.readyInterval);
                    Tabzilla.readyInterval = null;
                    Tabzilla.ready();
                    n = null;
                } catch (ex) {
                }
            }, Tabzilla.READY_POLL_INTERVAL);
        }

    // The document's readyState in Safari currently will
    // change to loaded/complete before images are loaded.
    } else if (webkit && webkit < 525) {
        Tabzilla.readyInterval = setInterval(function() {
            var rs = document.readyState;
            if ('loaded' == rs || 'complete' == rs) {
                clearInterval(Tabzilla.readyInterval);
                Tabzilla.readyInterval = null;
                Tabzilla.ready();
            }
        }, Tabzilla.READY_POLL_INTERVAL);

    // FireFox and Opera: These browsers provide a event for this
    // moment.  The latest WebKit releases now support this event.
    } else {
        Tabzilla.addEventListener(document, 'DOMContentLoaded', Tabzilla.ready);
    }
};

Tabzilla.ready = function()
{
    if (!Tabzilla.DOMReady) {
        Tabzilla.DOMReady = true;

        var onLoad = function() {
            Tabzilla.init();
            Tabzilla.removeEventListener(
                document,
                'DOMContentLoaded',
                Tabzilla.ready
            );
        };

        // if we don't have jQuery, dynamically load jQuery from CDN
        if (typeof jQuery == 'undefined') {
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = Tabzilla.jQueryCDNSrc;
            document.getElementsByTagName('body')[0].appendChild(script);

            if (script.readyState) {
                // IE
                script.onreadystatechange = function() {
                    if (   script.readyState == 'loaded'
                        || script.readyState == 'complete'
                    ) {
                        onLoad();
                    }
                };
            } else {
                // Others
                script.onload = onLoad;
            }
        } else {
            onLoad();
        }
    }
};

Tabzilla.init = function()
{
    // add easing functions
    jQuery.extend(jQuery.easing, {
        'easeInOut':  function (x, t, b, c, d) {
            if (( t /= d / 2) < 1) {
                return c / 2 * t * t + b;
            }
            return -c / 2 * ((--t) * (t - 2) - 1) + b;
        }
    });

    Tabzilla.link  = document.getElementById('tabzilla');
    Tabzilla.panel = Tabzilla.buildPanel();

    // add panel as first element of body element
    var body = document.getElementsByTagName('body')[0];
    body.insertBefore(Tabzilla.panel, body.firstChild);

    // set up event listeners for link
    Tabzilla.addEventListener(Tabzilla.link, 'click', function(e) {
        Tabzilla.preventDefault(e);
        Tabzilla.toggle();
    });

    Tabzilla.$panel = jQuery(Tabzilla.panel);
    Tabzilla.$link  = jQuery(Tabzilla.link);

    Tabzilla.$panel.addClass('tabzilla-closed');
    Tabzilla.$link.addClass('tabzilla-closed');
    Tabzilla.$panel.removeClass('tabzilla-opened');
    Tabzilla.$link.removeClass('tabzilla-opened');

    // make panel unfocusable
    Tabzilla.$panel.attr('tabindex', '-1');

    Tabzilla.$link.attr({
        'role'          : 'button',
        'aria-expanded' : 'false',
        'aria-controls' : Tabzilla.$panel.attr('id'),
        'title'         : Tabzilla.LINK_TITLE.CLOSED
    });

    Tabzilla.opened = false;

    jQuery(document).keydown(function(e) {
        if (e.which === 27 && Tabzilla.opened) {
            Tabzilla.toggle();
        }
    });
    Tabzilla.$link.keypress(function(e) {
        if (e.which === 32) {
            Tabzilla.toggle();
            Tabzilla.preventDefault(e);
        }
    });
    Tabzilla.$panel.keypress(function(e) {
        if (e.which === 13 && !Tabzilla.smallMode) {
            Tabzilla.toggle();
            Tabzilla.$link.focus();
        }
    });

    if (Tabzilla.hasMediaQueryWidths) {
        jQuery(window).resize(Tabzilla.handleResize);
        Tabzilla.handleResize();
    }
};

Tabzilla.buildPanel = function()
{
    var panel = document.createElement('div');
    panel.id = 'tabzilla-panel';
    panel.innerHTML = Tabzilla.content;
    return panel;
};

Tabzilla.addEventListener = function(el, ev, handler)
{
    if (typeof el.attachEvent != 'undefined') {
        el.attachEvent('on' + ev, handler);
    } else {
        el.addEventListener(ev, handler, false);
    }
};

Tabzilla.removeEventListener = function(el, ev, handler)
{
    if (typeof el.detachEvent != 'undefined') {
        el.detachEvent('on' + ev, handler);
    } else {
        el.removeEventListener(ev, handler, false);
    }
};

Tabzilla.toggle = function()
{
    if (Tabzilla.opened) {
        Tabzilla.close();
    } else {
        Tabzilla.open();
    }
};

Tabzilla.open = function()
{
    if (Tabzilla.opened) {
        return;
    }

    Tabzilla.$panel.toggleClass('open');

    var $content = Tabzilla.$panel.children('#tabzilla-contents');
    var height = $content.height();

    Tabzilla.$panel
        .animate({ 'height' : height }, 200, 'easeInOut', function() {
            Tabzilla.$panel.css('height', 'auto');
        });

    Tabzilla.$link
        .attr({
            'aria-expanded' : 'true',
            'title'         : Tabzilla.LINK_TITLE.OPENED
        })
        .addClass('tabzilla-opened')
        .removeClass('tabzilla-closed');

    Tabzilla.$panel.focus();
    Tabzilla.opened = true;
};

Tabzilla.close = function()
{
    if (!Tabzilla.opened) {
        return;
    }

    // jQuery animation fallback
    Tabzilla.$panel
        .animate({ height: 0 }, 200, 'easeInOut', function() {
            Tabzilla.$panel.toggleClass('open');
        });

    Tabzilla.$link
        .attr({
            'aria-expanded' : 'false',
            'title'         : Tabzilla.LINK_TITLE.CLOSED
        })
        .addClass('tabzilla-closed')
        .removeClass('tabzilla-opened');


    Tabzilla.opened = false;
};

Tabzilla.preventDefault = function(ev)
{
    if (ev.preventDefault) {
        ev.preventDefault();
    } else {
        ev.returnValue = false;
    }
};

Tabzilla.handleResize = function(e)
{
    var width = jQuery(window).width();
    if (width <= 719 && !Tabzilla.smallMode) {
        Tabzilla.enterSmallMode();
    }

    if (width > 719 && Tabzilla.smallMode) {
        Tabzilla.leaveSmallMode();
    }
};

Tabzilla.toggleSmallMode = function()
{
    if (Tabzilla.smallMode) {
        Tabzilla.leaveSmallMode();
    } else {
        Tabzilla.enterSmallMode();
    }
};

Tabzilla.enterSmallMode = function()
{
    // add focusability to menu headers
    jQuery('#tabzilla-nav h2')
        .attr({
            'role'          : 'menuitem',
            'tabindex'      : '0',
            'aria-expanded' : 'false',
            'aria-haspopup' : 'true'
        })
        .each(function(i, e) {
            var $menu = jQuery(e).siblings('ul');
            var $item = jQuery(e);
            Tabzilla.initSubmenu($item, $menu);
            Tabzilla.closeSubmenu($item, $menu);
        });

    Tabzilla.smallMode = true;
};

Tabzilla.leaveSmallMode = function()
{
    // remove focusability from menu headers
    jQuery('#tabzilla-nav h2')
        .removeAttr('role')
        .removeAttr('tabindex')
        .removeAttr('aria-haspopup')
        .removeAttr('aria-expanded')
        .each(function(i, e) {
            var $menu = jQuery(e).siblings('ul');
            var $item = jQuery(e);
            Tabzilla.denitSubmenu($item, $menu);

        });

    Tabzilla.smallMode = false;
};

Tabzilla.initSubmenu = function($item, $menu)
{
    $item.click(function(e) {
        Tabzilla.toggleSubmenu($item, $menu);
    });
    $item.keyup(function(e) {
        if (e.keyCode === 13) {
            Tabzilla.preventDefault(e);
            Tabzilla.toggleSubmenu($item, $menu);
        }
        if (e.keyCode === 39) {
            Tabzilla.preventDefault(e);
            Tabzilla.openSubmenu($item, $menu);
        }
        if (e.keyCode === 37) {
            Tabzilla.preventDefault(e);
            Tabzilla.closeSubmenu($item, $menu);
        }
    });
    $menu.attr('role', 'menu');

    var $items = $menu.find('a');
    $items.attr('role', 'menuitem');
};

Tabzilla.denitSubmenu = function($item, $menu)
{
    $item.unbind('click');
    $menu.removeAttr('role');
    $menu.css('height', 'auto');

    var $items = $menu.find('a');
    $items
        .removeAttr('role')
        .removeAttr('tabindex')
        .unbind('keypress');
};

Tabzilla.toggleSubmenu = function($item, $menu)
{
    if ($item.attr('aria-expanded') === 'true') {
        Tabzilla.closeSubmenu($item, $menu);
    } else {
        Tabzilla.openSubmenu($item, $menu);
    }
};

Tabzilla.openSubmenu = function($item, $menu)
{
    $item.attr('aria-expanded', 'true');

    var $items = $menu.find('a');
    $items.attr('tabindex', '0');

    // get natural menu height
    var height = 0;
    $menu.find('li').each(function(i, e) {
        height += jQuery(e).height() + 1;
    });
    height--;

    $menu
        .css('height', height + 'px')
        .attr('aria-hidden', 'false');
};

Tabzilla.closeSubmenu = function($item, $menu)
{
    $item.attr('aria-expanded', 'false');

    $menu
        .css({
            'overflow' : 'hidden',
            'height'   : '0'
        })
        .attr('aria-hidden', 'true');

    var $items = $menu.find('a');
    $items.attr('tabindex', '-1');
};

Tabzilla.content =
    '<div id="tabzilla-contents">'
    + '  <div id="tabzilla-promo">'
    + '    <div class="snippet" id="tabzilla-promo-mobile">'
    + '    <a href="https://www.mozilla.org/firefox/fx/?WT.mc_id=tzfxmobile&amp;WT.mc_ev=click#mobile">'
    + '     <h4>{{ _('Fast. Smart. Safe.')|js_escape }}</h4>'
    + '     <p>{{ _('Get Firefox for Android')|js_escape }} »</p></a>'
    + '    </div>'
    + '  </div>'
    + '  <div id="tabzilla-nav">'
    + '    <ul>'
    + '      <li><h2>Mozilla</h2>'
    + '        <ul>'
    + '          <li><a href="https://www.mozilla.org/mission/">{{ _('Mission')|js_escape }}</a></li>'
    + '          <li><a href="https://www.mozilla.org/about/">{{ _('About')|js_escape }}</a></li>'
    + '          <li><a href="https://www.mozilla.org/projects/">{{ _('Projects')|js_escape }}</a></li>'
    + '          <li><a href="https://support.mozilla.org/">{{ _('Support')|js_escape }}</a></li>'
    + '          <li><a href="https://developer.mozilla.org">{{ _('Developer Network')|js_escape }}</a></li>'
    + '        </ul>'
    + '      </li>'
    + '      <li><h2>{{ _('Products')|js_escape }}</h2>'
    + '        <ul>'
    + '          <li><a href="https://www.mozilla.org/firefox">Firefox</a></li>'
    + '          <li><a href="https://www.mozilla.org/thunderbird">Thunderbird</a></li>'
    + '          <li><a href="https://www.mozilla.org/firefoxos">Firefox OS</a></li>'
    + '        </ul>'
    + '      </li>'
    + '      <li><h2>{{ _('Innovations')|js_escape }}</h2>'
    + '        <ul>'
    + '          <li><a href="https://webfwd.org/">WebFWD</a></li>'
    + '          <li><a href="https://mozillalabs.com/">Labs</a></li>'
    + '          <li><a href="https://webmaker.org/">Webmaker</a></li>'
    + '        </ul>'
    + '      </li>'
    + '      <li><h2>{{ _('Get Involved')|js_escape }}</h2>'
    + '        <ul>'
    + '          <li><a href="https://www.mozilla.org/contribute/">{{ _('Volunteer')|js_escape }}</a></li>'
    + '          <li><a href="https://www.mozilla.org/en-US/about/careers.html">{{ _('Careers')|js_escape }}</a></li>'
    + '          <li><a href="https://www.mozilla.org/en-US/about/mozilla-spaces/">{{ _('Find us')|js_escape }}</a></li>'
    + '          <li><a href="https://donate.mozilla.org/">{{ _('Join us')|js_escape }}</a></li>'
    + '        </ul>'
    + '      </li>'
    + '      <li id="tabzilla-search">'
    + '        <a href="https://www.mozilla.org/community/directory.html">{{ _('Website Directory')|js_escape }}</a>'
    + '        <form title="{{ _('Search Mozilla sites')|js_escape }}" role="search" action="http://www.google.com/cse">'
    + '          <input type="hidden" value="002443141534113389537:ysdmevkkknw" name="cx">'
    + '          <input type="hidden" value="FORID:0" name="cof">'
    + '          <label for="q">{{ _('Search')|js_escape }}</label>'
    + '          <input type="search" placeholder="{{ _('Search')|js_escape }}" id="q" name="q">'
    + '        </form>'
    + '      </li>'
    + '    </ul>'
    + '  </div>'
    + '</div>';

Tabzilla();
