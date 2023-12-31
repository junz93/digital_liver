# Generated by Django 4.2.3 on 2023-09-18 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0011_alter_environmentorder_paid_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.character')),
                ('interaction_types', models.ManyToManyField(to='material.wordslibrary')),
                ('qa_library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.questionanswerlibrary')),
                ('speech_library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.speechlibrary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
