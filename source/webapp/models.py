from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
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
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="название страны")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "валюта"
        verbose_name_plural = "валюты"
