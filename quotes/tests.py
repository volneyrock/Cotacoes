from unittest.mock import patch
from django.test import TestCase
from quotes.vat_comply import VatComplyService
from datetime import datetime


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
