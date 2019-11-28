from django.shortcuts import render

from ..models import Metabolite


def metabolites(request):
    mets = Metabolite.objects.all()[:5]
    context = {'metabolites': mets}
    return render(request, 'hmdb/metabolites.html', context)
