# Generated by Django 5.1.2 on 2024-11-05 09:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osauhingud', '0006_remove_individualshareholder_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualshareholder',
            name='company_registry_code',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
