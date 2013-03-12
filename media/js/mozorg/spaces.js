/*!
 * jQuery Tools v1.2.5 - The missing UI library for the Web
 * 
 * tooltip/tooltip.js
 * 
 * NO COPYRIGHTS OR LICENSES. DO WHAT YOU LIKE.
 * 
 * http://flowplayer.org/tools/
 * 
 */
(function(a){a.tools=a.tools||{version:"v1.2.5"},a.tools.tooltip={conf:{effect:"toggle",fadeOutSpeed:"fast",predelay:0,delay:30,opacity:1,tip:0,position:["top","center"],offset:[0,0],relative:!1,cancelDefault:!0,events:{def:"mouseenter,mouseleave",input:"focus,blur",widget:"focus mouseenter,blur mouseleave",tooltip:"mouseenter,mouseleave"},layout:"<div/>",tipClass:"tooltip"},addEffect:function(a,c,d){b[a]=[c,d]}};var b={toggle:[function(a){var b=this.getConf(),c=this.getTip(),d=b.opacity;d<1&&c.css({opacity:d}),c.show(),a.call()},function(a){this.getTip().hide(),a.call()}],fade:[function(a){var b=this.getConf();this.getTip().fadeTo(b.fadeInSpeed,b.opacity,a)},function(a){this.getTip().fadeOut(this.getConf().fadeOutSpeed,a)}]};function c(b,c,d){var e=d.relative?b.position().top:b.offset().top,f=d.relative?b.position().left:b.offset().left,g=d.position[0];e-=c.outerHeight()-d.offset[0],f+=b.outerWidth()+d.offset[1],/iPad/i.test(navigator.userAgent)&&(e-=a(window).scrollTop());var h=c.outerHeight()+b.outerHeight();g=="center"&&(e+=h/2),g=="bottom"&&(e+=h),g=d.position[1];var i=c.outerWidth()+b.outerWidth();g=="center"&&(f-=i/2),g=="left"&&(f-=i);return{top:e,left:f}}function d(d,e){var f=this,g=d.add(f),h,i=0,j=0,k=d.attr("title"),l=d.attr("data-tooltip"),m=b[e.effect],n,o=d.is(":input"),p=o&&d.is(":checkbox, :radio, select, :button, :submit"),q=d.attr("type"),r=e.events[q]||e.events[o?p?"widget":"input":"def"];if(!m)throw"Nonexistent effect \""+e.effect+"\"";r=r.split(/,\s*/);if(r.length!=2)throw"Tooltip: bad events configuration for "+q;d.bind(r[0],function(a){clearTimeout(i),e.predelay?j=setTimeout(function(){f.show(a)},e.predelay):f.show(a)}).bind(r[1],function(a){clearTimeout(j),e.delay?i=setTimeout(function(){f.hide(a)},e.delay):f.hide(a)}),k&&e.cancelDefault&&(d.removeAttr("title"),d.data("title",k)),a.extend(f,{show:function(b){if(!h){l?h=a(l):e.tip?h=a(e.tip).eq(0):k?h=a(e.layout).addClass(e.tipClass).appendTo(document.body).hide().append(k):(h=d.next(),h.length||(h=d.parent().next()));if(!h.length)throw"Cannot find tooltip for "+d}if(f.isShown())return f;h.stop(!0,!0);var o=c(d,h,e);e.tip&&h.html(d.data("title")),b=b||a.Event(),b.type="onBeforeShow",g.trigger(b,[o]);if(b.isDefaultPrevented())return f;o=c(d,h,e),h.css({position:"absolute",top:o.top,left:o.left}),n=!0,m[0].call(f,function(){b.type="onShow",n="full",g.trigger(b)});var p=e.events.tooltip.split(/,\s*/);h.data("__set")||(h.bind(p[0],function(){clearTimeout(i),clearTimeout(j)}),p[1]&&!d.is("input:not(:checkbox, :radio), textarea")&&h.bind(p[1],function(a){a.relatedTarget!=d[0]&&d.trigger(r[1].split(" ")[0])}),h.data("__set",!0));return f},hide:function(c){if(!h||!f.isShown())return f;c=c||a.Event(),c.type="onBeforeHide",g.trigger(c);if(!c.isDefaultPrevented()){n=!1,b[e.effect][1].call(f,function(){c.type="onHide",g.trigger(c)});return f}},isShown:function(a){return a?n=="full":n},getConf:function(){return e},getTip:function(){return h},getTrigger:function(){return d}}),a.each("onHide,onBeforeShow,onShow,onBeforeHide".split(","),function(b,c){a.isFunction(e[c])&&a(f).bind(c,e[c]),f[c]=function(b){b&&a(f).bind(c,b);return f}})}a.fn.tooltip=function(b){var c=this.data("tooltip");if(c)return c;b=a.extend(!0,{},a.tools.tooltip.conf,b),typeof b.position=="string"&&(b.position=b.position.split(/,?\s/)),this.each(function(){c=new d(a(this),b),a(this).data("tooltip",c)});return b.api?c:this}})(jQuery);

