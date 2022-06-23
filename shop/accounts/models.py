# from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
 
class Shopper(AbstractUser):  #on hérite de la classe prédéfinie qui nous renvoi un modele de connexion dont onse servira dans la vue pour céer l'utilisateur
    pass

