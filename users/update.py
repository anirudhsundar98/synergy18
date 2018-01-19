from django.utils.safestring import mark_safe
from utils import decorators, general
from django import forms
from django.shortcuts import render
from models.models import UserDetails as u
from forms.updateForm import updateForm
from django.http import JsonResponse as jr, HttpResponseRedirect, HttpResponse
from utils import general
from datetime import datetime

@decorators.check_logged_in(redirect_path="/login/")
def update_info(request):

    final_response = {}
    try:
        auth_token = request.session["cur_token"]
        user = u.objects.get(auth_token__exact = auth_token)
        cur_user_pwd = user.password
    except Exception as e:
        print("We're not able to recognize you as our user. Please try again !")
        return HttpResponse("We're not able to recognize you as our user. Please try again !")

    if request.method  == "GET":
        form = updateForm()
        try:
            form.data["fullname"] = user.fullname
        except:
            return HttpResponseRedirect("/?err_user=1")

        return render(request, "forms.html", {"form":form, "purpose":"update", "logged_in": True, "user":user.fullname})
    elif request.method != "POST":
        return jr({"status":400, "errors":"What are you really trying ? You can host your own server side code to play around"})

    entered_fn = request.POST.get('fullname')
    entered_pwd = request.POST.get('passwd')
    entered_newPwd = request.POST.get('newPasswd')

    if len(entered_newPwd) ==0 and len(entered_pwd) ==0:
        if len(entered_fn) ==0:
            final_response["status"] = 400
            final_response["errors"] = mark_safe("<ul class=\"errorslist\"><li>Please enter a non-empty full name !</li></ul>")
            return jr(final_response)

        try:
            user.fullname = entered_fn
            new_token = general.gen_auth_token(user.email)
            user.auth_token = new_token
            user.tokenCreatedAt = datetime.now()
            user.save()
            request.session["cur_token"] = new_token
            final_response["status"] = 200
            final_response["inline"] = True
            return jr(final_response)
        except:
            final_response["status"] = 400
            final_response["errors"] = mark_safe("<ul class=\"errorslist\"><li>There was an issue in processing your request. Please try again !</li></ul>")
            return jr(final_response)

    if general.hash_pwd(entered_pwd) != cur_user_pwd:
        print("cur : ", cur_user_pwd)
        print("entered : ", entered_pwd)
        final_response["status"] = 400
        final_response["errors"] = mark_safe("<ul class=\"errorslist\"><li>The current password you entered is wrong ! Please try again !</li></ul>")
        return jr(final_response)

    if len(entered_newPwd) < 5:
        final_response["status"] = 400
        final_response["errors"] = mark_safe(
            "<ul class=\"errorslist\"><li>Your new password has to be at least 6 characters long !</li></ul>")
        return jr(final_response)

    if entered_newPwd == cur_user_pwd:
        final_response["status"] = 400
        final_response["errors"] = mark_safe(
            "<ul class=\"errorslist\"><li>Your new password has to be different from your current password !</li></ul>")
        return jr(final_response)

    try:
        user.password = general.hash_pwd(entered_newPwd)
        new_token = general.gen_auth_token(user.email)
        user.auth_token = new_token
        user.tokenCreatedAt = datetime.now()
        if len(entered_fn) != 0:
            user.fullname = entered_fn
        user.save()
        request.session["cur_token"] = new_token
    except Exception as e:
        print("error")
        raise e

    final_response["status"] = 200
    final_response["inline"] = True
    return jr(final_response)
