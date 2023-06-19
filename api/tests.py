from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class QuoteListAPIViewTests(APITestCase):
    fixtures = ["test_api_data.json"]

    def setUp(self):
        self.url = reverse("api:quote-list-api")

    def test_list_quotes_without_params(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("base_currency", response.data)
        self.assertEqual(response.data["base_currency"], "USD")
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 6)

    def test_list_quotes_with_valid_params(self):
        response = self.client.get(
            self.url,
            {"symbol": "EUR", "start_date": "2023-06-05", "end_date": "2023-06-09"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("base_currency", response.data)
        self.assertEqual(response.data["base_currency"], "USD")
        self.assertIn("results", response.data)

    def test_list_quotes_return_only_rates_for_symbol(self):
        response = self.client.get(
            self.url,
            {"symbol": "EUR", "start_date": "2023-06-05", "end_date": "2023-06-09"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for result in response.data["results"]:
            self.assertEqual(result["target_currency"], "EUR")

    def test_list_quotes_return_only_rates_for_date_range(self):
        response = self.client.get(
            self.url,
            {"start_date": "2023-06-05", "end_date": "2023-06-09"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for result in response.data["results"]:
            self.assertGreaterEqual(result["date"], "2023-06-05")
            self.assertLessEqual(result["date"], "2023-06-09")

    def test_list_quotes_with_invalid_params(self):
        response = self.client.get(
            self.url,
            {"symbol": "EUR", "start_date": "2023-06-09", "end_date": "2023-06-05"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_quotes_with_invalid_symbol(self):
        response = self.client.get(
            self.url,
            {"symbol": "AAA", "start_date": "2023-06-05", "end_date": "2023-06-09"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
