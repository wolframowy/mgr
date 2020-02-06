$(document).ready(function() {
    $("#metabolites_search").on('keyup', function (e) {
        if (e.keyCode === 13) {
            met_search_btn_click();
        };
    });
    $('#adv_search_name, #adv_search_super_class, #adv_search_main_class, ' +
        '#adv_search_sub_class, #adv_search_biospecimen, #adv_search_mass_min, #adv_search_mass_max')
        .on('keyup', function (e) {
        if (e.keyCode === 13) {
            met_adv_search_btn_click();
        };
    });

    $('#minimal_intensity').on('keyup change', function (e) {
        if ($(this).val() > 100) {
            $(this).val(100);
        }
        else if ($(this).val() < 0) {
            $(this).val(0);
        };
        filterByIntensity($(this).val());
    });

    loadBiospecimenLocationList();
})

function filterByIntensity(intensity) {
    $(".reg_parm_spectrum_table tr").not(':first-child').not('.table_separator').filter(function() {
        $(this).toggle(parseFloat($(this).find(':last-child').text()) >= intensity)
    });
    colorTable('reg_parm_spectrum_table');
}

function colorTable(table_class) {
    $("table." + table_class + " tr").not('.table_separator').filter(":visible:odd").addClass("odd").removeClass("even");
    $("table." + table_class + " tr").not('.table_separator').filter(":visible:even").addClass("even").removeClass("odd");
}

function createRegistrationParamView(response) {
    $('.reg_parm_table_container > div').slice(1).remove();
    $.each(response, function(i, metabolite) {
        var reg_params = $('<div>', {class: 'reg_param_list_container table_scroll'});
        $.each(metabolite.spectra_params, function(mode, spectra) {
            var table = $('<table>', {class: 'reg_parm_spectrum_table'})
                .append(
                    $('<tr>').append(
                        $('<th>').text('Voltage'),
                        $('<th>').text('Q1'),
                        $('<th>').text('Q2/3'),
                        $('<th>').text('Intensity')
                    )
            );
            if (spectra.length === 0) {
                table.append(
                    $('<div>').text('No spectra found for this compound.')
                );
            } else {
                $.each(spectra, function(i, spectrum) {
                    $.each(spectrum.reg_param, function(i, param) {
                        var tr = $('<tr>').append(
                            $('<td>').text(spectrum.e),
                            $('<td>').text(parseFloat(metabolite.m_1) +
                                (spectrum.ionization_mode.toLowerCase() === 'positive' ? 1 : -1)),
                            $('<td>').text(param.q2_3),
                            $('<td>').text(parseFloat(param.rel_intensity).toPrecision(4))
                        );
                        table.append(tr);
                    })
                    table.append($('<tr>', {class: 'table_separator'}).append($('<td>', {colspan: 4})));
                });
            };
            var reg_parm_spectrum = $('<div>', {class: 'reg_parm_spectrum'})
                .append(
                    $('<div>', {class: 'separator'}),
                    $('<div>', {class: 'ionization_mode'}).text('Ionization mode: ' + mode),
                    table
                );

            reg_params.append(reg_parm_spectrum);
        });
        var single_met = $('<div>', {class: 'reg_parm_single_met'})
            .append(
                $('<a>', {class: 'metabolite_name'}).text(metabolite.name)
                    .attr('href', 'http://www.hmdb.ca/metabolites/' + metabolite.accession)
                    .attr('target', '_blank')
                    .append(
                        $('<span>', {class: 'hmdb_link'}).text('HMDB')
                        .append($('<img>', {class: 'hmdb_link_img'})
                            .attr('src', 'https://upload.wikimedia.org/wikipedia/commons/6/6a/External_link_font_awesome.svg')
                            .attr('alt', 'external link icon')
                            .attr('width', '10')
                            .attr('height', '10'))
                    ),
                $('<div>', {class: 'metabolite_avg_mol_wgt'})
                    .text('Monoisotopic molecular weight: ' + metabolite.m_1),
                reg_params
            );

        $('.reg_parm_table_container').append(single_met);
    })
    $('.reg_parm_table_container').show()
    filterByIntensity($('#minimal_intensity').val());
    colorTable('reg_parm_spectrum_table');
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
                    selected_ids: JSON.stringify(selected_ids)
                },
            contentType: "application/json",
            dataType: "json",
            timeout: 60000
        }).done(createRegistrationParamView).fail(function(jqXHR, textStatus) {
            alert('ERROR!')
        });
    });
}

function fill_met_names_table(response) {
    $.each(response, function(i, item) {
        var $tr = $('<tr>').append(
            $('<td>', {css:{'display':'none'}}).text(item.met_id),
            $('<td>').text(item.name)
        ).appendTo('#metabolites_table')
    });
    colorTable('reg_parm_met_table')
    $('.reg_parm_loading').hide()
    addOnTableClick();
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
    }).done(fill_met_names_table)
    .fail(function(error) {
        alert('ERROR!')
    })
}

function checkIfAllEmpty() {
    for (var i = 0; i < arguments.length; ++i) {
        if(arguments[i] !== '') return false;
    };
    return true;
}

function met_adv_search_btn_click() {
    var name = $("#adv_search_name").val().toLowerCase();
    var super_class = $("#adv_search_super_class").val().toLowerCase();
    var main_class = $("#adv_search_main_class").val().toLowerCase();
    var sub_class = $("#adv_search_sub_class").val().toLowerCase();
    var biolocation = $("#adv_search_biospecimen").val().toLowerCase();
    var mass_min = $("#adv_search_mass_min").val().toLowerCase();
    var mass_max = $("#adv_search_mass_max").val().toLowerCase();
    if (checkIfAllEmpty(name, super_class, sub_class, main_class, biolocation, mass_min, mass_max)) {
        $("#metabolites_table tr").show().children().show();
        return;
    }
    $('.reg_parm_loading').show();
    $('#metabolites_table').empty();
    $.ajax({
        url: async_get_url,
        type: "GET",
        data: {type:"advanced",
            name: name,
            super_class: super_class,
            main_class: main_class,
            sub_class: sub_class,
            biolocation: biolocation,
            mass_min: mass_min,
            mass_max: mass_max
        },
        contentType: "application/json",
        dataType: "json",
        timeout: 60000
    }).done(fill_met_names_table)
    .fail(function(error) {
        alert('ERROR!')
    })
}

function search_switch() {
    $('.simple_search').toggle();
    $('.advanced_search').toggle();
}

function loadBiospecimenLocationList() {
    $.ajax({
        url: async_get_url,
        type: "GET",
        data: {type:"biospecimen"},
        contentType: "application/json",
        dataType: "json",
        timeout: 60000
    }).done(function(response) {
        $.each(response, function(i, biolocation) {
            $('#biospecimen_locations').append($('<option>').attr('value', biolocation.name))
        })
    }).fail(function(error) {
        alert('ERROR!')
    })
}
