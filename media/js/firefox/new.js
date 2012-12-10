var Mozilla = window.Mozilla || {};
Mozilla.Firefox = window.Mozilla.Firefox || {};

Mozilla.Firefox.New = (function() {
	//"use strict";

	var _css3;

	var _init = function() {
		// hack to test android
		if (window.location.href.indexOf('forceandroid') > -1) {
			var h = document.documentElement;
			$(h).removeClass(site.platform).addClass('android');
		}

		if (!$('html').hasClass('android')) {
			_css3 = ($('html').is('.csstransforms.csstransitions')) ? true : false;

			// if browser does not support css transforms
			if (!_css3) {
				$('#stage-firefox').css('top', '-100%');
			}

			$('.download-firefox').on('click', function(e) {
				// prevent download during testing
				//e.preventDefault();

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