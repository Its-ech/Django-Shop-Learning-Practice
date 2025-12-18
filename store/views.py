from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator



def home(request):
    context = {
        "title": "Django Shop",
        "welcome_message": "Welcome to my Django shop from template!",
        "tagline": "learning Django step by step",
    }
    return render(request, "store/home.html", context)

def product_list(request):
    products_qs = Product.objects.filter(is_active=True).order_by("id")
    paginator = Paginator(products_qs, 5)  
    page_number = request.GET.get("page") 
    page_obj = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {"page_obj": page_obj})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})
