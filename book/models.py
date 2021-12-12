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
    category = models.ManyToManyField(Category, verbose_name="دسته بندی")
    issue = models.ManyToManyField(User, through='Issue')
    description = models.TextField(verbose_name="توضیحات")
    author = models.CharField(max_length=200, verbose_name="نویسنده")
    thumbnail = models.ImageField(upload_to='images', verbose_name="عکس")
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

    def thumbnail_tag(self):
        return format_html("<img width=100 src='{}'>".format(self.thumbnail.url))


class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issue_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_user')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    renewCount = models.IntegerField(verbose_name="تعداد تمدید")
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.book.name

    def is_on_time(self):
        last_two_week = timezone.now() - timedelta(days=14)
        if self.created > last_two_week:
            return True
        else:
            return False

    is_on_time.boolean = True

    def jpublish(self):
        return jalaly_converter(self.created)

    def thumbnail_book(self):
        return self.book.thumbnail_tag()

