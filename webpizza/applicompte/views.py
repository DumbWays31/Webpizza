from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from applipizza.models import Pizza
from applicompte.models import PizzaUser
from applicompte.forms import PizzaUserForm



# Create your views here.

#----------------------------#
#  CONNEXION ET DECONNEXION  #
#----------------------------#
def connexion (request) :
    usr = request.POST['username']
    pwd = request.POST['password']

    user = authenticate(request, username = usr, password = pwd)

    if user is not None:
        user = PizzaUser.objects.get(id = user.id)
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
            # 'applicompte/login.html'
            'applicompte/erreur.html'
        )

def deconnexion (request) :
    logout(request)
    return render( 
        request,
        'applicompte/logout.html'
    )



#----------------------------#
#           PROFIL           #
#----------------------------#
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
    
def traitementFormulaireProfil(request, user_id) :
    user = None

    # cas d'un utilisateur staff
    if request.user.is_authenticated :
        # user = PizzaUser.objects.get(id = request.user.id)
        user = PizzaUser.objects.get(id = user_id)
        form = PizzaUserForm(request.POST, request.FILES, instance = user)
        if form.is_valid() :
            form.save()
            user = PizzaUser.objects.get(id = request.user.id)
        lesPizzas = Pizza.objects.all()
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
    


#----------------------------#
#       INSCRIPTION          #
#----------------------------#
def formulaireInscription(request) :
    user = None

    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
        return redirect("/pizzas/")

    else :
        return render(
            request,
            'applicompte/formulaireInscription.html'
        )
    
def traitementFormulaireInscription(request) :
    # récupération des champs du formulaire
    fst = request.POST['first_name']
    lst = request.POST['last_name']
    usr = request.POST['username']
    eml = request.POST['email']
    pwd = request.POST['password']
    img = request.FILES['image']

    # création d'un PizzaUser
    user = PizzaUser()

    # affectation des champs récupérés aux attributs du PizzaUser
    user.first_name = fst
    user.last_name = lst
    user.username = usr
    user.email = eml
    user.set_password(pwd)
    user.image = img

    # sauvegarde du PizzaUser dans la base de données 
    user.save()

    # connexion du PizzaUser
    login(request, user)

    # récupération des pizzas
    lesPizzas = Pizza.objects.all()

    # on renvoie l'appel du template, avec les pizzas et le PizzaUser
    return render ( 
        request,
        'applipizza/pizzas.html', 
        {"pizzas" : lesPizzas, "user" : user}
    )