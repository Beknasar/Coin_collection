# Generated by Django 2.2 on 2021-06-21 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20210620_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
    ]
