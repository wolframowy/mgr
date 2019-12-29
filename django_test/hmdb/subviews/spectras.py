from django.shortcuts import render

from ..models import Spectra


def spectras(request):
    spectras = Spectra.objects.all().only("ms_ms")[:5]
    context = {'spectras': spectras}
    return render(request, 'hmdb/spectras.html', context)
