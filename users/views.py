from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render

from users.models import Utilisateur


def connexion(request):
    print(request)
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        return login_post(request)
    elif request.method == 'GET':
        return login_get(request)

def login_get(request):
    next_url = request.GET.get('next')

    # displaying custom messages if page is accessed via a redirect (permission denied)
    if next_url is not None and 'dashboard' in next_url:

        if not request.user.is_authenticated:  # if user is not connected
            error_message = 'Erreur, veuillez vous connecter avec un compte Agent pour accéder à cette page.'

        else:  # if user is connected but don't have permissions
            error_message = 'Erreur, vous n\'avez pas la permission de vous rendre sur cette page.\n' \
                            'Veuillez vous connecter avec un compte différent.'

    # we display nothing if page was accessed normally
    else:
        error_message = ''

    return render(
        request=request,
        template_name='login.html',
        context={
            'next_url': next_url,
            'error_message': error_message,
        },
    )

def login_post(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    next_url = request.POST.get('next_url')

    user = authenticate(request, username=username, email=email, password=password)

    if user is not None:
        login(request, user)

        if next_url is not None and next_url != 'None' and next_url != '':
            return redirect(next_url)
        else:
            return redirect('index')

    else:
        error_message = "Erreur, nom d'utilisateur ou mot de passe invalide"

        # and we return the same page with an error message
        return render(
            request=request,
            template_name='login.html',
            context={
                'error_message': error_message,
            },
        )

def inscription(request):
    next_url = '/'
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST['email']
        password = make_password(request.POST['password'])
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        try:
            if not Utilisateur.objects.filter(email=email).first():
                user = Utilisateur(username=username, email=email, password=password, first_name=first_name,
                                   last_name=last_name)
                user.save()
                login(request, user)
                return redirect(next_url)
            else:
                return render(request, 'register.html', {'error': 'Email déjà utilisé haha'})
        except ValueError as e:
            return render(request, 'register.html', {'error': str(e)})

    elif request.method == "GET":
        return render(request, 'register.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('index')