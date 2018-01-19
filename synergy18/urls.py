"""synergy18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import url, include
from django.contrib import admin
from users import login, register, update
from events.register import register_event as ev_r
from events.get_events import get
from django.views.generic import TemplateView
from users import qr

# event_urls= [url(r"^", TemplateView.as_view(template_name="events.html")),
#              url(r"^register/$", ev_r)
#              ]
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^login', login.login),
    url(r'^logout', login.logout),
    url(r"^register", register.register),
    url(r"^$", TemplateView.as_view(template_name="index.html")),
    url(r"^eve/$", TemplateView.as_view(template_name="events/index.html")),
    url(r"^events/register", ev_r),
    url(r"^events", get),
    url(r"^myQR/$", qr.render_qr),
    url(r"^update", update.update_info),
]