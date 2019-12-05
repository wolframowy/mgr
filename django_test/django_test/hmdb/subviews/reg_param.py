from django.shortcuts import render, Http404
from django.http import HttpResponseNotFound
import json

from ..models import Spectra, Metabolite
from ..reg_param.models.registration_parameter import RegistrationParameter, MetaboliteRegistration


def reg_param(request):
    if request.method == 'POST':
        return reg_parm_post(request)
    if request.method == 'GET':
        return reg_parm_get(request)
    raise Http404


def reg_parm_post(request):
    met_reg = []
    payload = json.loads(request.body)
    selected_ids = []
    for sel in payload['selected']:
        selected_ids.append(sel['id'])
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
                if peak.intensity >= payload['minimal_intensity']:
                    new_met_reg.add_reg_param(RegistrationParameter(e=spectrum.ms_ms.collision_energy_voltage,
                                                                    ionization_mode=spectrum.ms_ms.ionization_mode,
                                                                    intensity=peak.intensity,
                                                                    q2_3=peak.mass_charge))
        met_reg.append(new_met_reg)
    context = {'met_reg': met_reg}
    return render(request, 'hmdb/reg_parm.html', context)


def reg_parm_get(request):
    return render(request, 'hmdb/reg_parm.html')
