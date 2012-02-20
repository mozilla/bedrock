/**
 * Various tools for the HTML5 video element
 *
 * Meant to be used with CSS in /styles/tignish/video-player.css.
 *
 * This file contains Flash-detection routines adapted from SWFObject and
 * originally licensed under the MIT license.
 *
 * See http://blog.deconcept.com/flashobject/
 *
 * This file can make use of the SMILE-based subtitling routines provided
 * courtesy of Fabien Cazenave for INRIA under the BSD license. Those are
 * stored in mozilla-video-tools-addsubtitles.js
 *
 *
 * @copyright 2009-2011 Mozilla Corporation
 * @author    Michael Gauthier <mike@silverorange.com>
 */

// create namespace
if (typeof Mozilla == 'undefined') {
  var Mozilla = {};
}

// {{{ Mozilla.VideoControl

/**
 * Initializes video controls on this page after the document has been loaded
 */
$(document).ready(function() {
  $('.mozilla-video-control').each(function() {
    Mozilla.VideoControl.controls.push(
      new Mozilla.VideoControl($(this))
    )
  });
});

/**
 * Provides a click-to-play button for HTML5 video element content
 *
 * If the HTML5 video element is supported, the following markup will
 * automatically get the click-to-play button when the page initializes:
 * <code>
 * &lt;div class="mozilla-video-control"&gt;
 *   &lt;video ... /&gt;
 * &lt;/div&gt;
 * </code>
 *
 * @param jQuery|String container
 */
Mozilla.VideoControl = function(container)
{
  if (typeof container == 'String') {
    container = $('#' + container);
  }

  this.container = container;

  // Retrieve jQuery object and the corresponding DOM element
  var video = container.find('video:first');

  // If there is not preload attribute set, set it to metadata
  // because this library depends on preloading
  var preload = video.attr('preload');
  if(!preload || preload == 'none') {
      video.attr('preload', 'metadata');
  }

  this.video = video;
  this._video = this.video[0];

  this.semaphore = false;

  /*
   * Check if HTMLMediaElement exists to filter out browsers that do not
   * support the video element.
   */
  if (   typeof HTMLMediaElement != 'undefined'
    && this._video instanceof HTMLMediaElement
  ) {
    this.drawControl();
    this._video._control = this;
  }
}

Mozilla.VideoControl.controls = [];

Mozilla.VideoControl.prototype.drawControl = function()
{
  var buttonTag = '<a href="#" class="mozilla-video-control-overlay" style="opacity: 0">' +
                  '<span style="visibility:hidden;">' +
                  this._video.id +
                  '</span></a>';
  this.control = $(buttonTag);

  // Show the click-to-play button. In the future, this may be changed
  // to show the click-to-play button based on media events like the
  // hiding is done.
  if (this._video.paused || this._video.ended) {
    this.show();
  }

  var that = this;

  // hide click-to-play button on these events
  this.video.bind('play playing seeking waiting', function(event) {
    that.hide();
  });

  this.control.mouseover(function(event) {
    if (!that.semaphore) {
      that.prelight();
    }
  });

  this.control.mouseout(function(event) {
    if (!that.semaphore) {
      that.unprelight();
    }
  });

  this.control.click(function(event) {
    event.preventDefault();

    if (that.semaphore || !that.videoCanPlay()) {
      return;
    }

    that.semaphore = true;
    // rewind the video
    if (that._video.ended) {
      that._video.currentTime = 0;
    }
    that._video.play();
  });

  this.container.append(this.control);
}

Mozilla.VideoControl.prototype.videoCanPlay = function()
{
  // check if we're using an older draft version of the readyState spec
  var current_data = (typeof HTMLMediaElement.CAN_PLAY == 'undefined') ?
    HTMLMediaElement.HAVE_CURRENT_DATA : HTMLMediaElement.CAN_PLAY;

  return (this._video.readyState >= current_data);
}

Mozilla.VideoControl.prototype.show = function()
{
  var that = this;

  this._video.controls = false;
  // FIXME : Does not work on http://mozilla.local/en-US/firefox/video/
  // this.control.show();
  this.control.css('display', 'block');
  this.control.stop(true).fadeTo('slow', 0.7, function() {
    that.semaphore = false;
  });
}

Mozilla.VideoControl.prototype.hide = function()
{
  var that = this;

  if (this.control.is(':visible')) {
    this.semaphore = true;
    this.control.stop(true).fadeTo('fast', 0, function() {
      $(this).hide();
      that._video.controls = true;
    });
  }
}

Mozilla.VideoControl.prototype.prelight = function()
{
  if (this.control.is(':visible')) {
    this.control.stop(true).fadeTo('fast', 1);
  }
}

Mozilla.VideoControl.prototype.unprelight = function()
{
  if (this.control.is(':visible')) {
    this.control.stop(true).fadeTo('fast', 0.7);
  }
}

