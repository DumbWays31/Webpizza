from django.shortcuts import render, redirect


#import des modèles
from applipizza.models import Pizza, Ingredient, Composition
from applipizza.forms import IngredientForm, PizzaForm, CompositionForm
from applicompte.models import PizzaUser




#----------------------------#
# PIZZAS, PIZZA, INGREDIENTS #
#----------------------------#
def pizzas(request) :
    user = None
    if request.user.is_authenticated :
        user = PizzaUser.objects.get(id = request.user.id)

    #récup des pizzas de la BD avec les memes instructions que dans le shell
    lesPizzas = Pizza.objects.all()

    #on retourne l'emplacement du template et, meme s'il ne sert pas cette fois,
    #le parametre request ainsi que le contenu calculé (lesPizzas)
    # sous forme de dict python
    return render(
        request,
        'applipizza/pizzas.html',
        {'pizzas' : lesPizzas, "user" : user}
    )

def pizza(request, pizza_id):
    user = None

    if request.user.is_authenticated :
        user = PizzaUser.objects.get (id = request.user.id)

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
        {"pizza": laPizza, "ingredients_list": ingredients_list, "lesIng": lesIngredients, "user" : user}
    )

def ingredients(request) :
    # création du user
    user = None

    # utilisateur staff
    if request.user.is_staff :
        user = PizzaUser.objects.get (id = request.user.id)
        lesIngredients = Ingredient.objects.all()
        return render( 
            request,
            'applipizza/ingredients.html',
            {'ingredients' : lesIngredients
             ,"user" : user
             }
        )
    
    # client connecté
    elif request.user.is_authenticated :
        user = PizzaUser.objects.get (id = request.user.id)
        lesPizzas = Pizza.objects.al1()
        return render(
            request,
            'applipizza/pizzas.html',
            {'pizzas' : lesPizzas
             , "user" : user
             }
        )

    # internaute non connecté
    else :
        return render ( 
            request,
            'applicompte/login.html',
        )



#----------------------------#
#      CREER INGREDIENT      #
#----------------------------#
def formulaireCreationIngredient(request) :
    user = None

    # Vérifie si l'utilisateur est connecté et fait partie du personnel (staff)
    if request.user.is_authenticated and request.user.is_staff:
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
            request,
            'applipizza/formulaireCreationIngredient.html',
            {"user" : user}
        )
    else:
        # si l'accès n'est pas autorisé
        return render ( 
            request,
            'applicompte/login.html',
        )

def creerIngredient(request) : 
    user = None
    if request.user.is_authenticated :
        user = PizzaUser.objects.get(id = request.user.id)

    #recup du form posté
    form = IngredientForm(request.POST)

    if request.user.is_staff : 
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
                {"nom" : nomIng, "user" : user}
            )
    
    else : 
        return redirect('/pizzas/')



#----------------------------#
#       CREER PIZZA          #
#----------------------------#
def formulaireCreationPizza(request):
    user = None

    # Vérifie si l'utilisateur est connecté et fait partie du personnel (staff)
    if request.user.is_authenticated and request.user.is_staff:
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
            request,
            'applipizza/formulaireCreationPizza.html',
            {"user" : user}
        )
    else:
        # si l'accès n'est pas autorisé
        return render ( 
            request,
            'applicompte/login.html',
        )

def creerPizza(request) :
    user = None
    form = PizzaForm(request.POST, request.FILES)

    if request.user.is_staff : 
        user = PizzaUser.objects.get(id = request.user.id)
        if form.is_valid() :
            nomPiz = form.cleaned_data['nomPizza']
            prixPiz = form.cleaned_data['prix']
            imagePiz = request.FILES['image']

            piz = Pizza()

            piz.nomPizza = nomPiz
            piz.prix = prixPiz
            piz.image = imagePiz

            piz.save()

            return render(
                request,
                'applipizza/traitementFormulaireCreationPizza.html',
                {"nom" : nomPiz, "prix" : prixPiz, "image" : imagePiz, "user": user}
            )
        else : 
            return render(
                request,
                'applipizza/formulaireNonValide.html',
                {"errors" : form.errors}
            )
    else : 
        return redirect('/pizzas/')

    


#----------------------------#
#        COMPOSITION         #
#----------------------------#
def ajouterIngredientDansPizza(request, pizza_id) :
    #recupération du formulaire posté
    formulaire = CompositionForm(request.POST)

    if request.user.is_staff :
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

        return redirect('/pizzas/%d' % pizza_id)
    
    else : 
        return redirect ('/pizzas/')

def supprimerIngredientDansPizza(request, pizza_id, composition_id):

    if request.user.is_staff : 
        # Étape a : Récupérer la composition à supprimer
        composition = Composition.objects.get(id=composition_id)

        # Étape b : Appeler la méthode delete() sur cette composition
        composition.delete()
        
        # Étape c : Récupérer la pizza dont l'idPizza est passé en paramètre
        pizza = Pizza.objects.get(Pizza, idPizza=pizza_id)
        
        # Étape d : Récupérer toutes les compositions concernant la pizza
        compositions_pizza = Composition.objects.filter(pizza=pizza)
        
        # Étape e : Refabriquer la liste des ingrédients de la pizza
        ingredients_list = [(comp.ingredient, comp.quantite) for comp in compositions_pizza]
        
        # Étape f : Créer un nouveau formulaire CompositionForm
        composition_form = CompositionForm()
        
        # Étape g : Appeler le template pizzas.html en lui fournissant les données nécessaires
        return render(
            request, 
            'applipizza/pizzas.html', 
            {'pizzas': Pizza.objects.all(), 'pizza': pizza, 'ingredients_list': ingredients_list,
            'composition_form': composition_form,}
        )
    
    else : 
        return redirect ('/pizzas/')



