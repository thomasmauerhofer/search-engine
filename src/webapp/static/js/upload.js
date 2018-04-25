$(document).ready(function () {
    $("#navbar2").addClass('active').siblings().removeClass('active');

    $('#file').on('click touchstart', function () {
        $(this).val('');
    });

    $("#file").change(function (e) {
        $("#form-upload").submit();
    });
});