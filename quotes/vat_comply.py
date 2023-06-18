import requests


class VatComplyService:
    BASE_URL = "https://api.vatcomply.com"

    def parse_date(self, date):
        if type(date) is str:
            return date
        return date.strftime("%Y-%m-%d")

    def fetch_exchange_rates(self, date):
        url = f"{self.BASE_URL}/rates"
        date = self.parse_date(date)
        params = {
            "base": "USD",
            "date": date,
            "symbols": "EUR,JPY,BRL",
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
