jQuery(function($) {
	$('table.grants').each(function() {

		// Add extra cells to front of each row
		$('tr', this).each(function() {
			var el = (this.parentNode.nodeName === 'THEAD') ? 'th' : 'td';
			$(document.createElement(el)).prependTo(this).addClass('extra');
		});

		// Loop through each of the data groups, adding toggle buttons
		$('tbody', this).each(function(i, group) {
			$('td.extra', this).each(function(index) {
				if (index === 0) {
					var $btn = $(document.createElement('a'))
							.addClass('button-white')
							.text('+')
							.attr('href', '#toggle');

					$btn.click(function() {
						if ($(group).toggleClass('collapsed').hasClass('collapsed')) {
							$btn.text('+');
						} else {
							$btn.text('-');
						}
						return false;
					});

					$btn.appendTo(this);	
				} else {
					this.className = 'summary';
				}
			});

			this.className += ' collapsed';
		});
	});
});
