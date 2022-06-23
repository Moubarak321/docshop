from distutils.command.upload import upload
from django.utils import timezone
from pickle import TRUE
#from time import timezone
from tkinter import CASCADE
from django.db import models
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL


# Create your models here.

""""
Product
    Nom 
    Prix
    Stock
    Description
    Image

"""

class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)   #01 blank =true pour ne pas forcer l'utilisateur à entrer une description au produit lors de l'insertion du produit dans la base de donnée 02 textfield parceque c'est une longue chainede caractère contrairement au charfield qui est peu restrint
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True) #uploaded to pour grouper les images dans un dossier, null pour spécifier qu'in peut mettre uune valeur nulle dans la base de donnée.
    
    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug}) #renvoyer l'url nommé product tout en lui passant le paramètre kwargs qui comprend le slug. fais la même chose que la balise de l'url
        

"""
Article(Order):  les articles que l'utilisateur souhaite acheter et les details
    UTILISATEUR
    PRODUIT
    Quantité
    Commandé ou non
"""

class Order(models.Model):   #Commande de l'utilisateur
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #auth user modls fait appel à la variable précréée dans les settings pour illustrer le shopper.accounts. models.cascade indique à django de supprimer les articles choosies par l'user au cas où celui-ci suppimerait son compte
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


"""
Panier(Cart):  panier de l'utilsateur qui sera relié aux articles
    UTILISATEUR
    Articles
    Commandé ou non
    Date de commande
"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)  #one to one pour specifier que l'utilisatuer ne peut qu'avoir un seul panier
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)