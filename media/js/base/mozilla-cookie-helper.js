/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/*\
|*|
|*|  :: cookies.js ::
|*|
|*|  A complete cookies reader/writer framework with full unicode support.
|*|
|*|  Revision #1 - September 4, 2014
|*|
|*|  https://developer.mozilla.org/en-US/docs/Web/API/document.cookie
|*|  https://developer.mozilla.org/User:fusionchess
|*|
|*|  This framework is released under the GNU Public License, version 3 or later.
|*|  http://www.gnu.org/licenses/gpl-3.0-standalone.html
|*|
|*|  Syntaxes:
|*|
|*|  * Mozilla.Cookies.setItem(name, value[, end[, path[, domain[, secure[, samesite]]]]])
|*|  * Mozilla.Cookies.getItem(name)
|*|  * Mozilla.Cookies.removeItem(name[, path[, domain]])
|*|  * Mozilla.Cookies.hasItem(name)
|*|  * Mozilla.Cookies.keys()
|*|
\*/

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.Cookies = {
    getItem: function (sKey) {
        'use strict';
        if (!sKey) {
            return null;
        }
        return (
            decodeURIComponent(
                document.cookie.replace(
                    new RegExp(
                        '(?:(?:^|.*;)\\s*' +
                            encodeURIComponent(sKey).replace(
                                /[-.+*]/g,
                                '\\$&'
                            ) +
                            '\\s*\\=\\s*([^;]*).*$)|^.*$'
                    ),
                    '$1'
                )
            ) || null
        );
    },
    setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure, vSamesite) {
        'use strict';
        if (
            !sKey ||
            /^(?:expires|max-age|path|domain|secure|samesite)$/i.test(sKey)
        ) {
            return false;
        }
        var sExpires = '';
        if (vEnd) {
            switch (vEnd.constructor) {
                case Number:
                    sExpires =
                        vEnd === Infinity
                            ? '; expires=Fri, 31 Dec 9999 23:59:59 GMT'
                            : '; max-age=' + vEnd;
                    break;
                case String:
                    sExpires = '; expires=' + vEnd;
                    break;
                case Date:
                    sExpires = '; expires=' + vEnd.toUTCString();
                    break;
            }
        }

        vSamesite = this.checkSameSite(vSamesite);

        // setting the samesite attribute to 'none' requires the cookie to be 'secure'
        if (vSamesite === 'none') {
            bSecure = true;
        }
        document.cookie =
            encodeURIComponent(sKey) +
            '=' +
            encodeURIComponent(sValue) +
            sExpires +
            (sDomain ? '; domain=' + sDomain : '') +
            (sPath ? '; path=' + sPath : '') +
            (bSecure ? '; secure' : '') +
            (!vSamesite ? '' : '; samesite=' + vSamesite);
        return true;
    },
    removeItem: function (sKey, sPath, sDomain) {
        'use strict';
        if (!this.hasItem(sKey)) {
            return false;
        }
        document.cookie =
            encodeURIComponent(sKey) +
            '=; expires=Thu, 01 Jan 1970 00:00:00 GMT' +
            (sDomain ? '; domain=' + sDomain : '') +
            (sPath ? '; path=' + sPath : '');
        return true;
    },
    hasItem: function (sKey) {
        'use strict';
        if (!sKey) {
            return false;
        }
        return new RegExp(
            '(?:^|;\\s*)' +
                encodeURIComponent(sKey).replace(/[-.+*]/g, '\\$&') +
                '\\s*\\='
        ).test(document.cookie);
    },
    keys: function () {
        'use strict';
        var aKeys = document.cookie
            .replace(
                // see issue 11338.
                // eslint-disable-next-line no-useless-backreference
                /((?:^|\s*;)[^=]+)(?=;|$)|^\s*|\s*(?:=[^;]*)?(?:\1|$)/g,
                ''
            )
            .split(/\s*(?:=[^;]*)?;\s*/);
        for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) {
            aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]);
        }
        return aKeys;
    },
    enabled: function () {
        'use strict';
        /**
         * Cookies feature detect lifted from Modernizr
         * https://github.com/Modernizr/Modernizr/blob/master/feature-detects/cookies.js
         *
         * navigator.cookieEnabled cannot detect custom or nuanced cookie blocking
         * configurations. For example, when blocking cookies via the Advanced
         * Privacy Settings in IE9, it always returns true. And there have been
         * issues in the past with site-specific exceptions.
         * Don't rely on it.

         * try..catch because in some situations `document.cookie` is exposed but throws a
         * SecurityError if you try to access it; e.g. documents created from data URIs
         * or in sandboxed iframes (depending on flags/context)
         */
        try {
            // Create cookie
            document.cookie = 'cookietest=1; SameSite=Lax';
            var ret = document.cookie.indexOf('cookietest=') !== -1;
            // Delete cookie
            document.cookie =
                'cookietest=1; SameSite=Lax; expires=Thu, 01-Jan-1970 00:00:01 GMT';
            return ret;
        } catch (e) {
            return false;
        }
    },

    checkSameSite: function (vSamesite) {
        'use strict';
        /**
         *  valid vSamesite values are 'lax', 'strict' and 'none' (case insensitive).
         *  otherwise it will be 'lax'
         */

        if (!vSamesite) {
            return null;
        }
        vSamesite = vSamesite.toString().toLowerCase();

        if (
            vSamesite === 'lax' ||
            vSamesite === 'none' ||
            vSamesite === 'strict'
        ) {
            return vSamesite;
        } else {
            return 'lax';
        }
    }
};
