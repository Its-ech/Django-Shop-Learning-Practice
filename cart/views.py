from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.http import Http404
from store.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    
    if not cart.cart:
        return render(request, "cart/detail.html", {
            "cart_items": [],
            "total": 0,
            "is_empty": True,
        })

    product_ids = list(cart.cart.keys())
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    for p in products:
        item = cart.cart.get(str(p.id))
        qty = item["quantity"] if item else 0
        
        if qty > 0:  # فقط آیتم‌های معتبر
            cart_items.append({
                "product": p,
                "quantity": qty,
                "total_price": p.price * qty,
            })

    total = sum(i["total_price"] for i in cart_items)

    return render(request, "cart/detail.html", {
        "cart_items": cart_items,
        "total": total,
        "is_empty": len(cart_items) == 0,
    })


@require_POST
def cart_add(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("product_list")
    
    cart = Cart(request)
    qty = request.POST.get("quantity", "1")
    cart.add(product_id=product.id, quantity=int(qty) if qty.isdigit() else 1)
    
    messages.success(request, f"Added {product.name} to cart.")
    return redirect("cart_detail")


@require_POST
@require_http_methods(["POST"])
def cart_update(request, product_id):
    cart = Cart(request)
    qty_str = request.POST.get("quantity", "1")
    
    # Cart خودش ولیدیشن می‌کند، ولی اینجا هم چک می‌کنیم
    try:
        qty = int(qty_str)
        if qty < 0:
            qty = 0
    except ValueError:
        qty = 1
    
    cart.update(product_id, qty)
    
    if qty > 0:
        try:
            product = Product.objects.get(id=product_id)
            messages.success(request, f"Updated {product.name} quantity.")
        except Product.DoesNotExist:
            pass
    else:
        messages.info(request, "Item removed from cart.")
    
    return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product_id)
        messages.success(request, f"Removed {product.name} from cart.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    
    return redirect("cart_detail")


@require_POST
def cart_clear(request):
    cart = Cart(request)
    item_count = len(cart.cart)
    cart.clear()
    
    if item_count > 0:
        messages.success(request, f"Cleared {item_count} items from cart.")
    else:
        messages.info(request, "Cart was already empty.")
    
    return redirect("cart_detail")
