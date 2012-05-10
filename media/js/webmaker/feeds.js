google.load("feeds", "1");

var webmaker = window.webmaker || {};

webmaker = function() {
    var init = function() {
        var feed_url = $("#feed_url"),
            feed = new google.feeds.Feed(feed_url.attr('href')),
            feed_num = feed_url.attr('data-feed-list-num');
        feed.setNumEntries(feed_num);
        feed.load(function(result) {
            if (!result.error) {
                var feed_list = "<ul>";
                for (var i = 0; i < result.feed.entries.length; i++) {
                    var entry = result.feed.entries[i],
                        chunks = entry.title.split(':'),
                        name = chunks.shift();
                    feed_list += "<li><a href='" + entry.link + "'>";
                    feed_list += chunks.toString() + "</a> by " + name.toString();
                    feed_list += "</li>";
                }
                feed_list += "</ul>";
                $(feed_url).parent().before($(feed_list));
            }
        });
    };
    return {
        'init': init
    };
}();

google.setOnLoadCallback(webmaker.init);