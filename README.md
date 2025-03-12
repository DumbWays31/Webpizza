# WebPizza - Projet Django

## Installation

### 1. Créer et activer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Configurer la base de données

Si vous utilisez SQLite, aucune configuration supplémentaire n'est nécessaire.
Si vous utilisez PostgreSQL, mettez à jour le fichier `settings.py` dans la section `DATABASES`.

Appliquer les migrations :

```bash
python3 manage.py migrate
```

### 3. Lancer le serveur de développement

```bash
python3 manage.py runserver
```

## Fonctionnalités

- Gestion des utilisateurs avec authentification
- Gestion des pizzas
- Administration via Django Admin

## Technologies utilisées

- Python 3.13
- Django
- HTML / CSS
- SQLite
- Pillow (gestion des images)

## Auteur

Projet développé par **Elena Ferreira**.
