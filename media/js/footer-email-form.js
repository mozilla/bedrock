$(document).ready(function() {
	function footer_email_form_show_details(trigger_click) {
		$('#form-details').slideDown('normal', function() {
			if (trigger_click) {
				$('#footer_email_submit').trigger('click');
			}
        });
        
        $('#footer-email-form .form-details').slideDown();
	}

    $('#id_email, #id_interest').focus(function () {
        footer_email_form_show_details(false);
    });

    $('#footer_email_submit').click(function(e) {
		if (!$('#form-details').is(':visible')) {
			e.preventDefault();
			footer_email_form_show_details(true);
		}
    });

});
