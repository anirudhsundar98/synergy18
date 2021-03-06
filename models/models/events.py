from django.db import models
from .user import UserDetails as u

class EventDetails(models.Model):
    id = models.AutoField(primary_key=True)
    unique = models.CharField(max_length=20, unique=True, default=None) # internal id (unique hash)
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=300) # byline
    desc = models.TextField()
    types = (('event', 'event'), ('workshop', 'workshop'), ('gl', 'gl'))  # Enum
    type = models.CharField(max_length=20, choices=types, default="event")
    created_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'events'


class EventRegister(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(u)
    event = models.ForeignKey(EventDetails)
    req_payment = models.BooleanField(name="require_payment", default=False)
    paid = models.BooleanField(default=False)
    paid_online = models.BooleanField(default=False)

    class Meta:
        db_table = "registration"