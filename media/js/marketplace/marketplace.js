jQuery(document).ready(function ()
{
    var $world = jQuery('#apps-physics').jQb2({
        gravity: [0, 16],
        sleep: false,
        debug: false,
        mouse: true,
        autobody: false,
        bounds: true,
        controls: false,
        paused: false,
        fps: 60,
    });

    var worldScale = 30;

    function fromPixel(pos) {return parseInt(pos, 10) / worldScale}
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

});
