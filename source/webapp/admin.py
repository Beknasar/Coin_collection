from django.contrib import admin
from webapp.models import Country, Currency, Material, Coin, Nominal, Collection,  Coin_in_Collection


class CountryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class CurrencyAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__icontains',)


class NominalAdmin(admin.ModelAdmin):
    ordering = ('currency', 'nominal',)


class CoinAdmin(admin.ModelAdmin):
    exclude = ('description', 'year_of_issue_end', )
    list_display = ('pk', 'nominal', 'currency', 'year_of_issue')
    list_display_links = ('pk', 'nominal',)
    list_filter = ('country',)
    empty_value_display = '---'


admin.site.register(Coin_in_Collection)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Material)
admin.site.register(Coin, CoinAdmin)
admin.site.register(Nominal, NominalAdmin)
admin.site.register(Collection)

