var moz = (function (parent) {
    'use strict';
    var tabzilla = parent.tabzilla = parent.tabzilla || {};

    var tab = document.getElementById('tabzilla');
    tab.className = "tabzilla-closed";
    tab.setAttribute('role', 'button');
    tab.setAttribute('aria-expanded', 'false');
    tab.setAttribute('aria-label', 'Mozilla links');

    var loadCss = function () {
        var css = document.createElement("link");
        css.rel = "stylesheet";
        css.href = '/media/css/tabzilla-initialized.css';
        document.getElementsByTagName("head")[0].appendChild(css);
    };
    var loadJS = function (callback) {
        if (typeof window.jQuery !== 'undefined') {
            callback();
        } else {
            var script = document.createElement("script");
            if (script.readyState) {
                script.onreadystatechange = function(){
                    if (script.readyState == "loaded" || script.readyState == "complete") {
                        script.onreadystatechange = null;
                        callback();
                    }
                };
            } else {
                script.onload = function(){
                    callback();
                };
            }
            script.src = '//mozorg.cdn.mozilla.net/media/js/libs/jquery-1.7.1.min.js';
            document.getElementsByTagName('head')[0].appendChild(script);
        }
    };
    tabzilla.loadAssets = function(ev) {
        if (ev.preventDefault) {
            ev.preventDefault();
        } else {
            ev.returnValue = false;
        }
        tab.className += ' tabzilla-loading';
        loadCss();
        loadJS(function () {
            $.ajaxSetup({cache: true});
            jQuery.getScript('/media/js/tabzilla-initialized.js', function(){
                moz.tabzilla.init();
            });
        });
    };
    if (typeof tab.attachEvent != 'undefined') {
        tab.attachEvent('onclick', tabzilla.loadAssets);
    } else {
        tab.addEventListener('click', tabzilla.loadAssets, false);
    }
    return parent;
}(moz || {}));