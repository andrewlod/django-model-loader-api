from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class StringModelForm(forms.Form):
    model = forms.FileField()
    label_map = forms.FileField()
    storage_type = forms.CharField(max_length=16)


class ImageModelForm(forms.Form):
    model = forms.FileField()
    storage_type = forms.CharField(max_length=16)