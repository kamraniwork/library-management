# Generated by Django 3.2.10 on 2021-12-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('d', 'مخالفت با تمدید'), ('p', 'امانت عادی'), ('q', 'گذشت زمان مجاز'), ('o', 'درخواست تمدید کاربر'), ('k', 'تحویل کتاب')], max_length=1, verbose_name='وضعیت'),
        ),
    ]
