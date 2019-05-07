/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

/**
 * Feature detect for animating SVG line paths using CSS
 * Detection:
 * 1.) browser supports inline SVG
 * 2.) browser supports CSS animations
 * 3.) browser can animate stroke-dashoffset via a CSS keyframe animation
 *
 * Required less file: 'css/base/svg-animation-check.less'
 */
Mozilla.svgAnimCheck = function() {
    'use strict';

    if (!Mozilla.svgAnimCheck.supportsInlineSVG() || !Mozilla.svgAnimCheck.supportsCSSAnimations()) {
        return false;
    } else {
        return Mozilla.svgAnimCheck.supportsCSSAnimatedPaths();
    }
};

/**
 * Detect CSS animation support (only checks for webkit and unprefixed)
 */
Mozilla.svgAnimCheck.supportsCSSAnimations = function() {
    'use strict';

    var div = document.createElement('div');

    // note we're only checking for Webkit vendor prefix as all other browsers
    // now support unprefixed CSS animations
    if (div.style.animationName !== undefined || div.style.WebkitAnimationName !== undefined) {
        return true;
    }

    return false;
};

/**
 * Detect support for inline SVG elements.
 */
Mozilla.svgAnimCheck.supportsInlineSVG = function() {
    'use strict';

    var div = document.createElement('div');
    div.innerHTML = '<svg/>';
    return (div.firstChild && div.firstChild.namespaceURI) === 'http://www.w3.org/2000/svg';
};

/**
 * Try to animate stroke-dashoffset using CSS and then get the computed value to see if it has changed.
 */
Mozilla.svgAnimCheck.supportsCSSAnimatedPaths = function() {
    'use strict';

    var div = document.createElement('div');
    var circle;
    var offset;

    div.id = 'svg-test';
    div.innerHTML = '<svg role="presentation" xmlns="http://www.w3.org/2000/svg" version="1.1"><path id="svg-test-circle" fill-opacity="0" d="M33.665530413296274,58.589001490321166C43.94406883919239,58.59306994020939,52.274,66.92651000976564,52.274,77.205C52.274,87.486,43.939,95.821,33.658,95.821C23.377000000000002,95.821,15.042000000000002,87.48599999999999,15.042000000000002,77.205C15.041,66.923,23.376,58.589,33.658,58.589" stroke="#5d7489"></path></svg>';
    document.documentElement.appendChild(div);

    // try/catch is maybe a little over cautious
    // but better to show the fallback than throw an exception
    try {
        circle = document.getElementById('svg-test-circle');
        offset = window.getComputedStyle(circle).getPropertyValue('stroke-dashoffset');

        div.parentNode.removeChild(div);

        // webkit & blink return a string with px value
        if (offset.replace(/\D/g, '') === '0') {
            return true;
        }
        return false;
    } catch(e) {
        div.parentNode.removeChild(div);
        return false;
    }
};
