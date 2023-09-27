from django.shortcuts import render

#import des modèles
from applipizza.models import Pizza
from applipizza.models import Ingredient

from applipizza.models import Composition


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

    # On retourne l'emplacement du template, la pizza récupérée de la BD,
    # et la liste des ingrédients calculée ci-dessus
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza": laPizza, "ingredients_list": ingredients_list}
    )


def formulaireCreationIngredient(request) :
    #on retourn l'emplacement du template
    return render(
        request,
        'applipizza/formulaireCreationIngredient.html',
    )