from django.urls import path

from banques import views

app_name = 'banques'

urlpatterns = [
    path('<int:banque_id>', views.accueil_banque),
    path('comptes/<int:compte_id>', views.consulter_compte, name='consulter_compte'),
    path('comptes/recuperer_comptes', views.recuperer_comptes),
    path('depot/<int:compte_id>', views.depot),
    path('retrait/<int:compte_id>', views.retrait),
    path('transfert/<int:compte_source>', views.transfert),
    path('virement/<int:compte_source>', views.virement),
    path('enter_pin/<int:compte_id>', views.enter_pin_view, name='enter_pin'),
    path('pin/<int:compte_id>', views.modify_pin, name='pin'),

]
