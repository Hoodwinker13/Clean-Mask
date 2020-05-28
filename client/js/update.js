
$(document).ready(function() {
    $("#update").click(function() {
        var loading_particles = document.getElementById('loading_particles').value;
        var mask_type = document.getElementById('mask_type').value;
        var name = document.getElementById('name').value;
        var efficiency_03 = document.getElementById('efficiency_0.3').value;
        var efficiency_05 = document.getElementById('efficiency_0.5').value;
        var efficiency_1 = document.getElementById('efficiency_1').value;
        var efficiency_3 = document.getElementById('efficiency_3').value;
        var efficiency_5 = document.getElementById('efficiency_5').value;
        var efficiency_10 = document.getElementById('efficiency_10').value;
        var error_03 = document.getElementById('error_0.3').value;
        var error_05 = document.getElementById('error_0.5').value;
        var error_1 = document.getElementById('error_1').value;
        var error_3 = document.getElementById('error_3').value;
        var error_5 = document.getElementById('error_5').value;
        var error_10 = document.getElementById('error_10').value;
        var pa = document.getElementById('pa').value;
        var vair = document.getElementById('vair').value;
        var t = document.getElementById('t').value;
        var rh = document.getElementById('rh').value;
        var test_date = document.getElementById('test_date').value;
        
        var uri = "http://localhost:5000/update";
        var params = {
            "loading_particles" : loading_particles,
            "mask_type" : mask_type,
            "name" : name,
            "efficiency_0.3" : efficiency_03,
            "efficiency_0.5" : efficiency_05,
            "efficiency_1" : efficiency_1,
            "efficiency_3" : efficiency_3,
            "efficiency_5" : efficiency_5,
            "efficiency_10" : efficiency_10,
            "error_0.3" : error_03,
            "error_0.5" : error_05,
            "error_1" : error_1,
            "error_3" : error_3,
            "error_5" : error_5,
            "error_10" : error_10,
            "pa" : pa,
            "vair" : vair,
            "t" : t,
            "rh" : rh,
            "test_date" : test_date
        };
        
        $.ajax({
            url:uri,
            type:"POST",
            data:JSON.stringify(params),
            headers:{"Content-type":"application/json"},

            success: function(data) {
                alert("Success!");
                document.getElementById("my_mask").reset();
            },
            error: function(data) {
                alert(data.responseText);
            }
        });
    });
});