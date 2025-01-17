$(document).ready(function() {
    $("#plotBtn").click(function() {
        var equation = $("#equation").val();
        var mode = $("#mode").val();
        var xMin = parseFloat($("#xMin").val());
        var xMax = parseFloat($("#xMax").val());
        var yMin = parseFloat($("#yMin").val());
        var yMax = parseFloat($("#yMax").val());

        var data = {
            equation: equation,
            mode: mode,
            xMin: xMin,
            xMax: xMax,
            yMin: yMin,
            yMax: yMax
        };

        $.ajax({
            url: "/plot",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(response) {
                // Update the image source with the returned plot
                $("#plotImg").attr("src", "data:image/png;base64," + response.plot_image);
            },
            error: function(error) {
                alert("Error generating plot: " + error.responseText);
            }
        });
    });
});
