from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import date


class Material(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='название материала')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "материал"
        verbose_name_plural = "материалы"


class Country(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="название страны")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "страна"
        verbose_name_plural = "страны"


class Currency(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="название валюты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "валюта"
        verbose_name_plural = "валюты"


class Series(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="название серии")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "серия"
        verbose_name_plural = "серии"


class Coin(models.Model):
    picture = models.ImageField(null=True, blank=True, upload_to='coin_pics', verbose_name='картинка монеты')
    nominal = models.IntegerField(verbose_name='номинал', validators=(MinValueValidator(0),))
    material = models.ForeignKey('webapp.Material', related_name='coins', on_delete=models.PROTECT, verbose_name='материал')
    currency = models.ForeignKey('webapp.Currency', related_name='coins', on_delete=models.PROTECT, verbose_name='валюта')
    country = models.ForeignKey('webapp.Country', related_name='coins', on_delete=models.PROTECT, verbose_name='страна')
    weight = models.FloatField(verbose_name='Вес', validators=(MinValueValidator(0),))
    size = models.CharField(max_length=100, null=False, blank=False, verbose_name="размер")
    form = models.CharField(max_length=100, null=False, blank=False, verbose_name="Форма")
    year_of_issue = models.IntegerField(verbose_name='Дата выпуска', null=True, blank=True)
    year_of_issue_end = models.IntegerField(verbose_name='Дата окончания выпуска', null=True, blank=True)
    series = models.ForeignKey('webapp.Series', related_name='coins', on_delete=models.PROTECT, verbose_name='серия', null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f"{self.nominal} {self.currency} {self.year_of_issue}"

    class Meta:
        verbose_name = "монета"
        verbose_name_plural = "монеты"
