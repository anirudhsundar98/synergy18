from django import forms
from .baseForm import baseForm
from django.core.exceptions import ValidationError
from utils import general
from models.models import user

class updateForm(baseForm):
    fullname = forms.CharField(label="Full Name", max_length=200, required=False)
    passwd = forms.CharField(widget=forms.PasswordInput, label="Current Password", required=False)
    newPasswd = forms.CharField(widget=forms.PasswordInput, label="New Password", required=False)