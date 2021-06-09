from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from MaskGuestBook import views

urlpatterns = [
    path('', views.live, name="index"),
    url(r'^keyboard', views.keyboard),
    url(r'^go/$', views.goGuestBook, name="goGuestBook"),
    #url(r'^$', views.live, name='live'),
	url(r'^stream2/$', views.stream2, name='stream2'),
	url(r'^index/$', views.live, name='live'),
    url(r'^capture/$', views.capture, name = 'capture'),
    url(r'^recapture/$', views.recapture, name = 'recapture')
]