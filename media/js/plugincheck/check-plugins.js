$(function() {
    'use strict';

    var client = window.Mozilla.Client;

    var outdatedFx = $('.version-message-container');
    var wrapper = $('#wrapper');
    var $loader = $('.plugincheck-loader');
    var $pluginsContainer = $('#plugins');
    var $noPluginsContainer = $('#no-plugins');

    var readerRegEx = /Adobe \b(Reader|Acrobat)\b.*/;
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
        } else if (readerRegEx.test(pluginName)) {
            return 'icon-acrobat.png';
        } else if (pluginName.indexOf('Office Live') >= 0) {
            return 'icon-officelive.png';
        } else if (pluginName.indexOf('iPhoto') >= 0) {
            return 'icon-iphoto.png';
        } else {
            return 'default.png';
        }
    };
    var mediaURL = window.trans('media-url') + 'img/plugincheck/app-icons/';
    var unknownPluginUrl = function (pluginName) {
        return 'https://duckduckgo.com/?q=' + encodeURI(window.trans('ddgSearchq') + ' ' + pluginName);
    };

    function showPlugin(data) {
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
    }

    function displayPlugins(pluginList) {

        for (var i = 0, l = pluginList.length; i < l; i++) {
            var currentPlugin = {};
            var plugin = pluginList[i];

            if(plugin.status === 'vulnerable') {
                currentPlugin.vulnerablePlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('vulnerable'),
                    'vulnerability_url': plugin.vulnerability_url,
                    'vulnerability_link_txt': window.trans('vulnerableLinkTxt'),
                    'plugin_version': plugin.version,
                    'button_update': window.trans('button_update'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': plugin.url
                };

            } else if(plugin.status === 'outdated') {
                currentPlugin.outdatedPlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('outdated'),
                    'plugin_version': plugin.version,
                    'button_update': window.trans('button_update'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': plugin.url
                };
            } else if(plugin.status === 'latest' || plugin.status === 'newer') {
                currentPlugin.upToDatePlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('button_uptodate'),
                    'plugin_version': plugin.version,
                    'button_uptodate': window.trans('button_uptodate'),
                    'img_alt_txt': window.trans('icon_alt_txt'),
                    'url': plugin.url
                };
            } else if(plugin.status === 'unknown') {
                currentPlugin.unknownPlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('unknown'),
                    'plugin_version': plugin.version,
                    'button_research': window.trans('button_research'),
                    'url': unknownPluginUrl(plugin.name)
                };
            }

            showPlugin(currentPlugin);
        }
    }

    // show main download button to non Fx traffic
    if(!client.isFirefox && !client.isLikeFirefox) {
        wrapper.addClass('non-fx');
    }

    // show for outdated Fx versions
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        client.getFirefoxDetails(function(data) {
            if (!data.isUpToDate && !data.isESR) {
                outdatedFx.show();
            }
        });
    }

    // only execute the plugincheck code if this is Firefox
    if (client.isFirefoxDesktop || client.isFirefoxAndroid || client.isLikeFirefox) {

        $loader.removeClass('hidden');

        PluginCheck.getPluginsStatus('https://plugins.mozilla.org/en-us/plugins_list.json',
            function(response) {

                $loader.addClass('hidden');

                if (response.length > 0) {
                    $pluginsContainer.removeClass('hidden');
                    displayPlugins(response);
                } else {
                    $noPluginsContainer.removeClass('hidden');
                }
            }
        );
    }
});
