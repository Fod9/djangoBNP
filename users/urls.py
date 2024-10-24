from django.urls import path

app_name = 'users'

from . import views

urlpatterns = [
    path('login/', views.connexion),
    path('logout/', views.deconnexion),
]