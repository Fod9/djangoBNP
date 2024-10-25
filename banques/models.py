import uuid

from django.db import models
from django.db.models import Manager


class CompteEnBanque(models.Model):
    compte_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    solde = models.FloatField(default=0.0)
    taux_interet = models.FloatField(default=10)
    pin = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey('users.Utilisateur', related_name='comptes', on_delete=models.CASCADE, null=True)
    rib = models.UUIDField(default=uuid.uuid4, editable=False)

    def consulter_solde(self):
        return self.solde

    def deposer_argent(self, montant: float):
        montant = float(montant)
        if montant > 0:
            self.solde += montant
            self.save()
            transaction = Depot.objects.create(compte_source=self, montant=montant, type=Transaction.Types.DEPOT)
            transaction.save()
        else:
            raise ValueError("Le montant déposé doit être supérieur à 0")

    def retirer_argent(self, montant: float):
        montant = float(montant)
        if montant <= self.solde:
            self.solde -= montant
            self.save()
            transaction = Retrait.objects.create(compte_source=self, montant=montant, type=Transaction.Types.RETRAIT)
            transaction.save()
        else:
            raise ValueError("Solde insuffisant pour le retrait")

    def effectuer_transfert(self, compte_cible, montant: float):
        montant = float(montant)
        if montant <= self.solde:
            self.solde -= montant
            compte_cible.solde += montant
            transaction = Virement.objects.create(compte_source=self, compte_cible=compte_cible, montant=montant, type=Transaction.Types.VIREMENT)
            transaction.save()
            self.save()
            compte_cible.save()
        else:
            raise ValueError("Solde insuffisant pour le transfert")

    def effectuer_virement(self, compte_cible, montant: float):
        montant = float(montant)

        if montant <= self.solde:

            if self == compte_cible:
                raise ValueError("Impossible de faire un virement sur le même compte")

            self.solde -= montant
            compte_cible.solde += montant

            transaction = Virement.objects.create(
                compte_source=self,
                compte_cible=compte_cible,
                montant=montant,
                type=Transaction.Types.VIREMENT
            )
            transaction.save()
            self.save()
            compte_cible.save()

        else:
            raise ValueError("Solde insuffisant pour le virement")


class TransactionManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    compte_source = models.ForeignKey(CompteEnBanque, related_name='transactions_source', on_delete=models.CASCADE)
    compte_cible = models.ForeignKey(CompteEnBanque, related_name='transactions_cible', on_delete=models.CASCADE, null=True)
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Types(models.TextChoices):
        """
        Transaction types
        """
        TRANSACTION = "TRANSACTION", "Transaction"
        DEPOT = "DEPOT", "Dépot"
        RETRAIT = "RETRAIT", "Retrait"
        VIREMENT = "VIREMENT", "Virement"
        INTERET = "INTERET", "Intérêt"


    objects = TransactionManager()

    type_par_defaut = Types.TRANSACTION

    # user type field with choices from Types
    type = models.CharField(
        "Type", max_length=50, choices=Types.choices, default=type_par_defaut
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.type_par_defaut
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.date}: {self.compte_source} - {self.montant}"

class DepotManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Transaction.Types.DEPOT)

class InteretManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Transaction.Types.INTERET)

class Interet(Transaction):
    objects = InteretManager()

    type_par_defaut = Transaction.Types.INTERET

class Depot(Transaction):
    objects = DepotManager()

    type_par_defaut = Transaction.Types.DEPOT

class RetraitManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Transaction.Types.RETRAIT)

class Retrait(Transaction):
    objects = RetraitManager()

    type_par_defaut = Transaction.Types.RETRAIT

class VirementManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Transaction.Types.VIREMENT)

class Virement(Transaction):
    objects = VirementManager()

    type_par_defaut = Transaction.Types.VIREMENT

    def __str__(self):
        return f"{self.date}: {self.compte_source} vers {self.compte_cible} - {self.montant}"