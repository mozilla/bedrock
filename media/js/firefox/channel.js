/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {

    var $logo = $('#masthead h2 img');
    var logoOriginalSrc = $logo.attr('src');
    var logoOriginalSrcSet = $logo.attr('srcset');
    var logoInverseSrc = $logo.attr('data-inverse-src');
    var logoInverseSrcSet = $logo.attr('data-inverse-srcset');
    var pager = Mozilla.Pager.pagers[0];
    var dataLayer = window.dataLayer || [];

    pager.$container.bind('changePage', function() {
        if (pager.currentPage.id === 'developer') {
            $('body').removeClass('sky').addClass('blueprint');
            $logo.attr({ 'src': logoInverseSrc, 'srcset': logoInverseSrcSet });
        } else {
            $('body').removeClass('blueprint').addClass('sky');
            $logo.attr({ 'src': logoOriginalSrc, 'srcset': logoOriginalSrcSet });
        }

        $('.pager-tabs a').unbind('click.outgoing');
    });

    $('#carousel-left').click(function(e) {
        e.preventDefault();
        pager.prevPageWithAnimation();

        dataLayer.push({
            'event': 'channel-carousel-interaction',
            'direction': 'left',
            'nextPage': pager.currentPage.id
        });
    });

    $('#carousel-right').click(function(e) {
        e.preventDefault();
        pager.nextPageWithAnimation();

        dataLayer.push({
            'event': 'channel-carousel-interaction',
            'direction': 'right',
            'nextPage': pager.currentPage.id
        });
    });

    // init
    if (pager.currentPage.id === 'developer') {
        $('body').removeClass('sky').addClass('blueprint');
        $logo.attr({ 'src': logoInverseSrc, 'srcset': logoInverseSrcSet });
    } else {
        $('body').removeClass('blueprint').addClass('sky');
        $logo.attr({ 'src': logoOriginalSrc, 'srcset': logoOriginalSrcSet });
    }

    if (location.hash === '#aurora') {
        location.hash = '#developer';
    }
});
