from django.shortcuts import redirect, render
from store.models import Product
from .cart import Cart


def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id, quantity=1)
    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)

    product_ids = list(cart.cart.keys())
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    for p in products:
        item = cart.cart.get(str(p.id))
        qty = item["quantity"] if item else 0

        cart_items.append({
            "product": p,
            "quantity": qty,
            "total_price": p.price * qty,
        })

    total = sum(i["total_price"] for i in cart_items)

    return render(request, "cart/detail.html", {
        "cart_items": cart_items,
        "total": total,
    })
