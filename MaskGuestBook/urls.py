from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from MaskGuestBook import views

urlpatterns = [
    path('', views.index, name="index"),
    url(r'^keyboard', views.keyboard),
    path('index', views.index, name="index"),
    path('GuestBook', views.postGuestBook, name="GuestBook"),
    url(r'^go/$', views.goGuestBook, name="goGuestBook"),
    url(r'^$', views.live, name='live'),
	url(r'^stream2/$', views.stream2, name='stream2'),
	url(r'^live/$', views.live, name='live'),
    #url(r'^mask/$', views.mask, name = 'mask'),
    url(r'^capture/$', views.capture, name = 'capture')
]