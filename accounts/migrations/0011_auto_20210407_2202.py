# Generated by Django 3.1.7 on 2021-04-08 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210404_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
