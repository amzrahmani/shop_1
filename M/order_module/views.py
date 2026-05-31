from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from .models import Order, OrderItem, OrderHistory
from .forms import CheckoutForm
from product_module.models import Product
from cart_module.models import Cart, CartItem


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'order_module/checkout.html'

    def get(self, request):
        # بررسی اینکه سبد خرید خالی نباشد
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()

            if not cart_items.exists():
                messages.warning(request, 'سبد خرید شما خالی است')
                return redirect('cart_view')

        except Cart.DoesNotExist:
            messages.warning(request, 'سبد خرید شما خالی است')
            return redirect('cart_view')

        form = CheckoutForm()
        total_price = sum(item.total_price() for item in cart_items)

        context = {
            'form': form,
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = CheckoutForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    cart = Cart.objects.get(user=request.user)
                    cart_items = cart.items.all()

                    if not cart_items.exists():
                        messages.error(request, 'سبد خرید شما خالی است')
                        return redirect('cart_view')
                    order = Order.objects.create(
                        user=request.user,
                        status='pending',
                        total=0
                    )

                    total_order_price = 0
                    for cart_item in cart_items:
                        if cart_item.product.inventory < cart_item.quantity:
                            raise ValueError(f'موجودی محصول {cart_item.product.title} کافی نیست')

                        cart_item.product.inventory -= cart_item.quantity
                        cart_item.product.save()

                        order_item = OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                        total_order_price += order_item.total_price

                    order.total = total_order_price
                    order.save()

                    OrderHistory.objects.create(
                        order=order,
                        user=request.user,
                        created_at=order.created_at,
                        status=order.status,
                        total=order.total
                    )
                    checkout_data = form.cleaned_data
                    cart.items.all().delete()

                    messages.success(request, 'سفارش شما با موفقیت ثبت شد!')

                    payment_method = form.cleaned_data.get('payment_method', 'online')

                    if payment_method == 'online':
                        return redirect('order_payment', order_id=order.id)
                    else:
                        return redirect('order_confirmation', pk=order.id)

            except Cart.DoesNotExist:
                messages.error(request, 'سبد خرید شما خالی است')
                return redirect('cart_view')
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart_view')
            except Exception as e:
                messages.error(request, f'خطا در ثبت سفارش: {str(e)}')
                return redirect('checkout')

        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.total_price() for item in cart_items)

        context = {
            'form': form,
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, self.template_name, context)


class OrderPaymentView(LoginRequiredMixin, View):
    template_name = 'order_module/payment.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.status != 'pending':
            messages.warning(request, 'این سفارش قبلاً پردازش شده است')
            return redirect('order_detail', pk=order.id)

        context = {
            'order': order,
        }
        return render(request, self.template_name, context)

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        order.status = 'processing'
        order.save()
        order.history.status = 'processing'
        order.history.save()
        messages.success(request, 'پرداخت با موفقیت انجام شد! سفارش شما در حال پردازش است.')
        return redirect('order_confirmation', pk=order.id)


class OrderConfirmationView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_module/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderTrackingView(LoginRequiredMixin, View):
    template_name = "order_module/order_tracking.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        order_number = request.POST.get('order_number')
        email = request.POST.get('email', request.user.email)

        try:
            order = Order.objects.get(
                id=order_number,
                user__email=email
            )
        except Order.DoesNotExist:
            order = None

        context = {
            "order": order,
            "email": email,
            "order_number": order_number
        }

        return render(request, self.template_name, context)


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_module/order_history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_module/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class UpdateOrderStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        new_status = request.POST.get('status')

        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()

            if hasattr(order, 'history'):
                order.history.status = new_status
                order.history.save()
            messages.success(request, 'وضعیت سفارش به‌روزرسانی شد')
        return redirect('order_detail', pk=order.id)
