/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {

var PLATFORM_OTHER    = 0;
var PLATFORM_WINDOWS  = 1;
var PLATFORM_LINUX    = 2;
var PLATFORM_MACOSX   = 3;
var PLATFORM_MAC      = 4;

// Default to windows
var gPlatform = PLATFORM_WINDOWS;

if (navigator.platform.indexOf("Win32") != -1 || navigator.platform.indexOf("Win64") != -1)
  gPlatform = PLATFORM_WINDOWS;
else if (navigator.platform.indexOf("Linux") != -1)
  gPlatform = PLATFORM_LINUX;
else if (navigator.userAgent.indexOf("Mac OS X") != -1)
  gPlatform = PLATFORM_MACOSX;
else if (navigator.userAgent.indexOf("MSIE 5.2") != -1)
  gPlatform = PLATFORM_MACOSX;
else if (navigator.platform.indexOf("Mac") != -1)
  gPlatform = PLATFORM_MAC;
else
  gPlatform = PLATFORM_OTHER;

var gPlatformVista = navigator.userAgent.indexOf('Windows NT 6.0') !=-1


    $('<div id="overlay" />').appendTo('body');

  var tips = {}
  tips[PLATFORM_WINDOWS] = [
      {'left': 832, 'top': -48,  'id': 'not-this-marker'},
      {'left': 113, 'top': 34,  'id': 'firefox-menu-button'},
      {'left': 42,  'top': 70,  'id': 'app-tab', 'direction': 'up'},
      {'left': 587, 'top': 55,  'id': 'new-tab'},
      {'left': 89,  'top': 102, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 245, 'top': 62,  'id': 'tabs-on-top'},
      {'left': 325, 'top': 97,  'id': 'awesome-bar', 'direction': 'up'},
      {'left': 349, 'top': 56,  'id': 'addons-manager'},
      {'left': 530, 'top': 65,  'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 676, 'top': 82,  'id': 'customize-toolbar'},
      {'left': 755, 'top': 41,  'id': 'themes'},
      {'left': 933, 'top': 87,  'id': 'bookmark-button'},
      {'left': 894, 'top': 107, 'id': 'home-button', 'direction': 'up'}
  ];
  tips[PLATFORM_MACOSX] = [
      {'left': 832, 'top': -48,  'id': 'not-this-marker'},
      {'left': 38,  'top': 57,  'id': 'app-tab'},
      {'left': 582, 'top': 57,  'id': 'new-tab'},
      {'left': 76,  'top': 101, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 245, 'top': 57,  'id': 'tabs-on-top'},
      {'left': 345, 'top': 97,  'id': 'awesome-bar', 'direction': 'up'},
      {'left': 355, 'top': 61,  'id': 'addons-manager'},
      {'left': 510, 'top': 62,  'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 660, 'top': 88,  'id': 'customize-toolbar'},
      {'left': 750, 'top': 41,  'id': 'themes'},
      {'left': 940, 'top': 87,  'id': 'bookmark-button'},
      {'left': 899, 'top': 101, 'id': 'home-button', 'direction': 'up'}
  ];
  tips[PLATFORM_LINUX] = [
      {'left': 832, 'top': -48,  'id': 'not-this-marker'},
      {'left': 42,  'top': 94,  'id': 'app-tab'},
      {'left': 578, 'top': 100, 'id': 'new-tab'},
      {'left': 80,  'top': 142, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 155, 'top': 95,  'id': 'tabs-on-top'},
      {'left': 445, 'top': 134, 'id': 'awesome-bar', 'direction': 'up'},
      {'left': 415, 'top': 98,  'id': 'addons-manager'},
      {'left': 510, 'top': 110, 'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 699, 'top': 127, 'id': 'customize-toolbar'},
      {'left': 785, 'top': 50, 'id': 'themes'},
      {'left': 945, 'top': 123, 'id': 'home-button'}
  ];


    var tipWidth = 450;
    var sceneWidth = 950;

    $(tips[gPlatform]).each(function (index, tip) {
        drawTip(tip);
    })
    addHandlers();

	function addHandlers() {
	$('.tip-container').bind('mouseenter focusin', function (e) {
	    var $this = $(this);
	    var $tip = $this.find('.tip');
	    var left = parseInt($tip.data("left"), 10);
	    var top = parseInt($tip.data("top"), 10);
	    $this.children('.arrow, .tip, .callout').stop();
	    $tip.css({'left': left, 'top': top})
		.animate({'opacity': 1}, 300);
	    $this.children('.arrow')
		.animate({'opacity': 1}, 300);
	    $this.children('.callout')
		.animate({'opacity': 0}, 300);
	}).bind('mouseleave focusout', function (e) {
            var $this = $(this);
	    var $tip = $this.find('.tip');
	    $this.children('.arrow, .tip, .callout').stop();
	    $this.children('.arrow, .tip')
		.animate({'opacity': 0}, 300, function () {
		    $tip.css({'left': -999, 'top': 0});
		});
	    $this.children('.callout')
		.animate({'opacity': 1}, 300);
        });

    }

    function drawTip(tip) {
        var $container = $(document.createElement('div'));
        $container.addClass('tip-container');
        if (tip.direction == 'up') {
            $container.addClass('up');
        }

        var $callout = $(document.createElement('span'));
	$callout.addClass('callout').attr({'tabindex': '0'});
        $callout.css({'left': tip.left, 'top': tip.top});
        $container.append($callout);

        var $tip = $('#' + tip.id);        
        var left = Math.max(tip.left - (tipWidth/2), 0);
	if (left + tipWidth > sceneWidth) {
	    left = sceneWidth - tipWidth;
	}
	$tip.data({"left":left, "top":tip.top});
	$tip.css({'left': -999, 'top': 0, 'opacity': 0});
	$container.append($tip);

        var $arrow = $(document.createElement('span'));
        $arrow.addClass('arrow');
	$arrow.css({'left': tip.left, 'top': tip.top, 'opacity': 0});
        $container.append($arrow);

        $tip.removeAttr('id');
        $container.attr('id', tip.id);

        $('#figure').append($container);
    }

});
