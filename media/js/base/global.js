/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

/**
 * Bug 393263 A special function for IE < 9.
 * Without this hack there is no prompt to download after they click. sigh.
 * @param {link} direct link to download URL
 * @param {userAgent} optional UA string for testing purposes.
 */
function trigger_ie_download(link, userAgent) {
    'use strict';
    var ua = userAgent !== undefined ? userAgent : navigator.userAgent;
    // Only open if we got a link and this is IE < 9.
    if (link && window.site.platform === 'windows' && /MSIE\s[1-8]\./.test(ua)) {
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

function update_download_text_for_old_fx() {
    var client = window.Mozilla.Client;

    // if using Firefox
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        // look at each button to see if it's set to check for old firefox
        var $buttons = $('.download-button-check-old-fx');

        // if the page has download buttons
        if ($buttons.length) {
            client.getFirefoxDetails(function(data) {
                // if using an out of date firefox
                if (!data.isUpToDate) {
                    // replace subtitle copy
                    $buttons.find('.download-subtitle').text(window.trans('global-update-firefox'));
                }
            });
        }
    }
}

// Replace Google Play and Apple App Store links on Android and iOS devices to
// let them open the native marketplace app
function init_mobile_download_links() {
    if (site.platform === 'android') {
        $('a[href^="https://play.google.com/store/apps/"]').each(function() {
            $(this).attr('href', $(this).attr('href')
                .replace('https://play.google.com/store/apps/', 'market://'));
        });
    }

    if (site.platform === 'ios') {
        $('a[href^="https://itunes.apple.com/"]').each(function() {
            $(this).attr('href', $(this).attr('href')
                .replace('https://', 'itms-apps://'));
        });
    }
}

// language switcher
function init_lang_switcher() {
    var $language = $('#page-language-select');
    var previousLanguage = $language.val();
    $language.change(function() {

        window.dataLayer.push({
            'event': 'change-language',
            'languageSelected': $language.val(),
            'previousLanguage': previousLanguage
        });
        $('#lang_form').submit();
    });
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
