from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from MaskGuestBook import views

urlpatterns = [
    path('', views.index, name="index"),
    url(r'^keyboard', views.keyboard)
]
