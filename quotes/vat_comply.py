import requests


class VatComplyService:
    BASE_URL = "https://api.vatcomply.com"

    def fetch_exchange_rates(self, date):
        url = f"{self.BASE_URL}/rates"
        if type(date) is not str:
            date = date.strftime("%Y-%m-%d")
        params = {
            "base": "USD",
            "date": date,
            "symbols": "EUR,JPY,BRL",
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
