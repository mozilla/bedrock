var vulnerablePluginsTmpl = '{{#vulnerablePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative" target="_blank"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/vulnerablePlugins}}',
    outdatedPluginsTmpl = '{{#outdatedPlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative" target="_blank"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/outdatedPlugins}}',
    unknownPluginsTmpl = '{{#unknownPlugins}} <tr><th scope="row">' +
                        '{{plugin_name}} (v. {{ plugin_version }})' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="action"><a href="{{ url }}" class="button research" target="_blank"><span>{{button_research}}</span></a></td>' +
                        '</tr> {{/unknownPlugins}}',
    upToDatePluginsTmpl = '{{#upToDatePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button safe" target="_blank"><span>{{button_uptodate}}</span></a></td>' +
                        '</tr> {{/upToDatePlugins}}';
