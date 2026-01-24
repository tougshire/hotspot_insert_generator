from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'hotspot_insert_generator'
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('hotspot_insert_generator:insert-create'))),
    path('insert/create/', views.InsertCreate.as_view(), name='insert-create'),
    path('model/popup/', views.InsertTemplateCreate.as_view(), name='insert_template-popup'),
    path('model/detail/', views.InsertTemplateDetail.as_view(), name='insert_template-detail'),

]
