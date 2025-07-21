from django import forms
from django.urls import reverse_lazy

from touglates.widgets import TouglatesRelatedSelect
from .models import DeviceModel

class InsertForm(forms.Form):
    CODE_CHOICES=[
        ("A","A"),
        ("B","B"),
        ("C","C"),
        ("D","D"),
    ]
    
    start_code = forms.ChoiceField(label="start_code", choices=CODE_CHOICES, initial="A")
    stop_code = forms.ChoiceField(label="stop_code", choices=CODE_CHOICES, initial="B")
    barcode_number = forms.CharField(label="barcode")
    ssid = forms.CharField(label="SSID", blank=True)
    password = forms.CharField(label="password", blank=True)
    device_model = forms.ModelChoiceField(label="device", queryset=DeviceModel.objects.all(), widget=TouglatesRelatedSelect(
                related_data={
                    "model_name": "DeviceModel",
                    "app_name": "hotspot_insert_generator",
                    "add_url": reverse_lazy("hotspot_insert_generator:devicemodel-popup"),
                },
            ),
    )

class DeviceModelForm(forms.ModelForm):
    class Meta:
        model=DeviceModel
        fields = [
            'modelname',
            'instructions',
            'instructions_photo',
        ]
