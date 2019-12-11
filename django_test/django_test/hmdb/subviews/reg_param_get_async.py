from django.http import HttpResponseNotFound, Http404
from django.http import JsonResponse
from django.core import serializers

from ..models import Spectra, Metabolite, MetaboliteNames
from ..reg_param.models.registration_parameter import RegistrationParameter, MetaboliteRegistration


def reg_param_get_async(request):
    payload = request.GET
    if payload['type'] == 'names':
        return reg_parm_get_names(payload['value'])
    if payload['type'] == 'metabolites':
        return reg_parm_get_metabolites(payload)
    raise Http404


def reg_parm_get_names(value):
    mets = MetaboliteNames.objects.filter(name__icontains=value)
    serialized = serializers.serialize('python', mets)
    data = [val['fields'] for val in serialized]
    return JsonResponse(data, safe=False)


def reg_parm_get_metabolites(payload):
    met_reg = []
    selected_ids = payload['selected_ids']
    mets = list(Metabolite.objects.filter(id__in=selected_ids))
    if mets.__len__() == 0:
        return HttpResponseNotFound("Metabolites not found in database")
    for met in mets:
        new_met_reg = MetaboliteRegistration(name=met.name, m_1=met.average_molecular_weight)
        spec_ids = []
        if met.spectra is not None:
            for spectrum in met.spectra.spectrum:
                spec_ids.append(spectrum.spectrum_id)
        spectra = list(Spectra.objects.filter(id__in=spec_ids).only('ms_ms'))
        for spectrum in spectra:
            for peak in spectrum.ms_ms.ms_ms_peaks.ms_ms_peak:
                if peak.intensity >= float(payload['minimal_intensity']):
                    new_met_reg.add_reg_param(RegistrationParameter(e=spectrum.ms_ms.collision_energy_voltage,
                                                                    ionization_mode=spectrum.ms_ms.ionization_mode,
                                                                    intensity=peak.intensity,
                                                                    q2_3=peak.mass_charge).to_json())
        met_reg.append(new_met_reg.__dict__)
    return JsonResponse(met_reg, safe=False)

