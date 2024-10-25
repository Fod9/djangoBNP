from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def accueil(request):
    return redirect('banques:accueil_banque')

