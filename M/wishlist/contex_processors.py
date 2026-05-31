from .models import Wishlist


def wishlist_context(request):
    wishlist_count = 0

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist.items.count()
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    else:
        wishlist = request.session.get('wishlist_page', [])
        wishlist_count = len(wishlist)

    return {'wishlist_count': wishlist_count}
