from django.db import models
from applicompte.models import PizzaUser  
from applipizza.models import Pizza 


class Commande(models.Model):
    idCommande = models.AutoField(primary_key=True)
    dateCommande = models.DateTimeField(auto_now_add=True)
    payee = models.BooleanField(default=False)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pizzauser = models.ForeignKey(PizzaUser, on_delete=models.CASCADE)

class LigneCommande(models.Model):
    idLigneCommande = models.AutoField(primary_key=True)
    quantite = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
