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

function displayMetabolite(response) {
    $('.reg_parm_table_container > div').slice(1).remove();
    $('.reg_parm_table_container > table').slice(0).remove();
    $('.reg_parm_table_container > br').slice(0).remove();
    document.getElementById("metabolite_name").innerHTML= "<a href='http://www.hmdb.ca/metabolites/" +
     response.accession + "' target = '_blank' class = 'metabolite_name'>" +
      response.name + "<span class = 'hmdb_link' >HMDB <img class = 'hmdb_link_img' src"+
       "= 'https://upload.wikimedia.org/wikipedia/commons/6/6a/External_link_font_awesome.svg'"+
       "alt = 'external link icon' width = '10' height='10'></img></span>" + "</a>"

    $(".reg_parm_table_container").append($('<div>', {class: 'metabolite_avg_mol_wgt'})
                    .text('Monoisotopic molecular weight: ' + response.monoisotopic_molecular_weight))
    $(".reg_parm_table_container").append($('</br>'))
    $(".reg_parm_table_container").append($('<div>', {class: 'spectrum_table_title'})
                    .text('Spectra: '))

    var table = $('<table>', {class: 'spectrum_table'}).append(
    $('<tr>').append(
                        $('<th>').text('Id'),
                        $('<th>').text('Ionisation'),
                        $('<th>').text('Voltage'),
                        $('<th>').text('Matched peaks')
                    )
    )
    $.each(response.ranked_spectra, function(i, spectrum) {
                        var tr = $('<tr>').append(
                            $('<td>').append(
                            $('<a>', {class: 'metabolite_name'}).text(spectrum.id)
                    .attr('href', 'http://www.hmdb.ca/spectra/ms_ms/' + spectrum.id)
                    .attr('target', '_blank')
                    .append(
                        $('<span>', {class: 'hmdb_link'}).text('HMDB')
                        .append($('<img>', {class: 'hmdb_link_img'})
                            .attr('src', 'https://upload.wikimedia.org/wikipedia/commons/6/6a/External_link_font_awesome.svg')
                            .attr('alt', 'external link icon')
                            .attr('width', '10')
                            .attr('height', '10'))
                    )
                            ),
                            $('<td>').text(spectrum.ionization_mode),
                            $('<td>').text(spectrum.collision_energy_voltage),
                            $('<td>').text(spectrum.ranking)
                        );
                        table.append(tr);
                    })

    $(".reg_parm_table_container").append(table)

    $('.reg_parm_table_container').show()
    colorTable('spectrum_table');
}

function createRegistrationParamView(response) {
    $('.reg_parm_table_container > div').slice(1).remove();
    $.each(response, function(i, metabolite) {
        var reg_params = $('<div>', {class: 'reg_param_list_container table_scroll'});
        $.each(metabolite.spectra_params, function(mode, spectra) {
            if (spectra.length === 0) {
                reg_params.append(
                    $('<div>').text('No spectra found for this compound.')
                );
            };
            var table = $('<table>', {class: 'reg_parm_spectrum_table'})
                .append(
                    $('<tr>').append(
                        $('<th>').text('Voltage'),
                        $('<th>').text('Q1'),
                        $('<th>').text('Q2/3'),
                        $('<th>').text('Intensity')
                    )
            );
                $.each(spectra, function(i, spectrum) {
                    $.each(spectrum.reg_param, function(i, param) {
                        var tr = $('<tr>').append(
                            $('<td>').text(spectrum.e),
                            $('<td>').text(parseFloat(metabolite.m_1) +
                                (spectrum.ionization_mode.toLowerCase() === 'positive' ? 1 : -1)),
                            $('<td>').text(param.q2_3),
                            $('<td>').text(param.intensity)
                        );
                        table.append(tr);
                    })
                    table.append($('<tr>', {class: 'table_separator'}).append($('<td>', {colspan: 4})));
                });
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
        var peaks = $("#peaks").val();
        var peak_accuracy = $("#peak_accuracy").val();
        selected_ids.push(parseInt($(this).find('td:first').html()));
        $.ajax({
            url: metabolite_get_url,
            type: "GET",
            data:
                {
                    'id': JSON.stringify(selected_ids),
                    'peaks': peaks,
                    'peak_accuracy': peak_accuracy
                },
            contentType: "application/json",
            dataType: "json",
            timeout: 60000
        }).done(displayMetabolite).fail(function(jqXHR, textStatus) {
            alert('ERROR!')
        });
    });
}

function fill_met_names_table(response) {
    var $tr = $('<tr style="font-weight: bold;">').append(
            $('<th>').text('Name'),
            $('<th>').text('Matched peaks')
        ).appendTo('#metabolites_table')
    $.each(response, function(i, item) {
        var $tr = $('<tr>').append(
            $('<td>', {css:{'display':'none'}}).text(item.id),
            $('<td>').text(item.name),
            $('<td>').text(item.ranking)
        ).appendTo('#metabolites_table')
    });
    colorTable('reg_parm_met_table')
    $('.reg_parm_loading').hide()
    addOnTableClick();
}

function met_search_btn_click() {
    var peaks = $("#peaks").val();
    var peak_accuracy = $("#peak_accuracy").val();
    var minimum_ranking = $("#minimum_ranking").val();
    if (peaks === "") {
        $("#metabolites_table tr").show().children().show();
        return;
    }
    $('.reg_parm_loading').show()
    $('#metabolites_table').empty()
    $.ajax({
        url: async_get_url,
        type: "GET",
        data: {type:"spectrum_search",
                peaks: peaks,
                peak_accuracy: peak_accuracy,
                minimum_ranking: minimum_ranking
        },
        contentType: "application/json",
        dataType: "json",
        timeout: 60000
    }).done(fill_met_names_table)
    .fail(function(error) {
        alert('ERROR!')
    })
}

function load_example_btn_click() {
    document.getElementById("peaks").value= "148, 131.2, 130, 102.1, 84.1";
    document.getElementById("peak_accuracy").value= "0.1";
    document.getElementById("minimum_ranking").value= "3";
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
