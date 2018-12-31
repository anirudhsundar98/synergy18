from django import forms
from .baseForm import baseForm


class LoginForm(baseForm):
    email = forms.CharField(label="Email", max_length=200)
    passwd = forms.CharField(label="Password", widget=forms.PasswordInput)
