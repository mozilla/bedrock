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

    // Style selected option, unstyle previously selected
    $('#inquiry-form .option input').on('change', function() {
        $('#inquiry-form .option label').removeClass('selected');
        $(this).parents('label').addClass('selected');
    });

    // Style option labels when the option gets focus
    $('#inquiry-form .option input').on('focus', function() {
        $('#inquiry-form .option label').removeClass('hover');
        $(this).parents('label').addClass('hover');
    });

    // Show 'other ways to contribute' block on thankyou page
    $('.cta-other a').on('click', function(e) {
        e.preventDefault();
        $('.cta-other').fadeOut('fast', function() {
            $('#other').slideDown();
        });
    });

    // Style the selected option if one is selected when the page loads
    $('#inquiry-form .option input:checked').parents('label').addClass('selected');

    $('#inquiry-form input[name="category"]').on('change', function(){
        var $this = $(this);

        // Style the selected option (reset all of them first to unstyle previous selection)
        $('#inquiry-form .option label').removeClass('selected');
        $this.parents('label').addClass('selected');

        // Get all the area IDs
        var areas = $('#inquiry-form .area').map(function(index){ return this.id; });
        // Get the area for the selected category
        var categoryarea = 'area-' + $this.attr('value');

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
    });

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



/* // Info modal with navigation. Might need this later...

    var ltr = document.dir === 'ltr';

    // Set up the modal navigation
    var modal_paging = function(direction) {
        // get the current blurb
        var $current = $('.info-content:visible');
        var action;

        if (direction === 1) {
            action = 'modal next';
            // Fade out the current blurb
            $current.fadeOut('fast', function(){
                // Get the next blurb and fade it in; it becomes the new current blurb.
                $current = $current.next('.info-content').length ? $current.next('.info-content').fadeIn() : $current.siblings('.info-content:first').fadeIn();
                // Reset the nav
                $('.category-nav .current').removeClass('current');
                // Highlight the new current blurb's icon
                $('.category-nav a[href="#' + $current.attr('id') + '"]').addClass('current');
            });
        } else {
            action = 'modal prev';
            // Fade out the current blurb
            $current.fadeOut('fast', function(){
                // Get the previous blurb and fade it in; it becomes the new current blurb.
                $current = $current.prev('.info-content').length ? $current.prev('.info-content').fadeIn() : $current.siblings('.info-content:last').fadeIn();
                // Reset the nav
                $('.category-nav .current').removeClass('current');
                // Highlight the new current blurb's icon
                $('.category-nav a[href="#' + $current.attr('id') + '"]').addClass('current');
            });
        }
    };

    // Set up the modal
    $('#inquiry-form .info').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);
        var target = $(this).attr('href').replace( /.*?(#.*)/g, "$1" );// Extract the target element's ID from the link's href.

        Mozilla.Modal.createModal(this, $('.category-info'), {
            title: $('.category-info h2').text(),
            'onCreate': function () {
                // Hide all blurbs to reset
                $('.info-content').hide();
                // Show the target blurb
                $(target).show();

                // Reset the nav
                $('.category-nav .current').removeClass('current');
                // Highlight the target blurb's icon
                $('.category-nav a[href="' + target + '"]').addClass('current');

                // Add the prev/next buttons
                var $paging = $('<nav class="modal-nav" role="presentation"></nav>').insertBefore('#modal-close');
                $('<button class="button-prev" aria-controls="modal"></button>')
                    .text(window.trans('global-previous')).appendTo($paging);
                $('<button class="button-next" aria-controls="modal"></button>')
                    .text(window.trans('global-next')).appendTo($paging);

                $paging.on('click', 'button', function() {
                    modal_paging($(this).hasClass('button-prev') ? -1 : 1);
                });
            }
        });
    });

    $('.category-nav a').on('click', function(e){
        e.preventDefault();

        // get the current blurb
        var $current = $('.info-content:visible');

        var $this = $(this);
        var target = $(this).attr('href').replace( /.*?(#.*)/g, "$1" );// Extract the target element's ID from the link's href.

        // Hide all blurbs to reset
        $current.fadeOut('fast', function(){
            // Show the target blurb
            $(target).fadeIn();
        });

        // Reset the nav
        $('.category-nav a').removeClass('current');
        // Highlight the new current blurb's icon
        $this.addClass('current');
    });

    // Set up keyboard shortcuts for the modal
    $(document).on('keydown', '#modal', function(event) {
        var direction = 0;

        switch (event.keyCode) {
            case 37: // Left arrow
                direction = ltr ? -1 : 1;
                break;
            case 38: // Up arrow
                direction = -1;
                break;
            case 39: // Right arrow
                direction = ltr ? 1 : -1;
                break;
            case 40: // Down arrow
                direction = 1;
                break;
        }

        if (direction) {
            event.preventDefault();
            nav_modal(direction);
        }
    });
*/


})(window.jQuery);
