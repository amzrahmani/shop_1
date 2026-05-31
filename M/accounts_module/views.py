from django.shortcuts import render, redirect
from django.views import View
from .models import User
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



class Register(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'my_accounts/register.html', {
            'register_form': register_form
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            user_email = register_form.cleaned_data['email']
            user_password = register_form.cleaned_data['password']

            if User.objects.filter(email=user_email).exists():
                register_form.add_error(
                    'email',
                    'این ایمیل قبلاً ثبت شده است'
                )

            else:
                # ✅ ساخت username خودکار از ایمیل
                username = user_email.split("@")[0]

                # اگر تکراری بود یک عدد تصادفی اضافه می‌کنیم
                if User.objects.filter(username=username).exists():
                    username += get_random_string(5)

                new_user = User(
                    username=username,
                    email=user_email,
                    is_active=True
                )

                new_user.set_password(user_password)
                new_user.save()

                return redirect('dashboard_page')

        return render(request, 'my_accounts/register.html', {
            'register_form': register_form
        })


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'my_accounts/login_page.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data["email"]
            user_password = login_form.cleaned_data["password"]
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                login_form.add_error("email", "کاربری با این ایمیل وجود ندارد")
                return render(request, 'my_accounts/login_page.html', {"login_form": login_form})

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=user_password
            )
            if authenticated_user is not None:
                login(
                    request, authenticated_user
                )
                return redirect("home_page")
            else:
                login_form.add_error("password", "رمز عبور اشتباه است")
        return render(request, 'my_accounts/login_page.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home_page")


class UserDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'my_accounts/dashboard.html'
