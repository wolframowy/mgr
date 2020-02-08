from django.http import HttpResponseNotFound, Http404
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q

import json

from pymongo import MongoClient

from ..models import Spectra, Metabolite, MetaboliteNames, Biolocation
from ..reg_param.models.registration_parameter import RegistrationParameter, MetaboliteRegistration, SpectrumParameter
from ..subviews.metbolite_finder import MetaboliteFinder


def spectrum_search_get_async(request):
    metabolite_finder = MetaboliteFinder('localhost', 27017)
    payload = request.GET
    peaks = [float(i) for i in payload['peaks'].replace(',', '').split()]
    peak_accuracy = float(payload['peak_accuracy'])

    minimum_ranking = payload['minimum_ranking']
    if not minimum_ranking:
        minimum_ranking = 20
    else:
        minimum_ranking = float(minimum_ranking)

    found_metabolites, found_metabolites_names, _ = metabolite_finder.find_metabolites(peak_list=peaks,
                                                                                       tolerance=peak_accuracy,
                                                                                       minimum_ranking=minimum_ranking)
    print('test')
    result = []
    rankings = list(found_metabolites.keys())
    rankings.sort(reverse=True)
    duplicate_names = []
    for key in rankings:
        for metabolite in found_metabolites[key]:
            if metabolite['name'] not in duplicate_names:
                result.append({'name': metabolite['name'],
                               'ranking': key,
                               'id': metabolite['id']})
                duplicate_names.append(metabolite['name'])

    return JsonResponse(result, safe=False)


def metabolite_get_async(request):
    metabolite_finder = MetaboliteFinder('localhost', 27017)
    payload = request.GET
    raw_id = payload['id']
    peaks = [float(i) for i in payload['peaks'].replace(',', '').split()]
    peak_accuracy = float(payload['peak_accuracy'])
    parsed_id = json.loads(raw_id)

    if not parsed_id[0]:
        raise Http404

    found_metabolite = metabolite_finder.find_metabolite_by_id(parsed_id[0])

    ranked_spectra = []

    for spectrum in found_metabolite['spectra']['spectrum']:
        id = spectrum['spectrum_id']
        ranking, collision_energy_voltage, ionization_mode = metabolite_finder.get_spectrum_data(id, peaks=peaks, tolerance=peak_accuracy)
        ranked_spectra.append({
            'id': id,
            'ranking': ranking,
            'collision_energy_voltage': collision_energy_voltage,
            'ionization_mode': ionization_mode
        })
        ranked_spectra.sort(key=lambda x: x['ranking'], reverse=True)

    metabolite_to_return = {'name': found_metabolite['name'],
                            'accession': found_metabolite['accession'][0],
                            'monoisotopic_molecular_weight': found_metabolite['monisotopic_molecular_weight'],
                            'ranked_spectra': ranked_spectra}

    return JsonResponse(metabolite_to_return, safe=False)


def reg_parm_get_names(value):
    mets = MetaboliteNames.objects.filter(name__icontains=value)
    serialized = serializers.serialize('python', mets)
    data = [val['fields'] for val in serialized]
    return JsonResponse(data, safe=False)


def reg_parm_get_metabolites(payload):
    met_reg = []
    selected_ids = json.loads(payload['selected_ids'])
    mets = list(Metabolite.objects.filter(id__in=selected_ids))
    if mets.__len__() == 0:
        return HttpResponseNotFound("Metabolites not found in database")
    for met in mets:
        new_met_reg = MetaboliteRegistration(name=met.name, m_1=met.monisotopic_molecular_weight,
                                             accession=met.accession[0])
        spec_ids = []
        if met.spectra is not None:
            for spectrum in met.spectra.spectrum:
                spec_ids.append(spectrum.spectrum_id)
        spectra = list(Spectra.objects.filter(id__in=spec_ids).only('ms_ms'))
        for spectrum in spectra:
            new_spec_param = SpectrumParameter(e=spectrum.ms_ms.collision_energy_voltage,
                                               ionization_mode=spectrum.ms_ms.ionization_mode)
            peaks = sorted(spectrum.ms_ms.ms_ms_peaks.ms_ms_peak, key=lambda x: x.intensity, reverse=True)
            for peak in peaks:
                new_spec_param.add_reg_param(RegistrationParameter(intensity=peak.intensity,
                                                                   q2_3=peak.mass_charge).to_dict())
            new_met_reg.add_spectrum_param(new_spec_param.to_dict())
        met_reg.append(new_met_reg.__dict__)
    return JsonResponse(met_reg, safe=False)


def reg_parm_get_biospecimen():
    biospecimens = Biolocation.objects.all()
    serialized = serializers.serialize('python', biospecimens)
    data = [val['fields'] for val in serialized]
    return JsonResponse(data, safe=False)


def reg_parm_get_names_advanced(payload):
    q = Q()
    if payload['mass_min'] != '':
        q &= Q(monisotopic_molecular_weight__gte=payload['mass_min'])
    if payload['mass_max'] != '':
        q &= Q(monisotopic_molecular_weight__lte=payload['mass_max'])
    if payload['biolocation'] != '':
        q &= Q(biospecimen_locations__icontains=payload['biolocation'])
    if payload['name'] != '':
        q &= Q(name__icontains=payload['name'])
    if payload['super_class'] != '':
        q &= Q(super_class__icontains=payload['super_class'])
    if payload['main_class'] != '':
        q &= Q(main_class__icontains=payload['main_class'])
    if payload['sub_class'] != '':
        q &= Q(sub_class__icontains=payload['sub_class'])
    mets = MetaboliteNames.objects.filter(q)
    serialized = serializers.serialize('python', mets)
    data = [val['fields'] for val in serialized]
    return JsonResponse(data, safe=False)
