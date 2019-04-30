from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    #allow_save = forms.BooleanField()