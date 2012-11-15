var Mozilla = window.Mozilla || {};

Mozilla.FacebookMessengerTab = function() {
	var _init = function() {
		if (_get_firefox_version() >= 16) {
			$('#cta-messenger').show();
		} else {
			$('#cta-firefox').show();
		}
	};

	var _get_firefox_version = function() {
		var version = 0;

		var matches = /Firefox\/([0-9]+).[0-9]+(?:.[0-9]+)?/.exec(navigator.userAgent);

		if (matches !== null && matches.length > 0) {
			version = parseInt(matches[1], 10);
		}

		return version;
	};

	return {
		init: function() {
			_init();
		}
	};
}();

$(function() {
	Mozilla.FacebookMessengerTab.init();
});