/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

// Activate GA event tracking on download buttons
function init_download_links() {
    'use strict';

    var channels = {
        'release': 'Firefox',
        'beta': 'Firefox Beta',
        'aurora': 'Firefox Aurora',
        'nightly': 'Firefox Nightly',
        'esr': 'Firefox ESR'
    };
    var ancillaryLinks = {
        'all': 'Systems & Languages',
        'devices': 'Supported Devices',
        'notes': 'What’s New',
        'privacy': 'Privacy Policy'
    };

    $('.download-button').on('click', 'a', function(event) {
        var isDownloadLink = $(this).hasClass('download-link') ||
                             $(this).hasClass('button-green');
        var cmd = ['_trackEvent'];
        var newTab = (this.target === '_blank' || event.metaKey || event.ctrlKey);

        if (isDownloadLink) {
            var direct_link = $(this).data('direct-link');
            var url = (window.site.isIE && direct_link) ? direct_link : this.href;
            var product_name = channels[$(this).data('channel')];

            if ($(this).parent().hasClass('os_android')) {
                product_name += ' for Android';
            }

            cmd.push('Firefox Downloads', 'click', product_name);
            track_download_link(event, cmd, url);
        } else {
            cmd.push('Firefox Links Under DL Button', 'click',
                     ancillaryLinks[$(this).data('type')]);

            if (newTab) {
                gaTrack(cmd);
            } else {
                track_and_redirect(event, cmd, this.href);
            }
        }
    });

    $('#direct-download-link').on('click', function(event) {
        var cmd = [
            '_trackEvent',
            'Firefox Downloads',
            // Detect if the download is triggered manually or automatically
            (event.originalEvent) ? 'click' : 'auto',
            channels[$(this).data('channel')]
        ];

        track_and_redirect(event, cmd, this.href);
    });

    $('.download-list').attr('role', 'presentation');
}

// Replace Google Play links on Android devices to let them open
// the native Play Store app
function init_android_download_links() {
    if (site.platform === 'android') {
        $('a[href^="https://play.google.com/store/apps/"]').each(function() {
            $(this).attr('href', $(this).attr('href')
                .replace('https://play.google.com/store/apps/', 'market://'));
        });
    }
}

// language switcher

function init_lang_switcher() {
    $('#language').change(function(event) {
        event.preventDefault();
        gaTrack(
            ['_trackEvent', 'Language Switcher', 'change', $(this).val()],
            function() {$('#lang_form').submit();}
        );
    });
}

// platform images

function init_platform_imgs() {
    function has_platform(platforms, platform) {
        for (var i = 0; i < platforms.length; i++) {
            if (platforms[i] === platform && site.platform === platform) {
                return true;
            }
        }

        return false;
    }

    $('.platform-img').each(function() {
        var suffix = '';
        var $img = $(this);
        var default_platforms = ['osx', 'oldmac', 'linux'];
        var additional_platforms;
        var platforms = default_platforms;

        // use 'data-additional-platforms' to specify other supported platforms
        // beyond the defaults
        if ($img.data('additional-platforms')) {
            additional_platforms = $img.data('additional-platforms').split(' ');
            platforms = default_platforms.concat(additional_platforms);
        }

        if (has_platform(platforms, 'osx') || has_platform(platforms, 'oldmac')) {
            suffix = '-mac';
        } else if (has_platform(platforms, site.platform)) {
            suffix = '-' + site.platform;
        }

        var orig_src = $img.data('src');
        var i = orig_src.lastIndexOf('.');
        var base = orig_src.substring(0, i);
        var ext = orig_src.substring(i);
        this.src = base + suffix + ext;
        $img.addClass(site.platform);
    });
}

// init

$(document).ready(function() {
    init_download_links();
    init_android_download_links();
    init_lang_switcher();
    $(window).on('load', function () {
        $('html').addClass('loaded');
    });
});

//get Master firefox version
function getFirefoxMasterVersion(userAgent) {
    var version = 0;
    var ua = userAgent || navigator.userAgent;

    var matches = /Firefox\/([0-9]+).[0-9]+(?:.[0-9]+)?/.exec(
        ua
    );

    if (matches !== null && matches.length > 0) {
        version = parseInt(matches[1], 10);
    }

    return version;
}

