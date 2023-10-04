from django.shortcuts import render

#import des modèles
from applipizza.models import Pizza, Ingredient, Composition
from applipizza.forms import IngredientForm, PizzaForm



# Create your views here.
def pizzas(request) :

    #récup des pizzas de la BD avec les memes instructions que dans le shell
    lesPizzas = Pizza.objects.all()

    #on retourne l'emplacement du template et, meme s'il ne sert pas cette fois,
    #le parametre request ainsi que le contenu calculé (lesPizzas)
    # sous forme de dict python
    return render(
        request,
        'applipizza/pizzas.html',
        {'pizzas' : lesPizzas}
    )


def ingredients(request) :

    lesIngredients = Ingredient.objects.all()

    return render(
        request,
        'applipizza/ingredients.html',
        {'ingredients' : lesIngredients}
    )


from .models import Ingredient  # Assurez-vous d'importer le modèle Ingredient si ce n'est pas déjà fait

def pizza(request, pizza_id):
    # Récupération de la pizza dont l'identifiant a été passé en paramètre (pizza_id)
    laPizza = Pizza.objects.get(idPizza=pizza_id)

    # Récupération des ingrédients entrant dans la composition de la pizza
    composition = Composition.objects.filter(pizza=pizza_id)

    # Création d'une liste des ingrédients avec leurs quantités
    ingredients_list = []
    for compo in composition:
        ingredient_info = {
            'idComposition': compo.id,
            'nom': compo.ingredient.nomIngredient,
            'quantite': compo.quantite
        }
        ingredients_list.append(ingredient_info)

    # Récupération de tous les ingrédients pour construire le select de formulaire
    all_ingredients = Ingredient.objects.all()

    # On retourne l'emplacement du template, la pizza récupérée de la BD,
    # la liste des ingrédients calculée ci-dessus et la liste de tous les ingrédients
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza": laPizza, "ingredients_list": ingredients_list, "all_ingredients": all_ingredients}
    )




#CREER INGREDIENT
def formulaireCreationIngredient(request) :
    #on retourn l'emplacement du template
    return render(
        request,
        'applipizza/formulaireCreationIngredient.html',
    )

def creerIngredient(request) :
    
    #recup du form posté
    form = IngredientForm(request.POST)

    if form.is_valid() :
        #recup de la valeur du champ "nomIngredient"
        #form.cleaned_data nettoie la donnée au cas où des injections en tout genre seraient présentes
        nomIng = form.cleaned_data['nomIngredient']

        #creation du nvl ing
        ing = Ingredient()

        #affection de son attribut nomIngredient
        ing.nomIngredient = nomIng

        #enregistrement de l'ing dans la base
        ing.save()

        #on retourne l'emplacement de la vue (template au sens de django)
        #et le contenu calculé sous forme d'un dict python
        return render(
            request,
            'applipizza/traitementFormulaireCreationIngredient.html',
            {"nom" : nomIng}
        )


#CREER PIZZA
def formulaireCreationPizza(request) :
    return render(
        request,
        'applipizza/formulaireCreationPizza.html',
    )

def creerPizza(request) :
    
    form = PizzaForm(request.POST)

    if form.is_valid() :
        nomPiz = form.cleaned_data['nomPizza']
        prixPiz = form.cleaned_data['prix']

        piz = Pizza()

        piz.nomPizza = nomPiz
        piz.prix = prixPiz

        piz.save()

        return render(
            request,
            'applipizza/traitementFormulaireCreationPizza.html',
            {"nom" : nomPiz, "prix" : prixPiz}
        )