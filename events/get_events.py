from models.models.events import EventDetails as e, EventRegister as evr
from models.models.user import UserDetails as u
from django.views.decorators.http import require_GET
# from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

@require_GET
def get(request):

    events = e.objects.filter(type="event")
    workshops = e.objects.filter(type="workshop")
    gl = e.objects.filter(type="gl")

    g_lec = []
    for g in gl:
        g.desc = mark_safe(g.desc)
        g_lec.append(g)

    reg = {}


    try:
        auth_token = request.session["cur_token"]
        user = u.objects.get(auth_token__exact=auth_token)

    except:
        user = None

    for event in events:
        try:
            evr_user = evr.objects.get(user=user, event=event)
            reg[event.unique] = True
        except:
            reg[event.unique] = False

    for w in workshops:
        try:
            evr_user = evr.objects.get(user=user, event=w)
            reg[w.unique] = True
        except:
            reg[w.unique] = False

    events_list = []
    workshops_list = []

    for event in events:
        event.desc = mark_safe(event.desc)
        events_list.append((event, reg[event.unique]))

    for w in workshops:
        w.desc = mark_safe(w.desc)
        workshops_list.append((w, reg[w.unique]))

    logged_in = True
    fullname = ""
    if not user:
        logged_in = False
    else:
        fullname = user.fullname

    return render(request, "events/index.html", {"events": events_list, "workshops":workshops_list, "logged_in":logged_in, "user":fullname, "guest_lectures":g_lec})