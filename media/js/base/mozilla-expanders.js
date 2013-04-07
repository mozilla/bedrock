/**
 * Expandable page section widget
 *
 * Initializes all elements of a specific class as an expandable and
 * collapsable section. Does so in an accessible way.
 *
 * This code is licensed under the Mozilla Public License 1.1.
 *
 * Portions adapted from the jQuery Easing plugin written by Robert Penner and
 * used under the following license:
 *
 *   Copyright 2001 Robert Penner
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions are
 *   met:
 *
 *   - Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   - Neither the name of the author nor the names of contributors may be
 *     used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 *   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 *   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 *   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 *   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 *   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 *   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * @copyright 2007-2010 Mozilla Foundation, 2007-2010 silverorange Inc.
 * @license   http://www.mozilla.org/MPL/MPL-1.1.html Mozilla Public License 1.1
 * @author    Michael Gauthier <mike@silverorange.com>
 */

// create namespace
if (typeof Mozilla == 'undefined') {
	var Mozilla = {};
}

// create namespace
if (typeof Mozilla.Expander == 'undefined') {
	Mozilla.Expander = {};
}

// string resources
Mozilla.Expander.OPEN_TEXT  = 'Show';
Mozilla.Expander.CLOSE_TEXT = 'Hide';

$(document).ready(function() {

	// add easing functions
	$.extend($.easing, {
		'expanderOpen':  function (x, t, b, c, d) {
			return c * (t /= d) * t + b;
		},
		'expanderClose': function (x, t, b, c, d) {
			return -c * (t /= d) * (t - 2) + b;
		}
	});

	function Expander(container)
	{
		if (typeof container == 'String') {
			container = $(container).get(0);
		}

		// parse group id
		var matches = container.className.match(
			/\bexpander-group-([A-Za-z0-9]+)\b/);

		if (matches && matches.length) {
			this.groupId = 'group-' + matches[1];
			if (!Expander.expandersByGroup[this.groupId]) {
				Expander.expandersByGroup[this.groupId] = [];
			}
			Expander.expandersByGroup[this.groupId].push(this);
		} else {
			this.groupId = null;
		}

		// get header and content elements as first two child elements
		var header     = $(':first', container);
		this.content   = $(':eq(1)', container);
		this.container = $(container);

		if (!this.container.attr('id')) {
			this.container.attr('id', Expander.generateId());
		}

		this.id = this.container.attr('id');

		// build header markup
		this.anchor = $('<a href="#" class="expander-anchor"/>');
		this.anchor.data('expander', this);
		while (header.get(0).firstChild) {
			$(header.get(0).firstChild).appendTo(this.anchor);
		}
		this.anchor.appendTo(header);
		this.anchor.click(function(e) {
			e.preventDefault();
			var expander = $(this).data('expander');
			expander.toggleWithAnimation();
		});

		// build content markup
		this.contentAnimation = $('<div class="expander-animation">');
		this.contentAnimation.data('expander', this);
		var contentPadding = $('<div class="expander-padding">');
		while (this.content.get(0).firstChild) {
			$(this.content.get(0).firstChild).appendTo(contentPadding);
		}
		contentPadding.appendTo(this.contentAnimation);
		this.contentAnimation.appendTo(this.content);

		// prevent closing during opening animation and vice versa
		this.semaphore = false;

		this.container.removeClass('expander');

		if (   (location.hash.substring(1) == this.id)
			|| this.loadState() == Expander.OPEN
			|| this.container.hasClass('expander-default-open')
		) {
			this.open();
		} else {
			this.close();
		}
	}

	Expander.OPEN             = true;
	Expander.CLOSED           = false;
	Expander.OPEN_DURATION    = 250;
	Expander.CLOSE_DURATION   = 250;

	Expander.expanders        = [];
	Expander.expandersByGroup = {};

	Expander.idPrefix         = '-moz-expander-';
	Expander.idCount          = 0;

	Mozilla.Expander.openAll = function()
	{
		for (var i = 0; i < Expander.expanders.length; i++) {
			Expander.expanders[i].openWithAnimation();
		}
	};

	Mozilla.Expander.closeAll = function()
	{
		for (var i = 0; i < Expander.expanders.length; i++) {
			Expander.expanders[i].closeWithAnimation();
		}
	};

	Expander.generateId = function()
	{
		Expander.idCount++;
		return Expander.idPrefix + Expander.idCount;
	};

	Expander.prototype.toggle = function()
	{
		if (this.state == Expander.OPEN) {
			this.close();
		} else {
			this.open();
		}
	};

	Expander.prototype.saveState = function()
	{
		if (typeof sessionStorage != 'undefined') {
			var href = location.href.split('#')[0];
			var state = (this.state == Expander.OPEN) ?
				'open' : 'closed';

			sessionStorage.setItem(href + '-' + this.id, state);
		}
	};

	Expander.prototype.loadState = function()
	{
		var state = Expander.CLOSED;
		if (typeof sessionStorage != 'undefined') {
			var href = location.href.split('#')[0];
			var loadedState = sessionStorage.getItem(href + '-' + this.id);
			if (loadedState !== null) {
				state = (loadedState == 'open') ?
					Expander.OPEN : Expander.CLOSED;
			}
		}
		return state;
	};

	Expander.prototype.toggleWithAnimation = function()
	{
		if (this.state == Expander.OPEN) {
			this.closeWithAnimation();
		} else {
			this.openWithAnimation();
		}
	};

	Expander.prototype.openWithAnimation = function()
	{
		if (this.semaphore || this.state === Expander.OPEN) {
			return;
		}

		this.container.removeClass('expander-closed');
		this.container.addClass('expander-open');

		// get display height
		this.content
			.css('overflow', 'hidden')
			.css('height', '0');

		this.contentAnimation
			.css('visibility', 'hidden')
			.css('overflow', 'hidden')
			.css('display', 'block')
			.css('height', 'auto');

		var height = this.contentAnimation.get(0).offsetHeight;

		this.contentAnimation
			.css('height', '0')
			.css('visibility', 'visible');

		this.content
			.css('height', '')
			.css('overflow', 'visible');

		this.contentAnimation.animate({
			'height': height
		}, Expander.OPEN_DURATION, 'expanderOpen', function() {
			var expander = $(this).data('expander');
			expander.handleOpen();
		});

		this.semaphore = true;

		// close other expanders in the group
		if (this.groupId !== null) {
			var expander;
			var expanderGroup = Expander.expandersByGroup[this.groupId];
			for (var i = 0; i < expanderGroup.length; i++) {
				expander = expanderGroup[i];
				if (expander !== this) {
					expander.closeWithAnimation();
				}
			}
		}

		this.state = Expander.OPEN;
	};

	Expander.prototype.closeWithAnimation = function()
	{
		if (this.semaphore || this.state === Expander.CLOSED) {
			return;
		}

		this.container.removeClass('expander-open-complete');

		this.contentAnimation
			.css('overflow', 'hidden')
			.css('height', 'auto')

		this.contentAnimation.animate({
			height: 0
		},
		Expander.CLOSE_DURATION, 'expanderClose', function() {
			var expander = $(this).data('expander');
			expander.handleClose();
		});

		this.semaphore = true;

		this.state = Mozilla.Expander.CLOSED;
	};

	Expander.prototype.open = function()
	{
		this.container
			.removeClass('expander-closed')
			.addClass('expander-open')
			.addClass('expander-open-complete');

		this.semaphore = false;

		this.state = Expander.OPEN;
		this.anchor.attr('title', Mozilla.Expander.CLOSE_TEXT);

		// close other expanders in the group
		if (this.groupId !== null) {
			var expander;
			var expanderGroup = Expander.expandersByGroup[this.groupId];
			for (var i = 0; i < expanderGroup.length; i++) {
				expander = expanderGroup[i];
				if (expander !== this) {
					expander.close();
				}
			}
		}

		this.saveState();
	};

	Expander.prototype.close = function()
	{
		this.container
			.removeClass('expander-open-complete')
			.removeClass('expander-open')
			.addClass('expander-closed');

		this.semaphore = false;

		this.state = Expander.CLOSED;
		this.anchor.attr('title', Mozilla.Expander.OPEN_TEXT);

		this.saveState();
	};

	Expander.prototype.handleOpen = function()
	{
		this.container.addClass('expander-open-complete');

		// allow font resizing to work again and re-set overflow to visible
		// for styles that might depend on it
		this.contentAnimation
			.css('height', 'auto')
			.css('overflow', 'visible');

		this.anchor.attr('title', Mozilla.Expander.CLOSE_TEXT);

		this.semaphore = false;

		this.saveState();
	};

	Expander.prototype.handleClose = function()
	{
		this.container
			.removeClass('expander-open')
			.addClass('expander-closed');

		this.anchor.attr('title', Mozilla.Expander.OPEN_TEXT);

		this.semaphore = false;

		this.saveState();
	};

	// remember link location
	var hash = location.hash;

	// create expanders
	$('.expander').each(function() {
		Expander.expanders.push(new Expander(this));
	});

	// reset link location since the link may have moved on the page
	if (hash) {
		if ((/safari/gi).test(navigator.userAgent)) {
			location.hash = '#nothing'; /* Safari hack */
		}
		location.hash = hash;
	}
});
