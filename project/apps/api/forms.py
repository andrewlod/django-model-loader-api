from random import choices
from django import forms
from .models import TFModel
from .constants import STORAGE_TYPES, MODEL_OUTPUT_TYPES


class ImageModelForm(forms.ModelForm):
    model = forms.FileField()
    model_output_type = forms.CharField(max_length=16, widget=forms.Select(choices=([x,x] for x in MODEL_OUTPUT_TYPES.keys())))
    model_label_map = forms.FileField(required=False)
    model_storage_type = forms.CharField(max_length=16, widget=forms.Select(choices=([x,x] for x in STORAGE_TYPES.keys())))
    model_name = forms.CharField(max_length=32)

    class Meta:
        model = TFModel
        fields = [
            'model',
            'model_output_type',
            'model_label_map',
            'model_storage_type',
            'model_name'
        ]
    
    class Media:
        js = ('js/dynamic_model_fields.js',)