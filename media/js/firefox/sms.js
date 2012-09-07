$("#sms-send .subscribe").hide();

$("#number").focus(function(){
  $("#sms-send .subscribe").slideDown('fast');
});