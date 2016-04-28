/* exported vulnerablePluginsTmpl, outdatedPluginsTmpl, unknownPluginsTmpl,
   upToDatePluginsTmpl */

var vulnerablePluginsTmpl = '{{#vulnerablePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button red" target="_blank" data-name="{{plugin_name}}" data-status="{{status}}">{{button_update}}</a>' +
                        '<a class="vulnerability-link-txt more" href="{{ vulnerability_url }}" target="_blank">{{ vulnerability_link_txt }}</a></td>' +
                        '</tr> {{/vulnerablePlugins}}',
    outdatedPluginsTmpl = '{{#outdatedPlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button orange" target="_blank" data-name="{{plugin_name}}" data-status="{{status}} ">{{button_update}}</a></td>' +
                        '</tr> {{/outdatedPlugins}}',
    unknownPluginsTmpl = '{{#unknownPlugins}} <tr><th scope="row">' +
                        '{{plugin_name}} (v. {{ plugin_version }})' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="action"><a href="{{ url }}" class="button" target="_blank" data-name="{{plugin_name}}" data-status="{{status}} ">{{button_research}}</a></td>' +
                        '</tr> {{/unknownPlugins}}',
    upToDatePluginsTmpl = '{{#upToDatePlugins}} <tr><th scope="row">' +
                        '<img class="icon" width="60" height="60" src="{{icon}}" alt="" />' +
                        '{{plugin_name}}' +
                        '<small>{{{ plugin_detail }}}</small>' +
                        '</th>' +
                        '<td class="status">{{plugin_status}}<div class="plugin_version">{{ plugin_version }}</div></td>' +
                        '<td class="action"><a href="{{ url }}" class="button green" target="_blank" data-name="{{plugin_name}}" data-status="{{status}} ">{{button_uptodate}}</a></td>' +
                        '</tr> {{/upToDatePlugins}}';
