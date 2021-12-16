# Generated by Django 3.2.10 on 2021-12-12 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('author', models.CharField(max_length=200, verbose_name='نویسنده')),
                ('thumbnail', models.ImageField(upload_to='images', verbose_name='عکس')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')),
                ('status', models.CharField(choices=[('d', 'امانت گرفته شده'), ('p', 'موجود')], max_length=1, verbose_name='وضعیت')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(max_length=100, verbose_name='موضوع')),
                ('status', models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')),
                ('position', models.IntegerField(verbose_name='پوزیشن')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')),
                ('renewCount', models.IntegerField(verbose_name='تعداد تمدید')),
                ('status', models.BooleanField(default=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_book', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='book.Category', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='book',
            name='issue',
            field=models.ManyToManyField(through='book.Issue', to=settings.AUTH_USER_MODEL),
        ),
    ]