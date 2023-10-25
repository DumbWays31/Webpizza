from django.shortcuts import render, redirect

#from applipizza.models import Pizza
from applicompte.models import PizzaUser
from applipizza.models import Pizza
from applipanier.models import Commande, LigneCommande



# Create your views here.

#----------------------------#
#          PANIER            #
#----------------------------#
def afficherPanier(request):
    user = None
    panier = None
    lesLignesDuPanier = None

    if request.user.is_authenticated:
        # Récupération de l'utilisateur connecté
        user = PizzaUser.objects.get(id=request.user.id)

        # Récupération des commandes non payées de l'utilisateur
        lesCommandesNonPayees = Commande.objects.filter(pizzauser=user, payee=False)

        if lesCommandesNonPayees.exists():
            # Si l'utilisateur a une commande non payée, le panier est le premier élément de cet ensemble
            panier = lesCommandesNonPayees[0]

            # Récupération des lignes du panier associées à l'identifiant du panier
            lesLignesDuPanier = LigneCommande.objects.filter(commande_id=panier.idCommande)

    return render(
        request,
        'applipanier/panier.html',
        {"user": user, "panier": panier, "lesLignesDuPanier": lesLignesDuPanier}
    )


def ajouterPizzaAuPanier(request, pizza_id):
    if not request.user.is_authenticated:
        return redirect('/pizzas/')
    
    pizzauser = PizzaUser.objects.get(id=request.user.id)
    pizza = Pizza.objects.get(idPizza=pizza_id)

    lignes_panier = []

    commandes_non_payees = Commande.objects.filter(pizzauser=pizzauser, payee=False)

    if commandes_non_payees.exists():
        panier = commandes_non_payees.first()
    else:
        panier = Commande.objects.create(pizzauser=pizzauser, prix=0, payee=False)

    lignes_panier = LigneCommande.objects.filter(commande=panier, pizza=pizza)

    if lignes_panier.exists():
        ligne_panier_pizza = lignes_panier.first()
    else:
        ligne_panier_pizza = LigneCommande.objects.create(
            commande=panier,
            pizza=pizza,
            quantite=0,
            prix=0
        )

    ligne_panier_pizza.quantite += 1
    ligne_panier_pizza.prix += pizza.prix
    ligne_panier_pizza.save()

    panier.prix += pizza.prix
    panier.save()

    return redirect('/panier/')




def retirerDuPanier(request, pizza_id):
    if not request.user.is_authenticated:
        return redirect('/pizzas/')

    pizzauser = PizzaUser.objects.get(id=request.user.id)

    # Retrieve the current active cart (panier) for the user
    panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()

    if panier is not None:
        try:
            pizza = Pizza.objects.get(idPizza=pizza_id)
            # Retrieve the line for the pizza in the cart
            ligne_panier_pizza = LigneCommande.objects.get(commande=panier, pizza=pizza)
            quantite = ligne_panier_pizza.quantite

            # Delete the line from the cart
            ligne_panier_pizza.delete()

            # Update the total price of the cart by subtracting the removed pizza's price
            panier.prix -= quantite * pizza.prix
            panier.save()

            # Re-retrieve the cart and its lines
            panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()
            lesLignesDuPanier = LigneCommande.objects.filter(commande=panier)
            
            # If there are no more lines in the cart, delete it
            if not lesLignesDuPanier:
                panier.delete()
                panier = None
                lesLignesDuPanier = []

        except Pizza.DoesNotExist:
            # Handle the case where the pizza doesn't exist
            pass

    return redirect('/panier/')



def viderPanier(request):
    if not request.user.is_authenticated:
        return redirect('/pizzas/')

    pizzauser = PizzaUser.objects.get(id=request.user.id)

    # Récupérer le panier actif de l'utilisateur s'il en existe un
    panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()

    if panier is not None:
        # Supprimer le panier et ses lignes associées
        panier.delete()
    
    # Mettre le panier à None
    panier = None
    lesLignesDuPanier = []

    return redirect('/panier/')





def retirerUnePizzaDuPanier(request, pizza_id):
    if not request.user.is_authenticated:
        return redirect('/pizzas/')

    pizzauser = PizzaUser.objects.get(id=request.user.id)

    # Récupérer le panier actif de l'utilisateur
    panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()

    if panier is not None:
        try:
            pizza = Pizza.objects.get(idPizza=pizza_id)
            # Récupérer la ligne du panier correspondant à la pizza
            ligne_panier_pizza = LigneCommande.objects.get(commande=panier, pizza=pizza)
            
            # Réduire la quantité de cette ligne d'une unité
            if ligne_panier_pizza.quantite > 1:
                ligne_panier_pizza.quantite -= 1
                ligne_panier_pizza.prix -= pizza.prix
                ligne_panier_pizza.save()
            else:
                # S'il ne reste qu'une seule pizza dans la ligne, supprimer la ligne
                ligne_panier_pizza.delete()
            
            # Mettre à jour le prix total du panier
            panier.prix -= pizza.prix
            panier.save()

            # Réafficher le panier avec les lignes mises à jour
            panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()
            lesLignesDuPanier = LigneCommande.objects.filter(commande=panier)

            # Si le panier est vide, le supprimer
            if not lesLignesDuPanier:
                panier.delete()
                panier = None
                lesLignesDuPanier = []

        except Pizza.DoesNotExist:
            # Gérer le cas où la pizza n'existe pas
            pass

    return redirect('/panier/')



def payerPanier(request):
    if not request.user.is_authenticated:
        return redirect('/pizzas/')

    pizzauser = PizzaUser.objects.get(id=request.user.id)
    panier = Commande.objects.filter(pizzauser=pizzauser, payee=False).first()

    if panier:
        panier.payee = True
        panier.save()

    return render(
        request, 
        'applipanier/avisPaiement.html', 
        {'panier': panier, 'user': pizzauser})