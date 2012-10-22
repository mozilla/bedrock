/**
 * jquery.gridrotator.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2012, Codrops
 * http://www.codrops.com
 */

;( function( $, window, undefined ) {
	
	'use strict';

	// http://www.hardcode.nl/subcategory_1/article_317-array-shuffle-function
	Array.prototype.shuffle = function() {
		var i=this.length,p,t;
		while (i--) {
			p = Math.floor(Math.random()*i);
			t = this[i];
			this[i]=this[p];
			this[p]=t;
		}
		return this;
	};

	/*
	* debouncedresize: special jQuery event that happens once after a window resize
	*
	* latest version and complete README available on Github:
	* https://github.com/louisremi/jquery-smartresize/blob/master/jquery.debouncedresize.js
	*
	* Copyright 2011 @louis_remi
	* Licensed under the MIT license.
	*/
	var $event = $.event,
	$special,
	resizeTimeout;

	$special = $event.special.debouncedresize = {
		setup: function() {
			$( this ).on( "resize", $special.handler );
		},
		teardown: function() {
			$( this ).off( "resize", $special.handler );
		},
		handler: function( event, execAsap ) {
			// Save the context
			var context = this,
				args = arguments,
				dispatch = function() {
					// set correct event type
					event.type = "debouncedresize";
					$event.dispatch.apply( context, args );
				};

			if ( resizeTimeout ) {
				clearTimeout( resizeTimeout );
			}

			execAsap ?
				dispatch() :
				resizeTimeout = setTimeout( dispatch, $special.threshold );
		},
		threshold: 50
	};

	// global
	var $window				= $( window ),
		Modernizr			= window.Modernizr;

	$.GridRotator			= function( options, element ) {
		
		this.$el	= $( element );
		if( Modernizr.backgroundsize ) {

			var _self = this;
			this.$el.addClass( 'ri-grid-loading' );

			$( '<img/>' ).load( function() {

				_self._init( options );

			} ).attr( 'src', '/media/img/mosaic/loading.gif' );

		}
		
	};

	$.GridRotator.defaults	= {
		// number of rows
		rows			: 4,
		// number of columns 
		columns			: 10,
		w1024			: {
			rows	: 3,
			columns	: 8
		},
		w768			: {
			rows	: 3,
			columns	: 7
		},
		w480			: {
			rows	: 3,
			columns	: 5
		},
		w320			: {
			rows	: 2,
			columns	: 4
		},
		w240			: {
			rows	: 2,
			columns	: 3
		},
		// step: number of items that are replaced at the same time
		// random || [some number]
		// note: for performance issues, the number "can't" be > options.maxStep
		step			: 'random',
		maxStep			: 3,
		// prevent user to click the items
		preventClick	: true,
		// animation type
		// showHide || fadeInOut || slideLeft || 
		// slideRight || slideTop || slideBottom || 
		// rotateLeft || rotateRight || rotateTop || 
		// rotateBottom || scale || rotate3d || 
		// rotateLeftScale || rotateRightScale || 
		// rotateTopScale || rotateBottomScale || random
		animType		: 'random',
		// animation speed
		animSpeed		: 500,
		// animation easings
		animEasingOut	: 'linear',
		animEasingIn	: 'linear',
		// the item(s) will be replaced every 3 seconds
		// note: for performance issues, the time "can't" be < 300 ms
		interval		: 3000
	};

	$.GridRotator.prototype	= {

		_init				: function( options ) {

			var _self			= this;
			
			// options
			this.options		= $.extend( true, {}, $.GridRotator.defaults, options );

			// all types of animations
			this.animTypesAll	= [ 'fadeInOut', 'slideLeft', 'slideRight', 'slideTop', 'slideBottom', 'rotateLeft', 'rotateRight', 'rotateTop', 'rotateBottom', 'scale', 'rotate3d', 'rotateLeftScale', 'rotateRightScale', 'rotateTopScale', 'rotateBottomScale' ];
			// types of animations for "older" browsers
			this.animTypesCond	= [ 'fadeInOut', 'slideLeft', 'slideRight', 'slideTop', 'slideBottom' ];

			// array containing the animation types to choose from when the options.animType is set to 'random'
			this.animTypes		= this.animTypesCond;
			if( Modernizr.csstransforms3d ) {

				this.animTypes = this.animTypesAll;

			}

			this.animType		= this.options.animType;
			if( this.animType !== 'random' ) {

				if( !Modernizr.csstransforms3d && $.inArray( this.animType, this.animTypesCond ) === -1 && this.animType !== 'showHide' ) {

					// fallback to 'fadeInOut' if user sets a type which is not supported
					this.animType = 'fadeInOut';

				}

			}
			this.animTypesTotal	= this.animTypes.length;

			// the <ul> where the items are placed
			this.$list			= this.$el.children( 'ul' );
			// remove img's and add background-image to anchors
			// preload the images before
			var loaded			= 0,
				$imgs			= this.$list.find( 'img' ),
				count			= $imgs.length;

			$imgs.each( function() {

				var $img	= $( this ),
					src		= $img.attr( 'src' );

				$( '<img/>' ).load( function() {

					++loaded;
					$img.parent().css( 'background-image', 'url(' + src + ')' );
					if( loaded === count ) {

						$imgs.remove();
				 
						_self.$el.removeClass( 'ri-grid-loading' );

			// the items
						_self.$items		= _self.$list.children( 'li' );
			// make a copy of the items
						_self.$itemsCache	= _self.$items.clone();
			// total number of items
						_self.itemsTotal	= _self.$items.length;
			// the items that will be out of the grid
			// actually the item's child (anchor element)
						_self.outItems		= [];

						_self._layout();
						_self._initEvents();
			// replace "options.step" items after "options.interval" time
			// the items that go out are randomly chosen, while the ones that get in
			// respect the order (first in first out)
						_self._start();

					}

				} ).attr( 'src', src )
				 
			} );

		},
		_layout				: function( callback ) {

			var _self		= this;

			// sets the grid dimentions based on the container's width
			this._setGridDim();

			// reset
			this.$list.empty();
			this.$items		= this.$itemsCache.clone().appendTo( this.$list );
			
			var $outItems	= this.$items.filter( ':gt(' + ( this.showTotal - 1 ) + ')' ),
				$outAItems	= $outItems.children( 'a' );

			this.outItems.length = 0;

			$outAItems.each( function( i ) {

				_self.outItems.push( $( this ) );

			} );

			$outItems.remove();

				// container's width
			var containerWidth	= ( document.defaultView ) ? parseInt( document.defaultView.getComputedStyle( this.$el.get( 0 ), null ).width ) : this.$el.width(),
				// item's width
				itemWidth		= Math.floor( containerWidth / this.columns ),
				// calculate gap
				gapWidth		= containerWidth - ( this.columns * Math.floor( itemWidth ) );

			for( var i = 0; i < this.rows; ++i ) {

				for( var j = 0; j < this.columns; ++j ) {

					var $item	= this.$items.eq( this.columns * i + j ),
						h		= itemWidth,
						w		= ( j < Math.floor( gapWidth ) ) ? itemWidth + 1 : itemWidth;

					$item.css( {
						width	: w,
						height	: h
					} );

					
/*
					if( gapWidth % 1 !== 0 && j === this.columns - 1 ) {

						$item.children( 'a' ).css( {
							width	: '+=1',
							height	: '+=1'
						} );

					}
*/
					

				}

			}

			if( this.options.preventClick ) {

				this.$items.children().css( 'cursor', 'default' ).on( 'click.gridrotator', false );

			}

			if( callback ) {

				callback.call();

			}

		},
		// set the grid rows and columns
		_setGridDim			: function() {

			// container's width
			var c_w			= this.$el.width();

			// we will choose the number of rows/columns according to the container's width and the values set on the plugin options 
			switch( true ) {

				case ( c_w < 240 )	: this.rows = this.options.w240.rows; this.columns = this.options.w240.columns; break;
				case ( c_w < 320 )	: this.rows = this.options.w320.rows; this.columns = this.options.w320.columns; break;
				case ( c_w < 480 )	: this.rows = this.options.w480.rows; this.columns = this.options.w480.columns; break;
				case ( c_w < 768 )	: this.rows = this.options.w768.rows; this.columns = this.options.w768.columns; break;
				case ( c_w < 1024 )	: this.rows = this.options.w1024.rows; this.columns = this.options.w1024.columns; break;
				default				: this.rows = this.options.rows; this.columns = this.options.columns; break;

			}

			this.showTotal	= this.rows * this.columns;

		},
		// init window resize event
		_initEvents			: function() {

			var _self = this;

			$window.on( 'debouncedresize.gridrotator', function( event ) {

				clearTimeout( _self.playtimeout );

				_self._layout( function() {

					_self._start();

				} );
				
			} );

		},
		// start rotating elements
		_start				: function() {

			if( this.showTotal < this.itemsTotal ) {

				this._showNext();

			}

		},
		// get which type of animation
		_getAnimType		: function() {

			if( this.animType === 'random' ) {

				return this.animTypes[ Math.floor( Math.random() * this.animTypesTotal ) ];

			}
			else {

				return this.animType;

			}

		},
		// get css properties for the transition effect
		_getAnimProperties 	: function( $in, $out ) {

			var startInProp		= {},
				startOutProp	= {},
				endInProp		= {},
				endOutProp		= {},

				animType		= this._getAnimType(),
				speed;

			switch( animType ) {

				case 'showHide'	:
					speed = 0;
					
					endOutProp.opacity	= 0;
					
					break;
				case 'fadeInOut'	:
					endOutProp.opacity	= 0;
					
					break;
				case 'slideLeft'	:
					startInProp.left 	= $out.width();
					
					endInProp.left		= 0;
					endOutProp.left		= -$out.width();
					
					break;
				case 'slideRight'	:
					startInProp.left 	= -$out.width();
					
					endInProp.left		= 0;
					endOutProp.left		= $out.width();
					
					break;
				case 'slideTop'		:
					startInProp.top 	= $out.height();
					
					endInProp.top		= 0;
					endOutProp.top		= -$out.height();
					
					break;
				case 'slideBottom'	:
					startInProp.top 	= -$out.height();
					
					endInProp.top		= 0;
					endOutProp.top		= $out.height();
					
					break;
				case 'rotateLeft'	:
					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateY		= '90deg';
					
					endInProp.rotateY		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateY		= '-90deg';
					
					break;
				case 'rotateRight'	:
					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateY		= '-90deg';
					
					endInProp.rotateY		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateY		= '90deg';
					
					break;
				case 'rotateTop'	:
					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateX		= '90deg';
					
					endInProp.rotateX		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateX		= '-90deg';
					
					break;
				case 'rotateBottom'	:
					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateX		= '-90deg';
					
					endInProp.rotateX		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateX		= '90deg';
					
					break;
				case 'scale'		:
					speed					= this.options.animSpeed / 2;
					
					startInProp.scale		= '0';
					startOutProp.scale		= '1';
					
					endInProp.scale			= '1';
					endInProp.delay			= speed;
					endOutProp.scale		= '0';
					
					break;
				case 'rotateLeftScale'	:
					startInProp.scale		= '0.3';
					startOutProp.scale		= '1';
					endInProp.scale			= '1';
					endOutProp.scale		= '0.3';

					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateY		= '90deg';
					
					endInProp.rotateY		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateY		= '-90deg';
					
					break;
				case 'rotateRightScale'	:
					startInProp.scale		= '0.3';
					startOutProp.scale		= '1';
					endInProp.scale			= '1';
					endOutProp.scale		= '0.3';

					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateY		= '-90deg';
					
					endInProp.rotateY		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateY		= '90deg';
					
					break;
				case 'rotateTopScale'	:
					startInProp.scale		= '0.3';
					startOutProp.scale		= '1';
					endInProp.scale			= '1';
					endOutProp.scale		= '0.3';

					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateX		= '90deg';
					
					endInProp.rotateX		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateX		= '-90deg';
					
					break;
				case 'rotateBottomScale'	:
					startInProp.scale		= '0.3';
					startOutProp.scale		= '1';
					endInProp.scale			= '1';
					endOutProp.scale		= '0.3';

					speed					= this.options.animSpeed / 2;
					
					startInProp.rotateX		= '-90deg';
					
					endInProp.rotateX		= '0deg';
					endInProp.delay			= speed;
					endOutProp.rotateX		= '90deg';
					
					break;
				case 'rotate3d'		:
					speed					= this.options.animSpeed / 2;
					
					startInProp.rotate3d	= '1, 1, 0, 90deg';
					
					endInProp.rotate3d		= '1, 1, 0, 0deg';
					endInProp.delay			= speed;
					endOutProp.rotate3d		= '1, 1, 0, -90deg';
					
					break;

			}

			var animSpeed = ( speed != undefined ) ? speed : this.options.animSpeed;

			return {
				startInProp		: startInProp,
				startOutProp	: startOutProp,
				endInProp		: endInProp,
				endOutProp		: endOutProp,
				animSpeed		: animSpeed
			};

		},
		// show next "option.step" elements
		_showNext			: function( t ) {

			var _self = this;

			clearTimeout( this.playtimeout );

			this.playtimeout = setTimeout( function() {

				var step		= _self.options.step,
					max			= _self.options.maxStep,
					min			= 1;
				
				if( max > _self.showTotal ) {

					max = _self.showTotal;

				}

				var $items	= _self.$items, 
					outs	= [],
					// number of items to swith at this point of time
					nmbOut	= ( step === 'random' ) ? Math.floor( Math.random() * max + min ) : Math.min( Math.abs( step ) , max ) ,
					// array with random indexes. These will be the indexes of the items we will replace
					randArr	= _self._getRandom( nmbOut, _self.showTotal );
				
				for( var i = 0; i < nmbOut; ++i ) {

					// element to go out
					var $out = $items.eq( randArr[ i ] );

					// if element is active, which means it is currently animating,
					// then we need to get different positions.. 
					if( $out.data( 'active' ) ) {

						// one of the items is active, call again..
						_self._showNext( 1 );
						return false;

					}

					// add it to outs array
					outs.push( $out );

				}

				for( var i = 0; i < nmbOut; ++i ) {

					var $out		= outs[ i ],
						$outA		= $out.children( 'a:last' ),
						newElProp	= {
							width	: $outA.width(),
							height	: $outA.height()
						};

					// element stays active
					$out.data( 'active', true );

					// get the element (anchor) that will go in (first one inserted in _self.outItems)
					var $inA		= _self.outItems.shift();

					// save element that went out
					_self.outItems.push( $outA.clone() );
					
					// prepend in element
					$inA.css( newElProp ).prependTo( $out );

					var animProp	= _self._getAnimProperties( $inA, $outA );
					

					if( Modernizr.csstransitions ) {

						$inA.css( animProp.startInProp ).transition( animProp.endInProp, animProp.animSpeed, _self.options.animEasingIn );
						$outA.css( animProp.startOutProp ).transition( animProp.endOutProp, animProp.animSpeed, _self.options.animEasingOut, function() {

							$( this ).parent().data( 'active', false ).end().remove();

						} );
					
					}

					// fallback to jQuery animate
					else {

						$inA.css( animProp.startInProp ).stop().animate( animProp.endInProp, animProp.animSpeed );
						$outA.css( animProp.startOutProp ).stop().animate( animProp.endOutProp, animProp.animSpeed, function() {

							$( this ).parent().data( 'active', false ).end().remove();

						} )

					}

				}

				// again and again..
				_self._showNext();

			}, t || Math.max( Math.abs( this.options.interval ) , 300 ) );

		},
		_getRandom			: function( cnt, limit ) {

			var randArray = [];

			for( var i = 0; i < limit; ++i ) {

				randArray.push( i )

			}
			
			return randArray.shuffle().slice(0,cnt); 

		}

	};
	
	var logError		= function( message ) {

		if ( window.console ) {

			window.console.error( message );
		
		}

	};
	
	$.fn.gridrotator	= function( options ) {
		
		if ( typeof options === 'string' ) {
			
			var args = Array.prototype.slice.call( arguments, 1 );
			
			this.each(function() {
			
				var instance = $.data( this, 'gridrotator' );
				
				if ( !instance ) {

					logError( "cannot call methods on gridrotator prior to initialization; " +
					"attempted to call method '" + options + "'" );
					return;
				
				}
				
				if ( !$.isFunction( instance[options] ) || options.charAt(0) === "_" ) {

					logError( "no such method '" + options + "' for gridrotator instance" );
					return;
				
				}
				
				instance[ options ].apply( instance, args );
			
			});
		
		} 
		else {
		
			this.each(function() {
				
				var instance = $.data( this, 'gridrotator' );
				
				if ( instance ) {

					instance._init();
				
				}
				else {

					$.data( this, 'gridrotator', new $.GridRotator( options, this ) );
				
				}

			});
		
		}
		
		return this;
		
	};
	
} )( jQuery, window );

$(function() {

	$( '#mosaic' ).gridrotator( {
		rows		: 3,
		columns		: 15,
		animType	: 'fadeInOut',
		animSpeed	: 1000,
		interval	: 2000,
		step		: 1,
		w480		: {
			rows	: 2,
			columns	: 7
		},
		w320		: {
			rows	: 2,
			columns	: 5
		}
	} );

});