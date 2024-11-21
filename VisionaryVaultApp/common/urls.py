from django.urls import path

from VisionaryVaultApp.common import views
from VisionaryVaultApp.common.views import AddToBasketView, BasketView, RemoveFromBasketView, ProcessCheckoutView

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('add-to-basket/<int:art_piece_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('remove-from-basket/<int:item_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    path('checkout/', ProcessCheckoutView.as_view(), name='checkout')
]
