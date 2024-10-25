import random
from functools import wraps

from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from banques.models import CompteEnBanque


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


def generer_pin():
    return random.randint(1000, 9999)