from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    image = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to="products/")
    price = models.PositiveIntegerField(verbose_name='قیمت')
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, verbose_name='دسته بندی')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    best_seller = models.BooleanField(default=False, verbose_name='محبوب ترین محصولات')
    on_sale = models.BooleanField(default=False, verbose_name='فروش ویژه')
    short_description = models.CharField(max_length=300, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال ')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده/ حذف نشده')
    slug = models.SlugField(default="", max_length=200, unique=True, verbose_name='عنوان در URL')
    old_price = models.PositiveIntegerField(null=True, blank=True)
    is_new = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('product:product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tag')

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'برچسب محصول'
        verbose_name_plural = 'تگ محصولات'

