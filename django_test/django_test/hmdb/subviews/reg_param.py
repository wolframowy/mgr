from django.shortcuts import render, Http404
from django.http import HttpResponseNotFound
import json


from ..models import Spectra, Metabolite, MetaboliteNames
from ..reg_param.models.registration_parameter import RegistrationParameter, MetaboliteRegistration


def reg_param(request):
    return reg_parm_get(request)


def reg_parm_get(request):
    return render(request, 'hmdb/reg_parm.html')
