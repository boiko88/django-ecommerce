# Generated by Django 4.1.6 on 2023-09-30 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
