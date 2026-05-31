from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Wishlist, WishlistItem
from product_module.models import Product


class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = "wishlist/wishlist_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)

        context["wishlist_items"] = wishlist.items.all()

        return context


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    product = get_object_or_404(Product, id=product_id)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    return redirect("wishlist_page:wishlist")


def remove_from_wishlist(request, item_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    item = get_object_or_404(WishlistItem, id=item_id)
    item.delete()

    return redirect("wishlist_page:wishlist")
