from django.shortcuts import render

from ..models import Spectra


def index(request):
    all_spectra = Spectra.objects.all()
    context = {'all_spectra': all_spectra}
    return render(request, 'hmdb/index.html', context)
