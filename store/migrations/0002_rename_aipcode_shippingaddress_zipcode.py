# Generated by Django 4.1.6 on 2023-02-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='aipcode',
            new_name='zipcode',
        ),
    ]