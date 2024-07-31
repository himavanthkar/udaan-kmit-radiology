from django import forms
from .models import Mammography

class MammographyForm(forms.ModelForm):
    class Meta:
        model = Mammography
        fields = ('title', 'image')