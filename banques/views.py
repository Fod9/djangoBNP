from functools import wraps
from itertools import chain
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from banques.models import Banque, CompteEnBanque, Virement, Transaction
from users.models import Utilisateur
from django.http import JsonResponse, HttpResponseRedirect


def require_pin():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            compte_id = kwargs.get('compte_id')
            compte = CompteEnBanque.objects.get(pk=compte_id)

            if request.method == 'POST':
                pin = request.POST.get('pin')

                if int(compte.pin) == int(pin):
                    return view_func(request, *args, **kwargs)
                else:
                    next_url = request.get_full_path()
                    return render(request, 'enter_pin.html', context={
                        "next": next_url,
                        "compte_id": compte_id,
                        "error": "Le code pin est incorrect"
                    })
            else:
                next_url = request.get_full_path()
                url = reverse('banques:enter_pin', kwargs={'compte_id': compte_id})
                redirect_url = f'{url}?{urlencode({"next": next_url})}'
                return redirect(redirect_url)

        return _wrapped_view
    return decorator

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
    user = Utilisateur.objects.get(pk=request.user.utilisateur_id)
    comptes = user.lister_comptes()

    comptes = [{"id": compte.compte_id, "solde": compte.solde, "nom": compte.nom} for compte in comptes]

    return JsonResponse(data=comptes, safe=False)


def creer_compte()

@login_required
def accueil_banque(request, banque_id):

    banque = Banque.objects.get(pk=banque_id)

    user = request.user

    comptes_dans_la_banque = banque.comptes_bancaires.all()

    comptes_dans_la_banque = [compte for compte in comptes_dans_la_banque if compte.utilisateur == user]

    return render(request, 'home.html', context={
        "banque_nom": banque.nom,
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

        user = Utilisateur.objects.get(pk=request.user.utilisateur_id)

        user.transferer_argent(compte_source, compte_dest, montant)

        return JsonResponse(data={
            "compte_source": compte_source.nom,
            "compte_dest": compte_dest.nom,
            "montant": montant
        }, safe=False)


@login_required
def depot(request, compte_id):
    user = Utilisateur.objects.get(pk=request.user.utilisateur_id)

    compte = CompteEnBanque.objects.get(pk=compte_id)

    montant = request.POST.get('montant')

    user.deposer_argent(compte, montant)

    return JsonResponse(data={
        "compte": compte.compte_id,
        "montant": montant
    }, safe=False)

@login_required
def retrait(request, compte_id):
    user = Utilisateur.objects.get(pk=request.user.utilisateur_id)

    compte = CompteEnBanque.objects.get(pk=compte_id)

    montant = request.POST.get('montant')

    user.retirer_argent(compte, montant)

    return JsonResponse(data={
        "compte": compte.nom,
        "montant": montant
    }, safe=False)

@login_required
def virement(request, compte_source, compte_dest):
    user = Utilisateur.objects.get(pk=request.user.utilisateur_id)

    compte_source = CompteEnBanque.objects.get(pk=compte_source)
    compte_dest = CompteEnBanque.objects.get(pk=compte_dest)

    montant = request.POST.get('montant')

    user.transferer_argent(compte_source, compte_dest, montant)


    return JsonResponse(data={
        "compte_source": compte_source.nom,
        "compte_dest": compte_dest.nom,
        "montant": montant
    }, safe=False)

