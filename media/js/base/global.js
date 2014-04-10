/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

/**
 * A special function for IE.  Without this hack there is no prompt to download after they click.  sigh.
 * bug 393263
 * Note IE has since removed the 'MSIE' token in version 11. The hack is no longer needed for IE11.
 * http://msdn.microsoft.com/en-us/library/ie/bg182625%28v=vs.85%29.aspx#uaString
 * @param string direct link to download URL
 */
function trigger_ie_download(link, appVersion) {
    var version = appVersion || navigator.appVersion;
    // Only open if we got a link and this is IE < 11.
    if (link && version.indexOf('MSIE') !== -1) {
        window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
        window.focus();
    }
}

// attach an event to all the download buttons to trigger the special
// ie functionality if on ie
function init_download_links() {
    $('.download-link').each(function() {
        var $el = $(this);
        $el.click(function() {
            trigger_ie_download($el.data('direct-link'));
        });
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

// used in bedrock for desktop specific checks like `isFirefox() && !isFirefoxMobile()`
// reference https://developer.mozilla.org/en-US/docs/Gecko_user_agent_string_reference
function isFirefoxMobile(userAgent) {
    var ua = userAgent || navigator.userAgent;
    return /Mobile|Tablet|Fennec/.test(ua);
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
