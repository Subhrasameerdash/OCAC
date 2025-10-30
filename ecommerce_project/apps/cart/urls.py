from django.urls import path

from .views import (
    add_to_cart,
    cart_detail,
    checkout,
    checkout_success,
    remove_from_cart,
    update_cart_item,
)

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="detail"),
    path("add/<slug:slug>/", add_to_cart, name="add"),
    path("remove/<int:pk>/", remove_from_cart, name="remove"),
    path("update/<int:pk>/", update_cart_item, name="update"),
    path("checkout/", checkout, name="checkout"),
    path("success/", checkout_success, name="checkout_success"),
]