// }}}
// {{{ Mozilla.VideoPlayer

/**
 * Popup player using HTML5 video element with flash fallback
 *
 * @param String  id
 * @param Array   sources
 * @param String  flv_url
 * @param Booelan autoplay
 */
Mozilla.VideoPlayer = function(id, sources, flv_url, autoplay, extra_content)
{
  this.id = id;
  this.flv_url = flv_url;
  this.sources = sources;
  this.opened = false;

  if (arguments.length > 3) {
    this.autoplay = autoplay;
  } else {
    this.autoplay = true;
  }

  if (arguments.length > 4) {
    this.extra_content = extra_content;
  } else {
    this.extra_content = '';
  }

  var that = this;

  $(document).ready(function() {
    that.init();
  });
}

Mozilla.VideoPlayer.height = 385;
Mozilla.VideoPlayer.width = 640;
Mozilla.VideoPlayer.ie6 =
    ($.browser.msie && parseInt($.browser.version, 10) <= 6);

Mozilla.VideoPlayer.close_text = 'Close';

Mozilla.VideoPlayer.fallback_text =
    'This video requires a browser with support for open video or the '
  + '<a href="http://get.adobe.com/flashplayer">Adobe Flash '
  + 'Player</a>. Alternatively, you may use the video download links '
  + 'provided.';

Mozilla.VideoPlayer.prototype.init = function()
{
  var that = this;

  // add overlay and preview image to document
  this.overlay = $('<a class="mozilla-video-player-overlay" href="#"/>')
    .hide()
    .appendTo('body')
    .click(function(e) { e.preventDefault(); that.close(); });

  this.video_container = $('<div class="mozilla-video-player-window" />')
    .hide()
    .appendTo('body');

  // set video link and video preview link event handler
  $('#' + this.id + ', #' + this.id + '-preview').click(function(e) {
    e.preventDefault();
    that.open();
  });
}

Mozilla.VideoPlayer.prototype.clearVideoPlayer = function()
{
  // remove event handlers
  this.video_container.unbind('click');

  // workaround for FF Bug #533840, manually pause all videos
  this.video_container.find('video').each(function() {
    $(this)[0].pause();
  });

  // remove all elements
  this.video_container.empty();
}

Mozilla.VideoPlayer.prototype.drawVideoPlayer = function()
{
  var that = this;

  this.clearVideoPlayer();

  // get content for player
  if (typeof HTMLMediaElement != 'undefined') {
    var content = this.getVideoPlayerContent();
  } else if (Mozilla.VideoPlayer.flash_verison.isValid([7, 0, 0])) {
    var content = this.getFlashPlayerContent();
  } else {
    var content = this.getFallbackContent();
  }

  // add download links
  content += '<div class="video-download-links">';

  if (this.extra_content != '') {
      content += this.extra_content;
  }

  content += '<ul>';
  $.each(this.sources, function(index, source) {
    content += '<li><a href="' + source.url + '">' + source.title + '</a></li>';
  });
  content += '</ul></div>';

  this.video_container.append(
    $('<div class="mozilla-video-player-close" />').append(
      $('<a href="#" />').click(function(event) {
        event.preventDefault();
        that.close();
      }).append(
        $('<img src="/img/covehead/video/clothes-lol.png" height="32" width="32" alt="' + Mozilla.VideoPlayer.close_text + '" />')
      )
    )
  ).append(
    $('<div class="mozilla-video-player-content" />').html(content)
  );
}

Mozilla.VideoPlayer.prototype.getVideoPlayerContent = function()
{
  var content =
      '<video id="htmlPlayer" width="' + Mozilla.VideoPlayer.width + '" '
      + 'height="' + Mozilla.VideoPlayer.height + '" '
      + 'controls="controls"';

  if (this.autoplay) {
    content += ' autoplay="autoplay"';
  }

  content += '>';

  $.each(this.sources, function(index, source) {
    if (!source.type) return; // must have MIME type
    content += '<source src="' + source.url + '" '
        + 'type="' + source.type + '"/>';
  });

  content += '</video>';

  return content;
}

Mozilla.VideoPlayer.prototype.getFlashPlayerContent = function()
{
  var url = '/includes/flash/playerWithControls.swf?flv=' + this.flv_url
    + '&amp;autoplay=';
  url+= (this.autoplay) ? 'true' : 'false';

  var content =
      '<object type="application/x-shockwave-flash" style="'
    + 'width: ' + Mozilla.VideoPlayer.width + 'px; '
    + 'height: ' + Mozilla.VideoPlayer.height + 'px;" '
    + 'wmode="transparent" data="' + url + '">'
    + '<param name="movie" value="' + url + '">'
    + '<param name="wmode" value="transparent">'
    + '</object>';

  return content;
}

Mozilla.VideoPlayer.prototype.getFallbackContent = function()
{
  var content =
      '<div class="mozilla-video-player-no-flash">'
    + Mozilla.VideoPlayer.fallback_text
    + '</div>';

  return content;
}

