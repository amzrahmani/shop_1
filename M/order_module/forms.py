from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        label='نام کامل',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'})
    )
    phone = forms.CharField(
        max_length=15,
        label='تلفن همراه',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09123456789'})
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
    )
    address = forms.CharField(
        label='آدرس کامل',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'آدرس پستی کامل'})
    )
    city = forms.CharField(
        max_length=100,
        label='شهر',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مشهد'})
    )
    postal_code = forms.CharField(
        max_length=10,
        label='کد پستی',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'})
    )
    notes = forms.CharField(
        required=False,
        label='یادداشت (اختیاری)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'یادداشت‌های اضافی'})
    )

    payment_method = forms.ChoiceField(
        label='روش پرداخت',
        choices=[
            ('online', 'پرداخت آنلاین'),
            ('cash', 'پرداخت در محل'),
            ('bank', 'واریز بانکی'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
