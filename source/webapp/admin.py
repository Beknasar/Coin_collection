from django.contrib import admin
from webapp.models import Country, Currency, Material


class CountryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class CurrencyAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__icontains',)


admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Material)

