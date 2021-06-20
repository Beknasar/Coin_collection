from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from webapp.models import Coin, Collection, Coin_in_Collection, Currency


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class CoinForm(forms.ModelForm):
    def __init__(self, country, *args, **kwargs):
        super(CoinForm, self).__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.filter(country=country)

    class Meta:
        model = Coin
        exclude = ['owner', 'country']


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ['owner']


class CollectionCoinForm(forms.ModelForm):
    class Meta:
        model = Coin_in_Collection
        exclude = ['owner', 'country']

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('pk', None)
        coin = kwargs.get('instance', None)
        super(CollectionCoinForm, self).__init__(*args, **kwargs)
        user = get_object_or_404(User, id=user_id)
        # print(user)
        self.fields['collection'].queryset = Collection.objects.filter(owner=user)
        self.fields['currency'].queryset = Currency.objects.filter(country=coin.country)
        self.fields['quantity'].initial = 1

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        collection = cleaned_data.get('collection')
        if not collection:
            errors.append(ValidationError("You should create collection first!"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data
