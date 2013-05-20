/*
 * jQuery Plus Slider 1.4.7
 * By Jamy Golden
 * http://css-plus.com
 * @jamygolden
 *
 * Regarding licensing read license.txt. 
 * tl;dr MIT
 */
( function( $ ) {

    $.plusSlider = function( el, options ) {

        // To avoid scope issues, use 'base' instead of 'this'
        // To reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $( el );
        base.el = el;

        // Add a reverse reference to the DOM object
        base.$el.data('plusSlider', base);
        
        base.init = function () {

            base.options = $.extend( {}, $.plusSlider.defaults, options );
            base.$el.addClass('plusslider-container').wrap('<div class="plusslider plusslider-' + base.$el.attr('id') + '" />');
            base.$wrap                  = base.$el.parent();              // References the .plusslider jQuery object
            base.$slides                = base.$el.children();            // References all slide jQuery slide objects
            base.$slideCloneFirst;                                        // First clone needed for infinite slide
            base.$slideCloneLast;                                         // Last clone needed for infinite slide
            base.$wrapContainer         = base.$wrap.parent();            // References the jQuery object of .plusSlider's container - This object isn't part of PlusSlider
            base.slideCount             = base.$slides.length;            // A numerical value of the amount of slides
            base.slideIndexCount        = base.slideCount - 1;            // The index value of the amount of slides
            base.sliderWidth            = 0;                              //Stores the slider width value. This changes on resize if fullWidth is enableds
            base.animating              = false;                          // Boolean - true means the slider is busy animating.
            base.wrapContainerWidth     = base.$wrapContainer.width();    // A numerical value of the width of base.$wrapContainer
            base.wrapContainerHeight    = base.$wrapContainer.height();   // A numerical value of the height of base.$wrapContainer
            base.currentSlideIndex      = base.options.defaultSlide;      // References the index number of the current slide
            base.$currentSlide          = base.$slides.eq( base.currentSlideIndex ); // References the current/active slide's jQuery object
            base.currentSlideWidth      = base.$currentSlide.outerWidth(); // References a numerical value of the width of the current/active slide
            base.currentSlideHeight     = base.$currentSlide.outerHeight(); // References a numerical value of the height of the current/active slide

            // base.functions
            base.calculateSliderWidth = function() {

                for ( var i = 0; i < base.slideCount; i++ ) {
                    if ( i == 0 ) base.sliderWidth = 0;
                    base.sliderWidth += base.$slides.eq( i ).outerWidth();
                };

                if ( base.options.infiniteSlide ) {
                    base.sliderWidth += base.$slides.eq(0).outerWidth();
                    base.sliderWidth += base.$slides.eq(base.slideIndexCount).outerWidth();
                }

            }; // base.calculateSliderWidth

            base.beginTimer = function() {

                base.timer = window.setInterval( function () {
                    base.toSlide('next');
                }, base.options.displayTime);

            }; // base.beginTimer

            base.clearTimer = function() {
                
                if ( base.timer) { // If the timer is set, clear it
                    window.clearInterval(base.timer);
                };

            }; // base.clearTimer

            base.setSliderDimensions = function() {

                // Set values
                base.calculateSliderWidth();
                base.currentSlideWidth  = base.$currentSlide.outerWidth();
                base.currentSlideHeight = base.$currentSlide.outerHeight();
                // Values Set
                
                if ( base.options.fullWidth ) {

                    base.sliderWidth = base.wrapContainerWidth * base.slideCount;
                    if ( base.options.infiniteSlide == true ) {
                        base.sliderWidth = base.wrapContainerWidth * base.slideCount + 2;
                    }
                    base.wrapContainerWidth = base.$wrapContainer.width();

                    base.$slides.width( base.wrapContainerWidth );

                    if ( base.options.infiniteSlide ) {
                        base.$slideCloneFirst.width( base.wrapContainerWidth );
                        base.$slideCloneLast.width( base.wrapContainerWidth );
                    }

                    base.calculateSliderWidth();

                    base.$wrap.width( base.wrapContainerWidth ).height( base.currentSlideHeight );
                    base.$el.width( base.sliderWidth ).height( base.currentSlideHeight ).css('left', base.$currentSlide.position().left * -1 + 'px');

                } else {

                    // Set wrapper dimensions to equal the slide
                    base.$wrap.width( base.currentSlideWidth ).height( base.currentSlideHeight );

                }

            }; // base.setSliderDimensions

            base.toSlide = function( slide ) {

                if ( base.animating == false ) {

                    // Set values
                    base.animating = true;
                    // Values set

                    // Handling of slide values
                    var lastSlideIndex = base.currentSlideIndex;
                    if ( slide === 'next' || slide === '' ) {
                        base.currentSlideIndex += 1;
                    } else if ( slide === 'prev' ) {
                        base.currentSlideIndex -= 1;
                    } else {
                        base.currentSlideIndex = parseInt(slide);
                    }
                    // End Handling of slide values

                    // Disable first and last buttons on the first and last slide respectively
                    if ( ( base.options.disableLoop == 'first' || base.options.disableLoop == 'both' && base.currentSlideIndex < 0 ) || ( base.options.disableLoop == 'last' || base.options.disableLoop == 'both' && base.currentSlideIndex > base.slideIndexCount )) {
                         return;
                    }  // End Disable first and last buttons on the first and last slide respectively

                    // Handle possible slide values
                    if ( base.currentSlideIndex > base.slideIndexCount ) {
                        base.currentSlideIndex = 0;
                    } else if ( base.currentSlideIndex < 0 ) {
                        base.currentSlideIndex = base.slideIndexCount;
                    }; // Handle possible slide values

                    // Set values
                    base.$currentSlide      = base.$slides.eq( base.currentSlideIndex );
                    base.currentSlideWidth  = base.$currentSlide.width();
                    base.currentSlideHeight = base.$currentSlide.height();
                    // Values set

                    // onSlide callback
                    if ( base.options.onSlide && typeof( base.options.onSlide ) == 'function' ) base.options.onSlide( base );
                    // End onSlide callback

                    if ( base.options.createPagination ) {
                        base.$sliderControls.find('li').removeClass('current').eq( base.currentSlideIndex ).addClass('current');
                    }; // base.options.createPagination

                    if ( base.options.sliderType == 'slider' ) {

                        var toPosition = base.$currentSlide.position().left; // Position for slider position to animate to next

                        // Edit animation position to achieve the infinite slide effect
                        if ( base.options.infiniteSlide === true ) {
                            if ( base.currentSlideIndex == 0 && slide == 'next') { // only animate to the clone if toSlide('next') is run.
                                toPosition = base.$slideCloneFirst.position().left;
                            } else if ( base.currentSlideIndex == base.slideIndexCount && slide == 'prev') { // only animate to the clone if toSlide('prev') is run.
                                toPosition = base.$slideCloneLast.position().left;
                            };
                        };

                        // Animate slide position
                        base.$el.animate({
                            height: base.$currentSlide.outerHeight(),
                            left: toPosition * -1 + 'px'
                        }, base.options.speed, base.options.sliderEasing, function() {

                            if ( base.currentSlideIndex == 0 ) {
                                base.$el.css('left', base.$slides.eq(0).position().left * -1);
                            } else if ( base.currentSlideIndex == base.slideIndexCount ) {
                                base.$el.css('left', base.$slides.eq(base.slideIndexCount).position().left * -1);
                            }

                            base.endToSlide();

                        });

                    // End slider

                    } else { 
                
                    // Begin Fader

                        if (lastSlideIndex !== base.currentSlideIndex) {
                            base.$slides.eq( lastSlideIndex ).fadeOut(base.options.speed);
                        }
                        
                        base.$slides.eq( base.currentSlideIndex ).fadeIn(base.options.speed, function() {

                            base.endToSlide();

                        });

                    }; // if sliderType slider/fader

                    // Animate wrapper size (for gradual transition between slides of differing sizes)
                    base.$wrap.animate({
                        height: base.$currentSlide.outerHeight(),
                        width: base.$currentSlide.outerWidth()
                    }, base.options.speed, base.options.sliderEasing);

                    // Set class on new "current" slide
                    base.$slides.removeClass('current').eq( base.currentSlideIndex ).addClass('current');

                }; // Don't slide while animated

                // Clear Timer
                if ( base.options.autoPlay ) {

                    base.clearTimer();
                    base.beginTimer();

                }; // if base.options.autoPlay 

            }; // base.toSlide

            base.endToSlide = function() { // perform cleanup operations after toSlide transition has finished (for both slider and fader type)

                base.animating = false;

                // afterSlide and onSlideEnd callback
                if ( base.options.afterSlide && typeof( base.options.afterSlide ) == 'function' ) base.options.afterSlide( base );
                if ( base.options.onSlideEnd && typeof( base.options.onSlideEnd ) == 'function' && base.currentSlideIndex == base.slideIndexCount ) base.options.onSlideEnd( base );
                // End afterSlide and onSlideEnd callback

            }; // base.endToSlide

            ////////////////////////////////////////////////////////////////////////////// End of methods

            // Handle dependant options
                if ( base.slideCount === 1 ) {

                    base.options.autoPlay = false;
                    base.options.createArrows = false;
                    base.options.createPagination = false;

                }; // base.slideCount === 1

                if ( base.options.sliderType == 'fader' ) {
                    base.$slides.not('.current').hide(); // Hide non-active slides
                    base.options.infiniteSlide = false;
                    base.options.fullWidth = false;
                }
        
            // DOM manipulations

                base.$slides.addClass('child').eq( base.currentSlideIndex ).addClass('current');

                // infinite Slide
                if ( base.options.infiniteSlide === true ) {
                    base.$slides.css('display', 'block'); //override no-js fallback in CSS that hides non-first slides (otherwise infiniteSlide effect won't work when moving backwards from first to last slide)
                    base.$slideCloneFirst = base.$slides.first().clone().addClass('plusslider-clone').removeClass('current').insertAfter( base.$slides.eq(base.slideIndexCount) );
                    base.$slideCloneLast = base.$slides.last().clone().addClass('plusslider-clone').insertBefore( base.$slides.eq(0) );
                }

                base.setSliderDimensions();

                // Set values
                base.currentSlideWidth  = base.$currentSlide.outerWidth();
                base.currentSlideHeight = base.$currentSlide.outerHeight();
                // Values set

                // Slider/Fader Settings
                if ( base.options.sliderType == 'slider' ) {

                    base.calculateSliderWidth();

                    base.$wrap.addClass('plustype-slider').find( base.$el ).width( base.sliderWidth );

                    if ( base.options.fullWidth ) {

                        base.setSliderDimensions();
                    
                        $(window).resize( function () {

                            // Reset timer
                            if ( base.options.autoPlay ) {
                                base.clearTimer();
                                base.beginTimer();
                            }; // if base.options.autoPlay 

                            // Reset dimensions
                            base.setSliderDimensions();

                        }); // window.resize
          
                    }; // base.options.fullWidth

                    base.$slides.show();
                    base.$el.css( 'left', base.$currentSlide.position().left * -1 + 'px' );

                } else {

                    base.$wrap.addClass('plustype-fader');
                    base.$slides.eq(0).show();

                }; // base.options.sliderType

                // Begin pagination
                if ( base.options.createPagination ) {

                    base.$sliderControls = $('<ul />', {
                        'class': 'plusslider-pagination'
                    });

                    switch (base.options.paginationPosition) {

                        case 'before':
                            base.$sliderControls.insertBefore( base.$wrap );
                            break;

                        case 'prepend':
                            base.$sliderControls.prependTo( base.$wrap );
                            break;

                        case 'after':
                            base.$sliderControls.insertAfter( base.$wrap );
                            break;

                        default: //'append'
                            base.$sliderControls.appendTo( base.$wrap );
                            break;

                    }

                    base.$sliderControls.wrap('<div class="plusslider-pagination-wrapper" />');

                    // Create Pagination
                    for ( var i = 0; i < base.slideCount; i++ ) {

                        $('<li />', {
                            'data-index': i,
                            text: (typeof base.$slides.eq( i ).attr('data-title') === 'undefined') ? i + 1 : base.$slides.eq( i ).attr('data-title')
                        }).appendTo(base.$sliderControls);

                    }; // Pagination appended

                    // Dynamic pagination width
                    if ( base.options.paginationWidth ) base.$sliderControls.width( base.$sliderControls.find('li').outerWidth(true) * base.slideCount );

                    // Pagination functionality
                    base.$sliderControls.find('li').click( function( ) {

                        var controlIndex = $(this).index();
                        base.toSlide( controlIndex );

                    }).eq( base.currentSlideIndex ).addClass('current'); 
                    // base.$sliderControls.find('li').click

                }; // End settings.pagination

                // Create Arrows
                if ( base.options.createArrows ) {

                    base.$arrows = $('<ul />', {
                        'class': 'plusslider-arrows'
                    });

                    switch (base.options.arrowsPosition) {

                        case 'before':
                            base.$arrows.insertBefore( base.$wrap );
                            break;

                        case 'append':
                            base.$arrows.appendTo( base.$wrap );
                            break;

                        case 'after':
                            base.$arrows.insertAfter( base.$wrap );
                            break;

                        default: //'prepend'
                            base.$arrows.prependTo( base.$wrap );
                            break;

                    }

                    base.$arrows.wrap('<div class="plusslider-arrows-wrapper" />');

                    // Prepend Next Arrow
                    $('<li />', {
                        'class': 'next',
                        text: base.options.nextText
                    }).prependTo( base.$arrows );

                    // Prepend Previous Arrow
                    $('<li />', {
                        'class': 'prev',
                        text: base.options.prevText
                    }).prependTo( base.$arrows );

                    base.$arrows.find('.next').click( function() {
                        base.toSlide('next');
                    }); // .next.click

                    base.$arrows.find('.prev').click( function() {
                        base.toSlide('prev');
                    }); // prev.click

                }; // base.options.createArrows

                // base.options.autoPlay
                if ( base.options.autoPlay ) {

                    base.beginTimer();

                    // Pause on hover
                    if ( base.options.pauseOnHover) {

                        base.$el.hover( function () {
                            base.clearTimer();
                        }, function() {
                            base.beginTimer();
                        }); // base.$el.hover

                    }; //  base.options.pauseOnHover

                }; // base.options.autoPlay
                
                // Keyboard navigation
                if ( base.options.keyboardNavigation ) {

                    base.$el.click( function () {
                        $('.active-plusslider').removeClass('active-plusslider');
                        $(this).addClass('active-plusslider');

                    });

                    $(window).keyup( function ( e ) {

                        if ( base.$el.is('.active-plusslider') ) {
                            if ( e.keyCode == 39 ) { // Right arrow
                                base.toSlide('next');
                            } else if ( e.keyCode == 37 ) { // Left arrow
                                base.toSlide('prev');
                            }; // e.keyCode
                        }; // if is .active-plusslider

                    }); // window.keyup

                }; // base.options.keyboardNavigation
                
            // onInit callback
                if ( base.options.onInit && typeof( base.options.onInit ) == 'function' ) base.options.onInit( base );

        }; // base.init

        // Run initializer
        base.init();

    };

    $.plusSlider.defaults = {

        /* General */
        sliderType          : 'slider', // Choose whether the carousel is a 'slider' or a 'fader'
        infiniteSlide       : true, // Gives the effect that the slider doesn't ever "repeat" and just continues forever
        disableLoop         : false, // Disables prev or next buttons if they are on the first or last slider respectively. 'first' only disables the previous button, 'last' disables the next and 'both' disables both
        fullWidth           : false, // sets the width of the slider to 100% of the parent container
        
        /* Display related */
        defaultSlide        : 0, // Sets the default starting slide - Number based on item index
        displayTime         : 4000, // The amount of time the slide waits before automatically moving on to the next one. This requires 'autoPlay: true'
        sliderEasing        : 'linear', // Anything other than 'linear' and 'swing' requires the easing plugin
        speed               : 500, // The amount of time it takes for a slide to fade into another slide

        /* Functioanlity related */
        autoPlay            : true, // Creats a times, looped 'slide-show'
        keyboardNavigation  : true, // The keyboard's directional left and right arrows function as next and previous buttons
        pauseOnHover        : true, // AutoPlay does not continue ifsomeone hovers over Plus Slider.

        /* Arrow related */
        createArrows        : true, // Creates forward and backward navigation
        arrowsPosition      : 'prepend', //Where to insert arrows in relation to the slider ('before', 'prepend', 'append', or 'after')
        nextText            : 'Next', // Adds text to the 'next' trigger
        prevText            : 'Previous', // Adds text to the 'prev' trigger

        /* Pagination related */
        createPagination    : true, // Creates Numbered pagination
        paginationPosition  : 'append', // Where to insert pagination in relation to the slider element ('before', 'prepend', 'append', or 'after')
        paginationWidth     : false, // Automatically gives the pagination a dynamic width

        /* Callbacks */
        onInit              : null, // Callback function: On slider initialize
        onSlide             : null, // Callback function: As the slide starts to animate
        afterSlide          : null, // Callback function: As the slide completes the animation
        onSlideEnd          : null // Callback function: Once the slider reaches the last slide

    }; // $.plusSlider

    $.fn.plusSlider = function(options) {

        return this.each( function () {
            (new $.plusSlider(this, options));
        }); // this.each

    }; // $.fn.plusSlider

})(jQuery);
