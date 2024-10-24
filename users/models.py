from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Utilisateur(AbstractUser):
    utilisateur_id = models.AutoField(primary_key=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_set',
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_permission_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def lister_comptes(self):
        return self.comptes.all()

    def deposer_argent(self, compte, montant: float):
        compte.deposer_argent(montant)

    def retirer_argent(self, compte, montant: float):
        compte.retirer_argent(montant)

    def transferer_argent(self, compte_source, compte_cible, montant: float):
        compte_source.effectuer_transfert(compte_cible, montant)

    def effectuer_virement(self, compte_source, compte_cible, montant: float):
        if compte_source.solde >= montant:
            compte_source.retirer_argent(montant)
            compte_cible.deposer_argent(montant)
        else:
            raise ValueError("Solde insuffisant pour le virement")
