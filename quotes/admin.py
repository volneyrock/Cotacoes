from django.contrib import admin

from quotes.models import Currency, Quote


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["symbol"]
    search_fields = ["symbol"]
    ordering = ["symbol"]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ["target_currency", "date", "price"]
    search_fields = ["target_currency__symbol"]
    list_filter = ["target_currency", "date"]
    date_hierarchy = "date"
    ordering = ["-date"]
