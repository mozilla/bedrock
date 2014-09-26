(function() {
  var size;
  var selector;
  var canvas;
  var ctxt;
  var assets = {};
  var nodes;
  var frameCounter = 0;
  var shapes;
  var gui = new dat.GUI()
  var sources = ['all','sumo','bugzilla','firefox','firefoxos','firefoxforandroid','github','qa']
  var sourceData = [];
  var rotationAngle = Math.PI * (56.82) / 180;
  var mouse = {x: 0, y: 0}
  var _time;
  var colors = [
    '#23336A', '#00549F', '#2194D2', '#26B786', '#6CB84D', '#FFCC06', '#F8941D', '#E56125', '#C13931', '#D54361', '#652562'
  ]
  var options = {
    'numNodes': 24,
    'numShapes': 4,
    'curveTightness': 0.5,
    'numDataPoints': 10,
    'drawBG': false,
    'drawNodes': false,
    'animate': true,
    'dataSource0': sources[0],
    'dataSource1': sources[1],
    'dataSource2': sources[2],
    'dataSource3': sources[3],
    'shapeMaxSize': -1,
    'shapeMinSize': -1,
    'mozillaMScale': 0.7,
    'explodedTween': 0,
    'transform': explode,
    'shapeMinDivider': 0.16,
    'shapeMaxDivider': 0.5,
    'curved': true,
    'dataKey': 'totalactive',
    'opacity': 0.8

  }

  var shapePositionPoints = [
    {x1: 0, y1: 0.19776364832, x2: 0.09512860274, y2: 0},
    {x1: 0.13571466766, y1: 1, x2:  0.22715362814, y2: 0.80932544032},
    {x1: 0.52141596706, y1: 1, x2: 0.61290840062, y2: 0.80932544032},
    {x1: 0.90845409336, y1: 1, x2: 1, y2: 0.80932544032},

  ]
  function init(_selector, _size) {
    selector = _selector;
    size = _size;
    options.shapeMaxSize = size * options.shapeMaxDivider
    options.shapeMinSize = size * options.shapeMinDivider
    var container = document.querySelectorAll(selector);
    console.log(container)
    canvas = document.createElement('canvas')
    canvas.setAttribute('width', size * 2)
    var height = size * 4
    canvas.setAttribute('height', height)
    container[0].appendChild(canvas)
    ctxt = canvas.getContext('2d')
    ctxt.font = "12px Arial"
    noise.seed(Math.random())

    
    initGUI()
    
    assetsNames = [
      "/media/img/styleguide/identity/mozilla/logo-prototype/m_sliced.png"
    ]
    loadAssets(assetsNames);
  }
  function loadSourceData() {
    var nextSource = sources[sourceData.length];

    // Temporarily load locally cached json data
    var sourceLink = '/media/js/styleguide/logo-prototype/';
    sourceLink += 'tab/' + nextSource
    $.getJSON(sourceLink, sourceLoaded)

  }
  function allSourceDataLoaded() {
    console.log('all source data loaded');
    console.log(sourceData);
    initShapes()
    start()
  }
  function sourceLoaded(data) {
    var thisSource = sources[sourceData.length];
    
    var dataObject = {
      key: thisSource,
      data: data
    }
    initKeyDataPoints(dataObject)
    sourceData.push(dataObject)

    if(sourceData.length === sources.length) {
      allSourceDataLoaded();
    } else {
      loadSourceData()
    }
  }
  function initKeyDataPoints(data) {
    var validData = _.filter(data.data, function(d) {
      return (+d.totalactive) > 0
    })
    var key = options.dataKey;
    data.dataPoints = _.pluck(_.last(validData, options.numDataPoints), key)
  }
  function initGUI() {
    gui.add(options, 'transform')
    gui.add(options, 'dataSource0', sources).onFinishChange(initShapes)
    gui.add(options, 'dataSource1', sources).onFinishChange(initShapes)
    gui.add(options, 'dataSource2', sources).onFinishChange(initShapes)
    gui.add(options, 'dataSource3', sources).onFinishChange(initShapes)

    gui.add(options,'shapeMinDivider', 0, 1).onFinishChange(updateScale)
    gui.add(options,'shapeMaxDivider', 0, 1).onFinishChange(updateScale)

    gui.add(options,'curved')
    gui.add(options, 'curveTightness', -2, 2).onChange(updateIfNotAnimating)
    
    gui.add(options,'dataKey', ['totalactive','new']).onFinishChange(updateSourceData)
    gui.add(options,'numDataPoints', 4, 20).step(1).onFinishChange(updateSourceData)
    gui.add(options,'opacity', 0, 1)
  }
  function updateIfNotAnimating() {
    //if animation is off, we still want to update display, but just once
    if(! options.animate) {
      requestAnimationFrame(animate)
    }
  }
  function updateScale() {
    if(options.shapeMinDivider > options.shapeMaxDivider) {
      alert('min divider should be less than max divider');
      return;
    }

    options.shapeMaxSize = size * options.shapeMaxDivider
    options.shapeMinSize = size * options.shapeMinDivider

    initShapes()
  }
  function updateSourceData() {
    _.each(sourceData, initKeyDataPoints)
    initShapes()
  }
  function initShapes() {
    $('.dataKey').text(options.dataKey)
    shapes = []
    _.each(_.range(options.numShapes), initShape)
  }
  function initShape(shapeIndex) {
    var shapeDataKey = options['dataSource' + shapeIndex];
    var shapeData = _.find(sourceData, function(d) { return d.key === shapeDataKey }).dataPoints
    var min = _.min(shapeData);
    var max = _.max(shapeData);

    shape = {};
    shape.min = min;
    shape.max = max;
    shape.key = shapeDataKey
    shape.points = [];
    while(true) {
      shape.color = colors[Math.floor(Math.random() * colors.length)]
      var unique = true;
      _.each(shapes, function(otherShape) {
        if(otherShape.color === shape.color) {
          unique = false;
        }
      })
      if(unique) {
        break;
      }
    }

    shape.width = size * 0.65
    _.each(shapeData, function(dataPoint, index) {
      var x = map(index, 0, shapeData.length - 1, 0, shape.width)
      var scaled =  - map(dataPoint, min, max, options.shapeMinSize, options.shapeMaxSize)
      shape.points.push({
        x: x,
        y: scaled
      })
    })

    if(shapeIndex < 2 ) {
      shape.angle = Math.PI - rotationAngle
    } else {
      shape.angle = - rotationAngle
    }
    shape.position = {x : size / 2, y : size / 2}
    var logoM = assets['m_sliced.png']
    if(typeof shapePositionPoints[shapeIndex] !== 'undefined') {
      var shapePoints = shapePositionPoints[shapeIndex];
      var pointsInSpace = {
        x1: logoM.positioning.x + logoM.positioning.w * shapePoints['x1'],
        y1: logoM.positioning.y + logoM.positioning.h * shapePoints['y1'],
        x2: logoM.positioning.x + logoM.positioning.w * shapePoints['x2'],
        y2: logoM.positioning.y + logoM.positioning.h * shapePoints['y2']
      }
      pointsInSpace.avgX = (pointsInSpace['x1'] + pointsInSpace['x2'] ) * 0.5
      pointsInSpace.avgY = (pointsInSpace['y1'] + pointsInSpace['y2'] ) * 0.5
      shape.position['x'] = pointsInSpace['avgX'] //+ 1.5
      shape.position['y'] = pointsInSpace['avgY'] //+ 1.5
      var offsetAmount = 0;
      if(shapeIndex === 0) {
        offsetAmount = 0.5
      } else if(shapeIndex === 1) {
        offsetAmount = 0.8
      } else if(shapeIndex === 2) {
        offsetAmount = 0.2
      } else if(shapeIndex === 3) {
        offsetAmount = 0.2
      }
      shape.position['x'] -= Math.cos(shape.angle) * shape.width * offsetAmount
      shape.position['y'] -= Math.sin(shape.angle) * shape.width * offsetAmount
    }

    shapes.push(shape);
    
    console.log(shape)



      
  }
  function resetShapes() {
    initNodes();
    initShapes();
    updateIfNotAnimating()

  }
  function loadAssets(assetsNames) {
    var numToLoad = assetsNames.length;
    var numLoaded = 0;
    _.each(assetsNames, function(asset) {
      var img = new Image()
      img.src = asset
      console.log(asset)
      img.onload = function() {
        var assetFinalName = asset.substr(asset.lastIndexOf('/') + 1)
        var assetObject = {name: assetFinalName, asset: img, w: img.width, h: img.height } ;
        var mW = size * options.mozillaMScale;
        var mH = img.height / img.width * mW;
        var mX = size / 2.0 - mW / 2.0
        var mY = size / 2.0 - mH / 2.0;
        assetObject.positioning = {
          w: mW,
          h: mH,
          x: mX,
          y: mY      
        }
        assets[assetFinalName] = assetObject
        numLoaded++;
        if(numLoaded === numToLoad) {
          loadSourceData()
        }
      }

    })
  }

  function start() {
    requestAnimationFrame(animate)
  }

  function animate(time) {
    _time = time;
    if(options.animate) {
      requestAnimationFrame(animate)
      TWEEN.update(time)
    }
    frameCounter ++;
    ctxt.clearRect(0,0, size * 4, size * 4);
    ctxt.save()
    var translateAmount = options.explodedTween * 200
    ctxt.translate(translateAmount,translateAmount / 4)
    if(options.drawBG) {
      drawBG();
    }
    if(options.animate) {
      updateNodes();
    }
    drawShapes();
    if(options.explodedTween === 1) {
      drawMozillaM();

    }
    ctxt.restore();
  }
  function drawBG() {
    function random255() { return Math.floor(Math.random() * 255 )}
    var hue = (~~(frameCounter  / 12))% 360
    ctxt.fillStyle = "hsl( " + hue + " ,100%, 50%)";
    ctxt.fillRect(0,0,size,size)
  }
  function drawMozillaM() {
    var mImg = assets['m_sliced.png']
 
    var mW = mImg.positioning.w;
    var mH = mImg.positioning.h;
    var mX = mImg.positioning.x;
    var mY = mImg.positioning.y;

    ctxt.drawImage(mImg.asset, 0, 0, mImg.w, mImg.h, mX, mY, mW, mH)
  }
  function updateNodes() {
    _.each(nodes, function(node) {
      node.update();
    })
  }

  function modulo(m,n) {
    return ((m%n)+n)%n;

  }
  function getControlPoints(x0,y0,x1,y1,x2,y2){
    var t = options.curveTightness
    var d01=Math.sqrt(Math.pow(x1-x0,2)+Math.pow(y1-y0,2));
    var d12=Math.sqrt(Math.pow(x2-x1,2)+Math.pow(y2-y1,2));
   
    var fa=t*d01/(d01+d12);
    var fb=t-fa;
  
    var p1x=x1+fa*(x0-x2);
    var p1y=y1+fa*(y0-y2);

    var p2x=x1-fb*(x0-x2);
    var p2y=y1-fb*(y0-y2);  
    
    return [p1x,p1y,p2x,p2y]
  }
  function drawCurvedShape(pts) {
    ctxt.beginPath();
    
    var cp = [];
    var n = pts.length
    var startPoints = [pts[0], pts[1]]
    pts.push(pts[0],pts[1],pts[2],pts[3]);
    pts.unshift(pts[n-1]);
    pts.unshift(pts[n-1]);
    for(var i=0;i<n;i+=2){
        cp=cp.concat(getControlPoints(pts[i],pts[i+1],pts[i+2],pts[i+3],pts[i+4],pts[i+5]));
    }
    cp=cp.concat(cp[0],cp[1]);   
    ctxt.moveTo(startPoints[0], startPoints[1])
    for(var i=2;i<n+2;i+=2){
        //ctxt.moveTo(pts[i],pts[i+1]);
        ctxt.bezierCurveTo(cp[2*i-2],cp[2*i-1],cp[2*i],cp[2*i+1],pts[i+2],pts[i+3]);
    }
    ctxt.fill();
      
  }
  function drawShapePoints(points) {
    ctxt.fillStyle = "red";
    _.each(points, function(point) {
      ctxt.beginPath();
      ctxt.arc(point.x, point.y, 5, 0, Math.PI * 2, true)

      ctxt.closePath();
      ctxt.fill()
    })
  }
  function drawFilledGraph(shape) {
    if(options.curved) {
      var points = [shape.width, 0, shape.width, 0, 0, 0, 0, 0]
      _.each(shape.points, function(point) {
        points.push(point.x, point.y)
      })
      drawCurvedShape(points)
    } else {
      ctxt.beginPath();
      ctxt.moveTo(shape.width, 0);
      ctxt.lineTo(0, 0);
      _.each(shape.points, function(point) {
        ctxt.lineTo(point.x,point.y)
      })
    
      ctxt.closePath();
      ctxt.fill()
    }
    
  }
  function drawShapes() {
    ctxt.globalAlpha = options.opacity;
    _.each(shapes, function(shape, shapeIndex) {
      if(shapeIndex !== 2) {
      //  return;
      }

      ctxt.save();
      

      var angle = shape.angle * options.explodedTween + 0 * (1-options.explodedTween)
      var x = shape.position.x * options.explodedTween + 20 * (1-options.explodedTween)
      var y = shape.position.y * options.explodedTween + (options.shapeMaxSize + 80) * (shapeIndex + 1) * (1-options.explodedTween)

      ctxt.translate(x, y)
      ctxt.rotate(angle)
      if(options.explodedTween === 0) {
        drawShapePoints(shape.points)
      }
      ctxt.fillStyle = shape.color
      drawFilledGraph(shape);

      if(options.explodedTween === 0) {
        ctxt.strokeStyle = "black";
        ctxt.beginPath();
        ctxt.moveTo(0, -options.shapeMinSize)
        ctxt.lineTo(shape.width, -options.shapeMinSize)
        ctxt.moveTo(0, -options.shapeMaxSize)
        ctxt.lineTo(shape.width, -options.shapeMaxSize)

        ctxt.closePath();
        ctxt.stroke()
        ctxt.fillStyle = "black"
        ctxt.fillText("" + shape.min, 0, -options.shapeMinSize - 5)
        ctxt.fillText("" + shape.max, 0, -options.shapeMaxSize - 5)
        ctxt.save();
        ctxt.textAlign = "end"
        ctxt.fillText(shape.key, shape.width, -options.shapeMaxSize - 5)
        ctxt.restore()
      }
      /*
      var tightness = 0.5;
      
      var pts = [];
      _.each(shape.nodes, function(node) {
        pts.push(node.x)
        pts.push(node.y)
      })
      drawCurvedShape(pts)
      */

      ctxt.restore()
    })
    ctxt.globalAlpha = 1;
  }

  function explode() {
    console.log('explode')
    var target = null;
    if(options.explodedTween === 0) {
      target = 1;
    } else if(options.explodedTween === 1) {
      target = 0;
    }
    if(target === null) {
      return;
    }
    console.log(target)
    var t = new TWEEN.Tween(options).to({
      'explodedTween': target
    },1000) .start(_time)
  }

  function map(value, istart, istop, ostart, ostop) {
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart));
  };
  if( ! window.mozillaID) {
    window.mozillaID = {}
  }
  window.mozillaID.clock = {
    init: init,
    play: start
  }
  /*
  document.addEventListener('mousemove', function(e) {
    mouse.x = e.x;
    mouse.y = e.y;
    if(typeof shapes !== 'undefined' && shapes.length > 0) {
      shapes[0].position = mouse
      console.log(shapes[0].position)
    }
  })
  */
})()


mozillaID.clock.init('#logo', 600)
