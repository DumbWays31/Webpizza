from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 
from applipizza.models import Pizza


# Create your views here.
def connexion (request) :
    usr = request. POST['username']
    pwd = request.POST['password']

    user = authenticate (request, username = usr, password = pwd)

    if user is not None:
        login (request, user)
        lesPizzas = Pizza.objects.all ()
        return render (
            request,
            'applipizza/pizzas.html',
            {"pizzas" : lesPizzas, "user" : user}
        )
    else:
        return render ( 
            request,
            'applicompte/login.html'
        )

def deconnexion (request) :
    logout(request)
    return render( 
        request,
        'applicompte/logout.html'
    )
