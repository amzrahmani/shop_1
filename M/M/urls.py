from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحه اصلی
    path('', include('home_module.urls')),

    # حساب کاربری
    path('accounts/', include('accounts_module.urls')),

    # محصولات
    path('products/', include('product_module.urls', namespace='product')),
    # سبد خرید
    path("cart/", include("cart_module.urls",namespace= 'cart')),
    # سفارشات
    path('orders/', include('order_module.urls',namespace='orders')),

    # بلاگ
    path("blog/", include("blog.urls", namespace="blog")),


    # تماس با ما
    path('contact_us/', include('contact_module.urls')),

    # درباره ما
    path('about_us/', include('about_us.urls')),

    path("wishlist_page/", include("wishlist.urls", namespace= 'wishlist_page')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
