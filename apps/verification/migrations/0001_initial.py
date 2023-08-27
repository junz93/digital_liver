# Generated by Django 4.2.3 on 2023-08-27 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_phone', models.CharField(max_length=11)),
                ('code', models.CharField(max_length=6)),
                ('valid', models.BooleanField(default=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
