$(document).ready(function(){
    var $status_obj = $('#id_status');
    var $grad_year_obj = $('#id_grad_year');
    var $major_obj = $('#id_major');
    var $major_free_text_obj = $('#id_major_free_text');

    function toggle_field(field, cmp, value) {
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
    $status_obj.on('change', function() {
        toggle_field($grad_year_obj, this, 'student');
    });
    $major_obj.on('change', function() {
        toggle_field($major_free_text_obj, this, 'other');
    });
});
