// create namespace
if (typeof Mozilla == 'undefined') {
  var Mozilla = {};
}

Mozilla.Modal = (function(w, $) {
  'use strict';

  var open = false;
  var $modal = null;
  var $body = $('body');
  var options = {};
  var $d = $(w.document);
  var evtNamespace = 'moz-modal';

  var $_contentParent;
  var $_content;

  var closeText = (typeof window.trans == "undefined") ? 'Close' : window.trans('global-close');

  /*
    origin: element that triggered the modal
    content: content to display in the modal
    options: object of optional params:
      title: title to display at the top of the modal
      onCreate: function to fire after modal has been created
      onDestroy: function to fire after modal has been closed
      allowScroll: boolean - allow/restrict page scrolling when modal is open
  */
  var _createModal = function(origin, content, opts) {
    options = opts;

    // Make sure modal is closed (if one exists)
    if (open) {
      _closeModal();
    }

    // Create new modal
    var title = (options && options.title) ? options.title : '';

    var $modal = $(
        '<div id="modal" role="dialog" aria-labelledby="' + origin.getAttribute('id') + '" tabindex="-1">' +
        '  <div class="window">' +
        '    <div class="inner">' +
        '      <header>' + title + '</header>' +
        '      <div id="modal-close">' +
        '        <a href="#close-modal" class="modal-close-text"> ' + closeText + '</a>' +
        '        <button type="button" class="button">×</button>' +
        '      </div>' +
        '    </div>' +
        '  </div>' +
        '</div>');

    // Add modal to page
    $body.append($modal);

    if (options && !options.allowScroll) {
      $body.addClass('noscroll');
    } else {
      $body.removeClass('noscroll');
    }

    $_content = content;
    $_contentParent = $_content.parent();
    $('#modal .inner').append($_content);
    $_content.addClass('overlay-contents');

    // close modal on clicking close button or background.
    $('#modal-close').click(_closeModal).attr('title', closeText);

    // close modal on clicking the background (but not bubbled event).
    $('#modal .window').click(function (e) {
      if (e.target === this) {
        _closeModal();
      }
    });

    $modal.hide();
    $modal.fadeIn('fast', function() {
      $modal.focus();
    });

    // close with escape key
    $d.on('keyup.' + evtNamespace, function(e) {
      if (e.keyCode === 27 && open) {
        _closeModal();
      }
    });

    // prevent focusing out of modal while open
    $d.on('focus.' + evtNamespace, 'body', function(e) {
      // .contains must be called on the underlying HTML element, not the jQuery object
      if (open && !$modal[0].contains(e.target)) {
        e.stopPropagation();
        $modal.focus();
      }
    });

    // remember which element opened the modal for later focus
    $(origin).addClass('modal-origin');

    open = true;

    // execute (optional) open callback
    if (options && typeof(options.onCreate) === 'function') {
      options.onCreate();
    }
  };

  var _closeModal = function(e) {
    if (e) {
      e.preventDefault();
    }

    $('#modal').fadeOut('fast', function() {
      $_contentParent.append($_content);
      $(this).remove();
    });

    // allow page to scroll again
    $body.removeClass('noscroll');

    // restore focus to element that opened the modal
    $('.modal-origin').focus().removeClass('modal-origin');

    open = false;
    $modal = null;

    // unbind document listeners
    $d.off('.' + evtNamespace);

    // execute (optional) callback
    if (options && typeof(options.onDestroy) === 'function') {
      options.onDestroy();
    }

    // free up options
    options = {};
  };

  return {
    createModal: function(origin, content, opts) {
      _createModal(origin, content, opts);
    },
    closeModal: function() {
      _closeModal();
    }
  };
})(window, window.jQuery);
