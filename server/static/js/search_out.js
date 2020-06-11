$(document).ready(function() {
    var search = function() {
        var name=$('#name').val();

        var params = {
            "name":name
        };
        $.ajax({
            url:"http://localhost:5000/search",
            type:"POST",
            data:JSON.stringify(params),
            headers:{"Content-type":"application/json"},

            success:function(data) {
                localStorage['search_data'] = JSON.stringify(data);
                window.location.href = '/data';
            },
            error:function(data) {
                alert("error");
            }
        });
    };

    $('#submit').click(search);
    $('#name').keyup(function(event) {
        if(event.keyCode==13) {
            search();
        }

        var name=$('#name').val();

        if(name != null) {
            var params = {
                "name":name
            };
            $.ajax({
                url:"http://localhost:5000/completion",
                type:"POST",
                data:JSON.stringify(params),
                headers:{"Content-type":"application/json"},

                success:function(data){
                    var names = []
                    for(var i=0; i<data['length']; i++) {
                        names.push(data['names'][i]);
                    }
                    
                    $('#name').autocomplete({
                    source:names,
                    autoFocus:true
                    });
                }
            });
        }
    });

});
