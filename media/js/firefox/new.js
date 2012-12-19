var Mozilla = window.Mozilla || {};
Mozilla.Firefox = window.Mozilla.Firefox || {};

Mozilla.Firefox.New = (function() {
	"use strict";

	var _css3;

	var _init = function() {
		if (!$('html').hasClass('android')) {
			// replace install images
			$(window).on('load', function() {
				$('html').addClass('ready-for-scene2');
				var img_os = (site.platform === 'osx') ? 'mac' : 'win';

				$('#install2').attr('src', $('#install2').attr('data-src').replace(/win/gi, img_os));
				$('#install3').attr('src', $('#install3').attr('data-src').replace(/win/gi, img_os));

				// screen 1 is unique for IE < 9
				if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
					img_os = 'winIE8';
				}

				$('#install1').attr('src', $('#install1').attr('data-src').replace(/win/gi, img_os));
			});

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

			$('.download-firefox').on('click', function(e) {
				// track download click
				if (window._gaq) {
					_gaq.push(['_trackPageview', '/en-US/products/download.html?referrer=new-b']);
				}

				if (!Modernizr.csstransitions) {
					$('#scene2').css('visibility', 'visible');
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