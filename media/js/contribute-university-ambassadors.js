$(document).ready(function(){
    var $current_status_obj = $('#id_current_status');
    var $expected_graduation_year_obj = $('#id_expected_graduation_year');
    var $area_obj = $('#id_area');
    var $area_free_text_obj = $('#id_area_free_text');

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
    $current_status_obj.on('change', function() {
        toggle_field($expected_graduation_year_obj, this, 'student');
    });
    $area_obj.on('change', function() {
        toggle_field($area_free_text_obj, this, 'other');
    });
});
