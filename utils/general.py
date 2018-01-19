from django import forms
from models.models.user import UserDetails as u
import hashlib, re, random, datetime

def email_lookup(email):
    try:
        user = u.objects.get(email__exact = email)
        return user

    except Exception as e:
        return None

def auth_token_lookup(token):
    try:
        num_users = u.objects.filter(auth_token__exact = token).count()
        if num_users > 1:
            return None
        else:
            return u.objects.get(auth_token__exact = token)
    except Exception as e:
        # raise e
        return None

def gen_auth_token(email):
    token = str(random.randint(1,1111111)) + email + str(datetime.datetime.now()) + str(random.randint(1,1111111))
    token = token.encode("utf8")
    return hashlib.md5(token).hexdigest()

def namedWidget(input_name, widget=forms.TextInput):
    print(isinstance(widget, type))
    if isinstance(widget, type):
        widget = widget()

    render = widget.render

    widget.render = lambda name, value, attrs=None: \
        render(input_name, value, attrs)

    return widget

def hash_pwd(pwd):
    padded_pwd = "1qsc2"+pwd+"kfa0"
    padded_pwd = padded_pwd.encode("utf8")
    return hashlib.sha1(padded_pwd).hexdigest()

def phno_validate(phno):

    if type(phno) != type("a") or len(phno) < 5:
        return False

    phno = phno.replace(" ", "")
    if not re.fullmatch('^[+\d][-\d]+',phno):
        return False
    return True

