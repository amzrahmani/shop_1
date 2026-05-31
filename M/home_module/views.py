from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from .models import Slider
from product_module.models import Product, Category
from blog.models import Blog
from django.db.models import Prefetch


class HomeView(TemplateView):
    template_name = "home_module/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_products = Product.objects.filter(
            is_active=True,
            is_delete=False
        ).select_related('category', 'brand')

        context["sliders"] = Slider.objects.filter(is_active=True)
        context["featured_products"] = active_products.filter(on_sale=True)[:8]
        context["best_sellers"] = active_products.filter(best_seller=True)[:8]
        context["new_arrivals"] = active_products.order_by('-id')[:8]
        context["trending_products"] = active_products.filter(best_seller=True)[:5]
        categories = Category.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'products',
                queryset=active_products,
                to_attr='active_products'
            )
        )
        context["categories"] = categories

        sale_offer = active_products.filter(on_sale=True).first()
        if sale_offer and sale_offer.old_price:
            sale_offer.discount = sale_offer.old_price - sale_offer.price
        else:
            sale_offer = None
        context["sale_offer"] = sale_offer
        context["latest_blogs"] = Blog.objects.filter(
            is_active=True
        ).order_by('-created_at')[:3]

        return context


def add_to_cart(request, product_id):
    """تابع موقت برای افزودن به سبد خرید"""
    # TODO: بعداً با cart_module کامل می‌کنیم
    # برای الان فقط redirect می‌کنیم
    return redirect('home_page')


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.session.get('wishlist_page', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
        request.session['wishlist_page'] = wishlist
        request.session.modified = True
    return redirect('home_page')

# def site_header_component(request):
#     return render(request, "shared/site_header_component.html", {
#         "categories": Category.objects.filter(is_active=True),
#         "cart_items": [],
#         "cart_total": 0,
#     })
#
#
# def site_footer_component(request):
#     return render(request, 'shared/site_footer_component.html')
