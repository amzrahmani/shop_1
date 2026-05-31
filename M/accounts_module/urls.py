from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path("dashboard/", views.UserDashboardView.as_view(), name="dashboard_page"),
    # path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),

]
