$(document).ready(function() {

    var email_open = $('.inline-email-form .email-form input[name=email]').not(':hidden');

    var pane = $('.inline-email-form .form-pane');
    var opened = $('.inline-email-form ul').hasClass('error');
    var overlayed = pane.css('position') == 'absolute';
    
    $(window).click(function(e) {
        if(overlayed) {
            close();
        }
    });

    $('.inline-email-form').click(function(e) {
        if(overlayed) {
            e.stopPropagation();
        }
    });

    function open()
    {
	if (!opened) {
	    $('#whatsnew .newsletter').css('height', 'auto');
	    $('.inline-email-form .form-pane').fadeIn();
	    $('.inline-email-form .form-pane select[name=country]').focus();

	    opened = true;
	}
    }

    function close() {
        $('.inline-email-form .form-pane').hide();
        $('.inline-email-form .email-open').removeClass('opened');

        opened = false;
    }

    if (email_open) {

	$('.inline-email-form').submit(function(e) {
	    if (!opened) {
		e.preventDefault();
		open();
	    }
	});
        
	$('.inline-email-form .email-open').click(function(e) {
	    e.preventDefault();

	    if (!opened) {
		$(this).addClass('opened');
		var uri = $(this).attr('data-wt_uri');
		var ti = $(this).attr('data-wt_ti');
		dcsMultiTrack('DCS.dcsuri', uri, 'WT.ti', ti);
	    }

	    open();
	});

        if(opened || $('.inline-email-form .success-pane').not(':hidden').length) {
            $('html, body').animate({
                scrollTop: $('.inline-email-form').offset().top
            }, 500);

            $('a.email-open').addClass('opened');
        }

    } else {

	$('.inline-email-form a:first').click(function(e) {
	    e.preventDefault();

	    $(this).hide();
	    var uri = $(this).attr('data-wt_uri');
	    var ti = $(this).attr('data-wt_ti');
	    dcsMultiTrack('DCS.dcsuri', uri, 'WT.ti', ti);

	    $('.form-pane').fadeIn();
	    $('.form-pane input[name=email]').focus();
	});

    }
});
