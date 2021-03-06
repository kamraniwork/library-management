from django.db import models
from django.utils import timezone
from extension.utils import jalaly_converter
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="children", verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, verbose_name="موضوع")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Book(models.Model):
    Status_Choise = (
        ('d', 'امانت گرفته شده'),
        ('p', 'موجود'),
    )

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    category = models.ManyToManyField(Category, blank=True, verbose_name="دسته بندی")
    issue = models.ManyToManyField(User, through='Issue')
    description = models.TextField(verbose_name="توضیحات")
    author = models.CharField(max_length=200, verbose_name="نویسنده")
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    status = models.CharField(max_length=1, choices=Status_Choise, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def category_to_string(self):
        return ", ".join([cat.title for cat in self.category.all()])

    def jpublish(self):
        return jalaly_converter(self.created)


class Issue(models.Model):
    Status_Choise = (
        ('d', 'مخالفت با تمدید'),
        ('p', 'امانت عادی'),
        ('q', 'گذشت زمان مجاز'),
        ('o', 'درخواست تمدید کاربر'),
        ('k', 'تحویل کتاب'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issue_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_user')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    renewCount = models.IntegerField(verbose_name="تعداد تمدید")
    delay = models.BooleanField(default=False, verbose_name='تاخیر')
    status = models.CharField(max_length=1, choices=Status_Choise, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.book.name

    def save(self, *args, **kwargs):
        if self.status == 'k':
            self.book.status = 'p'
        else:
            self.book.status = 'd'

        self.book.save()
        super(Issue, self).save(*args, **kwargs)

    def is_not_time(self):
        last_two_week = timezone.now() - timedelta(days=14)
        if self.created > last_two_week:
            self.delay = False
            self.save()
            return False
        else:
            self.delay = True
            self.save()
            return True

    is_not_time.boolean = True

    def jpublish(self):
        return jalaly_converter(self.created)
