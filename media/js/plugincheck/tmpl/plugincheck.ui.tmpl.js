var vulnerablePluginsTmpl = '{{#vulnerablePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/vulnerablePlugins}}',
    outdatedPluginsTmpl = '{{#outdatedPlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/outdatedPlugins}}',
    unknownPluginsTmpl = '{{#unknownPlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button research"><span>{{button_research}}</span></a></td>' +
                        '</tr> {{/unknownPlugins}}',
    upToDatePluginsTmpl = '{{#upToDatePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button safe"><span>{{button_uptodate}}</span></a></td>' +
                        '</tr> {{/upToDatePlugins}}';
