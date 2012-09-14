$(function(){
    $("#sms-send .subscribe").hide();

    $("#number").one('focus', function(){
        $("#sms-send .subscribe").slideDown('fast');
    });
});
