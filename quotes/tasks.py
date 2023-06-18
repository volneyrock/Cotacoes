from datetime import datetime, timedelta

from quotes.models import Currency, Quote
from quotes.vat_comply import VatComplyService


def parse_date(date):
    if type(date) is str:
        return datetime.strptime(date, "%Y-%m-%d").date()
    return date


def fetch_and_save_exchange_rates(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
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
