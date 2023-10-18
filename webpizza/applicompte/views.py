from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 
from applipizza.models import Pizza
from applicompte.models import PizzaUser
from applicompte.forms import PizzaUserForm



# Create your views here.
def connexion (request) :
    usr = request.POST['username']
    pwd = request.POST['password']

    user = authenticate(request, username = usr, password = pwd)
    
    user = PizzaUser.objects.get(id = user.id)

    if user is not None:
        login(request, user)
        lesPizzas = Pizza.objects.all ()
        return render (
            request,
            'applipizza/pizzas.html',
            {"pizzas" : lesPizzas, "user" : user}
        )
    else:
        return render( 
            request,
            'applicompte/login.html'
        )


def deconnexion (request) :
    logout(request)
    return render( 
        request,
        'applicompte/logout.html'
    )


def formulaireProfil(request) :
    user = None

    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
            request,
            'applicompte/profil.html',
            {"user" : user}
        )

    else :
        return render(
            request,
            'applicompte/login.html'
        )
    

def traitementFormulaireProfil(request) :
    user = None

    # cas d'un utilisateur staff
    if request.user.is_authenticated :
        user = PizzaUser.objects.get(id = request.user.id)
        form = PizzaUserForm(request.POST, request.FILES, instance = user)
        if form.is_valid() :
            form.save()
            user = PizzaUser.objects.get(id = request.user.id)
        lesPizzas = Pizza.objects.al1()
        return render(
            request,
            'applipizza/pizzas.html',
            {"pizzas" : lesPizzas, "user" : user}
        )
    
    else :
        return render ( 
            request,
            'applicompte/login.html',
        )