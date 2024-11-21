from .models import Basket


def basket_count(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
        if basket:
            basket_item_count = basket.items.count()
        else:
            basket_item_count = 0
    else:
        basket_item_count = 0

    return {'basket_item_count': basket_item_count}