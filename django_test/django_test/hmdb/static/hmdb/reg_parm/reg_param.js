
function addOnTableClick() {
    $("#metabolites_table tr").click(function(){
       $(this).addClass('selected').siblings().removeClass('selected');
       var value=$(this).find('td:first').html();
       alert(value);
    });
}

function met_search_btn_click() {
    var value = $("#metabolites_search").val().toLowerCase();
    if (value === "") {
        $("#metabolites_table tr").show().children().show();
        return;
    }
    $('.reg_parm_loading').show()
    $('#metabolites_table').empty()
    $.ajax({
        url: async_get_url,
        type: "GET",
        data: {"type":"names",
                "value": value
                },
        contentType: "application/json",
        dataType: "json",
        success: function(response){
            var data = JSON.parse(response);
            $.each(data, function(i, item) {
                var $tr = $('<tr>').append(
                    $('<td>', {css:{'visibility':'hidden'}}).text(item.met_id),
                    $('<td>').text(item.name)
                ).appendTo('#metabolites_table')
            });
            $('.reg_parm_loading').hide()
            addOnTableClick();
        },
        failure: function(error) {
            alert('ERROR!')
        }
    })
}
