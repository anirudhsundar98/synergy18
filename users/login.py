# Imports
import imaplib, random, hashlib
from models.models.user import UserDetails as u
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from utils import decorators, general
from forms import loginForm, regForm
from datetime import datetime


# Functions

@require_POST
def validate_user(request):

    final_response = {}

    entered_email = request.POST.get('email', None)
    entered_pwd = request.POST.get('passwd', None)


    try:
        current_user = u.objects.get(email__exact=entered_email, password__exact=general.hash_pwd(entered_pwd))
        token = general.gen_auth_token(entered_email)

        request.session['cur_token'] = token
        current_user.auth_token = token
        current_user.tokenCreatedAt = datetime.now()
        current_user.save()
        final_response["status"] = 200

        return JsonResponse(final_response)

    except Exception as e:
        current_user = None

    try:
        imap = imaplib.IMAP4('webmail.nitt.edu', 143)
        nitt_user = entered_email.split("@nitt.edu")[0]
        if not ((len(entered_email.split("@nitt.edu")) == 2) and entered_email.split("@nitt.edu")[1] == ""):
            raise Exception("Invalid Nitt mail")
        imap.login(nitt_user, entered_pwd)

        if len(nitt_user) != 9:
            raise Exception("Invalid NITT student")
        if not((nitt_user[5] >= "4" ) and (nitt_user[5] <= "7")):
            raise Exception("Invalid NITT student")

        YoS = 8-int(nitt_user[5])
        if general.email_lookup(entered_email) is None:
            uniq = str(random.randint(1212, 123123123)) + entered_email + str(random.randint(1212, 123123123)) + str(
                datetime.now())
            uniq = uniq.encode("utf8")
            auth_token = general.gen_auth_token(entered_email)
            user = u(
                email=entered_email,
                fullname=nitt_user,
                password=general.hash_pwd(entered_pwd),
                unique=hashlib.sha256(uniq).hexdigest(),
                country='india',
                phone=None,
                college="NIT Trichy",
                YoS=YoS,
                accommodation=False,
                auth_token=auth_token,
                tokenCreatedAt=datetime.now()
            )
            user.save()
            try:
                request.session["cur_token"] = auth_token
            except:
                final_response["status"] = 400
                final_response["errors"] = "There was an issue in setting up your account. Please try again."
                return JsonResponse(final_response)
            final_response["status"] = 200
            return JsonResponse(final_response)
        final_response["status"] = 200
        return JsonResponse(final_response)
    except Exception as e:
        print(e)

    if not current_user:
        final_response['status'] = 400
        final_response['errors'] = "Invalid Credentials"
        return JsonResponse(final_response)

@decorators.check_logged_in(redirect_path="/?already_in=1", do_while_loggedin=False)
def login(request):

    if request.method == 'GET':
        form = loginForm.LoginForm()
        return render(request, "forms.html", {'url':'/login/','form': form , 'purpose':'login'})
    elif request.method == 'POST':
        return validate_user(request)

def logout(request):
    response = HttpResponseRedirect("/")
    if 'cur_token' in request.session:
        request.session.pop("cur_token")
        return response
    return response
