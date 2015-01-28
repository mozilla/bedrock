(function(_,d3) {
  var size;
  var selector;
  var svgElement;
  var svg;
  var frameCounter = 0;
  var shapes;
  var controls = null;
  var sources = ['all','sumo','bugzilla','firefox','firefoxos','firefoxforandroid','github','qa']
  var sourceData = [];
  var rotationAngle = 56.82; //degrees
  var MPathData ="M40.797,115.531L25.443,138.95H6.509V44.962c0,0,0.155-4.541-1.695-9.645c-1.851-5.105-4.876-6.677-4.876-6.677L17.814,1.436c0,0,8.903,1.907,15.774,10.246c4.19,5.083,5.989,10.546,5.989,10.546l1.018-1.308C50.516,7.438,62.726,0.061,79.769,0.061c15.263,0,26.965,7.885,32.307,22.131c10.429-14.246,22.639-22.131,40.191-22.131c21.112,0,35.611,15.263,35.611,40.7v71.866l-17.202,26.322h-18.919V46.866c0-15.518-6.104-19.841-13.226-19.841c-9.921,0-16.536,6.867-23.403,18.823v66.778l-17.193,26.322H79.007V46.866c0-15.517-5.85-19.841-13.228-19.841c-9.919,0-16.534,6.867-23.147,18.823v66.887L40.797,115.531"
  var mDimensions = { w: 188 , h: 139 }
  var mScale = 2
  var mX;
  var mY;
  var defs;
  var historicalOffset = 0
  var lineGenerator;
  var numDataSources = 3;
  var colors = [
    { name: "nightly blue", colors: {base: '#23336A', vibrant:'#204182'} },
    { name: "developer blue", colors: {base: '#16498C', vibrant:'#1454A5'} },
    { name: "mobile blue", colors: {base: '#1E93CF', vibrant:'#219FD3'} },
    { name: "summit teal", colors: {base: '#26B786', vibrant:'#55C0A2'} },
    { name: "gecko green", colors: {base: '#6CB84D', vibrant:'#79C253'} },
    { name: "flame yellow", colors: {base: '#F5C926', vibrant:'#F5D52A'} },
    { name: "market orange", colors: {base: '#E98824', vibrant:'#F59B28'} },
    { name: "firefox orange", colors: {base: '#DB5627', vibrant:'#F36C21'} },
    { name: "dino red", colors: {base: '#BA3C33', vibrant:'#DA3F32'} },
    { name: "bikeshed magenta", colors: {base: '#D54361', vibrant:'#E6528F'} },
    { name: "aurora purple", colors: {base: '#652562', vibrant:'#8D3585'} },
  ]

  var colorNames = _.map(colors, function(d) { return d.name })
  var options = null;

  var shapePositionPoints = [
    {x1: 0.13571466766, y1: 1, x2:  0.22715362814, y2: 0.80932544032},
    {x1: 0.52141596706, y1: 1, x2: 0.61290840062, y2: 0.80932544032},
    {x1: 0.90845409336, y1: 1, x2: 1, y2: 0.80932544032},
    {x1: 0, y1: 0.19776364832, x2: 0.09512860274, y2: 0},

  ]
  function init(_selector, _size, _options) {
    selector = _selector;
    size = _size;
    mScale *= size / 500;
    mX = size / 2.0 - (mDimensions.w * mScale) / 2.0
    mY = size / 2.0 - (mDimensions.h * mScale) / 2.0

    svg = d3.select(selector).append('svg').attr('width', size)
      .attr('height', size)
      .attr('xmlns','http://www.w3.org/2000/svg')
      .attr('version', '1.1')
    svgElement = svg;
    defs = svg.append('defs')
    var translate = size * 0.5;
    var scaleAmount = 0.75;
    var transform = 'translate(' + translate + ',' + translate + ') scale(' + scaleAmount + ') translate(-' + translate +',-' + translate + ')'
    svg = svg.append('g')
      .attr('transform', transform )

    if(typeof _options !== 'undefined') {
      options = _options;
      var sourcesToLoad = [];
      sourcesToLoad.push(options.dataSource0['key'])
      sourcesToLoad.push(options.dataSource1['key'])
      sourcesToLoad.push(options.dataSource2['key'])
      sources = sourcesToLoad
    } else {
      initGUI()
    }
    
    loadSourceData()
    
  }
  function loadSourceData() {
    var nextSource = sources[sourceData.length];
    
    var sourceLink = 'http://booloo-mozid.appspot.com/payload/';
    sourceLink += nextSource
    d3.json(sourceLink, sourceLoaded)

  }
  function allSourceDataLoaded() {
    initShapes()
  }
  function sourceLoaded(err, data) {
    var thisSource = sources[sourceData.length];
    _.each(data, function(datum) {
      var d = datum.wkcommencing
      var dateParts = d.split('-')
      datum.date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2])
    })
    data.sort(function(a,b) {
      if(a.date === b.date) {
        return 0
      } else if(a.date > b.date) {
        return 1
      } else {
        return -1
      }
    })
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
    var key = options.dataKey.key;
    data.dataPoints = _.pluck(_.last(validData, options.numDataPoints), key)
    var historicalData = _.pluck(_.last(validData, options.numDataPoints + options.numHistoryToShow), key)
    data.dataPoints = historicalData
  }
  function controlsChanged() {
    initShapes()
  }
  function initGUI() {
    controls = window.mozillaID.controls
    controls.on('changed', controlsChanged )
    controls.on('updateDataKey', updateSourceData )
    controls.init(colors, svgElement)
    options = controls.getOptions();
  
  }
  function updateSourceData() {
    _.each(sourceData, initKeyDataPoints)
    initShapes()
  }
  function initShapes() {
    
    options.shapeMaxSize = size * options.graphRange[1]
    options.shapeMinSize = size * options.graphRange[0]

    defs.selectAll('*').remove()
    shapes = []
    _.each(_.range(numDataSources), initShape)
    animate()
  }
  function initShape(shapeIndex) {
    var shapeDataKey = options['dataSource' + shapeIndex].key;
    var shapeData = _.find(sourceData, function(d) { return d.key === shapeDataKey }).dataPoints
    var min = _.min(shapeData);
    var max = _.max(shapeData);

    var shape = {};
    shape.min = min;
    shape.max = max;
    shape.key = shapeDataKey
    shape.points = [];
    shape.color = colors[options['colorIndex' + shapeIndex]];

    var color2Index;
    if(options.fill === 'gradient') {
      color2Index = options['colorIndex' + shapeIndex] + 1;
      color2Index = color2Index % colors.length;
    
    } else if(options.fill == 'flat') {
      color2Index = options['colorIndex' + shapeIndex];
    }
    shape.color2 = colors[color2Index];
    
    shape.width = size * 0.65
    shape.data = shapeData
    _.each(shapeData, function(dataPoint, index) {
      var x = map(index, 0, shapeData.length - 1, 0, shape.width)
      var scaled =  - map(dataPoint, min, max, options.shapeMinSize, options.shapeMaxSize)
      var angleOffset = options.angleOffset * size / 12
      var xOffset = map(index, 0, shapeData.length, angleOffset, -angleOffset)
      x += xOffset
      shape.points.push({
        x: x,
        y: scaled
      })
    })
    var gradient = defs.append('linearGradient').attr('id', 'gradient'+shapeIndex)
      .attr('x1', 0).attr('x2', 0).attr('y1', 0).attr('y2', 1)

    var shapeHex = shape.color.colors[options.colorPalette]
    var shapeHex2 = shape.color2.colors[options.colorPalette]
    if(options['gradientDirection' + shapeIndex]) {
      var swap = shapeHex;
      shapeHex = shapeHex2;
      shapeHex2 = swap;
    }
    gradient.append('stop').attr('offset', '0%').attr('stop-color', shapeHex)
    gradient.append('stop').attr('offset', '100%').attr('stop-color', shapeHex2)

    shape.angle = - rotationAngle 
    shape.position = {x : size / 2, y : size / 2}
    if(typeof shapePositionPoints[shapeIndex] !== 'undefined') {
      var shapePoints = shapePositionPoints[shapeIndex];
      
      var pointsInSpace = {
        x1: mX + mDimensions.w * mScale * shapePoints['x1'],
        y1: mY + mDimensions.h * mScale * shapePoints['y1'],
        x2: mX + mDimensions.w * mScale * shapePoints['x2'],
        y2: mY + mDimensions.h * mScale * shapePoints['y2']
      }

      pointsInSpace.avgX = (pointsInSpace['x1'] + pointsInSpace['x2'] ) * 0.5
      pointsInSpace.avgY = (pointsInSpace['y1'] + pointsInSpace['y2'] ) * 0.5
      shape.position['x'] = pointsInSpace['avgX'] //+ 1.5
      shape.position['y'] = pointsInSpace['avgY'] //+ 1.5
      var offsetAmount = 0;
      if(shapeIndex === 0) {
        offsetAmount = 0.3
      } else if(shapeIndex === 1) {
        offsetAmount = 0.28
      } else if(shapeIndex === 2) {
        offsetAmount = 0.3
      } else if(shapeIndex === 3) {
        offsetAmount = 0.3
      }
      var radiansAngle = shape.angle * Math.PI / 180
      shape.position['x'] -= Math.cos(radiansAngle) * shape.width * offsetAmount
      shape.position['y'] -= Math.sin(radiansAngle) * shape.width * offsetAmount
    }

    shapes.push(shape);
  }

  function animate() {
    svg.selectAll('*').remove()
    drawShapes()
    if(options.mozillaLogo === 'show') {
      drawMozillaM()
    }
  }
  function drawMozillaM() {
    var offset = 0.5
    svg.append('path').attr('d', MPathData)
      .attr('transform', function() {
        return 'translate(' + (mX + offset) + ',' + (mY + offset) + ') scale(' + mScale + ')'
      }).style('fill', options.mColor)
    
  }

  function drawShapes() {
    var shapesPath = svg.selectAll('path.shape').data(shapes)
    lineGenerator = d3.svg.line()
      .x(function(d) { return (d.x) })
      .y(function(d) { return (d.y) })
      .interpolate('cardinal')
      .tension(options.curveTightness)
    shapesPath.enter().append('path').attr('class','shape')
    shapesPath
      .attr('transform', function(shape, shapeIndex) {
        var angle = shape.angle;
        var x = shape.position.x;
        var y = shape.position.y;
        return 'translate(' + x + ',' + y + ') rotate(' + angle + ')'
      }).attr('d', function(d) {
        var pointsToUse = [
          { x: 0, y: 0 }
        ]
        
        d.historicalOffset = historicalOffset
        if(options.animation === 'static') {
          d.historicalOffset = d.data.length - options.numDataPoints
        }
        
        var dataPoints = d.data.slice(d.historicalOffset, options.numDataPoints + d.historicalOffset)
        var min = _.min(dataPoints)
        var max = _.max(dataPoints)
        var shape = d;
        var points = _.map(dataPoints,  function(d,i) {
          var x = map(i, 0, options.numDataPoints - 1, 0, shape.width)
          var angleOffset = options.angleOffset * size / 12
          var xOffset = map(i, 0, options.numDataPoints - 1, angleOffset, -angleOffset)
          x += xOffset
          var scaled =  - map(d, min, max, options.shapeMinSize, options.shapeMaxSize)
          var y = options.animation === "animated" ? 0 : scaled;
          return {x: x, y: y}
        })
    
        pointsToUse = pointsToUse.concat(points)
        pointsToUse.push({ x: d.width, y: 0 })
        d.nullPoints = pointsToUse
        return lineGenerator(pointsToUse) + 'Z'
      }).style('fill', function(d,i) { return 'url(#gradient' + i + ')' })
      .style('opacity', options.opacity/100)
    if(options.animation === "animated") {
      shapesPath.transition().duration(1000).ease('cubic-in-out')
      .delay(function(d,i) {
        return 500 + i * 200
      })
      .attr('d', function(d) {

        var pointsToUse = [
          { x: 0, y: 0 }
        ]
        var dataPoints = d.data.slice(d.historicalOffset, options.numDataPoints + d.historicalOffset)
        var min = _.min(dataPoints)
        var max = _.max(dataPoints)
        var shape = d;
        _.each(dataPoints, function(d,i) {
          var x = map(i, 0, options.numDataPoints - 1, 0, shape.width)
          var angleOffset = options.angleOffset * size / 12
          var xOffset = map(i, 0, options.numDataPoints - 1, angleOffset, -angleOffset)
          x += xOffset
          var scaled =  - map(d, min, max, options.shapeMinSize, options.shapeMaxSize)

          pointsToUse.push({x: x, y: scaled})
        })
        pointsToUse.push({x: d.width, y: 0 });

        return lineGenerator(pointsToUse) + 'Z'
      }).each('end', nextAnimation)
    }
  }
  function nextAnimation(d,i) {
    var path = d3.select(this)
    d.historicalOffset ++;
    var shape = d;
    var trans = path.transition().duration(options.animationDuration).ease('linear')
      .attr('d', function() {
        var pointsToUse = [
          { x: 0, y: 0 }
        ]
        var dataPoints = d.data.slice(d.historicalOffset, options.numDataPoints + d.historicalOffset)
        var min = _.min(dataPoints)
        var max = _.max(dataPoints)
        var shape = d;
        _.each(dataPoints, function(d,i) {
          var x = map(i, 0, options.numDataPoints - 1, 0, shape.width)
           var angleOffset = options.angleOffset * size / 12
          var xOffset = map(i, 0, options.numDataPoints - 1, angleOffset, -angleOffset)
          x += xOffset
          var scaled =  - map(d, min, max, options.shapeMinSize, options.shapeMaxSize)
          pointsToUse.push({x: x, y: scaled})
        })
        pointsToUse.push({ x: d.width, y: 0 });
        return lineGenerator(pointsToUse) + 'Z'

      })
      if(d.historicalOffset + options.numDataPoints < d.data.length) {
        trans.each('end', nextAnimation)
      }
  }

  function map(value, istart, istop, ostart, ostop) {
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart));
  };
  if( ! window.mozillaID) {
    window.mozillaID = {}
  }
  window.mozillaID.logo = {
    init: init,
  }
  
})(_, d3)
if(typeof mozillaIDConfig !== 'undefined') {
  mozillaID.logo.init(mozillaIDConfig.selector,
    mozillaIDConfig.size,
    mozillaIDConfig.options)
}