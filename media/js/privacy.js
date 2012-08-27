/*global $:true, isDoNotTrackEnabled:true */
$(function() {
    "use strict";
    var privacyTOCContainer = $(".privacy-toc");
    var absoluteBottom = window.scrollMaxY;
    var footerTotalHeight = $("#colophon").outerHeight(true);
    var topBoundry = parseInt(privacyTOCContainer.css("top"), 10) - 15;
    var bottomBoundry = absoluteBottom - footerTotalHeight;
    var scrollTopOffset = 0;

    window.addEventListener("scroll", function(evt) {
        scrollTopOffset = window.pageYOffset;

        if((scrollTopOffset > topBoundry) && (scrollTopOffset < bottomBoundry)) {
            privacyTOCContainer.css({
                "top" : scrollTopOffset
            });
        }
     }, true);

    isDoNotTrackEnabled();
});