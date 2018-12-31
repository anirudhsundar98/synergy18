from django.http import JsonResponse
from django.shortcuts import render
from utils import decorators, general
from models.models import UserDetails as u

@decorators.check_logged_in("/")
def render_qr(request):
    if request.method == "POST":
        return JsonResponse({"message":"Hacker ? :P"})
    cur_user = None
    try:
        cur_token = request.session["cur_token"]
        cur_user = u.objects.get(auth_token__exact = cur_token)
    except:
        return JsonResponse({"status":500, "error":"sorry, we were unable to get your QR :/"})

    logged_in = False
    fullname = ""
    uniq = ""
    email = ""
    if cur_user:
        logged_in = True
        fullname = cur_user.fullname
        uniq = cur_user.unique
        email = cur_user.email

    return render(request, "QR.html", {"qr":uniq, "logged_in": logged_in, "user": fullname, "syn_id":uniq[len(uniq)-10:], "email":email, "purpose":"QR Code"})