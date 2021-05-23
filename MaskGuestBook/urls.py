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
    path('GuestBook', views.GuestBook, name="GuestBook"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
