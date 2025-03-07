# Generated by Django 5.1.7 on 2025-03-07 19:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='peca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=300)),
                ('code', models.CharField(max_length=120, unique=True)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
