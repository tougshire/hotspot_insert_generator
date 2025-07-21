from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'hotspot_insert_generator'
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('hotspot_insert_generator:insert-create'))),
    path('insert/create/', views.InsertCreate.as_view(), name='insert-create'),
    path('model/popup/', views.DeviceModelCreate.as_view(), name='devicemodel-popup'),
    path('model/detail/', views.DeviceModelDetail.as_view(), name='devicemodel-detail'),

]