/**
* hoverIntent r6 // 2011.02.26 // jQuery 1.5.1+
* <http://cherne.net/brian/resources/jquery.hoverIntent.html>
* 
* @param  f  onMouseOver function || An object with configuration options
* @param  g  onMouseOut function  || Nothing (use configuration options object)
* @author    Brian Cherne brian(at)cherne(dot)net
*/
(function($){$.fn.hoverIntent=function(f,g){var cfg={sensitivity:7,interval:100,timeout:0};cfg=$.extend(cfg,g?{over:f,out:g}:f);var cX,cY,pX,pY;var track=function(ev){cX=ev.pageX;cY=ev.pageY};var compare=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);if((Math.abs(pX-cX)+Math.abs(pY-cY))<cfg.sensitivity){$(ob).unbind("mousemove",track);ob.hoverIntent_s=1;return cfg.over.apply(ob,[ev])}else{pX=cX;pY=cY;ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}};var delay=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);ob.hoverIntent_s=0;return cfg.out.apply(ob,[ev])};var handleHover=function(e){var ev=jQuery.extend({},e);var ob=this;if(ob.hoverIntent_t){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t)}if(e.type=="mouseenter"){pX=ev.pageX;pY=ev.pageY;$(ob).bind("mousemove",track);if(ob.hoverIntent_s!=1){ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}}else{$(ob).unbind("mousemove",track);if(ob.hoverIntent_s==1){ob.hoverIntent_t=setTimeout(function(){delay(ev,ob)},cfg.timeout)}}};return this.bind('mouseenter',handleHover).bind('mouseleave',handleHover)}})(jQuery);

/***
 * Scripts for the maps
 */
$(document).ready(function(){

  // Show bubbles on the pins
  $("#map-sites .pin").removeAttr("title").hover(
    function(){
      $("#map-sites .info:visible").hide();
      $(this).css({ position: "relative", zIndex: "99" });
      var info = $(this).siblings(".info");
      info.fadeIn(100).removeAttr("aria-hidden");      
      // Try to display the bubble inside the viewport
      var w = $(window);
      var wd = {
          top: w.scrollTop(),
          left: w.scrollLeft()
      };
      wd.bottom = wd.top + w.height();
      wd.right = wd.left + w.width();
      var o = info.offset();
      if (o.top + info.outerHeight() > wd.bottom) {
          info.css('bottom', info.css('top'));
          info.css('top', 'auto')
      }
      if (o.left + info.outerWidth() > wd.right) {
          info.css('right', info.css('left'));
          info.css('left', 'auto')
      }
    },
    function(){
      $(this).removeAttr("style");
      $(this).siblings(".info:visible").delay(300).fadeOut(100).attr("aria-hidden", "true");
    }
  );

  // Keep the bubble visible when it's in use
  $("#map-sites .info").hover(
    function() { $(this).stop(true, true).show().removeAttr("aria-hidden"); },
    function() { $(this).delay(300).fadeOut(100).attr("aria-hidden", "true"); }
  );
      
  // Set up the tooltips on the map arrows
  $("#map-nav .north a").tooltip({ position: "bottom center", offset: [10,0], layout: '<div><i class="n"/></div>', effect: "fade", fadeInSpeed: 200, fadeOutSpeed: 200 });
  $("#map-nav .east a").tooltip({ position: "center left", offset: [0,-10], layout: '<div><i class="e"/></div>', effect: "fade", fadeInSpeed: 200, fadeOutSpeed: 200 });
  $("#map-nav .south a").tooltip({ position: "top center", offset: [-10,0], layout: '<div><i class="s"/></div>', effect: "fade", fadeInSpeed: 200, fadeOutSpeed: 200 });
  $("#map-nav .west a").tooltip({ position: "center right", offset: [0,10], layout: '<div><i class="w"/></div>', effect: "fade", fadeInSpeed: 200, fadeOutSpeed: 200 });
  
  // Reveal map bubbles when list links are hovered
  $(".site-list a").hoverIntent({
    interval: 200,
    over: function() {
      var target = $(this).attr("rel");
      if (target) {
        $("#map-sites .info").fadeOut(10); 
        $("#map-sites #"+target).delay(200).find(".info").fadeIn("fast").removeAttr("aria-hidden");
      }
    }, 
    out: function() {
      var target = $(this).attr("rel"); 
      if (target) { 
        $("#map-sites #"+target).find(".info").fadeOut(100).attr("aria-hidden", "true");
      }
    }
  });
  
  // Reveal map bubbles when list links are focused
  $(".site-list a").focus(function(){
    var target = $(this).attr("rel");
    if (target) {
      $("#map-sites .info:visible").hide(); 
      $("#map-sites #"+target).delay(200).find(".info").fadeIn("fast").removeAttr("aria-hidden");
    }
  });
  $(".site-list a").blur(function(){
    $("#map-sites .info").fadeOut(100).attr("aria-hidden", "true");
  });   

});
