from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model , login, logout, authenticate

# Create your views here.

User = get_user_model() # retourne les fonctionnalités du abstract user cée dans le models.py accounts


def signup(request):
    if request.method == "POST":   # si le formumaire est soumis,
        #traiter le formulaire
        username = request.POST.get("username") #recuperer les entrées de l'utilasteur dans les variables définies 
        password = request.POST.get("password") #avec password et username les noms issus du formulaire
        user = User.objects.create_user(username=username, password=password)# créer un utilisateur user à partir des infos recueillies du User et le connecter grâce a  la fonction login
        login(request, user)
        return redirect('index')  # rediriger vers la page d'accueil
        
    return render(request, 'accounts/signup.html')



def login_user(request):
    if request.method == "POST":
     #connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")

        user= authenticate(username=username, password=password) #authenticate permet de vérifier si les informations soumises sont les vraies
        if user:
            login(request, user)
            return redirect('index')
        

    return render(request, 'accounts/login.html')





def logout_user(request):
    logout(request)
    return redirect('index')