from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart
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

def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save() 
            product_ids = list(cart.cart.keys())
            products = Product.objects.filter(id__in=product_ids)

            for p in products:
                item = cart.cart.get(str(p.id))
                qty = item["quantity"] if item else 0
                if qty > 0:
                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        price=p.price,
                        quantity=qty,
                    )

            cart.clear()

            return render(request, "store/checkout_success.html", {"order": order})
    else:
        form = CheckoutForm()

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

    return render(request, "store/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": total,
    })
