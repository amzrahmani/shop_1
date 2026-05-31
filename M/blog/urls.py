from django.urls import path
from .  import views
app_name = "blog"

urlpatterns = [
    # لیست بلاگ‌ها
    path('',views.BlogListView.as_view(), name='blog-list'),

    # جزئیات بلاگ
    path('<slug:slug>/',views.BlogDetailView.as_view(), name='blog-detail'),
]
