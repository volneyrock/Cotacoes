from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from quotes.models import Currency, Quote
from quotes.tasks import fetch_and_save_exchange_rates
from quotes.utils import fetch_currency_quotes, validate_input
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


class ValidateInputTests(TestCase):
    def test_validate_input_valid(self):
        error = validate_input("2023-06-01", "2023-06-05", "BRL")
        self.assertIsNone(error)

    def test_validate_input_no_dates_or_currencies(self):
        error = validate_input(None, None, None)
        self.assertEqual(error, "Por favor, selecione data inicial, final e a moeda.")

    def test_validate_input_end_date_in_future(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        error = validate_input("2023-06-01", future_date, "EUR")
        self.assertEqual(error, "A data final não pode ser maior do que o dia de hoje")

    def test_validate_input_start_date_greater_than_end_date(self):
        error = validate_input("2023-06-05", "2023-06-01", "EUR")
        self.assertEqual(
            error, "A data de inicial não pode ser maior que a data final."
        )

    def test_validate_input_more_than_five_business_days(self):
        error = validate_input("2023-06-01", "2023-06-10", "EUR")
        self.assertEqual(
            error, "O período informado deve ser de no máximo 5 dias úteis."
        )


class FetchCurrencyQuotesTests(TestCase):
    fixtures = ["test_data.json"]

    def test_fetch_currency_quotes(self):
        start_date = "2023-06-05"
        end_date = "2023-06-09"
        resp_currency, quotes = fetch_currency_quotes(start_date, end_date, "EUR")
        self.assertEqual(resp_currency.symbol, "EUR")
        self.assertEqual(len(quotes), 5)

    def test_fetch_currency_quotes_with_invalid_dates(self):
        start_date = "2023-06-05"
        end_date = "2023-06-01"
        resp_currency, quotes = fetch_currency_quotes(start_date, end_date, "EUR")
        self.assertEqual(resp_currency.symbol, "EUR")
        self.assertEqual(len(quotes), 0)

    def test_fetch_currency_quotes_with_invalid_currency(self):
        start_date = "2023-06-05"
        end_date = "2023-06-09"
        resp_currency, quotes = fetch_currency_quotes(start_date, end_date, "AAA")
        self.assertIsNone(resp_currency)
        self.assertEqual(len(quotes), 0)


class ExchangeRatesViewTests(TestCase):
    fixtures = ["test_data.json"]

    def test_no_dates_or_currency(self):
        response = self.client.get(reverse("quotes:index"))
        self.assertContains(
            response,
            "Por favor, selecione data inicial, final e a moeda.",
            status_code=200,
        )

    def test_end_date_in_future(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(
            reverse("quotes:index"),
            {"start_date": "2023-06-01", "end_date": future_date, "currency": "EUR"},
        )
        self.assertContains(
            response,
            "A data final não pode ser maior do que o dia de hoje",
            status_code=200,
        )

    def test_start_date_greater_than_end_date(self):
        response = self.client.get(
            reverse("quotes:index"),
            {"start_date": "2023-06-05", "end_date": "2023-06-01", "currency": "EUR"},
        )
        self.assertContains(
            response,
            "A data de inicial não pode ser maior que a data final.",
            status_code=200,
        )

    def test_more_than_five_business_days(self):
        response = self.client.get(
            reverse("quotes:index"),
            {"start_date": "2023-06-01", "end_date": "2023-06-10", "currency": "EUR"},
        )
        self.assertContains(
            response,
            "O período informado deve ser de no máximo 5 dias úteis.",
            status_code=200,
        )

    def test_valid_input(self):
        response = self.client.get(
            reverse("quotes:index"),
            {"start_date": "2023-06-05", "end_date": "2023-06-09", "currency": "EUR"},
        )
        self.assertContains(response, "EUR", status_code=200)
        self.assertContains(response, "2023-06-05", status_code=200)
        self.assertContains(response, "2023-06-09", status_code=200)
        self.assertContains(response, "0.92", status_code=200)
