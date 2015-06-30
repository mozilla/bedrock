/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('plugincheck.js', function() {

    'use strict';

    var plugins;
    var flashNewer;
    var flashLatest;
    var flashOutdated;
    var flashVulnerable;
    var unknownPlugin;

    // set some variable values used by the below tests.
    beforeEach(function () {
        plugins = {
            adobe_flash_player: {
                description: '',
                display_name: 'Adobe Flash Player',
                mimes: [
                    'application/x-shockwave-flash',
                    'application/futuresplash'
                ],
                regex: ['.*Flash.*'],
                url: 'http://www.adobe.com/go/getflashplayer',
                versions: {
                    all: {
                        latest: [
                            {
                                detected_version: '17.0.0.134',
                                detection_type: 'original',
                                os_name: '*',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'latest',
                                version: '17.0.0.134'
                            },
                        ],
                        vulnerable: [
                            {
                                detected_version: '13.0.0.214',
                                detection_type: '*',
                                os_name: '*',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'vulnerable',
                                version: '13.0.0.214',
                                vulnerability_description: 'Message',
                                vulnerability_url: 'http://helpx.adobe.com/'
                            }
                        ]
                    },
                    mac: {
                        latest: [
                            {
                                detected_version: '17.0.0.134',
                                detection_type: 'original',
                                os_name: 'mac',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'latest',
                                version: '17.0.0.134'
                            }
                        ],
                        vulnerable: [
                            {
                                detected_version: '16.0.0.296',
                                detection_type: '*',
                                os_name: 'mac',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'vulnerable',
                                version: '16.0.0.296',
                                vulnerability_description: 'Message',
                                vulnerability_url: 'http://helpx.adobe.com/'
                            }
                        ]
                    },
                    win: {
                        latest: [
                            {
                                detected_version: '17.0.0.134',
                                detection_type: 'original',
                                os_name: 'win',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'latest',
                                version: '17.0.0.134'
                            }
                        ],
                        vulnerable: [
                            {
                                detected_version: '16.0.0.296',
                                detection_type: '*',
                                os_name: 'win',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'vulnerable',
                                version: '16.0.0.296',
                                vulnerability_description: 'Message',
                                vulnerability_url: 'http://helpx.adobe.com/'
                            }
                        ]
                    },
                    lin: {
                        latest: [
                            {
                                detected_version: '11.2.202.451',
                                detection_type: 'original',
                                os_name: 'win',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'latest',
                                version: '11.2.202.4514'
                            }
                        ],
                        vulnerable: [
                            {
                                detected_version: '11.2.202.359',
                                detection_type: '*',
                                os_name: 'win',
                                platform: {
                                    app_id: '*',
                                    app_release: '*',
                                    app_version: '*',
                                    locale: '*'
                                },
                                status: 'vulnerable',
                                version: '11.2.202.359',
                                vulnerability_description: 'Message',
                                vulnerability_url: 'http://helpx.adobe.com/'
                            }
                        ]
                    }
                }
            }
        };

        flashNewer = {
            description: 'Shockwave Flash 18.0 r0',
            name: 'Shockwave Flash',
            version: '18.0.1.135'
        };

        flashLatest = {
            description: 'Shockwave Flash 17.0 r0',
            name: 'Shockwave Flash',
            version: '17.0.0.134'
        };

        flashOutdated = {
            description: 'Shockwave Flash 13.0 r0',
            name: 'Shockwave Flash',
            version: '13.0.0.200'
        };

        flashVulnerable = {
            description: 'Shockwave Flash 13.0 r0',
            name: 'Shockwave Flash',
            version: '13.0.0.214'
        };

        unknownPlugin = {
            description: 'Some unknown plugin',
            name: 'Unknown',
            version: '3.14'
        };

    });

    it('should return true Totem file name types', function() {
        expect(PluginCheck.isTotem('libtotem-narrowspace-plugin.so')).toBe(true);
    });

    it('should return false, as this is VLC', function() {
        expect(PluginCheck.isTotem('libtotem-cone-plugin.so')).toBe(false);
    });

    it('should return an object for a match', function() {
        var pluginData = PluginCheck.isKnownPlugin(plugins, flashLatest);

        expect(pluginData.display_name).toBe('Adobe Flash Player');
        expect(pluginData.versions.win.vulnerable[0].version).toBe('16.0.0.296');
    });

    it('should return false for no match', function() {
        expect(PluginCheck.isKnownPlugin(plugins, unknownPlugin)).toBe(false);
    });

    it('should return a correctly populated plugin object for a newer plugin version', function() {
        var plugin = PluginCheck.populatePluginObject(plugins.adobe_flash_player, flashNewer);
        expect(plugin.name).toBe('Adobe Flash Player');
        expect(plugin.status).toBe('newer');
        expect(plugin.vulnerability_description).toBe(undefined);
    });

    it('should return a correctly populated plugin object for a latest plugin version', function() {
        var plugin = PluginCheck.populatePluginObject(plugins.adobe_flash_player, flashLatest);
        expect(plugin.name).toBe('Adobe Flash Player');
        expect(plugin.status).toBe('latest');
        expect(plugin.vulnerability_description).toBe(undefined);
    });

    it('should return a correctly populated plugin object for an outdated plugin version', function() {
        var plugin = PluginCheck.populatePluginObject(plugins.adobe_flash_player, flashOutdated);
        expect(plugin.name).toBe('Adobe Flash Player');
        expect(plugin.status).toBe('outdated');
        expect(plugin.vulnerability_description).toBe(undefined);
    });

    it('should return a correctly populated plugin object for a vulnerable plugin version', function() {
        var plugin = PluginCheck.populatePluginObject(plugins.adobe_flash_player, flashVulnerable);
        expect(plugin.name).toBe('Adobe Flash Player');
        expect(plugin.status).toBe('vulnerable');
        expect(plugin.vulnerability_description).toBe('Message');
        expect(plugin.vulnerability_url).toBe('http://helpx.adobe.com/');
    });

    it('return a list of known versions for the current OS and those marked All', function() {
        var knownVersions = PluginCheck.getKnownVersionInfo(plugins.adobe_flash_player.versions);

        expect(knownVersions.latest.length).toBe(2);
        expect(knownVersions.vulnerable.length).toBe(2);
    });
});
