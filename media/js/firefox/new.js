var Mozilla = window.Mozilla || {};
Mozilla.Firefox = window.Mozilla.Firefox || {};

Mozilla.Firefox.New = (function() {
	//"use strict";

	var _css3;

	var _init = function() {
		// wrap #wrapper in div for noise bg
		$('#wrapper').wrap('<div id="inner-wrapper" />');

		// replace install images
		if (site.platform === 'osx') {
			$('.install-image').each(function(i, img) {
				$(this).attr('src', $(this).attr('src').replace(/win/gi, 'mac'));
			});
		} else if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
			$('#install1').attr('src', $('#install1').attr('src').replace(/win/gi, 'winIE8'));
		}

		// swipe FF dl link from button & add to 'click here' link
		// better way coming in bedrock soon
		var ff_dl_link;

		$('.download-list li').each(function(i, li) {
			if ($(li).is(':visible')) {
				ff_dl_link = $(li).find('a:first').attr('href');
				$('#direct-download-link').attr('href', ff_dl_link);
				return false;
			}
		});

		if (!$('html').hasClass('android')) {
			_css3 = ($('html').is('.csstransforms.csstransitions')) ? true : false;

			$('.download-firefox').on('click', function(e) {
				// track download click
				if (window._gaq) {
					var track_url = window.location.pathname;
					track_url += (track_url.charAt(track_url.length - 1) === '/') ? 'download/' : '/download/';

					_gaq.push(['_trackPageview', track_url]);
				}

				$('#scene2').show();

				if (!_css3) {
					$('#stage-firefox').animate({
						bottom: '-400px'
					}, 400, function() {
						$('.thankyou').focus();
					});
				} else {
					$('#stage-firefox').addClass('scene2');
					// transitionend firing multiple times in FF 17, including before transition actually finished
					// work-around with setTimeout
					setTimeout(function() {
						$('.thankyou').focus();
					}, 500);
				}
			});
		}
	};

	return {
		init: function() { _init(); }
	};
})();

$(function() {
	Mozilla.Firefox.New.init();
});