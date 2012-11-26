/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Initializes pagers on this page after the document has been loaded
 */
$(document).ready(function ()
{
	if (Mozilla.hasPersonas) {
		var iframe = document.createElement('iframe');
		iframe.setAttribute('src', Mozilla.PersonaPreviewer.LIVE_URL);
		iframe.setAttribute('id', 'persona-preview-frame');
		iframe.setAttribute('width', '100%');
		iframe.setAttribute('height', '180');

		var previewers = $('.persona-previewer');

		if (previewers.length > 0) {
			var previewer = previewers[0];
			previewer.parentNode.replaceChild(iframe, previewer);
		}

		$('try-on').addClass('fx36');
		$('see-all-personas').addClass('fx36');

		if (iframe.contentWindow.postMessage && iframe.addEventListener) {
			iframe.addEventListener('load', function () {
				iframe.contentWindow.postMessage("activatePersonas", "*");
			}, false);
		}

	} else {
		var previewers = $('.persona-previewer').each(function (index, previewer) {
			new Mozilla.PersonaPreviewer(previewer);
		});
	}
});

// create namespace
if (typeof Mozilla == 'undefined') {
	var Mozilla = {};
}

Mozilla.hasPersonas = (function() {
	var hasPersonas = false;

	var matches = navigator.userAgent.match(
		/Gecko\/[0-9]+ .*(Firefox|Namoroka|Minefield)\/([0-9]+\.[0-9]+)/
	);

	if (matches !== null) {
		hasPersonas = (parseFloat(matches[2]) >= 3.6);
	}

	return hasPersonas;
})();

/**
 * Persona previewer widget
 *
 * @param DOMElement container
 */
Mozilla.PersonaPreviewer = function(container)
{
	this.container = $(container);

	this.page_container = this.container.find('div.persona-previewer-content');

	// this.id             = this.container.attr('id');
	this.pages_by_id    = {};
	this.pages          = [];
	this.previous_page  = null;
	this.current_page   = null;
	this.in_animation   = null;
	this.out_animation  = null;

	this.random_start_page = this.container.hasClass('persona-previewer-random');

	this.tabs = this.container.find('ul.persona-previewer-tabs');

	// add pages
	var page_nodes = this.page_container.children('div');

	var that = this;

	// initialize pages with tabs
	var tab_nodes = this.tabs.find('a').each(function(index, tab_node) {
		that.addPersona(new Mozilla.Persona(page_nodes[index], index, $(tab_node)));
	});

	// initialize current page
	var current_page = null;

	if (this.pages.length > 0) {
		if (this.random_start_page) {
			this.setPersona(this.getPseudoRandomPersona());
		} else {
			var def_page = this.page_container.children('.default-page');

			if (def_page) {
				var def_id;
				if (def_page.attr('id').substring(0, 5) == 'page-') {
					def_id = def_page.attr('id').substring(5);
				} else {
					def_id = def_page.attr('id');
				}
				this.setPersona(this.pages_by_id[def_id]);
			} else {
				this.setPersona(this.pages[0]);
			}
		}
	}
}

Mozilla.PersonaPreviewer.LIVE_URL =
	'http://www.getpersonas.com/en-US/external/mozilla/';

Mozilla.PersonaPreviewer.prototype.getPseudoRandomPersona = function()
{
	var page = null;

	if (this.pages.length > 0) {
		var now = new Date();
		page = this.pages[now.getSeconds() % this.pages.length];
	}

	return page;
}

Mozilla.PersonaPreviewer.PAGE_DURATION     = 150; // milliseconds

Mozilla.PersonaPreviewer.prototype.prevPersonaWithAnimation = function()
{
	var index = this.current_page.index - 1;
	if (index < 0) {
		index = this.pages.length - 1;
	}

	this.setPersonaWithAnimation(this.pages[index]);
}

Mozilla.PersonaPreviewer.prototype.nextPersonaWithAnimation = function()
{
	var index = this.current_page.index + 1;
	if (index >= this.pages.length) {
		index = 0;
	}

	this.setPersonaWithAnimation(this.pages[index]);
}

Mozilla.PersonaPreviewer.prototype.addPersona = function(page)
{
	this.pages_by_id[page.id] = page;
	this.pages.push(page);
	if (page.tab) {
		var that = this;
		$(page.tab).mouseover('mouseover', function (e) {
				e.preventDefault();
				that.setPersonaWithAnimation(page);
			});
	}
}

Mozilla.PersonaPreviewer.prototype.update = function()
{
	if (this.tabs) {
		this.updateTabs();
	}
}

Mozilla.PersonaPreviewer.prototype.updateTabs = function()
{
	var class_name = this.tabs.attr('class');
	class_name = class_name.replace(/pager-selected-[\w-]+/g, '');
	class_name = class_name.replace(/^\s+|\s+$/g,'');
	this.tabs.attr('class', class_name);

	this.current_page.selectTab();
	this.tabs.addClass('pager-selected-' + this.current_page.id);
}

Mozilla.PersonaPreviewer.prototype.setPersona = function(page)
{
	if (this.current_page !== page) {
		if (this.current_page) {
			this.current_page.deselectTab();
			this.current_page.hide();
		}

		if (this.previous_page) {
			this.previous_page.hide();
		}

		this.previous_page = this.current_page;

		this.current_page = page;
		this.current_page.show();
		this.update();
	}
}

Mozilla.PersonaPreviewer.prototype.setPersonaWithAnimation = function(page)
{
	if (this.current_page !== page) {
		// deselect last selected page (not necessarily previous page)
		if (this.current_page) {
			this.current_page.deselectTab();
		}
		
		var that = this;
		if (!this.in_animation) {
			this.previous_page = this.current_page;
		}
		this.page_container.stop(true);
		this.page_container.animate({opacity: 0}, Mozilla.PersonaPreviewer.PAGE_DURATION, function () {that.fadeInPersona()})
		this.in_animation = true;

		// always set current page
		this.current_page = page;
		this.update();
	}

	// for Safari 1.5.x bug setting window.location.
	return false;
}

Mozilla.PersonaPreviewer.prototype.fadeInPersona = function()
{
	if (this.previous_page) {
		this.previous_page.hide();
	}
	this.current_page.show();
	this.in_animation = false;
	this.page_container.animate({opacity: 1}, Mozilla.PersonaPreviewer.PAGE_DURATION);
}

/**
 * @param DOMElement element
 * @param DOMElement tab_element
 */
Mozilla.Persona = function(element, index, tab_element)
{
	this.element = element;

	this.index      = index;

	if (tab_element) {
		this.tab = tab_element;
	} else {
		this.tab = null;
	}

	this.hide();
}

Mozilla.Persona.prototype.selectTab = function()
{
	if (this.tab) {
		this.tab.addClass('selected');
	}
}

Mozilla.Persona.prototype.deselectTab = function()
{
	if (this.tab) {
		this.tab.removeClass('selected');
	}
}

Mozilla.Persona.prototype.focusTab = function()
{
	if (this.tab) {
		this.tab.focus();
	}
}

Mozilla.Persona.prototype.hide = function()
{
	this.element.style.display = 'none';
}

Mozilla.Persona.prototype.show = function()
{
	this.element.style.display = 'block';
}
