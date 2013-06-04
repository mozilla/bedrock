// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

Mozilla.Modal = (function(w, $) {
  'use strict';

  var _open = false;
  var _modal = null;
  var $_body = $('body');
  var _options = {};

  var _init = function() {
    var $d = $(w.document);

    // close modal on clicking close button or background.
    $d.on('click', '#modal .close', _close_modal);

    // close on escape
    $d.on('keyup', function(e) {
      if (e.keyCode === 27 && _open) { // esc
        _close_modal();
      }
    });

    // prevent focusing out of modal while open
    $d.on('focus', function(e) {
      if (_open && !_modal.contains(e.target)) {
        e.stopPropagation();
        _modal.focus();
      }
    });
  };

  /*
    origin: element that triggered the modal
    content: content to display in the modal
    options: object of optional params:
      onCreate: function to fire after modal has been created
      onDestroy: function to fire after modal has been closed
      allowScroll: boolean - allow/restrict page scrolling when modal is open
  */
  var _create_modal = function(origin, content, options) {
    // Clear existing modal, if necessary,
    $('#modal').remove();
    $('.modalOrigin').removeClass('modalOrigin');

    // Create new modal
    var html = (
        '<div id="modal" role="dialog" aria-labelledby="' + origin.getAttribute('id') + '" tabindex="-1">' +
        '  <div class="inner">' +
        '    <button type="button" id="modal-close" class="close">' +
        '      <span class="close-text">' + window.trans('close') + '</span>' +
        '    </button>' +
        '  </div>' +
        '</div>'
    );

    if (!options.allowScroll) {
      $_body.addClass('noscroll');
    }

    // Add it to the page.
    $_body.append(html);

    _modal = $('#modal');

    $("#modal .inner").append(content);

    _modal.fadeIn('fast', function() {
      $(this).focus();
    });

    // remember which element opened the modal for later focus
    $(origin).addClass('modalOrigin');

    _open = true;

    // execute (optional) open callback
    if (typeof(options.onCreate) === 'function') {
      options.onCreate();
    }

    // store options for later use
    _options = options;
  };

  var _close_modal = function() {
    $('#modal').fadeOut('fast', function() {
      $(this).remove();
    });

    $_body.removeClass('noscroll');

    // restore focus to element that opened the modal
    $('.modalOrigin').focus().remove('modalOrigin');

    _open = false;
    _modal = null;

    // execute (optional) callback
    if (typeof(_options.onDestroy) === 'function') {
      _options.onDestroy();
    }

    // free up options
    _options = {};
  };

  return {
    init: function() {
      _init();
    },
    create_modal: function(origin, content, options) {
      _create_modal(origin, content, options);
    },
    close_modal: function() {
      _close_modal();
    }
  };
})(window, window.jQuery);

$(document).ready(function() {
  Mozilla.Modal.init();
});