



$(document).ready(function () {
    $('.input').on('focus', function() {
        $('.input').val("");
    });
});




$(document).ready(function () {
    
    $("#delete").attr('disabled', 'disabled');
});



$(document).ready(function () {
    var user = $("#my-data").data("user");
    $("#text-field").keyup(function () {
        if ($(this).val() != user) {
            $("#delete").attr('disabled', 'disabled');
        } else if ($(this).val() === user) {
            $("#delete").removeAttr('disabled', 'disabled');
        }
        $("text-field").val("");
    });
});
