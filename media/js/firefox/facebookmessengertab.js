var Mozilla = window.Mozilla || {};

Mozilla.FacebookMessengerTab = function() {
	var _init = function() {
		if (getFirefoxMasterVersion() >= 17) {
			$('#cta-messenger').show();
		} else {
			$('#cta-firefox').show();
		}
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