/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    var $logo = $('#masthead h2 img');
    var logoOriginalSrc = $logo.attr('src');

    var pager = Mozilla.Pager.rootPagers[0];
    var selected_href = false;

    function redirect(a) {
        var href = a.href;

        if (href.indexOf('#beta') != -1) {
            window.location = '/firefox/beta/';
        } else if (href.indexOf('#aurora') != -1) {
            window.location = '/firefox/aurora/';
        } else if (href.indexOf('#firefox') != -1) {
            window.location = '/firefox/';
        }
    }

    pager.$container.bind('changePage', function(e, tab) {
        if (pager.currentPage.id == 'aurora') {
            $('body').addClass('space');
            $logo.attr('src', $logo.attr('data-inverse-src'));
        } else {
            $('body').removeClass('space');
            $logo.attr('src', logoOriginalSrc);
        }

        $('.pager-tabs a').unbind('click.outgoing');
        $('.pager-tabs a.selected').bind('click.outgoing', function() {
            redirect(this);
        });
    });

    $('#carousel-left').click(function(e) {
        e.preventDefault();
        pager.prevPageWithAnimation();
    });

    $('#carousel-right').click(function(e) {
        e.preventDefault();
        pager.nextPageWithAnimation();
    });

    // init
    if (pager.currentPage.id == 'aurora') {
        $('body').removeClass('sky');
        $('body').addClass('space');
        $logo.attr('src', $logo.attr('data-inverse-src'));
    } else {
        $('body').removeClass('space');
        $('body').addClass('sky');
        $logo.attr('src', logoOriginalSrc);
    }

    $('.pager-tabs a.selected').bind('click.outgoing', function() {
        redirect(this);
    });
});
