# Generated by Django 2.2 on 2021-06-21 14:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0036_auto_20210621_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin_in_Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='coin_pics', verbose_name='картинка монеты')),
                ('nominal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='номинал')),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Вес')),
                ('size', models.CharField(max_length=100, verbose_name='размер')),
                ('form', models.CharField(max_length=100, verbose_name='Форма')),
                ('year_of_issue', models.IntegerField(blank=True, null=True, verbose_name='Дата выпуска')),
                ('year_of_issue_end', models.IntegerField(blank=True, null=True, verbose_name='Дата окончания выпуска')),
                ('series', models.CharField(blank=True, max_length=100, null=True, verbose_name='Серия')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coins_coll', to='webapp.Collection', verbose_name='коллекция')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coin_in_collection', to='webapp.Country', verbose_name='страна')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coin_in_collection', to='webapp.Currency', verbose_name='валюта')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coin_in_collection', to='webapp.Material', verbose_name='материал')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='coins', to=settings.AUTH_USER_MODEL, verbose_name='создатель')),
            ],
            options={
                'verbose_name': 'монета в коллекции',
                'verbose_name_plural': 'монеты в коллекции',
            },
        ),
    ]
