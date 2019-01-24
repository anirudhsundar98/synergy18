from utils import general
from django.shortcuts import render
from models.models import UserDetails as u
from django.http import HttpResponse

def get_stats(r):

    loggedIn = True
    user = None

    try:
        auth_token = r.session["cur_token"]
        user = general.auth_token_lookup(auth_token)
    except:
        loggedIn = False

    if not loggedIn or not user:
        return render(r, "404.html")
    if not user.admin:
        return render(r, "404.html")

    registrants = 0
    try:
        registrants = u.objects.count()
    except Exception as e:
        return HttpResponse("Sorry there was an issue in fetching details. Pls try again.")


    return render(r, "Attendee_Report.html", {"count":registrants})
