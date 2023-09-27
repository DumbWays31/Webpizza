from django import forms
from django.forms import ModelForm #formulaires automatiques
from applipizza.models import Ingredient

#form pour un nvl ingredient
class IngredientForm(ModelForm) :
    class Meta : 
        model = Ingredient
        fields = ['nomIngredient']
