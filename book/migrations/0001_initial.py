# Generated by Django 3.2.10 on 2021-12-17 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('delay', models.BooleanField(default=False, verbose_name='تاخیر')),
                ('status', models.BooleanField(default=True, verbose_name='آیا هنوز در امانت است یا خیر؟ ')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_book', to='book.book')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
