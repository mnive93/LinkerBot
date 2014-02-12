from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32,widget=forms.PasswordInput())
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=200)
    def clean_firname(self):
        firstname = self.cleaned_data['firstname']
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
            raise forms.ValidationError("Username already exists")
        except ObjectDoesNotExist:
            return username


