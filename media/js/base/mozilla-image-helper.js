/**
 * Utility class for high-resolution detection and display and also platform
 * images
 *
 * This code is licensed under the Mozilla Public License 1.1.
 *
 * @copyright 2013 Mozilla Foundation
 * @license   http://www.mozilla.org/MPL/MPL-1.1.html Mozilla Public License 1.1
 * @author    Nick Burka <nick@silverorange.com>
 */

$(document).ready(function() {
    Mozilla.ImageHelper.initPlatformImages();
    Mozilla.ImageHelper.initHighResImages();
});

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

// {{{ Mozilla.ImageHelper

/**
 * ImageHelper object
 */
Mozilla.ImageHelper = function() {
};

Mozilla.ImageHelper.is_high_dpi = null;

// }}}

// Platform Images
// {{{ initPlatformImages()

Mozilla.ImageHelper.initPlatformImages = function() {
    $('.platform-img').each(function() {
        var $img = $(this);
        var suffix = '';
        var platforms;
        var additional_platforms;

        // special handling for mac
        if (site.platform === 'osx' || site.platform === 'oldmac') {
            suffix = '-mac';
        } else {
            platforms = ['linux']; // linux is supported by default

            // use 'data-additional-platforms' to specify other supported platforms
            // beyond the defaults
            if ($img.data('additional-platforms')) {
                additional_platforms = $img.data('additional-platforms').split(' ');
                platforms = platforms.concat(additional_platforms);
            }

            if ($.inArray(site.platform, platforms) > -1) {
                suffix = '-' + site.platform;
            }
        }

        var orig_src = $img.data('src');
        var i = orig_src.lastIndexOf('.');
        var base = orig_src.substring(0, i);
        var ext = orig_src.substring(i);
        var src = base + suffix + ext;

        if ($img.data('high-res') && Mozilla.ImageHelper.isHighDpi()) {
            src = Mozilla.ImageHelper.convertUrlToHighRes(src);
        }

        this.src = src;

        $img.addClass(site.platform);
    });
};

// }}}

// High Resolution Images
// {{{ initHighResImages()

Mozilla.ImageHelper.initHighResImages = function() {
    $('img[data-src][data-high-res="true"]').each(function() {
        var src = $(this).data('src');
        if (Mozilla.ImageHelper.isHighDpi()) {
            src = Mozilla.ImageHelper.convertUrlToHighRes(src);
        }
        this.src = src;
    });
};

// }}}
// {{{ isHighDpi()

Mozilla.ImageHelper.isHighDpi = function() {
    if (Mozilla.ImageHelper.is_high_dpi === null) {
        var media_query = '(-webkit-min-device-pixel-ratio: 1.5),' +
                          '(-o-min-device-pixel-ratio: 3/2),' +
                          '(min--moz-device-pixel-ratio: 1.5),' +
                          '(min-resolution: 1.5dppx)';

        Mozilla.ImageHelper.is_high_dpi = (window.devicePixelRatio > 1 ||
               (window.matchMedia && window.matchMedia(media_query).matches));
    }

    return Mozilla.ImageHelper.is_high_dpi;
};

// }}}
// {{{ convertUrlToHighRes()

Mozilla.ImageHelper.convertUrlToHighRes = function(url) {
    var i = url.lastIndexOf('.');
    var base = url.substring(0, i);
    var ext = url.substring(i);
    return base + '-high-res' + ext;
};

// }}}
