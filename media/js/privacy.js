/*global $:true, isDoNotTrackEnabled:true */
$(function() {
    "use strict";
    var privacyTOCContainer = $(".privacy-toc");
    var privacyTOCContainerHeight = privacyTOCContainer.outerHeight(true);
    var originalTopOffset = privacyTOCContainer.css("top");
    var absoluteBottom = window.scrollMaxY;
    var footerTotalHeight = $("#colophon").outerHeight(true);
    var topBoundry = parseInt(originalTopOffset, 10) - 15;
    var bottomBoundry = absoluteBottom - footerTotalHeight;
    var scrollTopOffset = 0;

    window.addEventListener("scroll", function(evt) {
        scrollTopOffset = window.pageYOffset;

        if((scrollTopOffset > topBoundry) && ((scrollTopOffset + privacyTOCContainerHeight) < bottomBoundry)) {
            privacyTOCContainer.css({
                "top" : scrollTopOffset
            });
        } else if(scrollTopOffset < topBoundry) {
            privacyTOCContainer.css({
                "top" : ""
            });
        }
     }, true);

    isDoNotTrackEnabled();
});
