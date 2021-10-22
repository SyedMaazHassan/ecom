from django.forms.widgets import FILE_INPUT_CONTRADICTION
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
from .forms import CreateUserForm, UpdateUserForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test


def mark_as_favorite(request):
    output = {
        'status': False,
        'message': None
    }
    if request.method == "GET":
        try:
            product_id = request.GET["id"]
            query = Product.objects.filter(id=int(product_id))

            if query.exists():
                product = query[0]

                if request.user.is_authenticated:
                    new_query = Favourite.objects.filter(
                        product=product, user=request.user)

                    if new_query.exists():
                        product = new_query[0]
                        product.delete()
                        output['favorite'] = False
                        output['message'] = "Product unmarked as favorite"
                    else:
                        new_wishlist = Favourite(
                            product=product,
                            user=request.user
                        )
                        new_wishlist.save()
                        output['favorite'] = True
                        output['message'] = "Product marked as favorite"
                    output['auth'] = True
                else:
                    output['auth'] = False
                output['status'] = True
        except Exception as e:
            output['message'] = str(e)

    return JsonResponse(output)


def get_favorites(request):
    output = {
        'ids': []
    }
    if request.user.is_authenticated:
        query = Favourite.objects.filter(user=request.user)
        product_list = list(query)
        for i in range(len(product_list)):
            product_list[i] = product_list[i].get_product_id()
        output['ids'] = product_list

    return JsonResponse(output)


def get_all_categories():
    all_categories = Category.objects.all()
    return all_categories


def get_all_products():
    all_products = Product.objects.all().order_by("-id")
    all_products[0].abc = 1
    return all_products


# main page function
def home(request):
    all_my_products = get_all_products()
    if all_my_products.count() > 4:
        all_my_products = all_my_products[0:4]
    context = {
        'all_products': all_my_products,
        'home': True
    }
    wish_list = request.GET.get('wishlist')
    print(wish_list)
    context['categories'] = get_all_categories()
    return render(request, 'home.html', context)


def category(request, id):
    category = Category.objects.get(id=id)
    filtered_products = Product.objects.filter(category=category)
    context = {
        'all_products': filtered_products,
        'category': category,
        'my_cat': category
    }
    context['categories'] = get_all_categories()
    return render(request, "category.html", context)

# @login_required(login_url='application:sign_in')


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
    context['categories'] = get_all_categories()
    return render(request, "detail.html", context)


def all_products(request):
    context = {
        'all_products': get_all_products()
    }
    context['categories'] = get_all_categories()
    return render(request, "all-products.html", context)

# @login_required(login_url='application:sign_in')


def all_categories(request):
    all_categories = Category.objects.all()
    context = {
        'all_categories': all_categories,
    }
    return render(request, "all_categories.html", context)

# FUNCTION FOR WISHLIST PAGE


@login_required(login_url='application:sign_in')
def wishlist(request):
    query = Favourite.objects.filter(user=request.user)
    all_products = []
    for i in query:
        all_products.append(i.product)

    context = {
        'all_products': all_products
    }
    context['categories'] = get_all_categories()
    return render(request, 'wishlist.html', context)

# FUNCTION FOR PROFLE PAGE


@login_required(login_url='application:sign_in')
def profile(request):
    form = UpdateUserForm()
    context = {'form': form}
    if request.method == "POST":
        post_data = {
            'email': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        request.user.username = post_data['email']
        request.user.first_name = post_data['first_name']
        request.user.last_name = post_data['last_name']
        request.user.save()
        messages.info(request, "Profile updated successfully!")

        return redirect('application:profile')

    context['categories'] = get_all_categories()

    return render(request, 'profile.html', context)


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
                return HttpResponseRedirect(reverse('application:sign_in'))

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
                if next_param == '':
                    return redirect('application:home')
                return redirect(next_param)

            else:
                messages.error(request, f"Username or Password is Incorrect:(")

        context = {}
        context['categories'] = get_all_categories()
        return render(request, 'sign-in.html', context)

# FUNCTION FOR LOGOUT


def sign_out(request):
    logout(request)
    return redirect('application:home')
