from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from apps.products.models import Product


class CartItem(models.Model):
    """Represents a single product entry in a user's cart."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Order(models.Model):
    """Stores completed checkout information for auditing and fulfilment."""

    PAYMENT_CHOICES = [
        ("card", "Credit/Debit Card"),
        ("cod", "Cash on Delivery"),
        ("paypal", "PayPal"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity
