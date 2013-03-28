// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Slider class
DOWNLOADTAB.classes.Slider = (function (singleton) {
    function Slider($, selector) {
        singleton.classes.Base.call(this);

        this.$ = $;

        this._initData = undefined;

        // Cache
        this.cache = {
            slider: this.$(selector),
            items: this.$(selector).find('li')
        };

        // Initialize slider
        this.init();
    }

    // Initialize Base object and set correct constructor
    Slider.prototype = new singleton.classes.Base();
    Slider.prototype.constructor = Slider;

    // Class methods
    Slider.prototype.init = function() {
        var self = this;

        self.cache.slider.find('.next').on('click', function() {
            self.cycle('next');
        });
        self.cache.slider.find('.prev').on('click', function() {
            self.cycle('prev');
        });
    };

    Slider.prototype.cycle = function (direction) {
        var self = this;
        var visible = self.cache.items.not('.visuallyhidden');
        var animation;

        // Hide them all
        self.cache.items.removeClass().addClass('visuallyhidden');

        // Decide which animation we're gonna use.
        if (direction === 'next') {
            animation = 'fadeInRight';
        } else {
            animation = 'fadeInLeft';
        }

        if (visible[direction]().length !== 0) {
            visible[direction]()
                .removeClass()
                .addClass('animated ' + animation);
        } else {
            if (direction === 'next') {
                self.cache.items.first()
                    .removeClass()
                    .addClass('animated fadeInRight');
            } else {
                self.cache.items.last()
                    .removeClass()
                    .addClass('animated fadeInLeft');
            }
        }
    };

    return Slider;
} (DOWNLOADTAB));
