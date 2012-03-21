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

    $('#features li a')
        .click(function(e) {
            e.preventDefault();
            $('#overlay')
                .css('display', 'block')
                .css('height', $(document).height() + 'px');

            var width = $('#overlay-' + this.id).outerWidth();
            var height = $('#overlay-' + this.id).outerHeight();
            var docWidth = $(document).width();
            var viewHeight = $(window).height();
            

            var $overlay = $('#overlay-' + this.id);
            var top = ((viewHeight - height) / 2);
            if ($overlay.css('position') == 'absolute') {
              top += $(window).scrollTop();
            }
            $overlay.appendTo('body')
                .css('display', 'block')
                .css('top', top + 'px')
                .css('left', ((docWidth - width) / 2) + 'px')
        });

    $('#overlay,.overlay-box .close').click(function(e) {
        e.preventDefault();
        $('.overlay-box').each(function() {
            $(this).css('display', 'none');
        });
        $('#overlay').css('display', 'none');
        $('video').each(function() {
            if (typeof this.pause != 'undefined') {
                this.pause();
            }
        });
    });
  var tips = {}
  tips[PLATFORM_WINDOWS] = [
      {'left': 77, 'top': 73, 'id': 'firefox-menu-button'},
      {'left': 28, 'top': 105, 'id': 'app-tab'},
      {'left': 37, 'top': 137, 'id': 'private-browsing', 'direction': 'up'},
      {'left': 88, 'top': 137, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 155, 'top': 105, 'id': 'tabs-on-top'},
      {'left': 345, 'top': 137, 'id': 'awesome-bar', 'direction': 'up'},
      {'left': 355, 'top': 105, 'id': 'addons-manager'},
      {'left': 510, 'top': 137, 'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 575, 'top': 105, 'id': 'password-manager'},
      {'left': 695, 'top': 105, 'id': 'customize-toolbar'},
      {'left': 805, 'top': 105, 'id': 'personas'},
      {'left': 920, 'top': 137, 'id': 'bookmark-button', 'direction': 'up'},
      {'left': 928, 'top': 105, 'id': 'sync'}
  ];
  tips[PLATFORM_MACOSX] = [
      {'left': 18, 'top': 105, 'id': 'app-tab'},
      {'left': 37, 'top': 137, 'id': 'private-browsing', 'direction': 'up'},
      {'left': 80, 'top': 137, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 155, 'top': 105, 'id': 'tabs-on-top'},
      {'left': 345, 'top': 137, 'id': 'awesome-bar', 'direction': 'up'},
      {'left': 355, 'top': 105, 'id': 'addons-manager'},
      {'left': 510, 'top': 137, 'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 575, 'top': 105, 'id': 'password-manager'},
      {'left': 695, 'top': 105, 'id': 'customize-toolbar'},
      {'left': 805, 'top': 105, 'id': 'personas'},
      {'left': 920, 'top': 137, 'id': 'bookmark-button', 'direction': 'up'},
      {'left': 928, 'top': 105, 'id': 'sync'}
  ];
  tips[PLATFORM_LINUX] = [
      {'left': 18, 'top': 130, 'id': 'app-tab'},
      {'left': 37, 'top': 170, 'id': 'private-browsing', 'direction': 'up'},
      {'left': 91, 'top': 170, 'id': 'instant-website-id', 'direction': 'up'},
      {'left': 155, 'top': 130, 'id': 'tabs-on-top'},
      {'left': 345, 'top': 170, 'id': 'awesome-bar', 'direction': 'up'},
      {'left': 355, 'top': 130, 'id': 'addons-manager'},
      {'left': 510, 'top': 170, 'id': 'switch-to-tab', 'direction': 'up'},
      {'left': 575, 'top': 130, 'id': 'password-manager'},
      {'left': 695, 'top': 130, 'id': 'customize-toolbar'},
      {'left': 805, 'top': 130, 'id': 'personas'},
      {'left': 928, 'top': 130, 'id': 'sync'}
  ];


    var tipWidth = 500;
    var sceneWidth = 950;

    $(tips[gPlatform]).each(function (index, tip) {
        drawTip(tip);
    })
    addHandlers();

    function addHandlers() {
        // Fix for keyboard accessibility
        $('.tip-container').bind('mouseenter', function (e) {
            var $this = $(this);
            $this.children('.arrow, .tip')
                .css({'display': 'block'})
                .animate({'opacity': 1}, 300);
            $this.children('.callout')
                .animate({'opacity': 0}, 300);
        }).bind('mouseleave', function (e) {
            var $this = $(this);
            $this.children('.arrow, .tip')
                .animate({'opacity': 0}, 300, function () {
                    $(this).css({'display': 'none'});
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
        $callout.addClass('callout')
        $callout.attr('tabindex', 0);
        $callout.css({'left': tip.left, 'top': tip.top});
        $container.append($callout);

        var $tip = $('#' + tip.id);        
        var left = Math.max(tip.left - (tipWidth/2), 0);
        if (left + tipWidth > sceneWidth) {
            left = sceneWidth - tipWidth;
        }
        $tip.css({'left': left, 'top': tip.top, 'opacity': 0, 'display': 'none'});
        $container.append($tip);

        var $arrow = $(document.createElement('span'));
        $arrow.addClass('arrow');
        $arrow.css({'left': tip.left, 'top': tip.top, 'opacity': 0, 'display': 'none'});
        $container.append($arrow);

        $tip.removeAttr('id');
        $container.attr('id', tip.id);

        $('#figure').append($container);
    }

});
