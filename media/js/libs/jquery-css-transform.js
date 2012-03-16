(function ($) {
    // Monkey patch jQuery 1.3.1+ css() method to support CSS 'transform'
    // property uniformly across Webkit/Safari/Chrome, Firefox 3.5+, and IE 9+.
    // 2009-2010 Zachary Johnson www.zachstronaut.com
    // Updated 2010.11.26
    function getTransformProperty(element)
    {
        // Try transform first for forward compatibility
        var properties = ['transform', 'WebkitTransform', 'MozTransform', 'msTransform', 'OTransform'];
        var p;
        while (p = properties.shift())
        {
            if (typeof element.style[p] != 'undefined')
            {
                return p;
            }
        }
        
        // Default to transform also
        return 'transform';
    }
    
    var proxied = $.fn.css;
    $.fn.css = function (arg, val)
    {
        // Find the correct browser specific property and setup the mapping using
        // $.props which is used internally by jQuery.attr() when setting CSS
        // properties via either the css(name, value) or css(properties) method.
        // The problem with doing this once outside of css() method is that you
        // need a DOM node to find the right CSS property, and there is some risk
        // that somebody would call the css() method before body has loaded or any
        // DOM-is-ready events have fired.
        if
        (
            typeof $.props['transform'] == 'undefined'
            &&
            (
                arg == 'transform'
                ||
                (
                    typeof arg == 'object'
                    && typeof arg['transform'] != 'undefined'
                )
            )
        )
        {
            $.props['transform'] = getTransformProperty(this.get(0));
        }
        
        // We force the property mapping here because jQuery.attr() does
        // property mapping with jQuery.props when setting a CSS property,
        // but curCSS() does *not* do property mapping when *getting* a
        // CSS property.  (It probably should since it manually does it
        // for 'float' now anyway... but that'd require more testing.)
        //
        // But, only do the forced mapping if the correct CSS property
        // is not 'transform' and is something else.
        if ($.props['transform'] != 'transform')
        {
            // Call in form of css('transform' ...)
            if (arg == 'transform')
            {
                arg = $.props['transform'];
                
                // User wants to GET the transform CSS, and in jQuery 1.4.3
                // calls to css() for transforms return a matrix rather than
                // the actual string specified by the user... avoid that
                // behavior and return the string by calling jQuery.style()
                // directly
                if (typeof val == 'undefined' && jQuery.style)
                {
                    return jQuery.style(this.get(0), arg);
                }
            }

            // Call in form of css({'transform': ...})
            else if
            (
                typeof arg == 'object'
                && typeof arg['transform'] != 'undefined'
            )
            {
                arg[$.props['transform']] = arg['transform'];
                delete arg['transform'];
            }
        }
        
        return proxied.apply(this, arguments);
    };
})(jQuery);
