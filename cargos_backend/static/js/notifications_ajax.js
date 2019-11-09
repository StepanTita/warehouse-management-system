function executeQuery() {
    $.ajax({
        type: "GET",
        url: "{% url 'notify_create' %}",
        success: function (data) {
            // do something with the return value here if you like
        }
    });
    setTimeout(executeQuery, 5 * 10000); // you could choose not to continue on failure...
}

$(document).ready(function () {
    // run the first time; all subsequent calls will take care of themselves
    setTimeout(executeQuery, 5 * 10000);
});