#----------------------------#
#       MODIFIER PIZZA       #
#----------------------------#
def supprimerPizza(request, pizza_id):
    # Récupération de la pizza à supprimer
    pizza_a_supprimer = Pizza.objects.get(idPizza=pizza_id)

    if request.user.is_staff : 
        # Suppression de la pizza
        pizza_a_supprimer.delete()
        
        # Récupération de la liste de toutes les pizzas
        liste_pizzas = Pizza.objects.all()
        
        # Rediriger vers la vue pizzas avec la liste mise à jour
        return redirect('/pizzas/')
    
    else :
        return redirect('/pizzas/')

def afficherFormulaireModificationPizza(request, pizza_id) :
    user = None

    pizza_a_modifier = Pizza.objects.get(idPizza = pizza_id)
    # Vérifie si l'utilisateur est connecté et fait partie du personnel (staff)
    if request.user.is_authenticated and request.user.is_staff:
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
            request,
            'applipizza/formulaireModificationPizza.html',
            {"pizza" : pizza_a_modifier, "user" : user}
        )
    else:
        # si l'accès n'est pas autorisé
        return render ( 
            request,
            'applicompte/login.html',
        )

def modifierPizza(request, pizza_id):
    user = None

    if request.user.is_authenticated :
        user = PizzaUser.objects.get(id = request.user.id)

    # Récupération de la pizza à modifier
    pizza_a_modifier = Pizza.objects.get(idPizza=pizza_id)
    
    if request.user.is_staff :
        if request.method == 'POST':
            # Récupération du formulaire posté avec l'instance de la pizza
            form = PizzaForm(request.POST, request.FILES, instance=pizza_a_modifier)
            
            if form.is_valid():
                pizza_a_modifier.image = request.FILES['image']
                # Si le formulaire est valide, sauvegardez les modifications
                form.save()
                # Recherchez à nouveau la pizza modifiée dans la base de données
                pizza_modifiee = Pizza.objects.get(idPizza=pizza_id)
                # Redirigez vers un template pour afficher un message de confirmation
                return render(
                    request,
                    'applipizza/traitementFormulaireModificationPizza.html',
                    {"pizza_modifiee": pizza_modifiee, "user" : user}
                )
        else:
            # Si la méthode n'est pas POST, affichez le formulaire avec la pizza à modifier
            form = PizzaForm(instance=pizza_a_modifier)
        
        return render(
            request,
            'applipizza/modifierPizza.html',
            {"form": form, "pizza_a_modifier": pizza_a_modifier}
        )
    else : 
        return redirect ('/pizzas/')



#----------------------------#
#    MODIFIER INGREDIENT     #
#----------------------------#
def supprimerIngredient(request, ingredient_id):
    # Récupération de la pizza à supprimer
    ingredient_a_supprimer = Ingredient.objects.get(idIngredient=ingredient_id)

    if request.user.is_staff : 
        # Suppression de la pizza
        ingredient_a_supprimer.delete()
        
        # Récupération de la liste de toutes les pizzas
        liste_ingredients = Ingredient.objects.all()
        
        # Rediriger vers la vue pizzas avec la liste mise à jour
        return redirect('/ingredients/')
    
    else : 
        return redirect('/pizzas/')

def afficherFormulaireModificationIngredient(request, ingredient_id) :
    user = None

    ingredient_a_modifier = Ingredient.objects.get(idIngredient = ingredient_id)

    if request.user.is_authenticated and request.user.is_staff:
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
        request,
        'applipizza/formulaireModificationIngredient.html',
        {"ingredient" : ingredient_a_modifier, "user" : user}
    )
    else:
        return render ( 
            request,
            'applicompte/login.html',
        )

def modifierIngredient(request, ingredient_id) :
    user = None
    if request.user.is_authenticated :
        user = PizzaUser.objects.get(id = request.user.id)

    ingredient_a_modifier = Ingredient.objects.get(idIngredient=ingredient_id)

    if request.user.is_staff : 
        if request.method == 'POST':
            form = IngredientForm(request.POST, instance=ingredient_a_modifier)
            
            if form.is_valid():
                form.save()
                ingredient_modifie = Ingredient.objects.get(idIngredient=ingredient_id)
                return render(
                    request,
                    'applipizza/traitementFormulaireModificationIngredient.html',
                    {"ingredient_modifie": ingredient_modifie, "user" : user}
                )
        else:
            form = IngredientForm(instance=ingredient_a_modifier)
        
        return render(
            request,
            'applipizza/modifierIngredient.html',
            {"form": form, "ingredient_a_modifier": ingredient_a_modifier}
        )
    else : 
        return redirect('/pizzas/')