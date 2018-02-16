from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.exceptions import ValidationError


# Create your models here.

class UserDetails(models.Model):
    max_val = MaxValueValidator(5)
    max_val.message = _(" This has to be a value less than \"5\". If this choice doesn't fit you, please contact support [at] synergy.nitt.edu")

    min_val = MinValueValidator(1)
    min_val.message = _(
        " This has to be a value greater than \"1\". If this choice doesn't fit you, please contact support [at] synergy.nitt.edu")
    Countries = (('india', 'India'), ('other', 'Other'))
    id = models.AutoField(primary_key=True)
    admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    uniq_val = models.CharField(max_length=100, unique=True, name="unique")
    fullname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100, name="password")
    country = models.CharField(max_length=100, choices=Countries, default='India')
    phone_no = models.CharField(max_length=20, name="phone", unique=True, default=None)
    college = models.CharField(max_length=100)
    yearOfStudy = models.IntegerField(name="YoS", validators=[max_val, min_val])
    accommodation = models.BooleanField()
    attended = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=500, default="")
    tokenCreatedAt = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    events_paid = models.BooleanField(default=False)
    alt_phone = models.CharField(max_length=20, default=None, null=True)

    class Meta:
        db_table = 'users'

class Hospi(models.Model):

    user = models.ForeignKey(UserDetails)
    hostel = models.CharField(max_length=200)
    days = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    check_in = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hospi'