Mozilla.VideoPlayer.prototype.open = function()
{
  // hide the language form because its select element won't render
  // correctly in IE6
  $('#lang_form').hide();

  if (Mozilla.VideoPlayer.ie6) {
      this.video_container.css('position', 'absolute');
      this.overlay.css('position', 'absolute');
  }

  var that = this;
  this.resizeHandler = function(e) {
      that.resizeOverlay();
  };
  $(window).resize(this.resizeHandler);
  if (Mozilla.VideoPlayer.ie6) {
    $(window).scroll(this.resizeHandler);
  }

  this.drawVideoPlayer();
  this.resizeOverlay();

  this.overlay.fadeTo(400, 0.75);
  this.video_container.fadeIn();

  this.opened = true;

  // getSubtitles() depends on mozilla-video-tools-addsubtitles.js
  if (window.getSubtitles) {
    getSubtitles(this.video_container.css('top'));
  }
}

Mozilla.VideoPlayer.prototype.resizeOverlay = function()
{
  if (Mozilla.VideoPlayer.ie6) {
    var scrollTop    = $(window).scrollTop();
    var docHeight    = $(document).height();
    var winHeight    = $(window).height();
    var playerHeight = 430;
    var bottom = scrollTop + (winHeight + playerHeight) / 2;
    if (bottom > docHeight) {
        // this prevents infinite scroll
        this.video_container.css('top', docHeight - playerHeight - 10);
    } else {
        this.video_container.css('top', scrollTop + (winHeight - playerHeight) / 2);
    }
    this.overlay.height(docHeight);
  } else {
    this.video_container.css('top', ($(window).height() - 430) / 2);
    this.overlay.height($(window).height());
  }
}

Mozilla.VideoPlayer.prototype.close = function()
{
  // hideSubtitles() depends on mozilla-video-tools-addsubtitles.js
  if (window.hideSubtitles) {
    hideSubtitles();
  }

  this.overlay.fadeOut();
  this.video_container.fadeOut();

  // clear the video content so IE will stop playing the audio
  this.clearVideoPlayer();

  // if language form was hidden, show it again
  $('#lang_form').show();

  $(window).unbind('resize', this.resizeHandler);

  this.opened = false;
}

Mozilla.VideoPlayer.prototype.toggle = function()
{
  if (this.opened)
    this.close();
  else
    this.open();
}

Mozilla.VideoPlayer.getFlashVersion = function()
{
  var version = new Mozilla.FlashVersion([0, 0, 0]);
  if (navigator.plugins && navigator.mimeTypes.length) {
    var x = navigator.plugins['Shockwave Flash'];
    if (x && x.description) {
      // strip text to get version number only
      version = x.description.replace(/([a-zA-Z]|\s)+/, '');

      // convert revisions and beta to dots
      version = version.replace(/(\s+r|\s+b[0-9]+)/, '.');

      // get version
      version = new Mozilla.FlashVersion(version.split('.'));
    }
  } else {
    if (navigator.userAgent && navigator.userAgent.indexOf('Windows CE') >= 0) {
      var axo = true;
      var flash_version = 3;
      while (axo) {
        // look for greatest installed version starting at 4
        try {
          major_version++;
          axo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash.' + major_version);
          version = new Mozilla.FlashVersion([major_version, 0, 0]);
        } catch (e) {
          axo = null;
        }
      }
    } else {
      try {
        var axo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash.7');
      } catch (e) {
        try {
          var axo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash.6');
          version = new Mozilla.FlashVersion([6, 0, 21]);
          axo.AllowScriptAccess = 'always';
        } catch (e) {
          if (version.major == 6) {
            return version;
          }
        }
        try {
          axo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash');
        } catch (e) {}
      }
      if (axo != null) {
        version = new Mozilla.FlashVersion(axo.GetVariable('$version').split(' ')[1].split(','));
      }
    }
  }
  return version;
};

Mozilla.FlashVersion = function(version)
{
  this.major = version[0] != null ? parseInt(version[0]) : 0;
  this.minor = version[1] != null ? parseInt(version[1]) : 0;
  this.rev   = version[2] != null ? parseInt(version[2]) : 0;
};

Mozilla.FlashVersion.prototype.isValid = function(version)
{
  if (version instanceof Array) {
    version = new Mozilla.FlashVersion(version);
  }

  if (this.major < version.major) {
    return false;
  }
  if (this.major > version.major) {
    return true;
  }
  if (this.minor < version.minor) {
    return false;
  }
  if (this.minor > version.minor) {
    return true;
  }
  if (this.rev < version.rev) {
    return false;
  }
  return true;
};

// init flash version
Mozilla.VideoPlayer.flash_verison = Mozilla.VideoPlayer.getFlashVersion();

// }}}
