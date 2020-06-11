$(document).ready(function() {
    if(localStorage['Name'] == null){
        alert("Please log in before entering data.");
        window.location.href = '/index';
    }
    $("#update").click(function() {
        var loading_particles = $("#loading_particles").val();
        var mask_type = $("#mask_type").val();
        var name = $("#name").val();
        var efficiency_03 = $("#efficiency_03").val();
        var efficiency_05 = $("#efficiency_05").val();
        var efficiency_1 = $('#efficiency_1').val();
        var efficiency_3 = $('#efficiency_3').val();
        var efficiency_5 = $('#efficiency_5').val();
        var efficiency_10 = $('#efficiency_10').val();
        var error_03 = $('#error_03').val();
        var error_05 = $('#error_05').val();
        var error_1 = $('#error_1').val();
        var error_3 = $('#error_3').val();
        var error_5 = $('#error_5').val();
        var error_10 = $('#error_10').val();
        var pa = $('#pa').val();
        var vair = $('#vair').val();
        var t = $('#t').val();
        var rh = $('#rh').val();
        var test_date = $('#test_date').val();
        var test_city = $('#test_city').val();
        var comment = $('#comment').val();
        var username = localStorage['Name'];
        var form = jQuery("#image")[0];
        
        var uri = "http://localhost:5000/update";
        var params = {
            "loading_particles" : loading_particles,
            "mask_type" : mask_type,
            "name" : name,
            "efficiency_03" : efficiency_03,
            "efficiency_05" : efficiency_05,
            "efficiency_1" : efficiency_1,
            "efficiency_3" : efficiency_3,
            "efficiency_5" : efficiency_5,
            "efficiency_10" : efficiency_10,
            "error_03" : error_03,
            "error_05" : error_05,
            "error_1" : error_1,
            "error_3" : error_3,
            "error_5" : error_5,
            "error_10" : error_10,
            "pa" : pa,
            "vair" : vair,
            "t" : t,
            "rh" : rh,
            "test_date" : test_date,
            "test_city" : test_city,
            "comment" : comment,
            "username" : username,
        };
        var formdata = new FormData(form);
        formdata.append("file", jQuery("#file")[0].files[0]);
        formdata.append("mask_data", JSON.stringify(params));

        $.ajax({
            url:"http://localhost:5000/update",
            type:"POST",
            data:formdata,
            contentType:false,
            processData:false,
            success: function(data){
                alert("Uploaded Successfully");
            },
            error:function(data){
                alert(data.responseText);
            }
        });
    });
});