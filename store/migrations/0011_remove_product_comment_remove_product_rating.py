# Generated by Django 4.1.6 on 2023-05-25 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_product_rating_remove_product_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]