$(document).ready(function() {
    $("#metabolites_search").on('keyup', function (e) {
        if (e.keyCode === 13) {
            met_search_btn_click();
        };
    });

    $('#minimal_intensity').on('focusout', function () {
        if ($(this).val() > 100) {
            $(this).val(100);
        }
        else if ($(this).val() < 0) {
            $(this).val(0);
        }
    });
})

function createRegistrationParamView(response) {
    $('.reg_parm_table_container div').not(':first').remove();
    $.each(response, function(i, metabolite) {
        var reg_params = $('<div>', {class: 'reg_param_list_container table_scroll'});
        $.each(metabolite.spectra_params, function(i, spectrum) {
            var table = $('<table>', {class: 'reg_parm_spectrum_table'})
                .append(
                    $('<tr>').append(
                        $('<th>').text('Q1'),
                        $('<th>').text('Q2/3')
                    )
                );
            $.each(spectrum.reg_param, function(i, param) {
                var tr = $('<tr>').append(
                    $('<td>').text(parseFloat(metabolite.m_1) +
                        (spectrum.ionization_mode.toLowerCase() === 'positive' ? 1 : -1)),
                    $('<td>').text(param.q2_3)
                );
                table.append(tr);
            })
            var reg_parm_spectrum = $('<div>', {class: 'reg_parm_spectrum'})
                .append(
                    $('<div>', {class: 'energy_voltage'}).text('Voltage: ' + spectrum.e + 'V'),
                    $('<div>', {class: 'ionization_mode'}).text('Ionization mode: ' + spectrum.ionization_mode),
                    table
                );

            reg_params.append(reg_parm_spectrum);
        });
        var single_met = $('<div>', {class: 'reg_parm_single_met'})
            .append($('<div>', {class: 'metabolite_name'}).text(metabolite.name),
                $('<div>', {class: 'metabolite_avg_mol_wgt'})
                    .text('Average molecular weight: ' + metabolite.m_1),
                reg_params
            );

        $('.reg_parm_table_container').append(single_met);
    })
    $('.reg_parm_table_container').show()
}

function addOnTableClick() {
    $("#metabolites_table tr").click(function() {
        $(this).addClass('selected').siblings().removeClass('selected');
        var selected_ids = [];
        selected_ids.push(parseInt($(this).find('td:first').html()));
        $.ajax({
            url: async_get_url,
            type: "GET",
            data:
                {
                    type:"metabolites",
                    selected_ids: JSON.stringify(selected_ids),
                    minimal_intensity: $('#minimal_intensity').val()
                },
            contentType: "application/json",
            dataType: "json",
            timeout: 60000
        }).done(createRegistrationParamView).fail(function(jqXHR, textStatus) {
            alert('ERROR!')
        });
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
        data: {type:"names",
                value: value
        },
        contentType: "application/json",
        dataType: "json",
        timeout: 60000
    }).done(function(response){
        $.each(response, function(i, item) {
            var $tr = $('<tr>').append(
                $('<td>', {css:{'display':'none'}}).text(item.met_id),
                $('<td>').text(item.name)
            ).appendTo('#metabolites_table')
        });
        $('.reg_parm_loading').hide()
        addOnTableClick();
    }).fail(function(error) {
        alert('ERROR!')
    })
}
