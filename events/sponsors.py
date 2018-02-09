from models.models.events import EventDetails as e, EventRegister as evr
from models.models.user import UserDetails as u
from django.views.decorators.http import require_GET
# from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from utils import general

def sponsors(request):

    loggedIn = True
    uname = ""

    try:
        auth_token = request.session["cur_token"]
        user = general.auth_token_lookup(auth_token)
        if not user:
            raise Exception("Invalid auth token")
        uname = user.fullname
    except:
        loggedIn = False

    return render(request, "sponsors.html", {"purpose":"sponsors", "logged_in":loggedIn, "user":uname})