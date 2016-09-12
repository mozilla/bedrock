/* global PluginCheck, Mustache, vulnerablePluginsTmpl, outdatedPluginsTmpl,
   unknownPluginsTmpl, upToDatePluginsTmpl */

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

    /**
     * Handles click events triggered from various plugin status buttons. Once the
     * click event is received, it sends the relevant data about the interaction to GA.
     */
    function handleButtonInteractions() {
        $pluginsContainer.on('click', 'a.button', function(event) {

            window.dataLayer.push({
                'event': 'plugincheck-interactions',
                'interaction': 'button click',
                'plugin-action': event.target.dataset['status'],
                'plugin-name': event.target.dataset['name']
            });
        });
    }

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
                    'url': plugin.url,
                    'status': plugin.status
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
                    'url': plugin.url,
                    'status': plugin.status
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
                    'url': plugin.url,
                    'status': plugin.status
                };
            } else if(plugin.status === 'unknown') {
                currentPlugin.unknownPlugins = {
                    'icon': mediaURL + iconFor(plugin.name),
                    'plugin_name': plugin.name,
                    'plugin_detail': plugin.description,
                    'plugin_status': window.trans('unknown'),
                    'plugin_version': plugin.version,
                    'button_research': window.trans('button_research'),
                    'url': unknownPluginUrl(plugin.name),
                    'status': plugin.status
                };
            }

            showPlugin(currentPlugin);
        }
    }

    /**
     * Counts the total number of plugins per category i.e vulnerable, outdated,
     * combines latest and newer as up to date, and lastly unknown.
     * @param {array} plugins - The array of plugins returned from the plugin service.
     * @returns pluginTotals - Object containing the totals for the various types of plugins.
     */
    function pluginCounter(plugins) {
        var pluginTotals = {
            vulnerableCount: 0,
            outdatedCount: 0,
            upToDateCount: 0,
            unknownCount: 0
        };

        // loop through all plugins and total up the plugin counts per category.
        for (var i = 0, l = plugins.length; i < l; i++) {
            if (plugins[i].status === 'vulnerable') {
                pluginTotals.vulnerableCount += 1;
            } else if (plugins[i].status === 'outdated') {
                pluginTotals.outdatedCount += 1;
            } else if (plugins[i].status === 'latest' || plugins[i] === 'newer') {
                pluginTotals.upToDateCount += 1;
            } else if (plugins[i].status === 'unknown') {
                pluginTotals.unknownCount += 1;
            }
        }

        return pluginTotals;
    }

    // show main download button to non Fx traffic
    if(!client.isFirefox && !client.isLikeFirefox) {
        wrapper.addClass('non-fx');
    }

    // show for outdated Fx versions
    // bug 1301721 only use major Firefox version until 49.0 is released
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        client.getFirefoxDetails(function(data) {
            if (!client._isFirefoxUpToDate(false) && !data.isESR) {
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

                    // filter out any undefined entries in the array that could be
                    // caused by data problems on the database side.
                    // https://bugzilla.mozilla.org/show_bug.cgi?id=1249892
                    response = response.filter(function(index) {
                        return typeof index !== 'undefined';
                    });

                    var pluginTotals = pluginCounter(response);

                    // ping GA with plugin totals
                    window.dataLayer.push({
                        'event': 'plugincheck-load',
                        'interaction': 'page load',
                        'total-plugins': response.length,
                        'plugin-vulnerable-count': pluginTotals.vulnerableCount,
                        'plugin-outdated-count': pluginTotals.outdatedCount,
                        'plugin-up-to-date-count': pluginTotals.upToDateCount,
                        'plugin-unknown-count': pluginTotals.unknownCount
                    });

                    $pluginsContainer.removeClass('hidden');

                    displayPlugins(response);
                    handleButtonInteractions();
                } else {
                    $noPluginsContainer.removeClass('hidden');
                }
            }
        );
    }
});
