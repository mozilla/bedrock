/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

jQuery(document).ready(function ()
{

    if ($.fn.jQb2) {

        var $world = jQuery('#apps-physics').jQb2({
            gravity: [0, 16],
            sleep: false,
            debug: false,
            mouse: true,
            autobody: false,
            bounds: true,
            controls: false,
            paused: false,
            fps: 60
        });

        var worldScale = 30;

        function fromPixel(pos) {return parseInt(pos, 10) / worldScale}

        var availableApps = [];
        var appSize = 96;
        var appRealSize = 76;

        var world   = $world.data('b2World');
        var objects = $world.data('b2Objects');

        var $apps = $world.find('div.apps-icon').each(function(index, value) {
            var $this = $(this);
            var el = this;

            var bodyDef = new Box2D.Dynamics.b2BodyDef();
            bodyDef.angle = (-Math.PI / 8) + (Math.random() * (Math.PI / 4));
            if (bodyDef.angle > 0) {
                bodyDef.angularVelocity = Math.random() * -0.25;
            } else {
                bodyDef.angularVelocity = Math.random() * 0.25;
            }
            bodyDef.type = Box2D.Dynamics.b2Body.b2_dynamicBody;

            var fixDef = new Box2D.Dynamics.b2FixtureDef();

            fixDef.density = 10.0;
            fixDef.friction = 0.5;
            fixDef.restitution = 0.2;

            var outerW = appRealSize;
            var outerH = appRealSize;
            var posX = 80 + Math.floor(Math.random() * (140 - appRealSize) + 1);
            var posY = 0;

            bodyDef.position.Set(
                fromPixel(posX + (outerW / 2)),
                fromPixel(posY + (outerH / 2))
            );

            availableApps.push([el, bodyDef, fixDef]);

        });

        var spawnInterval = setInterval(function() {
            if (availableApps.length > 0) {
                spawnApp();
            } else {
                clearInterval(spawnInterval);
            }
        }, 500);

        function spawnApp()
        {
            if (availableApps.length == 0) {
                return;

            }

            var data = availableApps.pop();

            $(data[0]).css(
                {
                    'position' : 'absolute',
                    'display' : 'block'
                }
            );

            var body = world.CreateBody(data[1]);
            $.data(data[0], 'b2Body', body);
            $.data(data[0], 'b2Type', 'DOM-Circle');

            data[2].shape = new Box2D.Collision.Shapes.b2CircleShape(
                fromPixel(appRealSize / 2)
            );

            body.CreateFixture(data[2]);
            objects.worldBodies.push(data[0]);
        };

    }

    var $button = $('#marketplace-button');

    var isFirefox18Android = (function() {
        var ua = navigator.userAgent;
        var matches = ua.match(/Android;.*(?:Firefox|Aurora)\/(\d+)\./);
        return (matches && matches[1] >= 18);
    })();

    if (isFirefox18Android) {

        // Hide default text in "Showcased" section, show Fx-specific version
        $('#showcased-nonfx').hide();
        $('#showcased-fx').show();

        // Remove the qr-codes from app previews
        $('.qr-code').remove();

        // swap marketplace button title
        $button.text($button.attr('data-mobile-title'));

    } else {
        
        // add accessible attributes
        $button.attr({
            'role': 'button',
            'aria-haspopup': true,
            'aria-expanded': false
        });

        var documentClickHandler = function(e)
        {
            var $target = $(e.target);

            // skip if we clicked on the panel
            if ($target.is($panel)
                || $target.parents('#marketplace-panel').length > 0
                || $target.is($button)
                || $target.parents('#marketplace-button').length > 0
            ) {
                return;
            }

            // skip if relatively positioned (mobile layout)
            if ($panel.css('position') == 'relative') {
                return;
            }

            // close the panel
            if ($panel.css('display') == 'block') {
                $panel.fadeOut();
                $button.focus();
            }
        }
        
        var documentKeydownHandler = function(event){
            if(event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
                return true;
            }
            if(event.keyCode === 27){
                $button.trigger('click');
            }
        }

        // prevent linking to apps, just let QR codes appear
        $('#apps-preview .pager-page a').click(function(e) {
            e.preventDefault();
        });

        // make clicking the button open the panel
        $panel = $('#marketplace-panel');
        $button.click(function(e) {
            e.preventDefault(e);
            
            // change the state of aria-expanded
            $button.attr('aria-expanded', $panel.css('display') !== 'block');

            // add document click-to-close handler
            if ($panel.css('display') == 'block') {
                $(document)
                    .unbind('click', documentClickHandler)
                    .unbind('keydown', documentKeydownHandler);
                // when closed set focus to button
                $button.focus();
            } else {
                $(document)
                    .click(documentClickHandler)
                    .keydown(documentKeydownHandler);
            }

            $panel.fadeToggle();
        });

    }

});
