$(document).ready(function(){
    var $statusObj = $('#id_status');
    var $gradYearObj = $('#id_grad_year');
    var $majorObj = $('#id_major');
    var $majorFreeTextObj = $('#id_major_free_text');

    function toggleField(field, cmp, value) {
        if (cmp.value === value) {
            field.parent().slideDown();
            field.attr('required', 'required');
        }
        else {
            field.parent().slideUp();
            field.val('');
            field.removeAttr('required');
        }
    }
    $statusObj.on('change', function() {
        toggleField($gradYearObj, this, 'student');
    });
    $majorObj.on('change', function() {
        toggleField($majorFreeTextObj, this, 'other');
    });
});
