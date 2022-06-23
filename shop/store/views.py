from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from store.models import Order
from store.models import Cart
from store.models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()                  # obtenir tous les produits de la base de donnée et les stocker dans la variable products

    return render(request, 'store/index.html' , context={"products": products})
   

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)                 #recuperer le produit ou une erreur 404
    return render (request, 'store/detail.html', context={"product": product})          #retourner le detail.html qui prend en paramètre de boucle product défini dans cette fonction


def add_to_cart(request, slug):
    user = request.user                 #recuperation de la requete de l'utilisateur
    product = get_object_or_404(Product, slug=slug)                 #recuperation du produit dont le slug est egal au slug dans l'url
    cart, _ = Cart.objects.get_or_create(user=user)             # permet de créer un object s'i n'existe pas ou de le recupérer s'il existe . ////Returns a tuple of ((object, created) ici (cart, _ et _ signifi une var qu'on n'ur=tilisera pas )), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.This is meant to prevent duplicate objects from being created when requests are made in parallel, and as a shortcut to boilerplatish code. For example:
    order, created =Order.objects.get_or_create(user=user, ordered=False, product=product)
    
    if created:             # si le panier vient d'être créé,
        cart.orders.add(order)              #ajouter à orders(dans la base de donnée) order puis stocker dans la variable cart (panier)
        cart.save()                 #sauvegarder dans la base
    else:                   # si le panier existe,
        order.quantity += 1              # incrémenter le nombre de produit dans le panier
        order.save()

    return redirect(reverse("product", kwargs={"slug":slug}))           # rediriger vers la page de detail du produit

    # la fonction add to cart recupère la requete de l'utilateur qui est celle d'ajouter un produit dans le panier
    #recupère le produit indexé dans le slug puisque l'utilisateur est censé voir le produit le produit dans la page des details
    # créer le panier ou le recupérer s'il existait
    # si un objet aavit eté ajouté dans la panier, on le recupère et on incrémente le nombre de produit
    # sinon, créer le panier et l'y ajouter  

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)               # de Cart, recuperer la requête de l'utilisateur  
    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})


def delete_cart(request):   
    if cart:= request.user.cart :        #recupérer la request de l'utilisateur 
       cart.delete()
    return redirect('index')