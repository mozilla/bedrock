/**
 * Utility class for high-resolution detection and display and also platform
 * images
 *
 * This code is licensed under the Mozilla Public License 1.1.
 *
 * @copyright 2013 Mozilla Foundation
 * @license   https://www.mozilla.org/MPL/1.1/ Mozilla Public License 1.1
 * @author    Nick Burka <nick@silverorange.com>
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

// {{{ Mozilla.ImageHelper

/**
 * ImageHelper object
 */
Mozilla.ImageHelper = function() {
    'use strict';
};

Mozilla.ImageHelper._isHighDpi = null;

// }}}

// Platform Images
// {{{ initPlatformImages()

Mozilla.ImageHelper.initPlatformImages = function() {
    'use strict';

    $('.platform-img').each(function() {
        var $img = $(this);
        var dataAttribute = 'src-';
        var isHighRes = $img.data('high-res');
        var newSrc;

        if (site.platform === 'oldwin') {
            dataAttribute += 'windows';
        }
        else if (site.platform === 'osx' || site.platform === 'oldmac') {
            dataAttribute += 'mac';
        }
        else {
            dataAttribute += site.platform;
        }

        newSrc = $img.data(dataAttribute);

        if (!newSrc) {
            // fall back to windows
            dataAttribute = 'src-windows';
            newSrc = $img.data(dataAttribute);
        }

        // if high res requested and path provided, set srcset attribute
        // needs to be set prior to src to avoid downloading standard res image
        // on high-res screens
        if (isHighRes && $img.data(dataAttribute + '-high-res')) {
            $img.attr('srcset', $img.data(dataAttribute + '-high-res') + ' 1.5x');
        }

        this.src = newSrc;

        $img.addClass(site.platform);
    });
};

// }}}
// {{{ isHighDpi()

Mozilla.ImageHelper.isHighDpi = function() {
    'use strict';

    if (Mozilla.ImageHelper._isHighDpi === null) {
        var mediaQuery = '(-webkit-min-device-pixel-ratio: 1.5),' +
                          '(-o-min-device-pixel-ratio: 3/2),' +
                          '(min--moz-device-pixel-ratio: 1.5),' +
                          '(min-resolution: 1.5dppx)';

        Mozilla.ImageHelper._isHighDpi = (window.devicePixelRatio > 1 ||
               (window.matchMedia && window.matchMedia(mediaQuery).matches));
    }

    return Mozilla.ImageHelper._isHighDpi;
};

// }}}

$(document).ready(function() {
    'use strict';

    Mozilla.ImageHelper.initPlatformImages();
});
