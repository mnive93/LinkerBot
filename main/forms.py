from django import forms
from django.contrib.auth.models import User
from main.models import Links
import re
class PostForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput())
    
