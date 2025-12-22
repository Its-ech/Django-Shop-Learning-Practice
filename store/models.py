from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
