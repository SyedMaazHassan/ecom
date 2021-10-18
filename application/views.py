from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *

# main page function

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'main.html')


def home(request):
    all_products = Product.objects.all()
    context = { 'all_products':all_products}
    return render(request, 'home.html', context)

def category(request):
    return render(request, "category.html") 

def detail(request, id):
    filtered_product = get_object_or_404(Product, pk=id)
    if filtered_product:
        primary_picture = filtered_product.get_primary_picture()
        secondary_pictures = filtered_product.get_all_pictures() #[query]
    else:
        messages.error(request, "Given product address is invalid!")
        return redirect("application:home")
    
    context = {
        'product' : filtered_product,
        'secondary_pictures': secondary_pictures,
        'primary_picture': primary_picture
    }
    return render(request, "detail.html", context)

def sign_up(request):
    return render(request, "sign-up.html")

def sign_in(request):
    return render(request, "sign-in.html")

# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")


def all_categories(request):
    all_categories = Category.objects.all()
    context = {
        'all_categories' : all_categories,
    }
    return render(request, "all_categories.html", context)