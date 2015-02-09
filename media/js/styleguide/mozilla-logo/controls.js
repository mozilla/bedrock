(function() {
  var base = '.logoGenerator';
  var parent;
  var leftControls;
  var rightControls;
  var controlTypes = ['data', 'color'];
  var dataSources = [
    {key: 'all', label: 'All'},
    {key: 'sumo', label: 'SUMO'},
    {key: 'bugzilla', label: 'Bugzilla'},
    {key: 'firefox', label: 'Firefox'},
    {key: 'firefoxos', label: 'Firefox OS'},
    {key: 'firefoxforandroid', label: 'Firefox for Android'},
    {key: 'github', label: 'Github'},
    {key: 'qa', label: 'QA'}
  ];
  var keyTypes = [
    {key: 'totalactive', label: 'Total Active'},
    {key: 'new', label: 'New'}
  ];
  var numDataSources = 3;

  var colorPalettes = ["vibrant", "base"];
  var fillTypes = ["gradient", "flat"];
  var mozillaLogoTypes = ["show", "hide"];
  var exports = d3.dispatch('changed','updateDataKey');
  var animationOptions = ["animated", "static"];
  var colors;
  var svg = null;
  var exportButton;
  var embedModal;

  var options = {
    controlType: controlTypes[0],
    dataSource0: dataSources[1],
    dataSource1: dataSources[2],
    dataSource2: dataSources[3],
    numDataPoints: 4,
    graphRange: [0.15, 0.5],
    curveTightness: 0.5,
    angleOffset: 0,
    opacity: 90,
    colorPalette: colorPalettes[0],
    fill: fillTypes[0],
    mozillaLogo: mozillaLogoTypes[0],
    colorIndex0: 0,
    colorIndex1: 1,
    colorIndex2: 2,
    dataKey: keyTypes[0],
    animationDuration: 30000,
    mColor: '#fff',
    animation: animationOptions[0],
    gradientDirection0: true,
    gradientDirection1: true,
    gradientDirection2: true
  };
  var dataSliders = [
    {label: "Data points", min: 2, max: 10, optionKey: 'numDataPoints'},
    {label: "Graph range", min: 0, max: 1.01, optionKey: 'graphRange', range: true, step: 0.01},
    {label: "Curve tightness", min: -2, max: 2.01, step: 0.01, optionKey: 'curveTightness'},
    {label: "Angle offset", min: -1, max: 1.01, optionKey: 'angleOffset', step: 0.01},
  ];

  var coloringOptions = [
    {label: "Opacity", type: "slider", optionKey: 'opacity'},
    {label: "Color Palette", type: "boolean", values: colorPalettes, optionKey: 'colorPalette' },
    {label: "Fill", type: "boolean", values: fillTypes, optionKey: 'fill' },
    {label: "Mozilla Logo", type: "boolean", values: mozillaLogoTypes, optionKey: 'mozillaLogo'}
  ];

  function init(_colors, _svg) {
    parent = d3.select(base);
    colors = _colors;
    svg = _svg;
    createControls();
  }
  function createControls() {
    leftControls = parent.select('.leftControls');
    rightControls = parent.select('.rightControls');
    createControlPicker();
    createAnimationControl();
    createDataControls();
    createColorControls();
    createSliderValues();
    createExportButton();
    createEmbedButton();
    //we show the colorControls briefly to accurately measure things
    parent.classed('colorControls', false); //but then hide it once things are setup
  }
  function createControlPicker() {
    var controlPickerList = leftControls.append('ul')
      .attr('class', 'controlPicker cf');
    var controlTypeLI = controlPickerList.selectAll('li').data(controlTypes);
    controlTypeLI.enter().append('li');
    controlTypeLI.attr('class',String)
      .on('click', clickControlType);

    function clickControlType(controlType,activeIndex) {
      if(controlType === options.controlType) {
        return;
      }
      parent.classed(options.controlType+"Controls", false);
      options.controlType = controlType;
      parent.classed(options.controlType+"Controls", true);
    }

  }
  function createAnimationControl() {
    var animatedControl = rightControls.append('div').attr('class','animationControls');
    animatedControl.append('div').attr('class','label').text('Animation');
    var animationButtons = animatedControl.append('div').attr('class','animationButtons cf')
      .selectAll('div').data(animationOptions);
    animationButtons.enter().append('div').text(capitalize)
      .classed('active',function(d,i) {
        return d === options.animation;
      });
    animationButtons.on('click', clickAnimationButton);

    function clickAnimationButton(d,i) {
      options.animation = d;
      animationButtons.classed('active', function(d,i) {
        return d === options.animation;
      });
      exports.changed();
    }
  }
  function createDataControls() {
    leftControls.append('div').attr('class','dataControls controls')
      .append('div').attr('class','label').text('Data Sources');
    rightControls.append('div').attr('class','dataControls controls');


    createDataSourceControls();
    createKeyControl();
    createSliders();

 
    function createDataSourceControls() {
      _.each(_.range(numDataSources), function(d,i) {
        var select = leftControls.select('.dataControls').append('div').attr('class','dataControl')
          .append('select');
        select.attr('class','dataSource' + i)
          .attr('data-placeholder', 'Data Source ' + (i + 1));
        var sourceOptions = dataSources.slice(0);
        var dataSourceOpts = select.selectAll('option').data(sourceOptions);
        dataSourceOpts.enter().append('option')
          .attr('value', function(d) {
            return d.key;
          }).text(function(d) {
            return d.label;
          }).attr('selected', function(d) {
            if(d === options['dataSource' + i]) {
              return 'selected';
            }
            return null;
          });
        $(select[0][0]).selectmenu({
          change: changeSelect
        });
        function changeSelect(event, ui) {
          var newValue = ui.item.value;
          var newOption = _.find(dataSources, function(d) {
            return d.key === newValue;
          });
          options['dataSource' + i ] = newOption;
          parent.select('.colorSelect' + i + ' .label').text(newOption.label);
          exports.changed();
        }
      });
    }
    function createKeyControl() {
        var keyControlDiv = leftControls.select('.dataControls').append('div')
          .attr('class','keyControlContainer');
        keyControlDiv.append('div').attr('class','label').text('Data Key');
        var keyControl = keyControlDiv.append('select');
        keyControl.attr('class','keyControl')
          .attr('data-placeholder', 'Key');
        var keyOptionData = keyTypes.slice(0);
        var keyOptions = keyControl.selectAll('option').data(keyOptionData);
        keyOptions.enter().append('option')
          .attr('value', function(d) {
            return d.key;
          }).text(function(d) {
            return d.label;
          }).attr('selected', function(d) {
            if(d === options.dataKey) {
              return 'selected';
            }
            return null;
          });
        $(keyControl[0][0]).selectmenu({
          change: changeKey
        });

        function changeKey(event, ui) {
          var newValue = ui.item.value;
          var newOption = _.find(keyTypes, function(d) {
            return d.key === newValue;
          });
          options.dataKey = newOption;
          exports.updateDataKey();
        }
    }
    function createSliders() {
      _.each(dataSliders, function(dataSlider) {
        var sliderDiv = rightControls.select('.dataControls').append('div').attr('class','dataSlider');
        sliderDiv.append('div').attr('class','label')
          .text(dataSlider.label);
        var slider = sliderDiv.append('div').attr('class','slider');
        var sliderOpts = {
          min: dataSlider.min,
          max: dataSlider.max,
          range: typeof dataSlider.range !== 'undefined' ? true : "min",
          step: typeof dataSlider.step !== 'undefined' ? dataSlider.step : 1
        };
        if(sliderOpts.range === true) {
          sliderOpts.values = options[dataSlider.optionKey];
        } else {
          sliderOpts.value = options[dataSlider.optionKey];
        }
        sliderOpts.slide = function(event, ui) {
            if(sliderOpts.range === true) {
              options[dataSlider.optionKey] = ui.values;
            } else {
              options[dataSlider.optionKey] = ui.value;
            }
            updateSliderValue.call(slider[0][0]);

            exports.changed();
          };
        sliderOpts.change = sliderOpts.slide;
        sliderOpts.stop = sliderOpts.slide;
        $(slider[0][0]).slider(sliderOpts);
      });
    }
  }
  function createColorControls() {
    leftControls.append('div').attr('class','colorControls controls')
      .append('div').attr('class','label').text('Visual');
    rightControls.append('div').attr('class','colorControls controls');

    createIndividualColors();
    createColoringOptions();
    updateColors();
    function createIndividualColors() {
      _.each(_.range(3), function(dataSourceIndex) {
        var colorDiv = leftControls.select('.colorControls')
          .append('div').attr('class','colorSelect')
          .classed('colorSelect' + dataSourceIndex, true);
        var colorToggle = colorDiv.append('div').attr('class','colorToggle cf');
        colorToggle.append('div').attr('class','label').text(options['dataSource' + dataSourceIndex].label);
        colorToggle.append('div').attr('class','handle').html('&#x25BE;');
        var colorDrawer = colorDiv.append('div').attr('class','colorDrawer cf');
        var previewPane = colorDrawer.append('div').attr('class','previewPane');
        previewPane.append('div').attr('class','preview');
        previewPane.append('div').attr('class', 'gradientDirectionControl')
          .on('click', changeGradientDirection);
        var colorSwabs = colorDrawer.append('div').attr('class','swabs cf');
        var colorSwab = colorSwabs.selectAll('div.swab').data(colors);
        colorSwab.enter().append('div').attr('class','swab');
        colorSwab.style('background-color', function(d,swabIndex) {
          return d.colors[options.colorPalette];
        }).on('click', clickColorSwab);
      
        var drawerHeight = $(colorDrawer[0][0]).outerHeight();
        colorDrawer.attr('data-h', drawerHeight).style('height', '0');
        colorToggle.on('click', toggleDrawer);

        function clickColorSwab(swab, swabIndex) {
          options['colorIndex' + dataSourceIndex] = swabIndex;
          updateColors();
          exports.changed();
        }
        function toggleDrawer(d,i) {
          var drawer = d3.select(this.parentNode).selectAll('.colorDrawer');
          var curHeight = drawer.style('height');
          var animateHeight = 0;
          var colorDivOpen = false;
          if(curHeight === '0px') {
            colorDivOpen = true;
            animateHeight = drawer.attr('data-h');
          }
          d3.select(this).classed('open', colorDivOpen);
          drawer.transition().duration(300)
            .ease(d3.ease('cubic-in-out'))
            .style('height', animateHeight + 'px');
        }
        function changeGradientDirection(d,i) {
          options['gradientDirection' + dataSourceIndex] = ! options['gradientDirection' + dataSourceIndex];
          updateColors();
          exports.changed();
        }
      });

      
    }
    function createColoringOptions() {
      _.each(coloringOptions, function(option) {
        var div = rightControls.select('.colorControls').append('div')
          .attr('class','colorOption');
        div.append('div').attr('class','label').text(option.label);
        var component = div.append('div');
        if(option.type === 'slider') {
          var sliderOpts = {
            range: "min", value: options[option.optionKey], min: 0, max: 100,
            slide: function(event, ui) {
              options[option.optionKey] = ui.value;
              updateSliderValue.call(component[0][0]);
              exports.changed();
            }
          };
          sliderOpts.change = sliderOpts.slide;
          sliderOpts.stop = sliderOpts.slide;
          $(component[0][0]).slider(sliderOpts);
        } else if(option.type === 'boolean') {
          var btns = component.classed('cf colorButtons', true).selectAll('div').data(option.values);
          btns.enter().append('div');
          btns.text(capitalize)
            .classed('active', function(d) {
              return d === options[option.optionKey];
            })
            .on('click', clickColoringOptionButton);
        }
        function clickColoringOptionButton(clickedOpt,clickedIndex) {
          if(clickedOpt === options[option.optionKey]) {
            return;
          }
          btns.classed('active', function(d, i) {
            return i === clickedIndex;
          });
          options[option.optionKey] = clickedOpt;
          exports.changed();
          if(option.optionKey === 'colorPalette') {
            updateColors();
          }
        }
      });
    }
    function updateColors() {
      leftControls.selectAll('.colorSelect').each(function(d,i) {
        //update color of border, handle and preview
        var color = colors[options['colorIndex' + i]];
        var hex = color.colors[options.colorPalette];
        var d3This = d3.select(this);
        var bgColor;
        if(options.fill === 'gradient') {
          var hex1 = hex;
          var colorIndex2 = options['colorIndex' + i] + 1;
          colorIndex2 = colorIndex2 % colors.length;
          var hex2 = colors[colorIndex2].colors[options.colorPalette];
          if(options['gradientDirection' + i]) {
            var swap = hex1;
            hex1 = hex2;
            hex2 = swap;
          }
          bgColor = 'linear-gradient(90deg, ' + hex1 + ', ' + hex2 + ')';
        } else if(options.fill === 'flat') {
          bgColor = hex;
        }
        d3This.selectAll('.label').style('border-color',hex);
        d3This.selectAll('.handle').style('background-color',hex);

        d3This.selectAll('.previewPane .preview').style('background',bgColor);
      });
    }
  }

  function createSliderValues() {
    parent.selectAll('.ui-slider').each(function() {
      var slider = d3.select(this);
      var $slider = $(this);
      var numHandles = slider.selectAll('.ui-slider-handle')[0].length;
      _.each(_.range(numHandles), function(handleIndex) {
        var text = numHandles === 1 ? $slider.slider('value')
          : $slider.slider('values')[handleIndex];
        slider.append('div').attr('class','value');
        

      });
    }).each(updateSliderValue);
  }
  function updateSliderValue() {
    var slider = d3.select(this);
    var $slider = $(this);
    var handles = slider.selectAll('.ui-slider-handle');
    var numHandles = handles[0].length;
    slider.selectAll('div.value')
      .text(function(d,i) {
        var text = numHandles === 1 ? $slider.slider('value')
          : $slider.slider('values')[i];
        return text;
      }).style('left', function(d,i) {
        var left = $(handles[0][i]).offset().left;
        var offset = $slider.offset();
        left -= offset.left;
        var textWidth = $(this).width();
        var handleWidth = 10;
        left += (handleWidth - textWidth) / 2;
        return left + 'px';
      });
  }
  function createExportButton() {
    exportButton = parent.append('a').attr('class','exportBtn')
      .text('Download SVG')
      .attr('download', 'mozilla_logo.svg')
      .attr('href-lang-', 'image/svg+xml')
      .on('click', exportSVG);
  }
  function createEmbedButton() {
    parent.append('a').attr('class','embedBtn')
      .text('Embed')
      .on('click', showEmbedCode);
    embedModal = parent.append('div').attr('class','embedModal');
    embedModal.on('click', clickModalBackground);
    var content = embedModal.append('div').attr('class', 'modalContent');
    var instructions = "Copy and paste the following code to your website to embed the Mozilla logo. Be sure to edit the <b>size</b> parameter appropriately to control dimensions. Advanced users can modify the <b>selector</b> to any CSS selector to place the logo anywhere on their page.";
    content.append('div').attr('class','instructions').html(instructions);
    content.append('code');
    content.append('div').attr('class','close').html('&times;')
      .on('click', closeEmbedModal);
  }
  function getOptions() {
    return options;
  }

  function capitalize(str) {
    return str.substr(0,1).toUpperCase() + str.substr(1);
  }
  function exportSVG() {
    var content = $(svg[0][0].parentNode).html();
    content = stripBadStrings(content);
    var b64 = btoa(content);
    var href = 'data:image/svg+xml;base64,\n'+b64;
    exportButton.attr('href', href);

    //replace &quot;s around css style strings in SVG
    //we didn't add them, but some browsers add them automagically :(
    //other browsers also add css strings we didn't add. :()
    function stripBadStrings(str) {
      //remove bad quote characters
      str = str.replace(/&quot;/g,'');
      //remove 'none' from fill styles
      str = str.replace(/(fill: url\([^)]+\)) none/g, '$1');
      return str;
    }
  }
  function showEmbedCode() {
    var optionJSON = JSON.stringify(options);
    var config = "var mozillaIDConfig = {\n" + 
    "  selector: '.mozillaLogo',\n" +
    "  size: <b>500</b>,\n" +
    "  options: " + optionJSON + "\n" +
    "};\n";
    //TODO update the server address in the embed
    var embedCode = "(function() {\n" +
      "  var ml = document.createElement('script');\n" +
      "  ml.src = '//50.250.207.157/mozillaid/deploy/logo-build.js';\n" +
      "  ml.type = 'text/javascript';\n" +
      "  ml.async = 'true';\n" +
      "  var s = document.getElementsByTagName('script')[0];\n" +
      "  s.parentNode.insertBefore(ml, s);\n" +
      "})();\n";
    var fallbackImage = "  &lt;img src='//50.250.207.157/mozillaid/deploy/images/staticLogo.png' width='500' height='500' alt='Mozilla' /&gt;";
    var templateContainer = "&lt;div class='mozillaLogo'&gt;\n" + fallbackImage + "\n&lt;/div&gt;\n";
    var scriptTag = "&lt;script&gt;\n" + config + embedCode + "&lt;/scr" + "ipt&gt";
    var fullCode = templateContainer + scriptTag;
    embedModal.select('.modalContent code').html(fullCode);
    embedModal.style('display','block');
  }
  function closeEmbedModal() {
    embedModal.style('display', 'none');
  }
  function clickModalBackground() {

    if(d3.select(d3.event.target).classed('embedModal')) {
      closeEmbedModal();
    }
  }
  if( ! window.mozillaID) {
    window.mozillaID = {};
  }
  exports.init = init;
  exports.getOptions = getOptions;
  window.mozillaID.controls = exports;
  
})();
