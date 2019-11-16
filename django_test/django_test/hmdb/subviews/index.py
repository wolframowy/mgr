from django.shortcuts import render

from ..models import Spectra


def index(request):
    spectras = Spectra.objects.all().only("ms_ms")[:5]
    context = {'spectras': spectras}
    return render(request, 'hmdb/index.html', context)
