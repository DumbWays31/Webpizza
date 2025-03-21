from django.db import models

# Create your models here.

class Ingredient(models.Model) : 
    #idIngredient clé primaire, n auto-incrémente =>AutoField
    idIngredient = models.AutoField(primary_key=True)

    #nomIngredient chaine de caractère =>CharField
    nomIngredient = models.CharField(max_length=50, verbose_name="le nom de cet ingrédient")

    def __str__(self) -> str : 
        return self.nomIngredient


class Pizza(models.Model) : 
    idPizza = models.AutoField(primary_key=True)

    nomPizza = models.CharField(max_length=50, verbose_name="le nom de cette pizza")

    #prix est décimal, max 4 chiffres dont 2 décimales
    prix = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="le prix")

    #fichier image de la pizza
    image = models.ImageField(default='imagesPizzas/default.PNG', upload_to='imagesPizzas/')

    def __str__(self) -> str:
        return 'pizza ' + self.nomPizza + ' (prix : ' +str(self.prix) + ' €)'
    

class Composition(models.Model) : 
    class Meta : 
        unique_together = ('ingredient', 'pizza')
    
    #idComposition = models.AutoField(primary_key=True)

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    quantite = models.CharField(max_length=100, verbose_name="la quantité")

    def __str__(self) -> str:
        ing = self.ingredient
        piz = self.pizza
        return ing.nomIngredient + ' fait partie de la pizza ' + piz.nomPizza + ' (quantité : ' + self.quantite + ')'