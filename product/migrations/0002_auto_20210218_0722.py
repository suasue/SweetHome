# Generated by Django 3.1.6 on 2021-02-18 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeliveryMethod',
            new_name='DeliveryType',
        ),
        migrations.RenameField(
            model_name='deliveryfee',
            old_name='won',
            new_name='fee',
        ),
        migrations.AlterField(
            model_name='productreview',
            name='like_user',
            field=models.ManyToManyField(related_name='user_like_product', through='product.ReviewLike', to='user.User'),
        ),
        migrations.AlterModelTable(
            name='deliverytype',
            table='delivery_types',
        ),
    ]