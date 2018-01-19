from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from utils import decorators
from django.views.decorators.http import require_POST
from models.models.user import UserDetails as u
from models.models.events import EventDetails as e
from models.models.events import EventRegister as evr

@require_POST
def register_event(request):
    final_response = {}

    try:
        auth_token = request.session['cur_token']

        cur_user = u.objects.get(auth_token__exact=auth_token)

    except:
        return JsonResponse({"status":400, "errors":"You need to login first !"})

    event_unique = request.POST.get("event")

    try:
        cur_event = e.objects.get(unique__exact=event_unique)
    except:
        error = "This event doesn't exist !"
        final_response["status"] = 400
        final_response["errors"] = error
        return JsonResponse(final_response)

    try:
        register = evr.objects.get(user=cur_user, event=cur_event)
        error = "Looks like you have already registered for {} !".format(cur_event.name)
        final_response["status"] = 400
        final_response["errors"] = error
        return JsonResponse(final_response)
    except:
        pass

    try:
        register = evr()
        register.user = cur_user
        register.event = cur_event
        register.save()
    except:
        error = "There was an error in registering. Please try again !"
        final_response["status"] = 500
        final_response["errors"] = error
        return JsonResponse(final_response)

    final_response["status"] = 200
    return JsonResponse(final_response)