$(document).ready(function () {
    $("#navbar2").addClass('active').siblings().removeClass('active');

    $('#files').on('click touchstart', function () {
        $(this).val('');
    });

    $("#files").change(function (e) {
        $("#form-upload").submit();
    });
});