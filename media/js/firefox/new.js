var Mozilla = window.Mozilla || {};
Mozilla.Firefox = window.Mozilla.Firefox || {};

Mozilla.Firefox.New = (function() {
	//"use strict";

	var _init = function() {
		$('#firefox-new-a .download-firefox').on('click', function(e) {
			e.preventDefault();

			$('#features-download').fadeOut('fast', function() {
				$('#dl-feedback').fadeIn('fast');
			});
		});

		$('#firefox-new-b .download-firefox').on('click', function(e) {
			e.preventDefault();

			$('#dl-feedback').slideDown('normal', function() {

			});

			$('html, body').animate({
				scrollTop: $('#dl-feedback').offset().top
			}, 500);
		});

		$('#firefox-new-c .download-firefox, #firefox-new-d .download-firefox, #firefox-new-e .download-firefox').on('click', function(e) {
			e.preventDefault();

			$('#stage').addClass('scene2');
		});
	};

	return {
		init: function() { _init(); }
	};
})();

$(function() {
	Mozilla.Firefox.New.init();
});