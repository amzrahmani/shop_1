from django.shortcuts import render
from django.views.generic import View ,TemplateView


# Create your views here.
class AboutUsView(TemplateView):
    template_name = 'about/about_page.html'
