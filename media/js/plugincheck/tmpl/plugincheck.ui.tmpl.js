var vulnerablePluginsTmpl = '{{#vulnerablePlugins}} <tr><td>' +
                        '<section>' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="{{img_alt_txt}}" />' +
                        '<h4 class="name">{{plugin_name}}</h4>' +
                        '<p class="plugin-detail">{{{ plugin_detail }}}</p>' +
                        '</section></td>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/vulnerablePlugins}}',
    outdatedPluginsTmpl = '{{#outdatedPlugins}} <tr><td>' +
                        '<section>' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="{{img_alt_txt}}" />' +
                        '<h4 class="name">{{plugin_name}}</h4>' +
                        '<p class="plugin-detail">{{{ plugin_detail }}}</p>' +
                        '</section></td>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button button-negative"><span>{{button_update}}</span></a></td>' +
                        '</tr> {{/outdatedPlugins}}',
    unknownPluginsTmpl = '{{#unknownPlugins}} <tr><td>' +
                        '<section>' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="{{img_alt_txt}} />' +
                        '<h4 class="name">{{plugin_name}}</h4>' +
                        '<p class="plugin-detail">{{{ plugin_detail }}}</p>' +
                        '</section></td>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button research"><span>{{button_research}}</span></a></td>' +
                        '</tr> {{/unknownPlugins}}',
    upToDatePluginsTmpl = '{{#upToDatePlugins}} <tr><td>' +
                        '<section>' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="{{img_alt_txt}}" />' +
                        '<h4 class="name">{{plugin_name}}</h4>' +
                        '<p class="plugin-detail">{{{ plugin_detail }}}</p>' +
                        '</section></td>' +
                        '<td class="status">{{plugin_status}}</td>' +
                        '<td class="action"><a href="{{ url }}" class="button insensitive"><span>{{button_uptodate}}</span></a></td>' +
                        '</tr> {{/upToDatePlugins}}';
