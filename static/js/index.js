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
                $("#dy_dx").text(`dy/dx = ${data.dy_dx}`);
                let info = data.lines.length == 0 ? "No tangent line" : "";
                for (let i = 0; i < data.lines.length; ++i) {
                    let line = data.lines[i];
                    info += `Point: (${line.x_value}, ${line.y_value})<br>${line.equation} = 0<br><br>`;
                }
                $("#info").html(info);
            }
        });
    });
});
