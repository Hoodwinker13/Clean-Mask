$(document).ready(function() {
        $.ajax({
            type:"POST",

            success:function(data) {
                $("table tbody").remove();
                var html = '<tbody>';
                    value = value['_source'];
                    for(int i =0; i < value.length; i++){
                    html += '<tr>';
                    html += '<td style="width: 70px">' + value['loading_particles'] + '</td>';
                    html += '<td style="width: 80px">' + value['mask_type'] + '</td>';
                    html += '<td style="width: 100px">' + value['name'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_0.3'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_0.5'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_1'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_3'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_5'] + '</td>';
                    html += '<td style="width: 50px">' + value['efficiency_10'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_0.3'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_0.5'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_1'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_3'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_5'] + '</td>';
                    html += '<td style="width: 50px">' + value['error_10'] + '</td>';
                    html += '<td style="width: 50px">' + value['pa'] + '</td>';
                    html += '<td style="width: 50px">' + value['vair'] + '</td>';
                    html += '<td style="width: 50px">' + value['t'] + '</td>';
                    html += '<td style="width: 50px">' + value['rh'] + '</td>';
                    html += '<td style="width: 80px">' + value['test_date'] + '</td>';
                    html += '</tr>';
                html += '</tbody>';
            }
                $("table").append(html);
            },
            error:function(data) {
                alert("error");
            }
        });});

