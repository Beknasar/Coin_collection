# Generated by Django 2.2 on 2021-06-15 09:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_auto_20210610_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin_in_Collection',
            fields=[
                ('coin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webapp.Coin')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'монета в коллекции',
                'verbose_name_plural': 'монеты в коллекции',
            },
            bases=('webapp.coin',),
        ),
        migrations.AlterModelOptions(
            name='nominal',
            options={'verbose_name': 'номинал', 'verbose_name_plural': 'номиналы'},
        ),
    ]
