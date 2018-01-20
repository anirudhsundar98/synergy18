from models.models.events import EventDetails as e, EventRegister as evr
from models.models.user import UserDetails as u
from django.views.decorators.http import require_GET
# from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

def home(request):
    try:
        auth_token = request.session["cur_token"]
        user = u.objects.get(auth_token__exact=auth_token)

    except:
        user = None

    logged_in = True
    uname = ''
    if not user:
        logged_in = False
    else:
        uname = user.fullname


    return render(request, "index.html", {"logged_in":logged_in, "user":uname})