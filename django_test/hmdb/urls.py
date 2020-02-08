from django.urls import path

from . import views

app_name = 'hmdb'
urlpatterns = [
    path('', views.index, name='index'),
    path('reg_param', views.reg_param, name='reg_param'),
    path('reg_param/get', views.reg_param_get_async, name='reg_param_get_async'),
    path('spectrum_search', views.spectrum_search, name='spectrum_search'),
    path('spectrum_search/get', views.spectrum_search_get_async, name='spectrum_search_get_async'),
    path('spectrum_search/metabolite_get', views.metabolite_get_async, name='metabolite_get_async')
]
