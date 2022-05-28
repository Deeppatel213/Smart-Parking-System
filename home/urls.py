from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path('faq',views.faq),
    path('our_team',views.our_team),
]