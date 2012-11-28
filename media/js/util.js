/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Borrowed from addons.mozilla.org - thanks :)

var PLATFORM_OTHER    = 0;
var PLATFORM_WINDOWS  = 1;
var PLATFORM_LINUX    = 2;
var PLATFORM_MACOSX   = 3;
var PLATFORM_MAC      = 4;

// Default to windows
var gPlatform = PLATFORM_WINDOWS;

if (navigator.platform.indexOf("Win32") != -1 || navigator.platform.indexOf("Win64") != -1)
  gPlatform = PLATFORM_WINDOWS;
else if (navigator.platform.indexOf("Linux") != -1)
  gPlatform = PLATFORM_LINUX;
else if (navigator.userAgent.indexOf("Mac OS X") != -1)
  gPlatform = PLATFORM_MACOSX;
else if (navigator.userAgent.indexOf("MSIE 5.2") != -1)
  gPlatform = PLATFORM_MACOSX;
else if (navigator.platform.indexOf("Mac") != -1)
  gPlatform = PLATFORM_MAC;
else
  gPlatform = PLATFORM_OTHER;

var gPlatformVista = navigator.userAgent.indexOf('Windows NT 6.0') !=-1


// This function is used on the firstrun pages to show the correct image next to the
// "click this close button" text
function loadFirstRunInstallImage() {

    // The only thing we care about is if it's a mac, we're going to switch the
    // class, otherwise, stick with defaults.
    if (gPlatform == PLATFORM_MAC || gPlatform == PLATFORM_MACOSX) {
        document.getElementById('tab-close').setAttribute('class','mac');
    }

}

// Will change the class for the given element.  This is currently used on
// /index.html and /firefox/index.html
function rotateBackgroundForDiv(div_id) {

    // We're leaving a blank in here, since that is another (default) image
    var class_options = new Array( "variation1", "variation2", "variation3" );

    if (Math.random) {
        var choice = Math.floor(Math.random() * (class_options.length));

        // Just in case javascript gets carried away...
        choice = ( (choice < class_options.length)  && choice >= 0) ? choice : 0;

        if (document.getElementById(div_id)) {
            document.getElementById(div_id).setAttribute('class',class_options[choice]);
        }
    }

}

function createCookie(name,value,days, domain) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    } else {
        var expires = "";
    }

    if(domain) {
        domain = "; "+domain;
    } else {
        domain = '';
    }

    document.cookie = name+"="+value+expires+"; path=/"+domain;
}

function getArgs() {
    var args = new Object();
    var query = location.search.substring(1);
    var pairs = query.split("&");
    for(var i = 0; i < pairs.length; i++) {
    var pos = pairs[i].indexOf('=');
    if (pos == -1) continue;
    var argname = pairs[i].substring(0,pos);
    var value = pairs[i].substring(pos+1);
    args[argname] = unescape(value);
    }
    return args;
}

function in_array(search, array) {
    var found = false;

    for(value in array) {
        if(array[value] == search) {
            found = true;
        }
    }

    return found;
}

function vary_body_class(options) {
    var choice = Math.floor(Math.random() * (options.length));
    document.body.className += ' '+options[choice];
}
