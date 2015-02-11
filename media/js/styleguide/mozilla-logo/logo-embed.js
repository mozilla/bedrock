
var mozillaIDConfig = {
  selector: '.mozillaLogo',
  size: 200,
  options: {"controlType":"data","dataSource0":{"key":"sumo","label":"SUMO"},"dataSource1":{"key":"bugzilla","label":"Bugzilla"},"dataSource2":{"key":"firefox","label":"Firefox"},"numDataPoints":4,"graphRange":[0.15,0.5],"curveTightness":0.5,"angleOffset":0,"opacity":90,"colorPalette":"vibrant","fill":"gradient","mozillaLogo":"show","colorIndex0":0,"colorIndex1":1,"colorIndex2":2,"dataKey":{"key":"totalactive","label":"Total Active"},"animationDuration":30000,"mColor":"#fff","animation":"animated","gradientDirection0":true,"gradientDirection1":true,"gradientDirection2":true,"shapeMaxSize":240,"shapeMinSize":72}
};
(function() {
  var ml = document.createElement('script');
  //TODO update this address
  ml.src = ('https:' == document.location.protocol ? 'https' : 'http') +
    '://50.250.207.157/mozillaid/deploy/logo-build.js';
  ml.type = 'text/javascript';
  ml.async = 'true';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(ml, s);
})();