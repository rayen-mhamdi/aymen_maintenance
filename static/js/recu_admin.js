$(document).ready(function () {
    $('#id_famille').change(function () {
        var url = window.location.href.split('/');
        $.ajax({
            url: '/ticket/categories/?famille_id=' + $(this).val(),
            success: function (data) {
               $('#id_categorie').html(data);
            }
        });
    });
});