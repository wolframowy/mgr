from django.http import HttpResponseNotFound, Http404
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q

import json

from ..models import Spectra, Metabolite, MetaboliteNames, Biolocation
from ..reg_param.models.registration_parameter import RegistrationParameter, MetaboliteRegistration, SpectrumParameter


def reg_param_get_async(request):
    payload = request.GET
    if payload['type'] == 'names':
        return reg_parm_get_names(payload['value'])
    elif payload['type'] == 'metabolites':
        return reg_parm_get_metabolites(payload)
    elif payload['type'] == 'advanced':
        return reg_parm_get_names_advanced(payload)
    elif payload['type'] == 'biospecimen':
        return reg_parm_get_biospecimen()
    raise Http404


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
            max_intensity = peaks[0].intensity
            for peak in peaks:
                new_spec_param.add_reg_param(RegistrationParameter(intensity=peak.intensity,
                                                                   rel_intensity=peak.intensity/max_intensity*100,
                                                                   q2_3=peak.mass_charge).to_dict())
            new_met_reg.add_spectrum_param(new_spec_param.to_dict())
        new_met_reg.sort_spectra_params()
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
