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
});

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

// {{{ Mozilla.ImageHelper

/**
 * ImageHelper object
 */
Mozilla.ImageHelper = function() {};

// }}}

// Platform Images
// {{{ initPlatformImages()

Mozilla.ImageHelper.initPlatformImages = function() {
    $('.platform-img').each(function() {
        var $img = $(this);
        var data_attribute = 'src-';
        var is_high_res = $img.data('high-res');
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

        new_src = $img.data(data_attribute);

        if (!new_src) {
            // fall back to windows
            data_attribute = 'src-windows';
            new_src = $img.data(data_attribute);
        }

        // if high res requested and path provided, set srcset attribute
        // needs to be set prior to src to avoid downloading standard res image
        // on high-res screens
        if (is_high_res && $img.data(data_attribute + '-high-res')) {
            $img.attr('srcset', $img.data(data_attribute + '-high-res') + ' 1.5x');
        }

        this.src = new_src;

        $img.addClass(site.platform);
    });
};

// }}}
