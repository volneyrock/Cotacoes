from django.urls import path

from quotes.views import ExchangeRatesView

app_name = "quotes"


urlpatterns = [path("", ExchangeRatesView.as_view(), name="index")]
