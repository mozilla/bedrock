/* global PluginCheck, Mustache, featuredPluginsTmpl, otherPluginsTmpl, unknownPluginsTmpl */

$(function() {
    'use strict';

    var client = Mozilla.Client;
    var utils = Mozilla.Utils;
    var wrapper = $('#wrapper');

    // Plugin containers
    var $loader = $('.plugincheck-loader');
    var $pluginsStatusContainer = $('#plugins-status-container');
    var $pluginsContainer = $('#plugins-container');
    var $outOfDateContainer = $('#out-of-date-container');
    var $notSupportedContainer = $('#not-supported-container');
    var $noPluginsContainer = $('#no-plugins-container');

    // Plugin tables
    var $featuredPluginsSection = $('#sec-plugin-featured');
    var $featuredPluginsBody = $('#plugin-featured');
    var $outdatedPluginsSection = $('#sec-plugin-outdated');
    var $outdatedPluginsBody = $('#plugin-outdated');
    var $unknownPluginsSection = $('#sec-plugin-unknown');
    var $unknownPluginsBody = $('#plugin-unknown');
    var $upToDatePluginsSection = $('#sec-plugin-uptodate');
    var $upToDatePluginsBody = $('#plugin-uptodate');

    // Plugin button text and status strings
    var _updateNowButtonText = utils.trans('buttonUpdateNow');
    var _learnMoreButtonText = utils.trans('buttonLearnMore');
    var _iconAltText = utils.trans('iconAltTxt');
    var _pluginStatusUpToDate = utils.trans('upToDate');
    var _pluginStatusVulnerable = utils.trans('vulnerable');
    var _pluginStatusOutdated = utils.trans('outdated');
    var _pluginStatusUnknown = utils.trans('unknown');

    // Total number of vulnerable plugins that are *not* featured plugins.
    var _otherPluginVulnerableCount = 0;

    // Plugin icons
    var mediaURL = utils.trans('mediaUrl') + 'img/plugincheck/app-icons/';
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

    /**
     * Handles click events triggered from various plugin status buttons. Once the
     * click event is received, it sends the relevant data about the interaction to GA.
     */
    function handleButtonInteractions() {
        $pluginsContainer.on('click', 'a.action-link', function(event) {
            window.dataLayer.push({
                'event': 'plugincheck-interactions',
                'interaction': 'button click',
                'plugin-action': event.target.dataset['status'],
                'plugin-name': event.target.dataset['name']
            });
        });
    }

    /**
     * Renders a plugin object using associated template for each status.
     * @param {object} plugin - Plugin object to render.
     */
    function showPlugin(plugin) {
        var pluginHtml = '';

        // Response was a featured plugin.
        if (plugin.featured) {
            pluginHtml = Mustache.to_html(featuredPluginsTmpl, plugin);
            $featuredPluginsBody.append(pluginHtml);
            $featuredPluginsSection.show();
            return;
        }

        // Response was a vulnerable or outdated plugin.
        if (plugin.outdated) {
            pluginHtml = Mustache.to_html(otherPluginsTmpl, plugin);
            $outdatedPluginsBody.append(pluginHtml);
            $outdatedPluginsSection.show();

            // If the plugin is vulnerable keep a count for
            // displaying the "All Plugins" heading status.
            if (plugin.status === 'vulnerable') {
                _otherPluginVulnerableCount += 1;
            }
            return;
        }

        // Response was an unknown plugin.
        if (plugin.status === 'unknown') {
            pluginHtml = Mustache.to_html(unknownPluginsTmpl, plugin);
            $unknownPluginsBody.append(pluginHtml);
            $unknownPluginsSection.show();
            return;
        }

        // Response was an up to date plugin.
        if (plugin.status === 'latest' || plugin.status === 'newer') {
            pluginHtml = Mustache.to_html(otherPluginsTmpl, plugin);
            $upToDatePluginsBody.append(pluginHtml);
            $upToDatePluginsSection.show();
        }
    }

    /**
     * Gets the localized text for plugin action button.
     * @param {string} status - Status of the plugin.
     * @returns {string} - Localized button text dependent on status.
     */
    function getPluginButtonText(status) {
        if (status === 'vulnerable' || status === 'outdated') {
            return _updateNowButtonText;
        } else {
            return _learnMoreButtonText;
        }
    }

    /**
     * Gets the localized text for plugin status.
     * @param {string} status - Status of the plugin.
     * @returns {string} - Localized text for plugin status.
     */
    function getPluginStatusText(status) {
        var text;

        switch(status) {
        case 'latest':
        case 'newer':
            text = _pluginStatusUpToDate;
            break;
        case 'vulnerable':
            text = _pluginStatusVulnerable;
            break;
        case 'outdated':
            text = _pluginStatusOutdated;
            break;
        default:
            text = _pluginStatusUnknown;
            break;
        }
        return text;
    }

    /**
     * Gets the associated URL for a plugin.
     * @param {object} plugin - The plugin object for the URL needed.
     * @returns {string} - URL for plugin dependent on status.
     */
    function getPluginUrl(plugin) {
        if (plugin.status === 'unknown') {
            return 'https://duckduckgo.com/?q=' + plugin.name;
        } else {
            return plugin.url;
        }
    }

    /**
     * Determines if the plugin is either Flash or Silverlight.
     * @param {string} pluginName - Plugin name.
     * @returns {boolean}
     */
    function isFeaturedPlugin(pluginName) {
        return pluginName.indexOf('Flash') >= 0 || pluginName.indexOf('Silverlight') >= 0;
    }

    /**
     * Determines if the plugin is either out of date or vulnerable.
     * @param {string} status - Plugin status.
     * @returns {boolean}
     */
    function isOutdatedPlugin(status) {
        return status === 'vulnerable' || status === 'outdated';
    }

    /**
     * Processes the list of plugin data to prepare for template rendering.
     * @param {array} pluginList - Listy of plugins
     */
    function displayPlugins(pluginList) {
        pluginList.forEach(function(plugin) {
            var currentPlugin = {
                'icon': mediaURL + iconFor(plugin.name),
                'plugin_name': plugin.name,
                'plugin_detail': plugin.description,
                'plugin_status': getPluginStatusText(plugin.status),
                'plugin_version': plugin.version,
                'button_txt': getPluginButtonText(plugin.status),
                'img_alt_txt': _iconAltText,
                'url': getPluginUrl(plugin),
                'status': plugin.status,
                'featured': isFeaturedPlugin(plugin.name),
                'outdated': isOutdatedPlugin(plugin.status)
            };

            if (plugin.status === 'vulnerable' && plugin.vulnerability_url) {
                currentPlugin['vulnerability_url'] = plugin.vulnerability_url;
                currentPlugin['vulnerability_link_txt'] = _learnMoreButtonText;
            }

            showPlugin(currentPlugin);
        });
    }

    /**
     * Displays a count of vulnerable plugins contained in the "All Plugins"
     * expandable heading, if any exist.
     */
    function displayPluginVulnerableStatus() {
        var $vulnerableWarning;
        var count;
        if (_otherPluginVulnerableCount > 0) {
            count = '(' + _otherPluginVulnerableCount + ')';
            $vulnerableWarning = $('#vulnerable-warning');
            $vulnerableWarning.find('.count').text(count);
            $vulnerableWarning.removeClass('hidden');
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
        plugins.forEach(function(plugin) {
            if (plugin.status === 'vulnerable') {
                pluginTotals.vulnerableCount += 1;
            } else if (plugin.status === 'outdated') {
                pluginTotals.outdatedCount += 1;
            } else if (plugin.status === 'latest' || plugin === 'newer') {
                pluginTotals.upToDateCount += 1;
            } else if (plugin.status === 'unknown') {
                pluginTotals.unknownCount += 1;
            }
        });

        return pluginTotals;
    }

    // show main download button to non Fx traffic
    if(!client.isFirefox && !client.isLikeFirefox || client.isFirefoxiOS) {
        $pluginsStatusContainer.addClass('hidden');
        $notSupportedContainer.removeClass('hidden');
    }

    // show for outdated Fx versions
    // bug 1301721 only use major Firefox version until 49.0 is released
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        client.getFirefoxDetails(function(data) {
            if (!client._isFirefoxUpToDate(false) && !data.isESR) {
                wrapper.addClass('firefox-out-of-date');
                $outOfDateContainer.removeClass('hidden');
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

                    displayPlugins(response);
                    displayPluginVulnerableStatus();
                    handleButtonInteractions();
                    $pluginsContainer.removeClass('hidden');

                    // expand the plugins section if the user has no featured plugins.
                    if ($('#sec-plugin-featured:visible').length === 0) {
                        $('#all-plugins-heading[aria-expanded="false"]').click();
                    }
                } else {
                    $noPluginsContainer.removeClass('hidden');
                }
            }
        );
    }
});
