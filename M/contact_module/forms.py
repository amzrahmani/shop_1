from django import forms
from .models import CantactProduct


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = CantactProduct
        fields = {'name', 'email', 'title', 'message'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'row': '5',
                'id': 'message'
            }), }
        labels = {
            'name': 'نام نام خانوادگی'
        }
        error_messages = {
            'name': {
                'required': 'نام نام خانوادگی اجباری می باشد'
            },
            'email': {
                'required': ' اییل الزامی می باشد'
            }
        }
