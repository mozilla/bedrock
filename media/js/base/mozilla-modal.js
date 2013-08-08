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

  /*
    origin: element that triggered the modal
    content: content to display in the modal
    options: object of optional params:
      onCreate: function to fire after modal has been created
      onDestroy: function to fire after modal has been closed
      allowScroll: boolean - allow/restrict page scrolling when modal is open
  */
  var _createModal = function(origin, content, opts) {
    // Make sure modal is closed (if one exists)
    if (open) {
      _closeModal();
    }

    // Create new modal
    var html = (
        '<div id="modal" role="dialog" aria-labelledby="' + origin.getAttribute('id') + '" tabindex="-1">' +
        '  <div class="inner">' +
        '    <button type="button" id="modal-close" class="close">' +
        '      <span class="close-text">' + w.trans('close') + '</span>' +
        '    </button>' +
        '  </div>' +
        '</div>'
    );

    // Restrict scrolling
    if (!opts.allowScroll) {
      $body.addClass('noscroll');
    }

    // Add modal to page
    $body.append(html);

    $modal = $('#modal');

    // Add content to modal
    $("#modal .inner").append(content);

    $modal.fadeIn('fast', function() {
      $modal.focus();
    });

    // close modal on clicking close button
    $d.on('click.' + evtNamespace, '#modal .close', _closeModal);

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
    $(origin).addClass('modalOrigin');

    open = true;

    // execute (optional) open callback
    if (typeof(opts.onCreate) === 'function') {
      opts.onCreate();
    }

    // store options for later use
    options = opts;
  };

  var _closeModal = function() {
    $modal.fadeOut('fast', function() {
      $(this).remove();
    });

    // allow page to scroll again
    $body.removeClass('noscroll');

    // restore focus to element that opened the modal
    $('.modalOrigin').focus().removeClass('modalOrigin');

    open = false;
    $modal = null;

    // unbind document listeners
    $d.off('.' + evtNamespace);

    // execute (optional) callback
    if (typeof(options.onDestroy) === 'function') {
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