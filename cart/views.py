from django.shortcuts import redirect, render
from .cart import Cart
from store.models import Product

def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id, quantity=1)
    return redirect("cart_detail")

def cart_detail(request):
    cart = Cart(request)
    product_ids = cart.cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    return render(request, "cart/detail.html", {"cart": cart, "products": products})
