from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem
from product_module.models import Product


class ShoppingCartView(TemplateView):
    template_name = "cart/shopping_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context["cart"] = cart
            context["cart_items"] = cart.items.select_related('product').all()

        else:
            context["cart"] = None
            context["cart_items"] = []

        return context


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    cart_item.save()
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart:shopping_cart")


def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart:shopping_cart")
