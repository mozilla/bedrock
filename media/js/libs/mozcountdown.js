/**
 * Counts down to specific dates in the future.
 *
 * @example
 * $(".some-class").mozcountdown();
 *
 * @type jQuery
 *
 * Based on kkcountdown by Krzysztof Furtak http://krzysztof-furtak.pl/2010/05/kk-countdown-jquery-plugin/
 * @version 1.0 
 *
 */

(function($) {
  'use strict';

  $.fn.mozcountdown = function(options) {

  var defaults = {
      dayText : 'day',
      daysText : 'days',
      daysTextEx : 'days',
      hoursText : 'hrs',
      hoursTextEx : 'hours',
      minutesText : 'min',
      minutesTextEx : 'minutes',
      secondsText : 'sec',
      secondsTextEx : 'seconds',
      textAfterCount : '',
      oneDayClass : false,
      displayDays : true,
      displayZeroDays : true,
      addClass : false,
      callback : false
  };

  options =  $.extend(defaults, options);

  this.each(function() {
      var _this = $(this);
  
      var box = $(document.createElement('span')).addClass('countdown-box');
      var daysCount = $(document.createElement('span')).addClass('days-count count');
      var hoursCount = $(document.createElement('span')).addClass('hours-count count');
      var minsCount = $(document.createElement('span')).addClass('mins-count count');
      var secsCount = $(document.createElement('span')).addClass('secs-count count');
      var daysLabel = $(document.createElement('abbr')).addClass('days-label label').attr('title', options.daysTextEx);
      var hoursLabel = $(document.createElement('abbr')).addClass('hours-label label').attr('title', options.hoursTextEx);
      var minsLabel = $(document.createElement('abbr')).addClass('mins-label label').attr('title', options.minutesTextEx);
      var secsLabel = $(document.createElement('abbr')).addClass('secs-label label').attr('title', options.secondsTextEx);
  
      var daysBox = $(document.createElement('span')).addClass('days-box box');
      daysBox.append(daysCount).append(daysLabel);
  
      var hoursBox = $(document.createElement('span')).addClass('hours-box box');
      hoursBox.append(hoursCount).append(hoursLabel);
  
      var minsBox = $(document.createElement('span')).addClass('mins-box box');
      minsBox.append(minsCount).append(minsLabel);
  
      var secsBox = $(document.createElement('span')).addClass('secs-box box');
      secsBox.append(secsCount).append(secsLabel);
  
      if(options.addClass !== false){
        box.addClass(options.addClass);
      }
  
      daysLabel.html(options.daysText);
      hoursLabel.html(options.hoursText);
      minsLabel.html(options.minutesText);
      secsLabel.html(options.secondsText);
  
      box.append(daysBox).append(hoursBox).append(minsBox).append(secsBox);
  
      _this.append(box);
  
      mozCountdownInit(_this);
  });

  function mozCountdownInit(_this){
      var now = new Date();
      now = Math.floor(now.getTime() / 1000);
      var event = _this.data('time');
      var count = event - now;

      if (count <= 0) {
          _this.html(options.textAfterCount);
          if (options.callback) {
              options.callback();
          }
      } else if (count <= 24*60*60) {
          setTimeout(function(){
              mozCountDown(true, _this, count);
              mozCountdownInit(_this);
          }, 1000);
      } else {
          setTimeout(function(){
              mozCountDown(false, _this, count);
              mozCountdownInit(_this);
          }, 1000);
      }
  }

  function mozCountDown(oneDay, obj, count) {
      var seconds = fixTime(count % 60);
      count = Math.floor(count/60);
      var minutes = fixTime(count % 60);
      count = Math.floor(count/60);
      var hours = fixTime(count % 24);
      count = Math.floor(count/24);
      var days = count;

      if(oneDay && options.oneDayClass !== false) {
          obj.addClass(options.oneDayClass);
      }

      if(days === 0 && !options.displayZeroDays) {
          return;
      } else if (days === 1) {
          obj.find('.days-count').html(days);
          obj.find('.days-label').html(options.dayText);
      } else {
          obj.find('.days-count').html(days);
          obj.find('.days-label').html(options.daysText);
      }
      obj.find('.hours-count').html(hours);
      obj.find('.mins-count').html(minutes);
      obj.find('.secs-count').html(seconds);
  }

  function fixTime(obj) {
      if(obj < 10){
          obj = '0' + obj;
      }
      return obj;
    }
  };

})(jQuery);
