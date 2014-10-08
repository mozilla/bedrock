/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    // Add a more/less toggle on story pages
    if ($('.story-more').length > 0) {
        var $more_toggle = $('<div class="more-toggle"><button>' + window.trans('more') + '</button></div>');
        $more_toggle.insertAfter('.story-more');

        $('.more-toggle button').on('click', function() {
           $('.story-more').slideToggle('fast', function() {
                if ($('.story-more').is(':visible')) {
                    $('.more-toggle button').addClass('open').text(window.trans('less'));
                } else {
                    $('.more-toggle button').removeClass('open').text(window.trans('more'));
                }
           });
        });
    }

    // Play videos in a modal
    $('a.video-play').attr('role', 'button').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);
        var videoelem = $('#' + $this.attr('data-element-id'));

        Mozilla.Modal.createModal(this, videoelem, {
            title: '',
            onCreate: function() {
                play_video();
            }
        });
    });

    // Give the modal a chance to open before playing
    var play_video = function() {
        setTimeout(function() {
            $('#modal video:first')[0].play();
        }, 400);
    };

    // Show 'other ways to contribute' block on thankyou page
    $('.cta-other a').on('click', function(e) {
        e.preventDefault();
        $('.cta-other').fadeOut('fast', function() {
            $('#other').slideDown();
        });
    });

    var select_category = function(category) {
        // Style the selected option (reset all of them first to unstyle previous selection)
        $('#inquiry-form .option label').removeClass('selected');
        category.parents('label').addClass('selected');

        // Get all the area IDs
        var areas = $('#inquiry-form .area').map(function(index){ return this.id; });
        // Get the area for the selected category
        var categoryarea = 'area-' + category.attr('value');

        // Show the followup question for categories that have one
        if ($.inArray(categoryarea, areas) !== -1) {
            if ($('.areas').is(':hidden')) {
                $('.areas').slideDown('fast', function(){
                    show_area(categoryarea);
                });
            } else {
                show_area(categoryarea);
            }
        } else {
            $('.areas, .area').slideUp('fast', function(){
                $('.area:visible').find('select').prop('selectedIndex', 0);
            });
        }
    };

    $('#inquiry-form input[name="category"]').on('change', function(){
        var $this = $(this);
        select_category($this);
    });

    // If a category is checked at pageload, do the selection stuff
    if ( $('#inquiry-form input[name="category"]:checked').length > 0 ) {
        select_category($('#inquiry-form input[name="category"]:checked'));
    }

    // Style option labels when the option gets focus
    $('#inquiry-form .option input').on('focus', function() {
        $('#inquiry-form .option label').removeClass('hover');
        $(this).parents('label').addClass('hover');
    });

    // Show the specific area for the selected category
    var show_area = function(categoryarea) {
        // Get the ID of the previously selected area
        var oldarea = $('.area:visible').attr('id');

        if ($('#'+oldarea).length > 0) {
            $('#'+oldarea).fadeOut('fast', function(){
                $('#'+categoryarea).fadeIn('fast', function(){
                    $(this).find('select').attr('required', true).focus();
                });
                $('#'+oldarea).find('select').prop('selectedIndex', 0).attr('required', false);
            });
        } else {
            $('#'+categoryarea).fadeIn('fast');
        }
    };

    // Fake focus styles for styled selects
    $('.select select').on('focus', function(){
        $(this).parent('.select').addClass('focus');
    });

    $('.select select').on('blur', function(){
        $(this).parent('.select').removeClass('focus');
    });

    // Info tooltips
    $('#inquiry-form .info').on('mouseenter focus', function() {
        var $this = $(this);
        // Get the target element's ID from the link's href.
        var target = $(this).attr('href').replace( /.*?(#.*)/g, "$1" );
        $('<div class="tooltip arrow-top">'+ $(target + ' p').text() +'</div>').insertAfter($this).fadeIn('fast');
    });

    $('#inquiry-form .info').on('mouseleave blur', function() {
        var $this = $(this);
        var tooltip = $this.parents('.option').find('.tooltip');
        tooltip.delay(100).fadeOut('fast', function() {
            tooltip.remove();
        });
    });

    $('#inquiry-form .info').on('click', function(e) {
        e.preventDefault();
    });

})(window.jQuery);
