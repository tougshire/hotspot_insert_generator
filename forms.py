from django import forms
from django.urls import reverse_lazy

from touglates.widgets import TouglatesRelatedSelect
from .models import InsertTemplate

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
    ssid = forms.CharField(label="SSID", required=False )
    password = forms.CharField(label="password", required=False )
    insert_template = forms.ModelChoiceField(label="device", queryset=InsertTemplate.objects.all(), widget=TouglatesRelatedSelect(
                related_data={
                    "model_name": "InsertTemplate",
                    "app_name": "hotspot_insert_generator",
                    "add_url": reverse_lazy("hotspot_insert_generator:insert_template-popup"),
                },
            ),
    )

class InsertTemplateForm(forms.ModelForm):
    class Meta:
        model=InsertTemplate
        fields = [
            'template_title',
            'template_filename'
        ]
