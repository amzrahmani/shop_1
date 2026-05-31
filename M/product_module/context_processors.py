from .models import Category


def global_context(request):
    return {
        "categories": Category.objects.filter(is_active=True).order_by('title')
    }
