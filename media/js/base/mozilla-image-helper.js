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
        var data_attribute = 'src-';
        var is_high_res = $img.data('high-res') && Mozilla.ImageHelper.isHighDpi();
        var suffix;
        var new_src;

        if (site.platform == 'oldwin') {
            data_attribute += 'windows';
        }
        else if (site.platform === 'osx' || site.platform === 'oldmac') {
            data_attribute += 'mac';
        }
        else {
            data_attribute += site.platform;
        }

        if (is_high_res) {
            suffix = '-high-res';
        }
        else {
            suffix = '';
        }

        new_src = $img.data(data_attribute + suffix);
        if (!new_src) {
            // fall back to windows
            new_src = $img.data('src-windows' + suffix);
        }

        this.src = new_src;
        $img.attr('data-processed', 'true');
        $img.addClass(site.platform);
    });
};

// }}}

// High Resolution Images
// {{{ initHighResImages()

Mozilla.ImageHelper.initHighResImages = function() {
    $('img[data-src][data-high-res="true"][data-processed="false"]').each(function() {
        var $img = $(this);
        var src = $img.data('src');
        if (Mozilla.ImageHelper.isHighDpi()) {
            src = $img.data('high-res-src');
        }
        this.src = src;
        $img.attr('data-processed', 'true');
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
