$(document).ready(function() {
    $("#form").submit(function(event) {
        event.preventDefault();  // We will handle the form submission ourselves.
        let fcn = $("#fcn").val();
        let x = $("#x").val();
        let y = $("#y").val();
        let output = $("#output").val();
        $.ajax({
            url: "/calculate",
            type: "POST",
            data: JSON.stringify({fcn: fcn, x: x, y: y, output: output}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
            }
        });
    });
});