function isFirefox(userAgent) {
    var ua = userAgent || navigator.userAgent;
    // camino UA string contains 'like Firefox'
    return (
        (/\sFirefox/).test(ua) &&
        !(/like Firefox/i).test(ua) &&
        !(/SeaMonkey/i).test(ua)
    );
}

function isFirefoxUpToDate(latest, esr) {

    var $html = $(document.documentElement);
    var fx_version = getFirefoxMasterVersion();
    var esrFirefoxVersions = esr || $html.data('esr-versions');
    var latestFirefoxVersion;

    if (!latest) {
        latestFirefoxVersion = $html.attr('data-latest-firefox');
        latestFirefoxVersion = parseInt(latestFirefoxVersion.split('.')[0], 10);
    } else {
        latestFirefoxVersion = parseInt(latest.split('.')[0], 10);
    }

    return ($.inArray(fx_version, esrFirefoxVersions) !== -1 ||
            latestFirefoxVersion <= fx_version);
}

function isMobile() {
    return /\sMobile/.test(window.navigator.userAgent);
}

// Create text translation function using #strings element.
// TODO: Move to docs
// In order to use it, you need a block string_data bit inside your template,
// @see https://github.com/mozilla/bedrock/blob/master/apps/firefox/templates/firefox/partners/landing.html#L14
// then, each key name needs to be preceeded by data- as this uses data attributes
// to work. After this, you can access all strings defined inside the
// string_data block in JS using window.trans('keyofstring'); Thank @mkelly
var $strings = $('#strings');
window.trans = function trans(stringId) {
    return $strings.data(stringId);
};


function gaTrack(eventArray, callback) {
    // submit eventArray to GA and call callback only after tracking has
    // been sent, or if sending fails.
    //
    // callback is optional.
    //
    // Example usage:
    //
    // $(function() {
    //      var handler = function(e) {
    //           var _this = this;
    //           e.preventDefault();
    //           $(_this).off('submit', handler);
    //           gaTrack(
    //              ['_trackEvent', 'Newsletter Registration', 'submit', newsletter],
    //              function() {$(_this).submit();}
    //           );
    //      };
    //      $(thing).on('submit', handler);
    // });

    var timer = null;
    var hasCallback = typeof(callback) === 'function';
    var gaCallback;

    // Only build new function if callback exists.
    if (hasCallback) {
        gaCallback = function() {
            clearTimeout(timer);
            callback();
        };
    }
    if (typeof(window._gaq) === 'object') {
        // send event to GA
        window._gaq.push(eventArray);
        // Only set up timer and hitCallback if a callback exists.
        if (hasCallback) {
            // Failsafe - be sure we do the callback in a half-second
            // even if GA isn't able to send in our trackEvent.
            timer = setTimeout(gaCallback, 500);

            // But ordinarily, we get GA to call us back immediately after
            // it finishes sending our things.
            // https://developers.google.com/analytics/devguides/collection/gajs/#PushingFunctions
            // This is called after GA has sent the current pending data:
            window._gaq.push(gaCallback);
        }
    } else {
        // GA disabled or blocked or something, make sure we still
        // call the caller's callback:
        if (hasCallback) {
            callback();
        }
    }
}

// Track a download link. IEs need a popup as explained below. This function may
// be overridden in some cases, e.g. /firefox/new/
function track_download_link(event, cmd, url) {
    if (window.site.isIE) {
        track_and_popup(event, cmd, url);
        window.focus();
    } else {
        track_and_redirect(event, cmd, url);
    }
}

// We must use a popup to trigger download for IE as the delay sending the page
// view tracking in track_and_redirect() triggers the IE security blocker. Sigh.
function track_and_popup(event, cmd, url) {
    // Popup must go before tracking to prevent timeouts that
    // cause the security blocker.
    window.open(url, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
    gaTrack(cmd);
}

// An iframe can not be used here to trigger the download because it will be
// blocked by Chrome if the download link redirects to a HTTP URI and we are on
// HTTPS.
function track_and_redirect(event, cmd, url) {
    event.preventDefault();
    gaTrack(cmd, function() { window.location = url; });
}
