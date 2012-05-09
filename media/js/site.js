(function() {
    var site = {
        platform: 'windows'
    };

    if(navigator.platform.indexOf("Win32") != -1 ||
       navigator.platform.indexOf("Win64") != -1) {
        site.platform = 'windows';
    }
    else if (navigator.platform.indexOf("armv7l") != -1) {
        site.platform = 'android';
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
        // Add the platform as a class name immediately to avoid lots
        // of flickering
        var b = document.body;
        b.className = b.className.replace("windows", site.platform);
    }

    init();
    window.site = site;
})();