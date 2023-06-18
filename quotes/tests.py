from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from quotes.models import Currency, Quote
from quotes.tasks import fetch_and_save_exchange_rates
from quotes.vat_comply import VatComplyService


class VatComplyServiceTest(TestCase):
    def setUp(self):
        self.service = VatComplyService()
        self.mock_response_data = {
            "date": "2023-06-15",
            "base": "USD",
            "rates": {
                "BRL": 4.82,
                "EUR": 0.92,
                "JPY": 141.28,
            },
        }

    @patch("requests.get")
    def test_fetch_exchange_rates_with_invalid_date(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "Invalid date",
        }

        result = self.service.fetch_exchange_rates(datetime.today())

        self.assertIsNone(result)

    @patch("requests.get")
    def test_fetch_exchange_rates(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        result = self.service.fetch_exchange_rates(datetime.today())

        self.assertIsNotNone(result)
        self.assertEqual(result["base"], "USD")
        self.assertIn("EUR", result["rates"])
        self.assertIn("JPY", result["rates"])
        self.assertIn("BRL", result["rates"])

    @patch("requests.get")
    def test_fetch_exchange_rates_with_string_date(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        result = self.service.fetch_exchange_rates("2023-06-15")

        self.assertIsNotNone(result)
        self.assertEqual(result["base"], "USD")
        self.assertIn("EUR", result["rates"])
        self.assertIn("JPY", result["rates"])
        self.assertIn("BRL", result["rates"])


class FetchAndSaveExchangeRatesTest(TestCase):
    def setUp(self) -> None:
        self.mock_response_data = {
            "date": "2023-06-15",
            "base": "USD",
            "rates": {
                "BRL": 4.82,
                "EUR": 0.92,
                "JPY": 141.28,
            },
        }

    @patch("quotes.tasks.VatComplyService")
    def test_fetch_and_save_exchange_rates(self, mock_service):
        mock_service().fetch_exchange_rates.return_value = self.mock_response_data

        start_date = datetime(2023, 6, 15)
        end_date = datetime(2023, 6, 15)
        fetch_and_save_exchange_rates(start_date, end_date)

        self.assertEqual(Currency.objects.count(), 3)
        self.assertEqual(Quote.objects.count(), 3)

        for symbol in ["BRL", "EUR", "JPY"]:
            currency = Currency.objects.get(symbol=symbol)
            quote = Quote.objects.get(target_currency=currency, date=start_date)
            self.assertEqual(
                float(quote.price),
                mock_service().fetch_exchange_rates.return_value["rates"][symbol],
            )

    @patch("quotes.tasks.VatComplyService")
    def test_fetch_and_save_exchange_rates_with_no_rates(self, mock_service):
        mock_service().fetch_exchange_rates.return_value = None

        start_date = datetime(2023, 6, 16)
        end_date = datetime(2023, 6, 16)
        fetch_and_save_exchange_rates(start_date, end_date)

        self.assertEqual(Currency.objects.count(), 0)
        self.assertEqual(Quote.objects.count(), 0)

    @patch("quotes.tasks.VatComplyService")
    def test_fetch_and_save_exchange_rates_with_dates_as_string(self, mock_service):
        mock_service().fetch_exchange_rates.return_value = self.mock_response_data

        start_date = "2023-06-15"
        end_date = "2023-06-15"
        fetch_and_save_exchange_rates(start_date, end_date)

        self.assertEqual(Currency.objects.count(), 3)
        self.assertEqual(Quote.objects.count(), 3)

        for symbol in ["BRL", "EUR", "JPY"]:
            currency = Currency.objects.get(symbol=symbol)
            quote = Quote.objects.get(target_currency=currency, date=start_date)
            self.assertEqual(
                float(quote.price),
                mock_service().fetch_exchange_rates.return_value["rates"][symbol],
            )
