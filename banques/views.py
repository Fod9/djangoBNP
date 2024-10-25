from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from banques.models import CompteEnBanque, Transaction
from users.models import Utilisateur
from banques.utils import require_pin, generer_pin


@login_required
def enter_pin_view(request, compte_id,  error=None):
    next_url = request.GET.get('next')
    return render(request, 'enter_pin.html', context={
        "next": next_url,
        "compte_id": compte_id,
        "error": error
    })

@login_required
def recuperer_comptes(request):
    user = Utilisateur.objects.get(pk=request.user.pk)
    comptes = user.lister_comptes()

    comptes = [{"id": compte.compte_id, "solde": compte.solde, "nom": compte.nom} for compte in comptes]

    return JsonResponse(data=comptes, safe=False)


@require_http_methods(["GET", "POST"])
@login_required
def creer_compte(request):
    if request.method == 'GET':
        return render(request, 'creer_compte.html', context={
            "pin": generer_pin()
        })

    elif request.method == 'POST':
        nom = request.POST.get('nom')
        taux_interet = request.POST.get('taux_interet')
        pin = request.POST.get('pin')

        print(nom, taux_interet, pin)
        compte = CompteEnBanque(
            nom=nom,
            taux_interet=float(taux_interet),
            pin=float(pin),
            utilisateur=request.user,
        )
        compte.save()

        return redirect('/')

@login_required
def accueil_banque(request):
    user = request.user

    comptes_dans_la_banque = CompteEnBanque.objects.filter(utilisateur=user)

    return render(request, 'home.html', context={
        "comptes" : comptes_dans_la_banque
    })

@login_required
@require_pin()
def consulter_compte(request, compte_id):

    compte = CompteEnBanque.objects.get(pk=compte_id)

    if compte.utilisateur != request.user:
        return render(request, 'error.html', context={
            "message": "Vous n'êtes pas autorisé à consulter ce compte"
        })

    transactions_sortante = Transaction.objects.filter(compte_source=compte)
    transactions_entrante = Transaction.objects.filter(compte_cible=compte)

    resultats_combines = sorted(
        chain(transactions_sortante, transactions_entrante),
        key=lambda transaction: transaction.date,
    )

    return render(request, 'compte.html', context={
        "compte": compte,
        "transactions" : resultats_combines[::-1],
    })

@login_required
def transfert(request, compte_source):

        compte_dest = request.POST.get('compte_dest')

        compte_source = CompteEnBanque.objects.get(pk=compte_source)
        compte_dest = CompteEnBanque.objects.get(pk=compte_dest)

        montant = request.POST.get('montant')

        user = Utilisateur.objects.get(pk=request.user.pk)

        user.transferer_argent(compte_source, compte_dest, montant)

        return JsonResponse(data={
            "compte_source": compte_source.nom,
            "compte_dest": compte_dest.nom,
            "montant": montant
        }, safe=False)


@login_required
def depot(request, compte_id):
    user = Utilisateur.objects.get(pk=request.user.pk)

    compte = CompteEnBanque.objects.get(pk=compte_id)

    montant = request.POST.get('montant')

    user.deposer_argent(compte, montant)

    return JsonResponse(data={
        "compte": compte.compte_id,
        "montant": montant
    }, safe=False)

@login_required
def retrait(request, compte_id):
    user = Utilisateur.objects.get(pk=request.user.pk)

    compte = CompteEnBanque.objects.get(pk=compte_id)

    montant = request.POST.get('montant')

    user.retirer_argent(compte, montant)

    return JsonResponse(data={
        "compte": compte.nom,
        "montant": montant
    }, safe=False)

@login_required
def virement(request, compte_source, compte_dest):
    user = Utilisateur.objects.get(pk=request.user.pk)

    compte_source = CompteEnBanque.objects.get(pk=compte_source)
    compte_dest = CompteEnBanque.objects.get(pk=compte_dest)

    montant = request.POST.get('montant')

    user.transferer_argent(compte_source, compte_dest, montant)


    return JsonResponse(data={
        "compte_source": compte_source.nom,
        "compte_dest": compte_dest.nom,
        "montant": montant
    }, safe=False)

