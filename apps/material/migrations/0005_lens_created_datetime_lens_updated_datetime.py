# Generated by Django 4.2.3 on 2023-09-06 07:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_lens'),
    ]

    operations = [
        migrations.AddField(
            model_name='lens',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lens',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]