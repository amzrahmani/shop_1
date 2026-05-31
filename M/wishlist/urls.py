from django.urls import path
from . import views

app_name = "wishlist_page"

urlpatterns = [
    path("", views.WishlistView.as_view(), name="wishlist"),
    path("add/<int:product_id>/", views.add_to_wishlist, name="add"),
    path("remove/<int:item_id>/", views.remove_from_wishlist, name="remove"),
]