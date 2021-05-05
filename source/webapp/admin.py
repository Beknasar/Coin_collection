from django.contrib import admin
from webapp.models import Country, Currency, Material, Series, Coin


class CountryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class CurrencyAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__icontains',)


class SeriesAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__icontains',)


class CoinAdmin(admin.ModelAdmin):
    exclude = ('description', 'year_of_issue_end', )
    list_display_links = ('pk', 'name')
    list_filter = ('country',)
    empty_value_display = '---'


admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Material)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Coin)


