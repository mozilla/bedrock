/*globals Utils, versionCompare */

(function(exports) {

    'use strict';

    var clientOS = Utils.getOS(navigator.userAgent);

    /**
     * Java plugin version numbers are exposed with a leading 1. which obscures
     * the actual version number we will find in the plugincheck database. This
     * removes the leading bits and returns the 'real' version number.
     * @returns The Java version number excluding the leading 1.
     */
    function setJavaVersion() {
        var type;
        var installedVersion;
        var mimes = navigator.mimeTypes['application/x-java-applet'].enabledPlugin;

        for (var mime in mimes) {
            if(mimes.hasOwnProperty(mime) && mime.indexOf('jpi-version') > -1) {
                type = mime;
                // + 3 to strip of the leading 1. in java versions
                installedVersion = type.substring(type.indexOf('=') + 3)
                    .replace('_', '.');
            }
        }
        return installedVersion;
    }

    /**
    * Creates and populates a plugin object for an unknown plugin.
    * @param {object} pluginInfo - Information about the plugin from the plugins DB
    * @param {object} currentPlugin - The current installed plugin with info from the browser.
    * @returns The unknown plugin as an object
    */
    function populateUnknownPlugin (currentPlugin) {
        return {
            name: currentPlugin.name,
            version: currentPlugin.version,
            description: currentPlugin.description,
            status: 'unknown'
        };
    }

    /**
     * Sets the status of the current plugin.
     *
     * @param {object} plugin - The plugin object to update
     * @param {string} installedVersion - Version of the current installed plugin
     * @param {array} knownVersions - Array of all known versions
     *
     * @returns the updated plugin object with the status set. For vulnerable
     * plugins, the vulnerability_description and vulnerability_url fields are
     * also set.
     */
     function setPluginStatus (plugin, installedVersion, knownVersions) {
        var knownAbsLatest;

        // sort versions from low to high
        knownVersions.latest.sort(function(v1, v2) {
            // TODO: the server currently returns some versions with a leading
            // space, therefore the trim workaround is currently required.
            // Remove the trims once the backend rewrite is done.
            return versionCompare($.trim(v1.version), $.trim(v2.version));
        });

        if (Utils.isMatch(installedVersion, knownVersions.latest)) {

            plugin['status'] = 'latest';
            return plugin;

        } else if (Utils.isMatch(installedVersion, knownVersions.vulnerable) || knownVersions.latest.length === 0) {
            // If falling into this branch due to knownVersions.latest.length being 0,
            // vulnerableInfo is false, leaving 'vulnerability_description' and
            // 'vulnerability_url' as undefined. This seems to not cause any problems...
            var vulnerableInfo = Utils.isMatch(installedVersion, knownVersions.vulnerable);
            plugin['status'] = 'vulnerable';
            plugin['vulnerability_description'] = vulnerableInfo.vulnerability_description;
            plugin['vulnerability_url'] = vulnerableInfo.vulnerability_url;

            return plugin;
        }

        // after checking for empty latest array, store the absolutely latest known version.
        knownAbsLatest = knownVersions.latest[knownVersions.latest.length - 1].version;

        if (versionCompare(installedVersion, knownAbsLatest) < 0) {

            // it is not the latest but also not vulnerable so, just outdated
            plugin['status'] = 'outdated';
            return plugin;

        } else if (versionCompare(installedVersion, knownAbsLatest) > 0) {

            // if newer than our known absolutely latest version, set status as newer but currently,
            // it will still show up as up to date (latest) in the UI
            plugin['status'] = 'newer';
            return plugin;
        }
    }

    var PluginCheck = {
        /**
        * Returns the latest and vulnrable known versions for the current plugin.
        * @params {object} knownPluginReleases
        * @returns The latest and vulnerable versions for this plugin.
        */
        getKnownVersionInfo:function (knownPluginReleases) {
            var latest;
            var vulnerable;

            // See whether we have data for the current OS
            if (knownPluginReleases.hasOwnProperty(clientOS)) {

                // Combine all release for the current OS and
                // versions marked for all operating systems.
                latest = knownPluginReleases[clientOS].latest.concat(
                    knownPluginReleases['all'].latest
                );
                vulnerable = knownPluginReleases[clientOS].vulnerable.concat(
                    knownPluginReleases['all'].vulnerable
                );
            } else if (knownPluginReleases.hasOwnProperty('all')) {
                latest = knownPluginReleases['all'].latest;
                vulnerable = knownPluginReleases['all'].vulnerable;
            }

            return { latest: latest, vulnerable: vulnerable };
        },
        /**
        * Populate the plugin object with the required data for the UI.
        * @param {object} pluginInfo - Information about the plugin from the plugins DB
        * @param {object} currentPlugin - The current installed plugin with info from the browser.
        * @returns The populated plugin object
        */
        populatePluginObject: function(pluginInfo, currentPlugin) {
            var installedVersion = currentPlugin.version;

            if (currentPlugin.name.indexOf('Java') > -1 &&
                'undefined' !== navigator.mimeTypes['application/x-java-applet']) {
                    // we need todo some extra work to get a decent version number
                    installedVersion = setJavaVersion();
            }

            var plugin = {};
            var knownVersions = PluginCheck.getKnownVersionInfo(pluginInfo.versions);
            var description = pluginInfo.description || currentPlugin.description;

            plugin = {
                name: pluginInfo.display_name,
                version: installedVersion,
                description: description,
                url: pluginInfo.url
            };

            return setPluginStatus(plugin, installedVersion, knownVersions);
        },
        /**
        * Determines whether we are dealing with one of the known plugins and returns it,
        * or false if this is not a known plugin.
        * @param {array} knownPlugins - Array of known plugins
        * @param {object} currentPlugin - The current installed plugin to test.
        * @returns The knownPlugin object or false
        */
        isKnownPlugin: function (knownPlugins, currentPlugin) {

            for (var plugin in knownPlugins) {
                if(knownPlugins.hasOwnProperty(plugin)) {
                    var knownPluginName = knownPlugins[plugin].display_name;
                    var patterns = [];

                    // For some plugins a regex is needed to match the name,
                    // see if it is the case for the current plugin.
                    if (knownPlugins[plugin].regex.length) {
                        patterns = knownPlugins[plugin].regex;
                    }

                    var patternsLength = patterns.length;
                    if (patternsLength) {
                        for (var i = 0; i < patternsLength; i++) {
                            var re = new RegExp(patterns[i], 'g');

                            if (re.test(currentPlugin.name)) {
                                return knownPlugins[plugin];
                            }
                        }
                    } else if (knownPluginName.indexOf(currentPlugin.name) > -1) {
                        return knownPlugins[plugin];
                    }
                }
            }
            return false;
        },
        /**
         * On Linux the Totem plugin handles Quicktime video but, it masquerade's
         * as the either the Quicktime player or the Windows Media player by
         * setting it's name accordingly. This causes problems when checking the
         * list of known plugins, hence we need this check to determine it's real
         * identity by looking at the filename for the enabledPlugin.
         *
         * @params {string} filename - The filename to check for libtotem
         * @returns {boolean} True if it is Totem else false
         */
        isTotem: function(filename) {

            var totemQuicktime = filename.indexOf('libtotem-narrowspace');
            var totemWindowsMedia = filename.indexOf('libtotem-gmp');

            if (totemQuicktime > -1 || totemWindowsMedia > -1) {
                return true;
            }

            return false;
        },
        /**
        * Get's a list of plugins and versions as a JSON object from the database. Iterates over
        * navigator.mimeTypes to gather the installed plugins. For each known plugin, it
        * determines whether the version is the latest, is outdated or vulnerable.
        * @param {string} endpoint - The JSON endpoint exposed by the plugins database service.
        * @returns pluginList - List of known and unknown plugins
        */
        getPluginsStatus: function(endpoint, callback) {

            // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1131137
            navigator.plugins.refresh();

            $.getJSON(endpoint, function(data) {

                var pluginNames = [];
                var installedPlugins = [];
                var pluginList = [];

                var mimes = navigator.mimeTypes;
                var knownPlugins = data.plugins;

                for (var i = 0, l = mimes.length; i < l; i++) {
                    var currentMime = mimes[i];
                    var pluginData = {};

                    if (typeof currentMime !== 'undefined' && currentMime.enabledPlugin) {
                        var enabledPlugin = currentMime.enabledPlugin;
                        var pluginName = enabledPlugin.name;

                        // on Linux we need to check whether this in fact the totem plugin?
                        if (clientOS === 'lin' && PluginCheck.isTotem(enabledPlugin.filename)) {
                            pluginName = 'Totem';
                        }

                        if ($.inArray(enabledPlugin.name, pluginNames) === -1) {
                            pluginData = {
                                name: pluginName,
                                version: enabledPlugin.version,
                                description: enabledPlugin.description
                            };

                            installedPlugins.push(pluginData);
                            pluginNames.push(enabledPlugin.name);
                        }
                    }
                }

                for (i = 0, l = installedPlugins.length; i < l; i++) {
                    var currentInstalledPlugin = installedPlugins[i];
                    var pluginInfo = PluginCheck.isKnownPlugin(knownPlugins, currentInstalledPlugin);

                    if (pluginInfo) {
                        pluginList.push(PluginCheck.populatePluginObject(pluginInfo, currentInstalledPlugin));
                    } else {
                        pluginList.push(populateUnknownPlugin(currentInstalledPlugin));
                    }
                }

                callback(pluginList);

            }).fail(function(xhr, status, error) {
                console.log('xhr', xhr);
                console.log('status', status);
                console.log('error', error);
            });
        }
    };

    exports.PluginCheck = PluginCheck;

})(window);
