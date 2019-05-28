from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _

from django.core.files.images import get_image_dimensions


class CustomUserCreationForm(UserCreationForm):
    """ Clase formulario para datos de usuarios basicos"""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget = forms.PasswordInput(attrs={'class': 'form-control', })

    class Meta(UserCreationForm):
        model = User
        msg_required = "Obligatory field"
        fields = (
            'username',

            'password1',
            'password2',
        )
        fields_required = (
            'username',
            'password1',
            'password2',
        )

        labels = {
            'username': _('UserName'),



        }
        help_texts = {

            'password1': _('not needed'),
            'password2': "SS",
        }
        error_messages = {
            'username': {
                'max_length': _("Length not valid"),
                'required': _(msg_required)
            },


        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),

            'password1': forms.PasswordInput(attrs={'class': 'form-control', }),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', }),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name')


class UserForm(forms.ModelForm):
    """ Clase formulario para datos de usuarios basicos"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control ', }))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            msg = "Passwords do not match"
            self.add_error('password', msg)

    class Meta:
        model = User
        msg_required = "Obligatory field"
        fields = (
        'username',
        'first_name',
        'email',
        'password',
        'confirm_password'
        )
        fields_required= (
            'username',
            'email',
            'password',
            'confirm_password'
            )

        labels = {
            'username': _('UserName'),
            'first_name': _('Name'),
            'email': _('Email:'),
            'password':  _('Password :'),
            'confirm_password':    _('Confirm password:'),
        }
        help_texts = {
            'first_name': _('Not obligatory, just to identify easily the user'),
        }
        error_messages = {
            'username': {
                'max_length': _("Length not valid"),
                'required': _(msg_required)
            },
            'password': {
                'required': _(msg_required)
            },
            'confirm_password': {
                'required': _(msg_required)
            },
            'email': {
                'required': _(msg_required)
            },
        }
        widgets = {
                    'username': forms.TextInput(attrs={'class': 'form-control',}),
                    'first_name': forms.TextInput(attrs={'class': 'form-control',}),
                    'email': forms.EmailInput(attrs={'class': 'form-control',}),
                }

