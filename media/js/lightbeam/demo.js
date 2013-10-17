/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var Demo = (function() {
  function show(graph) {
    function findPageLoadIntervals(json, requestReferrer) {
      var requests = [];

      if (typeof(requestRefferer) == "string")
        requestReferrer = [requestReferrer];

      for (var domain in json)
        for (var referrer in json[domain].referrers) {
          var time = json[domain].referrers[referrer][0];
          if (requestReferrer.indexOf(referrer) != -1) {
            requests.push(time);
          }
        }

      var uniqueRequests = [];
      requests.forEach(function(time) {
        if (uniqueRequests.indexOf(time) == -1)
          uniqueRequests.push(time);
      });

      return uniqueRequests.sort().reverse();
    }

    function getJsonAtTime(json, maxTime) {
      var filtered = {};

      for (var domain in json) {
        filtered[domain] = {referrers: {}};
        for (var referrer in json[domain].referrers) {
          var time = json[domain].referrers[referrer][0];
          if (time <= maxTime)
            filtered[domain].referrers[referrer] = json[domain].referrers[referrer];
        }
      }

      return filtered;
    }

    jQuery.getJSON("/media/js/collusion/sample-tracking-info.json", function(json) {
      $(".demo").find(".step").hide();
      $(".demo").show();
      $(".demo").find(".step.0").fadeIn();

      var step = 0;
      var DOMAINS = [
        "imdb.com",
        "nytimes.com",
        ["huffingtonpost.com", "atwola.com"],
        "gamespot.com",
        "reference.com"
      ];

      function showNextStep() {
        $(".exposition").slideUp();
        $(".demo").find(".step." + step).fadeOut(function() {
          var times = findPageLoadIntervals(json, DOMAINS[step]);
          var nextTime = times.pop();
          var virtualTime = 0;

          function triggerNextRequest() {
            virtualTime = nextTime;
            graph.update(getJsonAtTime(json, virtualTime));
            if (times.length) {
              nextTime = times.pop();
              setTimeout(triggerNextRequest, nextTime - virtualTime);
            } else
              $(".demo").find(".step." + step).fadeIn();
          }

          triggerNextRequest();

          step++;
        });
      }

      $(".demo").find(".next").click(showNextStep);
    });
  }

  var Demo = {
    show: show
  };

  return Demo;
})();
