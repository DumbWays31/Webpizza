from django.shortcuts import render

#import des modèles
from applipizza.models import Pizza

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
