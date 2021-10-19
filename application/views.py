from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# main page function

def home(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'home.html', context)


@login_required(login_url='application:sign_in')
def category(request):
    return render(request, "category.html")

@login_required(login_url='application:sign_in')
def detail(request, id):
    filtered_product = get_object_or_404(Product, pk=id)
    if filtered_product:
        primary_picture = filtered_product.get_primary_picture()
        secondary_pictures = filtered_product.get_all_pictures()  # [query]
    else:
        messages.error(request, "Given product address is invalid!")
        return redirect("application:home")

    context = {
        'product': filtered_product,
        'secondary_pictures': secondary_pictures,
        'primary_picture': primary_picture
    }
    return render(request, "detail.html", context)



@login_required(login_url='application:sign_in')
def all_categories(request):
    all_categories = Category.objects.all()
    context = {
        'all_categories': all_categories,
    }
    return render(request, "all_categories.html", context)

# FUNCTION FOR SIGN-UP


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('application:home')

    else:
        form = CreateUserForm()
        if request.method == "POST":
            form_data = request.POST
            form = CreateUserForm(form_data)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
                messages.success(
                    request, f"Account for {user_name} has been successfully made")
                return HttpResponseRedirect(reverse('application:sign-in'))

        context = {
            'form': form
        }
        return render(request, 'sign-up.html', context)

# FUNCTION FOR SIGN-IN


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('application:home')
    else:
        next_param = request.GET.get('next')
        if request.method == "POST":

            email = request.POST.get('email')
            password = request.POST.get('password')
            next_param = request.POST.get('next')

            user = authenticate(request, username=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                redirection_url = f"{reverse('application:home')}{next_param}"
                print(f"Reverse URL: {reverse('application:home')}")
                print(f"Next Value: {next_param}")
                print(f"Redirection URL: {redirection_url}")
                return redirect(f"{next_param}")

            else:
                messages.error(request, f"Username or Password is Incorrect:(")

        context = {}
        return render(request, 'sign-in.html', context)

# FUNCTION FOR LOGOUT


def sign_out(request):
    logout(request)
    return redirect('application:home')
