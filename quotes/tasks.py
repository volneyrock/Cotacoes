from datetime import datetime, timedelta

from celery import shared_task

from quotes.models import Currency, Quote
from quotes.vat_comply import VatComplyService


@shared_task
def fetch_and_save_exchange_rates():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=5)
    service = VatComplyService()
    date = start_date

    while date <= end_date:
        rates = service.fetch_exchange_rates(date)
        if rates is not None:
            for symbol, price in rates["rates"].items():
                currency, _ = Currency.objects.get_or_create(symbol=symbol)
                Quote.objects.update_or_create(
                    target_currency=currency, date=date, defaults={"price": price}
                )
        date += timedelta(days=1)
