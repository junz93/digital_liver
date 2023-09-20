# Generated by Django 4.2.3 on 2023-09-06 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0003_wordslibrary_words'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lens_name', models.CharField(max_length=100)),
                ('focus_object', models.CharField(choices=[('NONE', '无'), ('FACE', '面部'), ('FOOT', '脚部'), ('BODY', '全身')], max_length=10)),
                ('position_x', models.CharField(max_length=10)),
                ('position_y', models.CharField(max_length=10)),
                ('position_z', models.CharField(max_length=10)),
                ('focus', models.IntegerField()),
                ('aperture', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
