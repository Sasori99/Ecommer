# Generated by Django 3.1.7 on 2021-06-18 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210618_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.bookstatus', verbose_name='Tình trạng'),
        ),
    ]
