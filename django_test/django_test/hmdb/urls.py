from django.urls import path

from . import views

app_name = 'hmdb'
urlpatterns = [
    path('', views.index, name='index'),
    path('spectras', views.spectras, name='spectras'),
    path('metabolites', views.metabolites, name='metabolites'),
    path('reg_param', views.reg_param, name='reg_param'),
]
