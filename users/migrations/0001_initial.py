# Generated by Django 4.2 on 2023-05-06 20:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('payment_info', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('wilaya', models.CharField(max_length=255)),
                ('daira', models.CharField(max_length=255)),
                ('mairie', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('addresse_line', models.TextField()),
                ('code_postal', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(11111), django.core.validators.MaxValueValidator(99999)])),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
