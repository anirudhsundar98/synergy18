from utils import general
from django.shortcuts import render
from django.http import JsonResponse as jr
from models.models import UserDetails as u
from models.models.events import EventRegister as er
from django.db import transaction
from datetime import datetime
from models.models.user import Hospi as h

def mark_users(r):

    user = general.check_loggedInUser_admin(r)
    if not user:
        return render(r, "404.html")
    return render(r, "pr.html", {"logged_in":True, "user":user.fullname})

def mark_attended_paid(r):

    print('events' in r.POST)

    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status':400, "errors":"Sorry, you can't access this !"})

    try:
        entered_email = r.POST["email"]
        entered_phone = r.POST["phone"]
        entered_ticket = r.POST["ticket"]
    except Exception as e:
        print(e)
        return jr({'status':400, 'errors':'Invalid request !'})

    try:
        user = u.objects.get(email__exact=entered_email)
    except:
        return jr({'status': 400, 'errors': 'This user doesn\'t even exist ! They\'ll have to sign up first !'})

    ws_dict = {'automobile':3, 'creo':16, 'automation':17, 'swarm':19, '3d':20, 'photography':21}
    money_dict = {'automobile':450, 'creo':300, 'automation':300, 'swarm':0, '3d':200, 'photography':50}
    money = 0

    if 'swarm' in r.POST:
        if r.POST['swarm'] not in ["2400", "3000", "2750", "None"]:
            return jr({"status":400, "errors":"Incorrect detail for swarm !"})
        elif r.POST['swarm'] != "None":
            money_dict["swarm"] = int(r.POST["swarm"])

    try:
        with transaction.atomic():
            if 'events' in r.POST and not user.events_paid:
                user.events_paid = True
                money+=150
                user.save()

            for w in ws_dict:
                if w == "swarm" and r.POST['swarm'] == "None":
                    continue
                if w in r.POST:
                    reg = None
                    try:
                        reg = er.objects.get(user=user, event_id=ws_dict[w])
                    except:
                        pass

                    e = er()
                    if not reg:
                        e.user = user
                        e.event_id = ws_dict[w]
                        e.paid = True
                        e.save()
                        money+=money_dict[w]
                    elif not reg.paid:
                        reg.paid = True
                        reg.save()
                        money += money_dict[w]
    except Exception as e:
        print(e)
        return jr({'status': 400, 'errors': 'There was problem in saving your response. Please try again !'})

    try:
        user.paid = True
        user.amount += money
        user.alt_phone = entered_phone
        if user.ticket is not None and len(user.ticket)!=0 and len(entered_ticket)!=0:
            user.ticket += ", {}".format(entered_ticket)

        elif len(entered_ticket)!=0:
            user.ticket = entered_ticket
        user.save()
    except Exception as e:
        print(e)
        return jr({"status":400, "errors":"There was an error in saving to the database. Please try again !"})


    return jr({"status":200, "fullname":user.fullname, "email":user.email, "paid":"Success", "amount":user.amount, "ticket":user.ticket})

def mark_hospi(r):
    user = general.check_loggedInUser_admin(r)
    if not user:
        return render(r, "404.html")
    return render(r, "hospi.html", {"logged_in":True, "user":user.fullname})

def mark_hostels(r):

    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status':400, "errors":"Sorry, you can't access this !"})

    hostels = ["garnet a", "garnet b", "garnet c", "jasper", "aquamarine a", "aquamarine b", "ruby", "pearl", "opal"]

    try:
        email = r.POST["email"]
        hostel = r.POST["hostel"]
        days = int(r.POST["days"])
        time = datetime.now()
    except Exception as e:
        print(e)
        return jr({'status':400, 'errors':'Invalid request !'})

    try:
        user = u.objects.get(email__exact=email)
    except:
        return jr({'status':400, 'errors':'This user doesn\'t exist !'})

    try:
        hospi= h.objects.get(user=user)
    except:
        hospi = None

    if hospi:
        return jr({'status':400, 'errors':'This person has already paid for accommodation ! '})
    else:
        hospi = h()

    if hostel not in hostels:
        return jr({'status':400, 'errors':'Invalid hostel in request ! '})

    amount = 150 + 150*days

    try:
        hospi.user = user
        hospi.hostel = hostel
        hospi.days = days
        hospi.amount = amount
        hospi.check_in = time
        hospi.save()

        user.accommodation = True
        user.save()

    except:
        return jr({'status':500, 'errors':'Server issue. Please try again ! '})
    return jr({"status":200, "fullname":user.fullname, "email":email, "hostel":hostel, "check_in":time, "amount":amount})