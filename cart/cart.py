class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def _normalize_quantity(self, quantity, default=1, max_qty=99):
        """
        تبدیل مقدار ورودی به عدد صحیح بین 1 و max_qty.
        اگر ورودی خراب باشد، default استفاده می‌شود.
        """
        try:
            qty = int(quantity)
        except (TypeError, ValueError):
            qty = default

        if qty < 1:
            qty = default
        if qty > max_qty:
            qty = max_qty
        return qty

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        quantity = self._normalize_quantity(quantity, default=1)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}

        self.cart[product_id]["quantity"] += quantity
        # سقف برای جمع هم اعمال می‌کنیم
        self.cart[product_id]["quantity"] = self._normalize_quantity(
            self.cart[product_id]["quantity"], default=1
        )
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            qty = self._normalize_quantity(quantity, default=0)
            if qty <= 0:
                del self.cart[product_id]
            else:
                self.cart[product_id]["quantity"] = qty
            self.session.modified = True
