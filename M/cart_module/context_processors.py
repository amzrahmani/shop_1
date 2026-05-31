from .models import Cart, CartItem

def cart_context(request):
    cart_items = []
    cart_total = 0
    cart_count = 0

    # اگر کاربر لاگین کرده
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product').all()

        cart_total = sum(item.total_price() for item in cart_items)
        cart_count = sum(item.quantity for item in cart_items)


    else:
        cart_items = []
        cart_total = 0
        cart_count = 0

    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,
    }
