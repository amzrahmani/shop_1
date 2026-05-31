from django.db import models
from django.conf import settings
from product_module.models import Product



class Order(models.Model):
    """
    مدل سفارش: نماینده یک سفارش کاربر با وضعیت، تاریخ و مجموع.
    """
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total(self):
        """
        محاسبه مجموع سفارش بر اساس آیتم‌ها و ذخیره در فیلد total.
        """
        total = sum(item.total_price for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])
        return self.total


class OrderItem(models.Model):
    """
    آیتم‌های هر سفارش: محصول، تعداد و قیمت.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity}x {self.product.title}"

    @property
    def total_price(self):
        """
        مجموع قیمت برای این آیتم (قیمت × تعداد)
        """
        return self.price * self.quantity


class OrderHistory(models.Model):
    """
    مدل تاریخچه سفارشات: نگهداری خلاصه سفارشات کاربر برای نمایش در داشبورد.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_history'
    )
    created_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"OrderHistory #{self.order.id} - {self.user.username}"

