from django import forms
from django.forms import ModelForm #formulaires automatiques
from applipizza.models import Ingredient, Pizza, Composition

#form pour un nvl ingredient
class IngredientForm(ModelForm) :
    class Meta : 
        model = Ingredient
        fields = ['nomIngredient']


class PizzaForm(ModelForm) :
    class Meta : 
        model = Pizza
        fields = ['nomPizza', 'prix']

class CompositionForm(ModelForm):
    class Meta:
        model = Composition
        fields = ['ingredient', 'quantite']

