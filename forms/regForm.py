from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .baseForm import baseForm
from utils import general
from models.models import user

class regForm(baseForm, ModelForm):
    class Meta:
        model = user.UserDetails

        fields = ('fullname', 'email', 'password', 'college', 'country',  'phone', 'YoS', 'accommodation' )

        labels = {
            'fullname':'Full Name',
            'passwd':'Password',
            'phone': 'Phone Number',
            'YoS':'Year of Study'
        }

        widgets = {
            'password' : forms.PasswordInput,
        }


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if user.UserDetails.objects.filter(phone=phone).exists():
            raise ValidationError("This Phone Number \"{}\" has already registered".format(phone))
        if not general.phno_validate(phone):
            raise ValidationError("Invalid phone number")
        print("received phno : ", phone)
        if phone=="":
            print("returning none")
            return None
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if user.UserDetails.objects.filter(email=email).exists():
            raise ValidationError("This Email \"{}\" already exists".format(email))
        return email

    def clean_password(self):
        passwd = self.cleaned_data['password']
        if len(passwd)<5:
            raise ValidationError("Please enter a password of at least 5 characters")
        return passwd

    # def clean_college(self):
    #
    # if len(college)==0:
    #     form.errors['College'] = "Please enter a non-empty college name"
    def clean_accommodation(self):
        accommodation = self.cleaned_data["accommodation"]
        if type(accommodation) != type(True):
            raise ValidationError("Invalid value")
        return accommodation
