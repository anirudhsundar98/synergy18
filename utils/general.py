import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django import forms
from models.models.user import UserDetails as u
import hashlib, re, random, datetime
from django.conf import settings

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

def send_mail(html, subject, email):
    me = "synergy18.web@outlook.com"
    you = email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp-mail.outlook.com', 587)
    s.starttls()

    creds_file = open(settings.BASE_DIR+"/utils/mail_creds", "r+")
    creds = []
    for k in creds_file:
        creds.append(k.strip())

    s.login(creds[0], creds[1])
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()


def send_welcome_mail(fullname, email, uniq):
    me = "synergy18.web@outlook.com"
    you = email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Hello from Synergy !"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
      <script src='http://synergy.nitt.edu/static/js/qrcode.min.js'></script>
        <img style='width:300px;' src='http://synergy.nitt.edu/static/images/synergy_logo.png'>
        <p>Dear {},</p>
        <br>
    <p>Greetings from Team Synergy! Please check our website <a href='http://synergy.nitt.edu'>synergy.nitt.edu</a> for the workshop and event schedules and other such details.
    On-spot registrations are also available, but due to the high volume of participants, registering on-spot may not guarantee a place in any of our workshops.
    To have a hassle free experience at Synergy, we request you to register online and book a place in the workshop you're interested in by paying well in advance.
    </p>
    <p>An important point to be noted  is that a QR code will be assigned to those who have registered. Do make it a point to save the QR code image on your phone.</p>
    <img src='https://www.patrick-wied.at/static/qrgen/qrgen.php?r=5&a=0&content={}'>
    <p><strong>Rs. 150</strong> will have to be paid at the PR desk as a fee for attending all guest lectures and events.</p>

    <p>The fees for accommodation within NITT campus is as follows:
    <strong>Rs. 150</strong> per day for one participant.</p>
    <p>A caution deposit of <strong>Rs. 150</strong> which will be refunded to you once we get back the provisions you have paid for, for the duration of your stay.</p>
    <p> Your registration Id : <strong> {} </strong></p>
    <p>For more details about your stay or events or workshops, do contact:
    <ul>
    <li>PR head, Dharnesh: <a href='tel:7904453042'>7904453042</a></li>
    <li>Hospitality head, Gokul: <a href='9444936082'>9444936082</a></li>
    <li>Events head, Prashanth: <a href='9444741389'>9444741389</a></li> 
    <li>Workshops head, Babu: <a href='8870708062'>8870708062</a></li>
    </ul>
    <br>
    <p>Team Synergy thanks you for the interest you have shown in our symposium. We hope you will participate in forthcoming MEA events!</p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html.format(fullname, uniq, uniq[len(uniq)-10:]), 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp-mail.outlook.com', 587)
    s.starttls()

    creds_file = open(settings.BASE_DIR+"/utils/mail_creds", "r+")
    creds = []
    for k in creds_file:
        creds.append(k.strip())

    s.login(creds[0], creds[1])
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

def check_loggedInUser_admin(r):

    loggedIn = True
    user = None

    try:
        auth_token = r.session["cur_token"]
        user = auth_token_lookup(auth_token)
    except:
        loggedIn = False

    if not loggedIn or not user:
        return False
    if not user.admin:
        return False

    return user