from django.contrib import admin
from django.urls import path,include
from . import views,cut

urlpatterns = [
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('logout/',views.logout),
    path('on/',views.on),
    path('off/',views.off),
    path('cut',cut.cut),
    path('dashboard',views.dashboard),
    path('add_balance',views.addbalance),
    path('booksloat',views.book),
    path('cancelsloat',views.cancel),
    path('open',views.open),
    path('exit',views.exit),
]

