from django.contrib import admin

from banques.models import CompteEnBanque, Transaction
from users.models import Utilisateur

admin.site.register(Utilisateur)
admin.site.register(CompteEnBanque)
admin.site.register(Transaction)