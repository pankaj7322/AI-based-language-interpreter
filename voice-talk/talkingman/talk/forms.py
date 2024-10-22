from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    language = forms.CharField(max_length=10)

class AudioUploadForm(forms.Form):
    audio = forms.FileField()
    language = forms.CharField(max_length=10)

from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=True)
    language = forms.CharField(max_length=10, required=True)
