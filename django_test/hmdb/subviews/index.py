from django.shortcuts import render

from ..models import Spectra


def index(request):
    return render(request, 'hmdb/index.html')
