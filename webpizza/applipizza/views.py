from django.shortcuts import render

#import des modèles
from applipizza.models import Pizza
from applipizza.models import Ingredient


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


def pizza(request,pizza_id) :

    #récup de la pizza dont l'identifiant a été passé en paramètre (c'est l'int pizza_id) 
    laPizza = Pizza.objects.get(idPizza = pizza_id)

    #on retourne l'emplacement du template et la pizza récupérée de la BD
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza" : laPizza}
    )
