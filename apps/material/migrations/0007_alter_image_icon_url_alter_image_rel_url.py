# Generated by Django 4.2.3 on 2023-09-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0006_image_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='icon_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='image',
            name='rel_url',
            field=models.URLField(),
        ),
    ]
