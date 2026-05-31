from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('tracking/', views.OrderTrackingView.as_view(), name='order_tracking'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/status/', views.UpdateOrderStatusView.as_view(), name='update_status'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<int:order_id>/', views.OrderPaymentView.as_view(), name='order_payment'),
    path('confirmation/<int:pk>/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
]