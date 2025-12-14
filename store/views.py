from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404


def home(request):
    context = {
        "title": "Django Shop",
        "welcome_message": "Welcome to my Django shop from template!",
        "tagline": "learning Django step by step",
    }
    return render(request, "store/home.html", context)

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/product_list.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})
