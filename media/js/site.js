
(function() {
    var site = {
        platform: 'windows'
    };

    if(navigator.platform.indexOf("Win32") != -1 ||
       navigator.platform.indexOf("Win64") != -1) {
        site.platform = 'windows';
    }
    else if(navigator.platform.indexOf("Linux") != -1) {
        site.platform = 'linux';
    }
    else if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        site.platform = 'osx';
    }
    else if (navigator.userAgent.indexOf("MSIE 5.2") != -1) {
        site.platform = 'osx';
    }
    else if (navigator.platform.indexOf("Mac") != -1) {
        site.platform = 'mac';
    }
    else {
        site.platform = 'other';
    }

    function init() {
        var b = $(document.body);
        // Remove the default platform
        b.removeClass('windows');
        b.addClass(site.platform);
    }

    $(document).ready(init);
    window.site = site;
})();
