from __future__ import annotations

from decimal import Decimal

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product

from .models import CartItem, Order, OrderItem


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20)
    payment_type = forms.ChoiceField(choices=Order.PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base_class}".strip()


@login_required
def cart_detail(request: HttpRequest) -> HttpResponse:
    cart_items = request.user.cart_items.select_related("product")
    total = sum((item.subtotal for item in cart_items), Decimal("0"))
    return render(
        request,
        "cart/cart.html",
        {"cart_items": cart_items, "total": total},
    )


@login_required
def add_to_cart(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if product.stock == 0:
        messages.warning(request, "This product is currently out of stock.")
        return redirect("products:product_detail", slug=product.slug)

    quantity = int(request.POST.get("quantity", 1)) if request.method == "POST" else 1
    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if created:
        cart_item.quantity = 0

    new_quantity = cart_item.quantity + quantity
    if new_quantity > product.stock:
        new_quantity = product.stock
        messages.warning(request, "Requested quantity exceeds stock. Quantity adjusted.")

    cart_item.quantity = max(new_quantity, 1)
    cart_item.save()
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("cart:detail")


@login_required
def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponse:
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == "POST":
        cart_item.delete()
        messages.info(request, "Item removed from your cart.")
    return redirect("cart:detail")


@login_required
def update_cart_item(request: HttpRequest, pk: int) -> HttpResponse:
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if request.method != "POST":
        return redirect("cart:detail")

    if quantity < 1:
        cart_item.delete()
        messages.info(request, "Item removed from your cart.")
    else:
        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
            messages.warning(request, "Quantity reduced to available stock.")
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")
    return redirect("cart:detail")


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart_items = list(request.user.cart_items.select_related("product"))
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("products:product_list")

    total = sum((item.subtotal for item in cart_items), Decimal("0"))
    insufficient_item = next((i for i in cart_items if i.product.stock < i.quantity), None)
    if insufficient_item:
        messages.error(
            request,
            f"Not enough stock for {insufficient_item.product.name}. Please adjust your cart.",
        )
        return redirect("cart:detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        user=request.user,
                        full_name=form.cleaned_data["full_name"],
                        address=form.cleaned_data["address"],
                        city=form.cleaned_data["city"],
                        postal_code=form.cleaned_data["postal_code"],
                        payment_type=form.cleaned_data["payment_type"],
                        total_amount=total,
                    )

                    for item in cart_items:
                        product = (
                            Product.objects.select_for_update()
                            .get(pk=item.product_id)
                        )
                        if product.stock < item.quantity:
                            raise ValueError("Insufficient stock during checkout")
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item.quantity,
                            unit_price=product.price,
                        )
                        product.stock -= item.quantity
                        product.save(update_fields=["stock"])

                    request.user.cart_items.all().delete()
            except ValueError:
                messages.error(
                    request,
                    "Unfortunately, one of the items went out of stock. Please review your cart.",
                )
                return redirect("cart:detail")

            messages.success(request, "Order placed successfully!")
            return redirect("cart:checkout_success")
    else:
        form = CheckoutForm()

    return render(
        request,
        "cart/checkout.html",
        {"form": form, "cart_items": cart_items, "total": total},
    )


@login_required
def checkout_success(request: HttpRequest) -> HttpResponse:
    return render(request, "cart/checkout_success.html")
