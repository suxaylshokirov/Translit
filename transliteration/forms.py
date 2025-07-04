from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.txt,.docx,.csv,.xlsx,.html,.json'}))