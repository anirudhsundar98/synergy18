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
from django.conf.urls import url, include, handler404
from django.contrib import admin
from users import login, register, update
from events.register import register_event as ev_r
from events.get_events import get_events
from events.get_events import get_workshops
from events.get_events import get_gls
from events.handlers import handler_404
from users import qr, user_home
from django.views.generic import TemplateView
from events.sponsors import sponsors
from events.accommodation import accommodation
from events.coming_soon import coming_soon
from users.stats import get_stats
from users.admin_mod.register import *
# event_urls= [url(r"^", TemplateView.as_view(template_name="events.html")),
#              url(r"^register/$", ev_r)
#              ]
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^login', login.login),
    url(r'^logout', login.logout),
    url(r"^register", register.register),
    url(r"^$", user_home.home),
    # url(r"^eve/$", TemplateView.as_view(template_name="events/index.html")),
    url(r"^events/register", ev_r),
    url(r"^events$", get_events),
    url(r"^workshops", get_workshops),
    # url(r"^guest_lectures", get_gls),
    url(r"^guest_lectures", coming_soon),
    url(r"^myQR", qr.render_qr),
    url(r"^update", update.update_info),
    # url(r"^schedule$", coming_soon),
    url(r"^sponsors$", sponsors),
    url(r"^accommodation$", accommodation),
    # url(r"^sponsors$", coming_soon),
    url(r"^iuwetgiu4bgiuweg4iu23tg/27384t23tg2u3gt2g3t2323r$", get_stats), # Static data, Admin Page
    url(r"^iurbhiuerbhiw4ouebgiwu4b/w48bgiuw4bgiuw4ebiuw/iewugbiweugbewiugb$", mark_users), # Admin Page
    url(r"^sdkjgbu34iugb3i4/gejhgj34gib3/34gb34gig4$", mark_hospi), # Admin Page
    url(r"^dlkfjskljcslkdj/slkjdlkseoiuit$", vacancies),
    url(r"^admin/wggef23t23g23eg23$", mark_attended_paid),
    url(r"^admin/gjkrgiu24g34t$", mark_hostels),
    url(r"^dsdfu43bgiu3b4g/sefwefwef$", checkout_page), # Admin Page
    url(r"^admin/fdgu23t8934g", checkout),
    url(r"^admin/sdfiurgb34gu34ds", checkout_details),
    url(r"^", handler_404)
]
