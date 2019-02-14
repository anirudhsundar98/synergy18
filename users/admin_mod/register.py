from utils import general
from django.shortcuts import render
from django.http import JsonResponse as jr
from models.models import UserDetails as u
from models.models.events import EventRegister as er
from django.db import transaction
from django.db.models import Count
from datetime import datetime, timezone
from models.models.user import Hospi as h
import pytz

def mark_users(r):

    user = general.check_loggedInUser_admin(r)
    if not user:
        return render(r, "404.html")
    return render(r, "pr.html", {"logged_in":True, "user":user.fullname})

def mark_attended_paid(r):
    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status':400, "errors":"Sorry, you can't access this."})

    try:
        # entered_email = r.POST["email"]
        entered_unique_id = r.POST["unique"]
        # entered_phone = r.POST["phone"]
        entered_ticket = r.POST["ticket"]
        paymentOnline = False
        if ("online-pay" in r.POST.keys()):
            paymentOnline = True
    except Exception as e:
        print(e)
        return jr({'status':400, 'errors':'Invalid request.'})

    try:
        # user = u.objects.get(email__exact=entered_email)
        user = u.objects.get(unique__contains=entered_unique_id)
    except:
        return jr({'status': 400, 'errors': 'This user doesn\'t exist. They\'ll have to sign up first.'})

    # ws_dict = {'automobile':2, 'creo':7}
    ws_dict = {"fusion360": 11, "matlab": 12, "robotics": 13, "automobile": 14, 'sketch': 15}
    # ws_dict = {'automobile':3, 'creo':16, 'automation':17, 'robotics':19, '3d':20, 'photography':21}
    # money_dict = {'automobile':450, 'creo':300, 'automation':300, 'swarm':0, '3d':200, 'photography':50}
    money_dict = {
        'fusion360': 250,
        'matlab': 250,
        'automobile': 500,
        'sketch': 1000,
        'robotics': 0
    }
    # restrict = {"automation":74, "creo":17}
    money = 0

    if 'robotics' in r.POST:
        if r.POST['robotics'] not in ["2250", "2500", "None"]:
            return jr({"status":400, "errors":"Incorrect detail for robotics"})
        elif r.POST['robotics'] == "2250":
            money_dict["robotics"] = 562.5
        elif r.POST['robotics'] == "2500":
            money_dict["robotics"] = 500

    try:
        with transaction.atomic():
            if 'events' in r.POST and not user.events_paid:
                user.events_paid = True
                money+=200
                user.save()

            for w in ws_dict:
                if w == "robotics" and r.POST['robotics'] == "None":
                    continue
                if w in r.POST:
                    try:
                        all_reg = er.objects.filter(event_id=ws_dict[w], paid=True)
                        reg_count = all_reg.count()
                    except:
                        return ({"status":400, "errors":"Error. Please try again "})
                    # if w in restrict and reg_count >= restrict[w]:
                    #     return jr({"status":400, "errors":"Sorry. There are already {} on-spot registrants for {}.".format(restrict[w], w)})
                    reg = None
                    try:
                        reg = er.objects.get(user=user, event_id=ws_dict[w])
                    except:
                        pass

                    e = er()
                    try:
                        if not reg:
                            e.user = user
                            e.event_id = ws_dict[w]
                            if (paymentOnline):
                                e.paid_online = True
                            else:
                                e.paid = True
                            e.save()
                            money+=money_dict[w]
                        elif not reg.paid:
                            if (paymentOnline):
                                reg.paid_online = True
                            else:
                                reg.paid = True
                                pass
                            reg.save()
                            money += money_dict[w]
                    except Exception as e:
                        print(e)
                        return jr({'status': 400, 'errors': 'There was a problem with the server. Please try again.'})
    except Exception as e:
        print(e)
        return jr({'status': 400, 'errors': 'There was a problem in saving your response. Please try again.'})

    try:
        user.paid = True
        user.attended = True
        if (paymentOnline):
            user.amount_online += money
        else:
            user.amount += money
        # user.alt_phone = entered_phone
        if user.ticket is not None and len(user.ticket)!=0 and len(entered_ticket)!=0:
            user.ticket += ", {}".format(entered_ticket)

        elif len(entered_ticket)!=0:
            user.ticket = entered_ticket
        user.save()
    except Exception as e:
        print(e)
        return jr({"status":400, "errors":"There was an error in saving to the database. Please try again."})


    ticket = user.ticket
    if ticket is None:
        ticket = ""

    return jr({"status":200, "fullname":user.fullname, "email":user.email, "paid":"Success", "amount":user.amount + user.amount_online, "ticket":ticket})

