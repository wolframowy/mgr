from django.shortcuts import render


def reg_param(request):
    return reg_parm_get(request)


def reg_parm_get(request):
    return render(request, 'hmdb/reg_param.html')
