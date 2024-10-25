from django.urls import path

app_name = 'users'

from . import views

urlpatterns = [
    path('login/', views.connexion, name='login'),
    path('register/', views.inscription, name='register'),
    path('logout/', views.deconnexion, name='logout'),
]