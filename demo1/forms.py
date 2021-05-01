from django import forms

from .models import Lugar

class FormLugar(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50)
    provincia= forms.CharField(label='Provincia', max_length=50)