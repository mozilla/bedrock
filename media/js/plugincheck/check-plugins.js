$(function() {
    'use strict';

    var iconFor = function (pluginName) {
        if (pluginName.indexOf('Flash') >= 0) {
            return 'icon-flash.png';
        } else if (pluginName.indexOf('Java') >= 0) {
            return 'icon-java.png';
        } else if (pluginName.indexOf('QuickTime') >= 0) {
            return 'icon-quicktime.png';
        } else if (pluginName.indexOf('DivX') >= 0) {
            return 'icon-divx.png';
        } else if (pluginName.indexOf('Totem') >= 0) {
            return 'icon-totem.png';
        } else if (pluginName.indexOf('Flip4Mac') >= 0) {
            return 'icon-flip4mac.png';
        } else if (pluginName.indexOf('WindowsMediaPlayer') >= 0) {
            return 'icon-wmp.png';
        } else if (pluginName.indexOf('VLC') >= 0) {
            return 'icon-vlc.png';
        } else if (pluginName.indexOf('Silverlight') >= 0) {
            return 'icon-silverlight.png';
        } else if (pluginName.indexOf('Shockwave') >= 0) {
            return 'icon-shockwave.png';
        } else if (pluginName.indexOf('RealPlayer') >= 0) {
            return 'icon-real.png';
        } else if (pluginName.indexOf('Adobe Acrobat') >= 0) {
            return 'icon-acrobat.png';
        } else if (pluginName.indexOf('Office Live') >= 0) {
            return 'icon-officelive.png';
        } else if (pluginName.indexOf('iPhoto') >= 0) {
            return 'icon-iphoto.png';
        } else {
            return 'default.png';
        }
    };

    var showPlugin = function(data) {
        var vulnerablePluginsSection = $('#sec-plugin-vulnerable'),
            vulnerablePluginsBody = $('#plugin-vulnerable'),
            vulnerablePluginsHtml = '',
            outdatedPluginsSection = $('#sec-plugin-outdated'),
            outdatedPluginsBody = $('#plugin-outdated'),
            outdatedPluginsHtml = '',
            unknownPluginsSection = $('#sec-plugin-unknown'),
            unknownPluginsBody = $('#plugin-unknown'),
            unknownPluginsHtml = '',
            upToDatePluginsSection = $('#sec-plugin-uptodate'),
            upToDatePluginsBody = $('#plugin-uptodate'),
            upToDatePluginsHtml = '';

        // If the latest response from the service was a vulnerable plugin,
        // pass the object here.
        if(data.vulnerablePlugins) {
            vulnerablePluginsHtml = Mustache.to_html(vulnerablePluginsTmpl, data);
            vulnerablePluginsBody.append(vulnerablePluginsHtml);

            vulnerablePluginsSection.show();
        }

        // If the latest response from the service was a outdated plugin,
        // pass the object here.
        if(data.outdatedPlugins) {
            outdatedPluginsHtml = Mustache.to_html(outdatedPluginsTmpl, data);
            outdatedPluginsBody.append(outdatedPluginsHtml);

            outdatedPluginsSection.show();

        }

        // If the latest response from the service was an unknown plugin,
        // pass the object here.
        if(data.unknownPlugins) {
            unknownPluginsHtml = Mustache.to_html(unknownPluginsTmpl, data);
            unknownPluginsBody.append(unknownPluginsHtml);

            unknownPluginsSection.show();
        }

        // If the latest response from the service was an up to date plugin,
        // pass the object here.
        if(data.upToDatePlugins) {
            upToDatePluginsHtml = Mustache.to_html(upToDatePluginsTmpl, data);
            upToDatePluginsBody.append(upToDatePluginsHtml);

            upToDatePluginsSection.show();
        }
    },
    unknownPluginUrl = function (pluginName) {
        return 'https://www.google.com/search?q=' + encodeURI(window.trans('googleSearchq') + ' ' + pluginName);
    },
    buildObject = function(data) {
        var plugin = data.pluginInfo.raw,
            url = data.url,
            currentPlugin = {},
            mediaURL = window.trans('media-url') + 'img/plugincheck/app-icons/',
            vulnerableStatusArray = ['should_disable', 'vulnerable', 'maybe_vulnerable',
                                    'outdated', 'maybe_outdated'];

        // There are rare occasions when the update URL for a plugin is not known.
        // In these cases, we want to add the plugin to the unknownPlugins array and not
        // the vulnerablePlugins nor the outdatedPlugins array.
        // @see https://bugzilla.mozilla.org/show_bug.cgi?id=887245
        if(typeof url === 'undefined' && $.inArray(data.status, vulnerableStatusArray) > -1) {
            currentPlugin.unknownPlugins = {
                'icon': mediaURL + iconFor(plugin.name),
                'plugin_name': plugin.name,
                'plugin_detail': plugin.description,
                'plugin_status': window.trans('vulnerable'),
                'button_research': window.trans('button_research'),
                'img_alt_txt': window.trans('icon_alt_txt'),
                'url': unknownPluginUrl(plugin.name)
            };
        } else {
            // Our URL has a value, do the usual song and dance.
            if(data.status === 'should_disable' || data.status === 'vulnerable' ||
                data.status === 'maybe_vulnerable') {
                currentPlugin.vulnerablePlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('vulnerable'),
                    'button_update': window.trans('button_update'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': url
                };

            } else if(data.status === 'outdated' || data.status === 'maybe_outdated') {
                currentPlugin.outdatedPlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('vulnerable'),
                    'button_update': window.trans('button_update'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': url
                };
            } else if(data.status === 'unknown') {
                currentPlugin.unknownPlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('unknown'),
                    'button_research': window.trans('button_research'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': unknownPluginUrl(plugin.name)
                };
            } else if(data.status === 'latest' || data.status === 'newer') {
                currentPlugin.upToDatePlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': plugin.version,
                    'button_uptodate': window.trans('button_uptodate'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': url
                };
            }
        }

        showPlugin(currentPlugin);
    },
    pluginCheckComplete = function() {
        var pfsStatus = $('#pfs-status');
        pfsStatus.empty();
    };

    checkPlugins('https://plugins.mozilla.org/pfs/v2', buildObject, pluginCheckComplete);
});
