jQuery(document).ready(function ()
{
    var $world = jQuery('#apps-physics').jQb2({
        gravity: [0, 7],
        sleep: false,
        debug: false,
        mouse: true,
        autobody: false,
        bounds: true,
        controls: false,
        paused: false,
        fps: 30,
    });

    var worldScale = 30;
    var pi = 

    function fromPixel(pos) {return parseInt(pos, 10) / worldScale}
    function fromPixel(pos) {return parseInt(pos, 10) / worldScale}

    var availableApps = [];

    var world   = $world.data('b2World');
    var objects = $world.data('b2Objects');

    var $apps = $world.find('div.apps-icon').each(function(index, value) {
        var $this = $(this);
        var el = this;

        var bodyDef = new Box2D.Dynamics.b2BodyDef();
        bodyDef.angle = (-Math.PI / 8) + (Math.random() * (Math.PI / 4));
        bodyDef.angularVelocity = -0.25 + Math.random() * 0.5;
        bodyDef.type = Box2D.Dynamics.b2Body.b2_dynamicBody;

        var fixDef = new Box2D.Dynamics.b2FixtureDef();

        fixDef.density = 1.0;
        fixDef.friction = 0.5;
        fixDef.restitution = 0.2;

        var outerW = 76;
        var outerH = 76;
        var posX = 100 + Math.floor(Math.random() * 100 - 66 + 1);
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
    }, 2000);

    function spawnApp()
    {
        if (availableApps.length == 0) {
            return;

        }

        var data = availableApps.pop();

        $(data[0])
            .css(
                {
                    'position' : 'absolute',
                    'display' : 'block',
                    'opacity' : '0'
                }
            )
            .animate(
                { 'opacity': '1' },
                700
            );

        var body = world.CreateBody(data[1]);
        $.data(data[0], 'b2Body', body);
        $.data(data[0], 'b2Type', 'DOM-Circle');

        data[2].shape = new Box2D.Collision.Shapes.b2CircleShape(
            fromPixel(76 / 2)
        );

        body.CreateFixture(data[2]);
        objects.worldBodies.push(data[0]);
    };

});
