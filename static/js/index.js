$(document).ready(function() {
    $("#form").submit(function(event) {
        event.preventDefault();  // We will handle the form submission ourselves.
        let fcn = $("#fcn").val();
        let x = $("#x").val();
        let y = $("#y").val();
        let output = $("#output").val();
        let loading_message = LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];
        $("#dy_dx").addClass("loading").html(`<em>${loading_message}</em>`);
        $("#info").html("");
        $.ajax({
            url: "/calculate",
            type: "POST",
            data: JSON.stringify({fcn: fcn, x: x, y: y, output: output}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                $("#dy_dx").removeClass("loading");
                $("#dy_dx").html(`<strong>dy/dx</strong> = ${data.dy_dx}`);
                let info = data.lines.length == 0
                    ? "<strong>No tangent line</strong>"
                    : `<strong>${data.lines.length} tangent line${data.lines.length > 1 ? "s" : ""}:</strong><br>`;
                for (let i = 0; i < data.lines.length; ++i) {
                    let line = data.lines[i];
                    info += `Point: (${line.x_value}, ${line.y_value})<br>${line.equation} = 0<br><br>`;
                }
                $("#info").html(info);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $("#dy_dx").removeClass("loading");
                if (jqXHR.status == 500) {
                    // We have dy/dx, but an error occurred when calculating the tangent line.
                    $("#dy_dx").html(`<strong>dy/dx</strong> = ${jqXHR.responseJSON.dy_dx}`);
                } else {
                    // We don't have anything.
                    $("#dy_dx").html("An error occurred.");
                }
                if (jqXHR.responseJSON) {
                    let error = jqXHR.responseJSON.error;
                    let error_msg = (typeof error === "string" ? error : JSON.stringify(error)).replaceAll("\n", "<br>");
                    $("#info").html(`Status code: ${jqXHR.status}<br>${error_msg}`);
                } else {
                    $("#info").html(`Status code: ${jqXHR.status}<br>Error thrown: ${errorThrown}`);
                }
            }
        });
    });
});
