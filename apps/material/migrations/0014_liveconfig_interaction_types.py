# Generated by Django 4.2.3 on 2023-09-18 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0013_remove_liveconfig_interaction_types_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='liveconfig',
            name='interaction_types',
            field=models.CharField(default='GIFT', max_length=50),
        ),
    ]
