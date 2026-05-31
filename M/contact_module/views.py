from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import ContactModelForm
from .models import CantactProduct
from django.core.mail import send_mail


class ContactUsView(CreateView):
    model = CantactProduct
    form_class = ContactModelForm
    template_name = 'contact/contact_us_page.html'
    success_url = reverse_lazy('contact_us')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'پیام شما با موفقیت ارسال شد. به زودی با شما تماس می‌گیریم 🌹'
        )
        return response

