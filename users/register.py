# Imports
import re, random, hashlib, requests
from models.models.user import UserDetails as u
from models.models.events import EventDetails as e
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from utils import decorators, general
from forms import regForm
from datetime import datetime
from django.utils.safestring import mark_safe
#Functions

@require_POST
def register_user(request):
    final_response = {}
    form = regForm.regForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        for e in form.errors.keys():
            if e == "YoS":
                form.errors["Year of Study"] = form.errors.pop(e)
            elif e == "fullname":
                form.errors["Full Name"] = form.errors.pop(e)
            elif e == "unique":
                form.errors.pop(e)
                form.errors["Your Account"] = mark_safe("<ul class=\"errorslist\"><li>There was an issue in setting up your account. Please try again 1 !</li></ul>")
            else:
                form.errors[e.title()] = form.errors.pop(e)

        final_response["errors"] = str(form.errors)
        final_response["status"] = 400
        return JsonResponse(final_response)#"There were errors in your details !")
    try:
        email = form.cleaned_data['email']
        fullname = form.cleaned_data['fullname']
        passwd = form.cleaned_data['password']
        country = form.cleaned_data['country']
        college = form.cleaned_data['college']
        ph_no = form.cleaned_data['phone']
        yearOfStudy = form.cleaned_data['YoS']
        accommodation = form.cleaned_data['accommodation']
    except Exception as e:
        # raise e
        final_response["errors"] = " There was an error in your request"
        final_response["status"] = 400
        return JsonResponse(final_response)

    try:
        url = "https://www.google.com/recaptcha/api/siteverify"
        secr = "6LcmLz8UAAAAAFUFuEGC7gQ8aHCTlSUiDQauPgwi"
        resp = requests.post(url, {'secret':secr, "response":request.POST.get("g-recaptcha-response", "")})
        resp = resp.json()
        if not resp["success"]:
            form.errors["Captcha"] = mark_safe("<ul class=\"errorslist\"><li>Invalid captcha response. Please try again !</li></ul>")
    except:
        form.errors["Captcha"] = mark_safe(
            "<ul class=\"errorslist\"><li>Invalid captcha response. Please try again !</li></ul>")



    errors = {}


    if len(form.errors)==0:
        uniq = str(random.randint(1212, 123123123)) + email + str(random.randint(1212, 123123123)) + str(datetime.now())
        uniq = uniq.encode("utf8")
        user = u(email=email,
                 fullname=fullname,
                 password=general.hash_pwd(passwd),
                 unique=hashlib.sha256(uniq).hexdigest(),
                 country=country,
                 phone=ph_no,
                 college=college,
                 YoS=yearOfStudy,
                 accommodation=accommodation,
                 tokenCreatedAt=datetime.now())
        user.save()
        try:
            general.send_welcome_mail(fullname, email, hashlib.sha256(uniq).hexdigest())
        except Exception as e:
            print("Error in sending mail : ", e)
        # return (0, None)
        final_response["status"] = 200
        return JsonResponse(final_response)

    final_response["status"] = 400
    final_response["errors"] = str(form.errors)
    return JsonResponse(final_response)

@decorators.check_logged_in(redirect_path="/", do_while_loggedin=False)
def register(request):

    if request.method == 'GET':

        form = regForm.regForm()
        return render(request, "forms.html", {'url':'/register/', 'form': form, 'purpose':'register'})

    elif request.method == 'POST':

        return register_user(request)
