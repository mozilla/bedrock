// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

Mozilla.Modal = (function(w, $) {
  'use strict';

  var _open = false;
  var _modal = null;
  var _close_callback = null;

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

  var _create_modal = function(origin, content, create_callback, close_callback) {
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

    // Add it to the page.
    $('body').addClass("noscroll").append(html);

    _modal = $('#modal');

    $("#modal .inner").append(content);

    _modal.fadeIn('fast', function() {
      $(this).focus();
    });

    // remember which element opened the modal for later focus
    $(origin).addClass('modalOrigin');

    _open = true;

    // store (optional) close callback
    if (typeof(close_callback) === 'function') {
      _close_callback = close_callback;
    }

    // execute (optional) callback
    if (typeof(create_callback) === 'function') {
      create_callback();
    }
  };

  var _close_modal = function() {
    $('#modal').fadeOut('fast', function() {
      $(this).remove();
    });

    $('body').removeClass('noscroll');

    // restore focus to element that opened the modal
    $('.modalOrigin').focus().remove('modalOrigin');

    _open = false;
    _modal = null;

    // execute (optional) callback
    if (_close_callback && typeof(_close_callback) === 'function') {
      _close_callback();
      _close_callback = null;
    }
  };

  return {
    init: function() {
      _init();
    },
    create_modal: function(origin, content, create_callback, close_callback) {
      _create_modal(origin, content, create_callback, close_callback);
    },
    close_modal: function() {
      _close_modal();
    }
  };
})(window, window.jQuery);

$(document).ready(function() {
  Mozilla.Modal.init();
});