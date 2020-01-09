from django import forms
from django.core import validators

from django.utils.translation import gettext as _


class ImportForm(forms.Form):
    """ Clase formulario para permitir elegir una coleccion existente"""
    file = forms.FileField(label='UPLOAD THE CSV:',
                           widget=forms.FileInput(attrs={'class': 'file-input btn btn-warning',
                                                         'required': 'required',
                                                         }))
