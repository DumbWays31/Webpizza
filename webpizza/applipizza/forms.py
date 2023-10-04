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

class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['ingredient', 'quantite']

    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].widget = forms.Select(choices=Ingredient.objects.all().values_list('id', 'nomIngredient'))
        self.fields['ingredient'].widget.attrs.update({'class': 'custom-select'})

