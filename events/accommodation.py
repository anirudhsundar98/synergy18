from models.models.events import EventDetails as e, EventRegister as evr
from models.models.user import UserDetails as u
from django.views.decorators.http import require_GET
# from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from utils import general


def accommodation(request):
    return render(request, "accommodation.html")
