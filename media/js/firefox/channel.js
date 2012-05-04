
$(document).ready(function() {
    var pager = Mozilla.Pager.rootPagers[0];
    var selected_href = false;

    function redirect(a) {
        var href = a.href;

        if(href.indexOf('#beta') != -1) {
            window.location = '/firefox/beta/';
        }
        else if(href.indexOf('#aurora') != -1) {
            window.location = '/firefox/aurora/';
        }
        else if(href.indexOf('#firefox') != -1) {
            window.location = '/firefox/';
        }
    }

    pager.$container.bind('changePage', function(e, tab) {
        if (pager.currentPage.id == 'aurora') {
            $('body').addClass('space');
        } else {
            $('body').removeClass('space');
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
    } else {
        $('body').removeClass('space');
        $('body').addClass('sky');
    }

    $('.pager-tabs a.selected').bind('click.outgoing', function() {
        redirect(this);
    });
});
