from django.contrib import admin

from banques.models import Banque, CompteEnBanque, Transaction
from users.models import Utilisateur

admin.site.register(Banque)
admin.site.register(Utilisateur)
admin.site.register(CompteEnBanque)
admin.site.register(Transaction)