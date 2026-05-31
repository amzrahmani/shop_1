from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, Category


class ProductViews(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, is_delete=False)
        category_id = self.kwargs.get('pk') or self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset.order_by('-price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        category_id = self.kwargs.get('pk') or self.request.GET.get('category')
        context['current_category'] = None
        if category_id:
            context['current_category'] = get_object_or_404(Category, pk=category_id)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorite_product_id = self.request.session.get('product_favorite')
        context['is_favorite'] = favorite_product_id == str(self.object.id)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class AddFavorite(View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        request.session["product_favorite"] = str(product.id)
        request.session.modified = True
        return redirect(product.get_absolute_url())


def category_products_view(request, id):
    category = get_object_or_404(Category, id=id, is_active=True)
    products = category.products.filter(is_active=True)
    return render(request, 'products/category_products.html', {
        'current_category': category,
        'products': products
    })


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()