def mark_hospi(r):
    user = general.check_loggedInUser_admin(r)
    if not user:
        return render(r, "404.html")
    return render(r, "hospi.html", {"logged_in":True, "user":user.fullname})

def vacancies(r):
    user = general.check_loggedInUser_admin(r)
    if not user:
        return jr({'status': 400, "errors": "Sorry, you can't access this."})

    hostel_max_slots = {
        "garnet a 1st floor common room": 30,
        "garnet a 2nd floor common room": 29,
        "garnet a 1st floor study room": 20,
        "garnet a 2nd floor study room": 16,
        "garnet b 2nd floor common room": 24,
        "garnet b 2nd floor study room": 17,
        "garnet c 1st floor common room": 29,
        "garnet c 2nd floor common room": 30
    }
    current_vacancies = {
        "garnet a 1st floor common room": 30,
        "garnet a 2nd floor common room": 29,
        "garnet a 1st floor study room": 20,
        "garnet a 2nd floor study room": 16,
        "garnet b 2nd floor common room": 24,
        "garnet b 2nd floor study room": 17,
        "garnet c 1st floor common room": 29,
        "garnet c 2nd floor common room": 30
    }

    hostel_count_query_result = h.objects.values('hostel').exclude(check_out__isnull=False).annotate(count=Count('hostel'))
    for item in hostel_count_query_result:
        current_vacancies[item["hostel"]] = hostel_max_slots[item["hostel"]] - item["count"]

    return render(r, "vacancies.html", {"vacancies": current_vacancies})


def mark_hostels(r):

    user = general.check_loggedInUser_admin(r)
    # SELECT hostel, count(*) as `count` FROM `hospi` WHERE check_out IS NULL GROUP BY hostel

    if not user:
        return jr({'status':400, "errors":"Sorry, you can't access this."})

    hostels = [
        "garnet a 1st floor common room",
        "garnet a 2nd floor common room",
        "garnet a 1st floor study room",
        "garnet a 2nd floor study room",
        "garnet b 2nd floor common room",
        "garnet b 2nd floor study room",
        "garnet c 1st floor common room",
        "garnet c 2nd floor common room"
    ]
    hostel_max_slots = {
        "garnet a 1st floor common room": 30,
        "garnet a 2nd floor common room": 29,
        "garnet a 1st floor study room": 20,
        "garnet a 2nd floor study room": 16,
        "garnet b 2nd floor common room": 24,
        "garnet b 2nd floor study room": 17,
        "garnet c 1st floor common room": 29,
        "garnet c 2nd floor common room": 30
    }
    current_hostel_count = {
        "garnet a 1st floor common room": 0,
        "garnet a 2nd floor common room": 0,
        "garnet a 1st floor study room": 0,
        "garnet a 2nd floor study room": 0,
        "garnet b 2nd floor common room": 0,
        "garnet b 2nd floor study room": 0,
        "garnet c 1st floor common room": 0,
        "garnet c 2nd floor common room": 0
    }

    try:
        unique = r.POST["unique"]
        hostel = r.POST["hostel"]
        days = int(r.POST["days"])
        time = datetime.now()
    except Exception as e:
        print(e)
        return jr({'status':400, 'errors':'Invalid request.'})

    # Vacancy Calculations
    hostel_count_query_result = h.objects.values('hostel').exclude(check_out__isnull=False).annotate(count=Count('hostel'))
    for item in hostel_count_query_result:
        current_hostel_count[item["hostel"]] = item["count"]

    try:
        # user = u.objects.get(email__exact=email)
        user = u.objects.get(unique__contains=unique)
    except:
        return jr({'status':400, 'errors':'This user doesn\'t exist.'})

    try:
        hospi= h.objects.get(user=user)
    except:
        hospi = None

    if hospi:
        return jr({'status':400, 'errors':'This person has already paid for accommodation. '})
    else:
        hospi = h()

    hostel_vacancy_count = hostel_max_slots[hostel] - current_hostel_count[hostel]
    if (hostel_vacancy_count <= 0):
        return jr({'status': 400, 'errors': 'This hostel does not have any vacancies.'})

    if hostel not in hostels:
        return jr({'status':400, 'errors':'Invalid hostel in request. '})

    amount = 150 + 150*days

    try:
        with transaction.atomic():
            hospi.user = user
            hospi.hostel = hostel
            hospi.days = days
            hospi.amount = amount
            hospi.check_in = time
            hospi.save()

            user.accommodation = True
            user.attended = True
            user.save()

    except Exception as e:
        print(e)
        return jr({'status':500, 'errors':'Server issue. Please try again. '})
    return jr({"status":200, "fullname":user.fullname, "email":user.email, "hostel":hostel, "vacancy_count":hostel_vacancy_count - 1, "check_in":time, "amount":amount})

