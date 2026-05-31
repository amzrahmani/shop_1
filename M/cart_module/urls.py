from django.urls import path
from .views import ShoppingCartView, add_to_cart, remove_from_cart

app_name = 'cart'

urlpatterns = [
    path("", ShoppingCartView.as_view(), name="shopping_cart"),
    path("add/<int:product_id>/", add_to_cart, name="add-to-cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
]
