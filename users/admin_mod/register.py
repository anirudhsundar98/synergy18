from utils import general
from django.shortcuts import render
from django.http import JsonResponse as jr
from models.models import UserDetails as u

def mark_users(r):

    if not general.check_loggedInUser_admin(r):
        return render(r, "404.html")

    return render(r, "pr.html")


def mark_attended_paid(r):

    user = general.check_loggedInUser_admin(r)

    if not user:
        return jr({'status':400, "errors":"Sorry, you can't access this !"})

    try:
        entered_email = r.POST["email"]
        entered_id = r.POST["syn_id"]
        entered_amt = int(r.POST["amount"])
    except Exception as e:
        print(e)
        return jr({'status':400, 'errors':'Invalid request !'})

    try:
        user = u.objects.get(email__exact=entered_email, unique__endswith=entered_id)
    except:
        return jr({'status': 400, 'errors': 'This user doesn\'t even exist ! They\'ll have to sign up first !'})

    if user.paid:
        return jr({'status': 400, 'errors': 'This user has already paid !'})

    if entered_amt<0 or entered_amt>5000:
        return jr({'status': 400, 'errors': 'Invalid amount !'})

    try:
        user.amount = entered_amt
        user.paid = True
        user.save()
    except Exception as e:
        print(e)
        return jr({"status":400, "errors":"There was an error in saving to the database. Please try again !"})


    return jr({"status":200, "fullname":user.fullname, "email":user.email, "paid":"Success", "amount":user.amount})