def checkout_page(r):
    user = general.check_loggedInUser_admin(r)
    if not user:
        return render(r, "404.html")
    return render(r, "checkout.html", {"logged_in":True, "user":user.fullname})

def checkout(r):
    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status': 400, "errors": "Sorry, you can't access this."})

    try:
        unique = r.POST["unique"]
    except Exception as e:
        print(e)
        return jr({'status': 400, "errors": "Invalid request."})

    try:
        # user = u.objects.get(email__exact=email)
        user = u.objects.get(unique__contains=unique)
    except:
        return jr({'status': 400, "errors": "This user doesn\'t exist."})

    try:
        h_user = h.objects.get(user=user)
    except:
        return jr({'status': 400, "errors": "This user never checked in."})

    try:
        if h_user.check_out:
            return jr({'status': 400, "errors": "This user already checked out at {}.".format(h_user.check_out)})
    except Exception as e:
        print(e)
        return jr({'status': 400, "errors": "Sorry there was an error. Try again."})

    try:
        h_user.check_out = datetime.now(timezone.utc)
        print("Checkin out ", h_user.check_out)
        co_time = h_user.check_out
        ci_time = h_user.check_in

        diff = co_time - ci_time
        stayed = "This person has stayed for {} days {} seconds ".format(diff.days, diff.seconds)

        h_user.save()
    except Exception as e:
        print(e)
        return jr({'status': 400, "errors": "Sorry there was an error in saving to database. Try again."})

    return jr({'status':200, 'fullname':user.fullname, 'email':user.email, 'hostel': h_user.hostel, 'check_in':h_user.check_in, 'days':h_user.days, 'amount':h_user.amount, 'check_out':h_user.check_out, 'stayed':stayed})

def checkout_details(r):
    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status': 400, "errors": "Sorry, you can't access this."})

    try:
        unique = r.POST["unique"]
    except Exception as e:
        print(e)
        return jr({'status': 400, "errors": "Invalid request."})

    try:
        user = u.objects.get(unique__contains=unique)
    except:
        return jr({'status': 400, "errors": "This user doesn\'t exist."})

    try:
        h_user = h.objects.get(user=user)
    except:
        return jr({'status': 400, "errors": "This user never checked in."})

    try:
        check_out = h_user.check_out
        co_time = h_user.check_out
        ci_time = h_user.check_in


        if not check_out:
            check_out = "NO"
            co_time = datetime.now(timezone.utc)

        diff = co_time - ci_time
        stayed = "This person has stayed for {} days {} seconds ".format(diff.days, diff.seconds)

        return jr({'status':200, 'fullname':user.fullname, 'email':user.email, 'hostel': h_user.hostel, 'check_in':h_user.check_in, 'days':h_user.days, 'amount':h_user.amount, 'check_out':check_out, 'stayed':stayed})

    except Exception as e:
        print(e)
        return jr({'status': 400, "errors": "Error in retrieving data. Please try again."})