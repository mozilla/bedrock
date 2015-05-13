$(function() {

    function supportsSVG() {
        return document.implementation.hasFeature('http://www.w3.org/TR/SVG11/feature#Image', '1.1');
    }

    // fallback to .png for browsers that don't support .svg as an image.
    if (!supportsSVG()) {
        $('img[src*="svg"][data-fallback="true"]').attr('src', function() {
            return $(this).attr('data-png');
        });
    }
});
