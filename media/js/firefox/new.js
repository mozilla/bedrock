var Mozilla = window.Mozilla || {};
Mozilla.Firefox = window.Mozilla.Firefox || {};

Mozilla.Firefox.New = (function() {
	//"use strict";

	var _css3;

	var _init = function() {
		// hack to test android
		// TODO: remove for production
		if (window.location.href.indexOf('forceandroid') > -1) {
			var h = document.documentElement;
			$(h).removeClass(site.platform).addClass('android');
		}

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

		// swipe FF dl link from button
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

			// if browser does not support css transforms
			if (!_css3) {
				$('#stage-firefox').css('top', '-100%');
			}

			$('.download-firefox').on('click', function(e) {
				// prevent download during testing
				//e.preventDefault();

				// track download click
				if (window._gaq) {
					_gaq.push(['_trackPageview', window.location.pathname]);
				}

				if (_css3) {
					$('#stage-firefox').addClass('transition scene2');
				} else {
					$('#stage-firefox').animate({
						top: '0%'
					}, 400);
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