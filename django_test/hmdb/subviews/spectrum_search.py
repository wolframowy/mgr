from django.shortcuts import render


def spectrum_search(request):
    return spectrum_search_get(request)


def spectrum_search_get(request):
    return render(request, 'hmdb/spectrum_search.html')
