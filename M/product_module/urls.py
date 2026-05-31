from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.ProductViews.as_view(), name='product-list'),

    path('product-favorite/', views.AddFavorite.as_view(), name='product-favorite'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:pk>/', views.ProductViews.as_view(), name='category-products'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
]
