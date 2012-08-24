(function ($) {
    // Monkey patch jQuery 1.3.1+ to add support for setting or animating CSS
    // scale and rotation independently.
    // 2009-2010 Zachary Johnson www.zachstronaut.com
    // Updated 2010.11.06
    var rotateUnits = 'deg';

    function Matrix(a, b, c, d, tx, ty)
    {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
        this.tx = tx;
        this.ty = ty;
    };

    Matrix.identity = function(string)
    {
        return new Matrix(
            1, 0,
            0, 1,
            0, 0
        );
    };

    Matrix.parse = function(string)
    {
        var matrix = Matrix.identity();

        var args = string.split('(').pop().split(')')[0];
        var vector = args.split(',');

        matrix.a  = vector[0];
        matrix.b  = vector[1];
        matrix.c  = vector[2];
        matrix.d  = vector[3];
        matrix.tx = vector[4];
        matrix.ty = vector[5];

        return matrix;
    };

    Matrix.prototype.multiply = function(matrix)
    {
        var new_matrix = new Matrix(
            this.a * matrix.a + this.b * matrix.c,
            this.a * matrix.b + this.b * matrix.d,
            this.c * matrix.a + this.d * matrix.c,
            this.c * matrix.b + this.d * matrix.d,
            this.tx, this.ty
        );

        return new_matrix;
    };

    Matrix.prototype.rotate = function(radians)
    {

        var rotate = new Matrix(
             Math.cos(radians), Math.sin(radians),
            -Math.sin(radians), Math.cos(radians),
            0, 0
        );

        return this.multiply(rotate);
    };

    Matrix.prototype.scale = function(scale)
    {
        var matrix = new Matrix(
            this.a,  this.b,
            this.c,  this.d,
            this.tx, this.ty
        );

        matrix.a *= scale;
        matrix.b *= scale;
        matrix.c *= scale;
        matrix.d *= scale;

        return matrix;
    };

    Matrix.prototype.getAngle = function()
    {
        return Math.atan2(this.b, this.a);
    };

    Matrix.prototype.getScale = function()
    {
        return Math.sqrt(this.a * this.a + this.b * this.b);
    };

    Matrix.prototype.toString = function()
    {
        var vector = [
            this.a,  this.b,
            this.c,  this.d,
            this.tx, this.ty
        ];

        return 'matrix(' + vector.join(', ') + ')';
    };

    $.fn.rotate = function (val)
    {
        var style = $(this).css('transform') || 'none';

        if (typeof val == 'undefined')
        {
            if (style)
            {
                var m = style.match(/rotate\(([^)]+)\)/);
                if (m && m[1])
                {
                    return m[1];
                }

                // Newer browsers use a generic matrix
                var matrix = Matrix.parse(style);
                var angle = matrix.getAngle();

                // convert to degrees
                angle = angle * (180 / Math.PI);

                return angle + 'deg';
            }

            return 0;
        }

        var m = val.toString().match(/^(-?\d+(?:\.\d+)?)(.+)?$/);
        if (m)
        {
            if (m[2])
            {
                rotateUnits = m[2];
            }

            var theta = m[1];

            // convert to radians
            if (rotateUnits == 'deg') {
                theta *= (Math.PI / 180);
            }

            var scale = $(this).scale();

            var matrix = Matrix.identity().rotate(theta).scale(scale);
            var style = matrix.toString();

            $(this).css(
                'transform',
                style
            );
        }

        return this;
    }

    // Note that scale is unitless.
    $.fn.scale = function (val, duration, options)
    {
        var style = $(this).css('transform');

        if (typeof val == 'undefined')
        {
            if (style)
            {
                var m = style.match(/scale\(([^)]+)\)/);
                if (m && m[1])
                {
                    return m[1];
                }

                // Newer browsers use a generic matrix
                var matrix = Matrix.parse(style);
                var scale = matrix.getScale();
                return scale;
            }

            return 1;
        }

        var rotate = $(this).rotate();
        var theta;

        // convert to radians
        if (rotate.match(/deg$/)) {
            theta = parseFloat(rotate) * (Math.PI / 180);
        } else {
            theta = parseFloat(rotate);
        }

        var matrix = Matrix.identity().rotate(theta).scale(scale);
        var style = matrix.toString();

        $(this).css(
            'transform',
            style
        );

        return this;
    }

    // fx.cur() must be monkey patched because otherwise it would always
    // return 0 for current rotate and scale values
    var curProxied = $.fx.prototype.cur;
    $.fx.prototype.cur = function ()
    {
        if (this.prop == 'rotate')
        {
            return parseFloat($(this.elem).rotate());
        }
        else if (this.prop == 'scale')
        {
            return parseFloat($(this.elem).scale());
        }
        
        return curProxied.apply(this, arguments);
    }
    
    $.fx.step.rotate = function (fx)
    {
        $(fx.elem).rotate(fx.now + rotateUnits);
    }
    
    $.fx.step.scale = function (fx)
    {
        $(fx.elem).scale(fx.now);
    }
    
    /*
    
    Starting on line 3905 of jquery-1.3.2.js we have this code:
    
    // We need to compute starting value
    if ( unit != "px" ) {
        self.style[ name ] = (end || 1) + unit;
        start = ((end || 1) / e.cur(true)) * start;
        self.style[ name ] = start + unit;
    }
    
    This creates a problem where we cannot give units to our custom animation
    because if we do then this code will execute and because self.style[name]
    does not exist where name is our custom animation's name then e.cur(true)
    will likely return zero and create a divide by zero bug which will set
    start to NaN.
    
    The following monkey patch for animate() gets around this by storing the
    units used in the rotation definition and then stripping the units off.
    
    */
    
    var animateProxied = $.fn.animate;
    $.fn.animate = function (prop)
    {
        if (typeof prop['rotate'] != 'undefined')
        {
            var m = prop['rotate'].toString().match(/^(([+-]=)?(-?\d+(\.\d+)?))(.+)?$/);
            if (m && m[5])
            {
                rotateUnits = m[5];
            }
            
            prop['rotate'] = m[1];
        }
        
        return animateProxied.apply(this, arguments);
    }
})(jQuery);
