from django.urls import path

#import des views par defaut du systm d'authentification de django, qui sera rename auth_views
from django.contrib.auth import views as auth_views
from applipanier import views

urlpatterns = [
    path('panier/', views.afficherPanier, name='panier'),
    path('pizzas/<int:pizza_id>/buy/', views.ajouterPizzaAuPanier),
    path('cart/<int:pizza_id>/delete/', views.retirerDuPanier),
    path('cart/delete/', views.viderPanier),
    path('cart/<int:pizza_id>/decrease/', views.retirerUnePizzaDuPanier),
    path('cart/pay/', views.payerPanier),
]
