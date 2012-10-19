(function(jQuery) {
	
	// !Definitions
	var worldScale = 30;
	// !- Collision
	/* Collision types and detections */
	var b2AABB = Box2D.Collision.b2AABB,
	b2Bound = Box2D.Collision.b2Bound,
	b2BoundValues = Box2D.Collision.b2BoundValues,
	b2Collision = Box2D.Collision.b2Collision,
	b2ContactID = Box2D.Collision.b2ContactID,
	b2ContactPoint = Box2D.Collision.b2ContactPoint,
	b2Distance = Box2D.Collision.b2Distance,
	b2DistanceInput = Box2D.Collision.b2DistanceInput,
	b2DistanceOutput = Box2D.Collision.b2DistanceOutput,
	b2DistanceProxy = Box2D.Collision.b2DistanceProxy,
	b2DynamicTree = Box2D.Collision.b2DynamicTree,
	b2DynamicTreeBroadPhase = Box2D.Collision.b2DynamicTreeBroadPhase,
	b2DynamicTreeNode = Box2D.Collision.b2DynamicTreeNode,
	b2DynamicTreePair = Box2D.Collision.b2DynamicTreePair,
	b2Manifold = Box2D.Collision.b2Manifold,
	b2ManifoldPoint = Box2D.Collision.b2ManifoldPoint,
	b2Point = Box2D.Collision.b2Point,
	b2RayCastInput = Box2D.Collision.b2RayCastInput,
	b2RayCastOutput = Box2D.Collision.b2RayCastOutput,
	b2Segment = Box2D.Collision.b2Segment,
	b2SeparationFunction = Box2D.Collision.b2SeparationFunction,
	b2Simplex = Box2D.Collision.b2Simplex,
	b2SimplexCache = Box2D.Collision.b2SimplexCache,
	b2SimplexVertex = Box2D.Collision.b2SimplexVertex,
	b2TimeOfImpact = Box2D.Collision.b2TimeOfImpact,
	b2TOIInput = Box2D.Collision.b2TOIInput,
	b2WorldManifold = Box2D.Collision.b2WorldManifold,
	ClipVertex = Box2D.Collision.ClipVertex,
	Features = Box2D.Collision.Features,
	// !-- Shapes
	/* Shape definitions */
	b2CircleShape = Box2D.Collision.Shapes.b2CircleShape,
	b2EdgeChainDef = Box2D.Collision.Shapes.b2EdgeChainDef,
	b2EdgeShape = Box2D.Collision.Shapes.b2EdgeShape,
	b2MassData = Box2D.Collision.Shapes.b2MassData,
	b2PolygonShape = Box2D.Collision.Shapes.b2PolygonShape,
	b2Shape = Box2D.Collision.Shapes.b2Shape,
	// !- Common
	/* Math functions and data types */
	b2Color = Box2D.Common.b2Color,
	b2Settings = Box2D.Common.b2Settings,
	b2Mat22 = Box2D.Common.Math.b2Mat22,
	b2Mat33 = Box2D.Common.Math.b2Mat33,
	b2Math = Box2D.Common.Math.b2Math,
	b2Sweep = Box2D.Common.Math.b2Sweep,
	b2Transform = Box2D.Common.Math.b2Transform,
	b2Vec2 = Box2D.Common.Math.b2Vec2,
	b2Vec3 = Box2D.Common.Math.b2Vec3,
	// !- Dynamics
	/* Bodies, fixtures and other object definitions */
	b2Body = Box2D.Dynamics.b2Body,
	b2BodyDef = Box2D.Dynamics.b2BodyDef,
	b2ContactFilter = Box2D.Dynamics.b2ContactFilter,
	b2ContactImpulse = Box2D.Dynamics.b2ContactImpulse,
	b2ContactListener = Box2D.Dynamics.b2ContactListener,
	b2ContactManager = Box2D.Dynamics.b2ContactManager,
	b2DebugDraw = Box2D.Dynamics.b2DebugDraw,
	b2DestructionListener = Box2D.Dynamics.b2DestructionListener,
	b2FilterData = Box2D.Dynamics.b2FilterData,
	b2Fixture = Box2D.Dynamics.b2Fixture,
	b2FixtureDef = Box2D.Dynamics.b2FixtureDef,
	b2Island = Box2D.Dynamics.b2Island,
	b2TimeStep = Box2D.Dynamics.b2TimeStep,
	b2World = Box2D.Dynamics.b2World,
	// !-- Contacts
	/* Types of contacts */
	b2CircleContact = Box2D.Dynamics.Contacts.b2CircleContact,
	b2Contact = Box2D.Dynamics.Contacts.b2Contact,
	b2ContactConstraint = Box2D.Dynamics.Contacts.b2ContactConstraint,
	b2ContactConstraintPoint = Box2D.Dynamics.Contacts.b2ContactConstraintPoint,
	b2ContactEdge = Box2D.Dynamics.Contacts.b2ContactEdge,
	b2ContactFactory = Box2D.Dynamics.Contacts.b2ContactFactory,
	b2ContactRegister = Box2D.Dynamics.Contacts.b2ContactRegister,
	b2ContactResult = Box2D.Dynamics.Contacts.b2ContactResult,
	b2ContactSolver = Box2D.Dynamics.Contacts.b2ContactSolver,
	b2EdgeAndCircleContact = Box2D.Dynamics.Contacts.b2EdgeAndCircleContact,
	b2NullContact = Box2D.Dynamics.Contacts.b2NullContact,
	b2PolyAndCircleContact = Box2D.Dynamics.Contacts.b2PolyAndCircleContact,
	b2PolyAndEdgeContact = Box2D.Dynamics.Contacts.b2PolyAndEdgeContact,
	b2PolygonContact = Box2D.Dynamics.Contacts.b2PolygonContact,
	b2PositionSolverManifold = Box2D.Dynamics.Contacts.b2PositionSolverManifold,
	// !-- Controllers
	/* Types of controllers */
	b2BuoyancyController = Box2D.Dynamics.Controllers.b2BuoyancyController,
	b2ConstantAccelController = Box2D.Dynamics.Controllers.b2ConstantAccelController,
	b2ConstantForceController = Box2D.Dynamics.Controllers.b2ConstantForceController,
	b2Controller = Box2D.Dynamics.Controllers.b2Controller,
	b2ControllerEdge = Box2D.Dynamics.Controllers.b2ControllerEdge,
	b2GravityController = Box2D.Dynamics.Controllers.b2GravityController,
	b2TensorDampingController = Box2D.Dynamics.Controllers.b2TensorDampingController,
	// !-- Joints
	/* Types of joints */
	b2DistanceJoint = Box2D.Dynamics.Joints.b2DistanceJoint,
	b2DistanceJointDef = Box2D.Dynamics.Joints.b2DistanceJointDef,
	b2FrictionJoint = Box2D.Dynamics.Joints.b2FrictionJoint,
	b2FrictionJointDef = Box2D.Dynamics.Joints.b2FrictionJointDef,
	b2GearJoint = Box2D.Dynamics.Joints.b2GearJoint,
	b2GearJointDef = Box2D.Dynamics.Joints.b2GearJointDef,
	b2Jacobian = Box2D.Dynamics.Joints.b2Jacobian,
	b2Joint = Box2D.Dynamics.Joints.b2Joint,
	b2JointDef = Box2D.Dynamics.Joints.b2JointDef,
	b2JointEdge = Box2D.Dynamics.Joints.b2JointEdge,
	b2LineJoint = Box2D.Dynamics.Joints.b2LineJoint,
	b2LineJointDef = Box2D.Dynamics.Joints.b2LineJointDef,
	b2MouseJoint = Box2D.Dynamics.Joints.b2MouseJoint,
	b2MouseJointDef = Box2D.Dynamics.Joints.b2MouseJointDef,
	b2PrismaticJoint = Box2D.Dynamics.Joints.b2PrismaticJoint,
	b2PrismaticJointDef = Box2D.Dynamics.Joints.b2PrismaticJointDef,
	b2PulleyJoint = Box2D.Dynamics.Joints.b2PulleyJoint,
	b2PulleyJointDef = Box2D.Dynamics.Joints.b2PulleyJointDef,
	b2RevoluteJoint = Box2D.Dynamics.Joints.b2RevoluteJoint,
	b2RevoluteJointDef = Box2D.Dynamics.Joints.b2RevoluteJointDef,
	b2WeldJoint = Box2D.Dynamics.Joints.b2WeldJoint,
	b2WeldJointDef = Box2D.Dynamics.Joints.b2WeldJointDef;
	
	// !- Helper Functions
	/* Common math functions */
	
	function randomID() {return parseInt(1024 * Math.random(), 10)};
	function fromPixel(pos) {return parseInt(pos, 10) / worldScale};
	function toPixel(pos) {return pos * worldScale};
	
	// !- Pause Function
	/* Pause the world */
	function setPaused(worldElement, set) {
		if (set) {
			jQuery(worldElement).addClass('jQb2-world-paused');
		} else {
			jQuery(worldElement).removeClass('jQb2-world-paused');
		}
		jQuery.data(worldElement, 'paused', set);
	}
	 
	// !- Build Body
	/* Create bodies based on DOM elements */
	function buildBody(worldElement, bodyElement, dens, fric, rest) {
		
		// !--Body Definition
		var bodyDef = new b2BodyDef();
		
		// !--Fixture Definition
		var fixDef = new b2FixtureDef();
		
		fixDef.density = dens;
		fixDef.friction = fric;
		fixDef.restitution = rest;
		
		var world = jQuery(worldElement).data('b2World');
		var outerW = jQuery(bodyElement).outerWidth() - 20;
		var outerH = jQuery(bodyElement).outerHeight() - 20;
		var posX = jQuery(bodyElement).position().left - 10;
		var posY = jQuery(bodyElement).position().top - 10;
		
		jQuery(bodyElement).css({
			'position': 'absolute'
		});
		
		if (jQuery(bodyElement).hasClass('jQb2-static')) {
			bodyDef.type = b2Body.b2_staticBody;
		} else {
			bodyDef.type = b2Body.b2_dynamicBody;
		}
		if (jQuery(bodyElement).children('map').length) {
			bodyDef.position.Set(fromPixel(posX + (outerW / 2)), fromPixel(posY + (outerH / 2)));
			jQuery.data(bodyElement, 'b2Body', world.CreateBody(bodyDef));
			jQuery.data(bodyElement, 'b2Type', 'Map-Custom');
			jQuery(bodyElement).find('area').each(function() {
				var polyVert = [];
				var areaShape = jQuery(this).attr('shape');
				var areaCoords = jQuery(this).attr('coords').split(",");
				switch (areaShape) {
				case 'poly':
					fixDef.shape = new b2PolygonShape();
					for (i = 0; i < areaCoords.length; i += 2) {
						var vex = new b2Vec2(fromPixel(areaCoords[i] - outerW / 2), fromPixel(areaCoords[i + 1] - outerH / 2));
						polyVert.unshift(vex);
					}
					fixDef.shape.SetAsArray(polyVert, polyVert.length);
					try {
						jQuery(bodyElement).data('b2Body').CreateFixture(fixDef);
					} catch (polyErr) {
						console.log("jQb2: Poly Areas need to be defined counter clockwise.");
					}
					break;
				case 'circle':
					fixDef.shape = new b2CircleShape(fromPixel(areaCoords[2]));
					var pos = new b2Vec2(fromPixel(areaCoords[0] - outerW / 2), fromPixel(areaCoords[1] - outerH / 2));
					fixDef.shape.SetLocalPosition(pos);
					jQuery(bodyElement).data('b2Body').CreateFixture(fixDef);
					break;
				case 'rect':
					fixDef.shape = new b2PolygonShape();
					polyVert[0] = new b2Vec2(fromPixel(areaCoords[0] - outerW / 2), fromPixel(areaCoords[1] - outerH / 2));
					polyVert[1] = new b2Vec2(fromPixel(areaCoords[2] - outerW / 2), fromPixel(areaCoords[1] - outerH / 2));
					polyVert[2] = new b2Vec2(fromPixel(areaCoords[2] - outerW / 2), fromPixel(areaCoords[3] - outerH / 2));
					polyVert[3] = new b2Vec2(fromPixel(areaCoords[0] - outerW / 2), fromPixel(areaCoords[3] - outerH / 2));
					fixDef.shape.SetAsArray(polyVert, polyVert.length);
					try {
						jQuery(bodyElement).data('b2Body').CreateFixture(fixDef);
					} catch (rectErr) {
						console.log("jQb2: Rectangles need to be created top to bottom.");
					}
					break;
				}
			});
		} else {
			bodyDef.position.Set(fromPixel(posX + (outerW / 2)), fromPixel(posY + (outerH / 2)));
			jQuery.data(bodyElement, 'b2Body', world.CreateBody(bodyDef));
			if (jQuery(bodyElement).hasClass('jQb2-circle')) {
				jQuery.data(bodyElement, 'b2Type', 'DOM-Circle');
				fixDef.shape = new b2CircleShape(fromPixel(outerW / 2));
			} else {
				jQuery.data(bodyElement, 'b2Type', 'DOM-Rectangle');
				fixDef.shape = new b2PolygonShape();
				fixDef.shape.SetAsBox(fromPixel(outerW / 2), fromPixel(outerH / 2));
			}
			jQuery(bodyElement).data('b2Body').CreateFixture(fixDef);
		}
		return bodyElement;
	}
	
	// !- Distance Joints
	/* Chain DOM elements in the same span */
	function buildDistanceJoint(worldElement, opt) {
		var world = jQuery(worldElement).data('b2World');
		var dist = {
			softness: [4.0, 0.5],
			collide: true,
			elementFrom: {
				anchor: {
					x: 0,
					y: 0
				}
			},
			elementTo: {
				anchor: {
					x: 0,
					y: 0
				}
			}
		};
		if (opt) jQuery.extend(true, dist, opt);
		if (dist.elementFrom.element && dist.elementTo.element) {
			var bodyFrom = jQuery(dist.elementFrom.element).data('b2Body');
			var bodyTo = jQuery(dist.elementTo.element).data('b2Body');
			var jointHTML = '<div class="jQb2-joint-distance"';
			jointHTML += ' ></div>';
			var jointElement = jQuery(jointHTML).prependTo(jQuery(dist.elementFrom.element).parent());
			jointDef = new b2DistanceJointDef();
			var fromAnchorOffset = {
				x: bodyFrom.GetPosition().x + dist.elementFrom.anchor.x,
				y: bodyFrom.GetPosition().y + dist.elementFrom.anchor.y
			};
			var toAnchorOffset = {
				x: bodyTo.GetPosition().x + dist.elementTo.anchor.x,
				y: bodyTo.GetPosition().y + dist.elementTo.anchor.y
			};
			jointDef.Initialize(bodyFrom, bodyTo, fromAnchorOffset, toAnchorOffset);
			jointDef.frequencyHz = dist.softness[0];
			jointDef.dampingRatio = dist.softness[1];
			jointDef.collideConnected = dist.collide;
			var joint = world.CreateJoint(jointDef);
			jQuery.data(jointElement, 'b2Joint', joint);
			return joint;
		} else {
			return false;
		}
	}
	
	var methods = { // !World Constructor
		world: function(options) { // !- World Variables
		
			var world;
			
			var objects = {
				worldBodies : [],
				worldJoints : [],
				worldID : randomID()
			};
			
			var worldElement = jQuery(this);
			var worldWidth = jQuery(worldElement).width();
			var worldHeight = jQuery(worldElement).height();
			var settings = {
				gravity: [0, 10],
				sleep: true,
				debug: false,
				controls: true,
				mouse: true,
				autobody: {
					density: 1.0,
					friction: 0.5,
					restitution: 0.2,
					softness: [4.0, 0.5],
					select: {
						body: 'li',
						chain: 'ol',
						bundle: 'ul'
					}
				},
				bounds: {
					density: 1.0,
					friction: 0.5,
					restitution: 0.2
				},
				fps: 60
			};
			
			// !- Autobody
			/* Automatically create bodies based on DOM elements */
			function autoBody() { // !--Build Bodies
				jQuery(worldElement).find(settings.autobody.select.body).each(function() {
					objects.worldBodies.push(buildBody(worldElement, this, settings.autobody.density, settings.autobody.friction, settings.autobody.restitution));
				}); // !--Build Chains
				jQuery(worldElement).find(settings.autobody.select.chain).each(function() {
					jQuery(this).children(settings.autobody.select.body).each(function() {
						var from = jQuery(this);
						var to = jQuery(this).next(settings.autobody.select.body);
						if (jQuery(this).next(settings.autobody.select.body).length){
							objects.worldJoints.push(
								buildDistanceJoint(worldElement, {
									softness: settings.autobody.softness,
									elementFrom: {
										element: from,
										anchor: {
											x: 0,
											y: 0.2
										}
									},
									elementTo: {
										element: to,
										anchor: {
											x: 0,
											y: -0.2
										}
									}
								})
							);
						}
					});
				});
				
				// !--Build Bundles
				jQuery(worldElement).find(settings.autobody.select.bundle).each(function() {
					jQuery(this).children(settings.autobody.select.body).each(function() {
						var from = jQuery(this);
						jQuery(this).nextAll(settings.autobody.select.body).each(function() {
							var to = jQuery(this);
							buildDistanceJoint(worldElement, {
								softness: settings.autobody.softness,
								elementFrom: {
									element: from,
									anchor: {
										x: 0,
										y: 0
									}
								},
								elementTo: {
									element: to,
									anchor: {
										x: 0,
										y: 0
									}
								}
							});
						});
					});
				});
			}
			
			// !- Build Bounds
			/* Create walls at the edges of the box */


			function buildBounds() {
				var bodyDef = new b2BodyDef();
				var fixDef = new b2FixtureDef();
				fixDef.density = settings.bounds.density;
				fixDef.friction = settings.bounds.friction;
				fixDef.restitution = settings.bounds.restitution;
				bodyDef.type = b2Body.b2_staticBody;
				fixDef.shape = new b2PolygonShape();
				fixDef.shape.SetAsBox(fromPixel(worldWidth + 20), fromPixel(20)); //top wall
				bodyDef.position.Set(fromPixel(worldWidth / 2), fromPixel(-20));
				world.CreateBody(bodyDef).CreateFixture(fixDef); //bottom wall
				bodyDef.position.Set(fromPixel(worldWidth / 2), fromPixel(worldHeight + 20));
				world.CreateBody(bodyDef).CreateFixture(fixDef);
				fixDef.shape.SetAsBox(fromPixel(20), fromPixel(worldHeight + 20)); //left wall
				bodyDef.position.Set(fromPixel(-20), fromPixel(worldHeight / 2));
				world.CreateBody(bodyDef).CreateFixture(fixDef); //right wall
				bodyDef.position.Set(fromPixel(worldWidth + 20), fromPixel(worldHeight / 2));
				world.CreateBody(bodyDef).CreateFixture(fixDef);
			}
			
			// !- Debug Mode
			/* Create a canvas element for debugging purposes */

			function buildDebug() {
				var debugDraw = new b2DebugDraw();
				var debugHTML = '<canvas id="jQb2-debug-' + objects.worldID + '"';
				debugHTML += ' class="jQb2-debug"';
				debugHTML += ' width="' + jQuery(worldElement).width() + '"';
				debugHTML += ' height="' + jQuery(worldElement).height() + '"';
				debugHTML += ' ></canvas>';
				var debugElement = jQuery(debugHTML).prependTo(worldElement);
				jQuery(debugElement).css({
					position: 'relative',
					top: '0',
					left: '0',
					background: '#333333'
				});
				debugDraw.SetSprite(debugElement[0].getContext("2d"));
				debugDraw.SetDrawScale(30.0);
				debugDraw.SetFillAlpha(0.5);
				debugDraw.SetLineThickness(1.0);
				debugDraw.SetFlags(b2DebugDraw.e_shapeBit | b2DebugDraw.e_jointBit | b2DebugDraw.e_aabbBit | b2DebugDraw.e_pairBit | b2DebugDraw.e_centerOfMassBit | b2DebugDraw.e_controllerBit);
				world.SetDebugDraw(debugDraw);
			} 
			// !- Mouse Functions
			/* Allows mouse to grab elements */


			function mouseBuilder() {
				jQuery(worldElement).bind("mousedown", function(e) {
					var mouseJoint;
					var mouseX = e.pageX - jQuery(worldElement).offset().left;
					var mouseY = e.pageY - jQuery(worldElement).offset().top;
					var mouseBody = getBodyAtMouse(mouseX, mouseY);
					if (mouseBody) {
						var mouseJointDef = new b2MouseJointDef();
						mouseJointDef.bodyA = world.GetGroundBody();
						mouseJointDef.bodyB = mouseBody;
						mouseJointDef.target.Set(fromPixel(mouseX), fromPixel(mouseY));
						mouseJointDef.collideConnected = true;
						mouseJointDef.maxForce = 300.0 * mouseBody.GetMass();
						mouseJoint = world.CreateJoint(mouseJointDef);
						mouseBody.SetAwake(true);
						jQuery(worldElement).bind("mousemove", function(f) {
							mouseX = f.pageX - jQuery(worldElement).offset().left;
							mouseY = f.pageY - jQuery(worldElement).offset().top;
							if (mouseJoint) mouseJoint.SetTarget(new b2Vec2(fromPixel(mouseX), fromPixel(mouseY)));
						});
						jQuery(worldElement).bind("mouseup", function(f) {
							jQuery(worldElement).unbind("mousemove");
							mouseX = undefined;
							mouseY = undefined;
							world.DestroyJoint(mouseJoint);
						});
					}
				});
			}
			
			function worldControls() {
				var controlHTML = '<div style="position:absolute; top:0; left: 0;" id="jQb2-controls-' + objects.worldID + '"';
				controlHTML += ' class="jQb2-controls"></div>';
				var controlPlayHTML = '<input class="';
				if (settings.paused) {
					controlPlayHTML += 'jQb2-controls-play';
				} else {
					controlPlayHTML += 'jQb2-controls-pause';
				}
				controlPlayHTML += '" type="button" value="';
				if (settings.paused) {
					controlPlayHTML += 'play';
				} else {
					controlPlayHTML += 'pause';
				}
				controlPlayHTML += '"></input>';
				var controlElement = jQuery(controlHTML).appendTo(worldElement);
				var controlPlay = jQuery(controlPlayHTML).appendTo(controlElement);
				jQuery(controlPlay).click(function() {
					if (jQuery(this).hasClass('jQb2-controls-pause')) {
						jQuery(worldElement).jQb2('pause');
						jQuery(this).removeClass('jQb2-controls-pause');
						jQuery(this).addClass('jQb2-controls-play');
						jQuery(this).val('play');
					} else if (jQuery(this).hasClass('jQb2-controls-play')) {
						jQuery(worldElement).jQb2('pause');
						jQuery(this).removeClass('jQb2-controls-play');
						jQuery(this).addClass('jQb2-controls-pause');
						jQuery(this).val('pause');
					}
				});
			}
			
			function getBodyAtMouse(pixelX, pixelY) {
				mousePVec = new b2Vec2(fromPixel(pixelX), fromPixel(pixelY));
				var aabb = new b2AABB();
				aabb.lowerBound.Set(fromPixel(pixelX) - 0.001, fromPixel(pixelY) - 0.001);
				aabb.upperBound.Set(fromPixel(pixelX) + 0.001, fromPixel(pixelY) + 0.001); // Query the world for overlapping shapes.
				selectedBody = null;
				world.QueryAABB(getBodyCB, aabb);
				return selectedBody;
			}
			
			function getBodyCB(fixture) {
				if (fixture.GetBody().GetType() != b2Body.b2_staticBody) {
					if (fixture.GetShape().TestPoint(fixture.GetBody().GetTransform(), mousePVec)) {
						selectedBody = fixture.GetBody();
						return false;
					}
				}
				return true;
			}
			
			// !- World Step
			/* Iterates this function based on the FPS and checks if the world is paused */
			function worldStep() {
				if (jQuery(worldElement).data('paused') === false || jQuery(worldElement).data('paused') === undefined) {
					updateBodies();
					world.Step(1 / settings.fps, 10, 10);
					world.DrawDebugData();
					world.ClearForces();
				}
			}
			
			// !- DOM Update
			/* Update the DOM based on the Box2D world */
			function updateBodies() {
				for (var b = 0; b < objects.worldBodies.length; b++) {
					var body = jQuery(objects.worldBodies[b]).data('b2Body');
					if (body !== null && body.GetType() == 2) {
						if (body.IsAwake()) {
							jQuery(objects.worldBodies[b]).removeClass('body-sleeping');
							for (var f = body.GetFixtureList(); f; f = f.GetNext()) {
								var posX = toPixel(body.GetPosition().x) - (jQuery(objects.worldBodies[b]).outerWidth() / 2);
								var posY = toPixel(body.GetPosition().y) - (jQuery(objects.worldBodies[b]).outerHeight() / 2);
								jQuery(objects.worldBodies[b]).css({
									left: posX + 'px',
									top: posY + 'px',
									'-webkit-transform': 'rotate(' + body.GetAngle() + 'rad)',
									'-moz-transform': 'rotate(' + body.GetAngle() + 'rad)',
									'transform': 'rotate(' + body.GetAngle() + 'rad)',
									msTransform : 'rotate(' + body.GetAngle() + 'rad)',
									OTransform : 'rotate(' + body.GetAngle() + 'rad)'
								});
							}
						} else {
							jQuery(objects.worldBodies[b]).addClass('body-sleeping');
						}
					}
				}
			}
			
			// !- World Constructor
			/* Go through all the selected elements and create worlds */
			return this.each(function() {
				jQuery(this).css({
					'position': 'relative'
				}).addClass('jQb2-world');
				if (options.autobody === true) options.autobody = settings.autobody;
				if (options.bounds === true) options.bounds = settings.bounds;
				if (options) jQuery.extend(true, settings, options);
				
				world = new b2World(new b2Vec2(settings.gravity[0], settings.gravity[1]), settings.sleep);
				jQuery.data(this, 'b2World', world);
				jQuery.data(this, 'b2Settings', settings);
				jQuery.data(this, 'b2Objects', objects );
				
				if (settings.autobody !== false) autoBody();
				if (settings.bounds !== false) buildBounds();
				if (settings.debug) buildDebug();
				if (settings.mouse) mouseBuilder();
				if (settings.controls) worldControls();
				if (settings.paused) setPaused(this, settings.paused);
				
				worldStep();
				window.setInterval(worldStep, 1000 / settings.fps);
			});
		},
		pause: function(set) {
			return this.each(function() {
				if (set !== undefined) {
					setPaused(this, set);
				} else {
					setPaused(this, !jQuery(this).data('paused'));
				}
			});
		},
		body: function(options) {
			
			return this.each(function() {
				var settings = {
					worldElement: jQuery(this).parents('.jQb2-world'),
					density: 1.0,
					friction: 0.5,
					restitution: 0.2
				};
				
				var objects = jQuery(settings.worldElement).data('b2Objects');
				
				if (options) jQuery.extend(settings, options);
				
				objects.worldBodies.push( buildBody(settings.worldElement, this, settings.density, settings.friction, settings.restitution) );
			});
		}
	};
	
	jQuery.fn.jQb2 = function(method) {
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.world.apply(this, arguments);
		} else {
			console.log('Method ' + method + ' does not exist on jQBox2D');
		}
	};
})(jQuery);
