# Generated by Django 2.2 on 2021-06-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_delete_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='series',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Серия'),
        ),
    ]
