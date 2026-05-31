from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('کلمه عبور مغایرت دارد')

        return confirm_password


class LoginForm(forms.Form):
    email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={
        "class": "form-control"
    }))
    password = forms.CharField(label="پسوورد", widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }
    ))
