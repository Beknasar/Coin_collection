# Generated by Django 2.2 on 2021-06-15 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='coins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='webapp.Coin_in_Collection', verbose_name='монеты'),
        ),
    ]
