$(function() {
    'use strict';

    var dntStatus = navigator.doNotTrack || navigator.msDoNotTrack;
    var $body = $('body');
    var $flashTalkingPixel = $('<img />', {
        width: '1',
        height: '1',
        src: 'https://servedby.flashtalking.com/spot/8/6247;40428;4669/?spotName=Mozilla_Download_Conversion'
    });

    // doNotTrack returns three possible values, 1, 0 or unspecified all as strings.
    // and prior to Gecko 32 yes, no, unspecified so, we need to check for all of these.
    // https://developer.mozilla.org/en-US/docs/Web/API/Navigator/doNotTrack
    var fxMatch = navigator.userAgent.match(/Firefox\/(\d+)/);
    if (fxMatch && Number(fxMatch[1]) < 32) {
        // Can't say for sure if it is 1 or 0, due to Fx bug 887703
        dntStatus = (dntStatus === 'yes') ? 'Unknown' : 'Unspecified';
    } else {
        dntStatus = { '0': 'Disabled', '1': 'Enabled' }[dntStatus] || 'Unspecified';
    }

    // only add the pixel if the value of dntStatus is disabled.
    if (dntStatus === 'Disabled') {
        $body.append($flashTalkingPixel);
    }
});
