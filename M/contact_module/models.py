from django.db import models


# Create your models here.
class CantactProduct(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام و نام خانواندگی')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    title = models.CharField(max_length=300, verbose_name='عنوان')
    message = models.TextField(verbose_name='متن تماس با ما')
    created = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.TextField(verbose_name='پاسخ تماس با ما', null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title





