from django.http import HttpRequest


def cart_item_count(request: HttpRequest) -> dict[str, int]:
    if request.user.is_authenticated:
        return {"cart_item_count": request.user.cart_items.count()}
    return {"cart_item_count": 0}
