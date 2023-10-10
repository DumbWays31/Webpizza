from django.shortcuts import render, redirect, get_object_or_404

#import des modèles
from applipizza.models import Pizza, Ingredient, Composition
from applipizza.forms import IngredientForm, PizzaForm, CompositionForm



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

    # Récupération de tous les ingrédients pour construire le select de formulaire
    lesIngredients = Ingredient.objects.all()

    # On retourne l'emplacement du template, la pizza récupérée de la BD,
    # la liste des ingrédients calculée ci-dessus et la liste de tous les ingrédients
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza": laPizza, "ingredients_list": ingredients_list, "lesIng": lesIngredients}
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
    


def ajouterIngredientDansPizza(request, pizza_id) :
    #recupération du formulaire posté
    formulaire = CompositionForm(request.POST)

    if formulaire.is_valid():
        #recuperation des données postées
        ing = formulaire.cleaned_data['ingredient']
        qte = formulaire.cleaned_data['quantite']
        piz = Pizza.objects.get(idPizza = pizza_id)
        compoPizza = Composition.objects.filter(pizza = pizza_id)
        lesIngredientsDeLaPizza = ((ligne.ingredient) for ligne in compoPizza)

        if ing in lesIngredientsDeLaPizza : 
            compo = Composition.objects.filter(pizza = pizza_id, ingredient = ing)
            compo.delete()
        
        #creation de la nvelle instance de Composition et remplissage des attributs
        compo = Composition()
        compo.ingredient = ing
        compo.pizza = piz
        compo.quantite = qte

        #sauvegarde dans la base de la composition
        compo.save()

    # #récupération de tous les ing pour construire le futur select
    # lesIngredients = Ingredient.objects.all()

    # #actualisation des ing entrant dans la composition de la pizza
    # compoPizza = Composition.objects.filter(pizza = pizza_id)

    # #on crée une liste dont chaque item contiendra l'identifiant de la compo (idComposition),
    # #le nom de l'ingrédient et la quantité de l'ing dans cette compo
    # listeIngredients = []
    # for ligneCompo in compoPizza :
    #     #on récupère l'ingrédient pour utiliser son nomIngredient
    #     ingredient = Ingredient.objects.get(idIngredient = ligneCompo.ingredient.idIngredient)
    #     listeIngredients.append(
    #         {"idComposition" : ligneCompo.id,
    #          "nom" : ingredient.nomIngredient,
    #          "qte" : ligneCompo.quantite}
    #     )

    # #on retourne l'emplacement du template, la pizza récupérée et la liste des ing calculée
    # return render(
    #     request,
    #     'applipizza/pizza.html',
    #     {"pizza" : piz,
    #      "liste" : listeIngredients,
    #      "lesIng" : lesIngredients}
    # )
    #return pizza(request,pizza_id)
    return redirect('/pizzas/%d' % pizza_id)


#mofif pizza
def supprimerPizza(request, pizza_id):
    # Récupération de la pizza à supprimer
    pizza_a_supprimer = Pizza.objects.get(idPizza=pizza_id)
    
    # Suppression de la pizza
    pizza_a_supprimer.delete()
    
    # Récupération de la liste de toutes les pizzas
    liste_pizzas = Pizza.objects.all()
    
    # Rediriger vers la vue pizzas avec la liste mise à jour
    return redirect('/pizzas/')

def afficherFormulaireModificationPizza(request, pizza_id) : 
    pizza_a_modifier = Pizza.objects.get(idPizza = pizza_id)
    return render(
        request,
        'applipizza/formulaireModificationPizza.html',
        {"pizza" : pizza_a_modifier}
    )

def modifierPizza(request, pizza_id):
    # Récupération de la pizza à modifier
    pizza_a_modifier = Pizza.objects.get(idPizza=pizza_id)
    
    if request.method == 'POST':
        # Récupération du formulaire posté avec l'instance de la pizza
        form = PizzaForm(request.POST, instance=pizza_a_modifier)
        
        if form.is_valid():
            # Si le formulaire est valide, sauvegardez les modifications
            form.save()
            # Recherchez à nouveau la pizza modifiée dans la base de données
            pizza_modifiee = Pizza.objects.get(idPizza=pizza_id)
            # Redirigez vers un template pour afficher un message de confirmation
            return render(
                request,
                'applipizza/traitementFormulaireModificationPizza.html',
                {"pizza_modifiee": pizza_modifiee}
            )
    else:
        # Si la méthode n'est pas POST, affichez le formulaire avec la pizza à modifier
        form = PizzaForm(instance=pizza_a_modifier)
    
    return render(
        request,
        'applipizza/modifierPizza.html',
        {"form": form, "pizza_a_modifier": pizza_a_modifier}
    )



#modif ingrédients
def supprimerIngredient(request, ingredient_id):
    # Récupération de la pizza à supprimer
    ingredient_a_supprimer = Ingredient.objects.get(idIngredient=ingredient_id)
    
    # Suppression de la pizza
    ingredient_a_supprimer.delete()
    
    # Récupération de la liste de toutes les pizzas
    liste_ingredients = Ingredient.objects.all()
    
    # Rediriger vers la vue pizzas avec la liste mise à jour
    return redirect('/ingredients/')

def afficherFormulaireModificationIngredient(request, ingredient_id) : 
    ingredient_a_modifier = Ingredient.objects.get(idIngredient = ingredient_id)
    return render(
        request,
        'applipizza/formulaireModificationIngredient.html',
        {"ingredient" : ingredient_a_modifier}
    )

def modifierIngredient(request, ingredient_id) : 
    ingredient_a_modifier = Ingredient.objects.get(idIngredient=ingredient_id)
    
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient_a_modifier)
        
        if form.is_valid():
            form.save()
            ingredient_modifie = Ingredient.objects.get(idIngredient=ingredient_id)
            return render(
                request,
                'applipizza/traitementFormulaireModificationIngredient.html',
                {"ingredient_modifie": ingredient_modifie}
            )
    else:
        form = IngredientForm(instance=ingredient_a_modifier)
    
    return render(
        request,
        'applipizza/modifierIngredient.html',
        {"form": form, "ingredient_a_modifier": ingredient_a_modifier}
    )




#modif composition
def supprimerIngredientDansPizza(request, pizza_id, composition_id):
    # Étape a : Récupérer la composition à supprimer
    composition = Composition.objects.get(id=composition_id)
    
    # Étape b : Appeler la méthode delete() sur cette composition
    composition.delete()
    
    # Étape c : Récupérer la pizza dont l'idPizza est passé en paramètre
    pizza = get_object_or_404(Pizza, idPizza=pizza_id)
    
    # Étape d : Récupérer toutes les compositions concernant la pizza
    compositions_pizza = Composition.objects.filter(pizza=pizza)
    
    # Étape e : Refabriquer la liste des ingrédients de la pizza
    ingredients_list = [(comp.ingredient, comp.quantite) for comp in compositions_pizza]
    
    # Étape f : Créer un nouveau formulaire CompositionForm
    composition_form = CompositionForm()
    
    # Étape g : Appeler le template pizzas.html en lui fournissant les données nécessaires
    return render(request, 'applipizza/pizzas.html', {
        'pizzas': Pizza.objects.all(),
        'pizza': pizza,
        'ingredients_list': ingredients_list,
        'composition_form': composition_form,
    })
