from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Coin, Country, Currency


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        exclude = []