from django.views.generic import TemplateView

from quotes.utils import fetch_currency_quotes, validate_input


class ExchangeRatesView(TemplateView):
    template_name = "quotes/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        selected_currency = self.request.GET.get("currency")

        # Validate input
        error_message = validate_input(start_date, end_date, selected_currency)
        if error_message:
            context["error_message"] = error_message
            return context

        # Fetch data
        currency, quotes = fetch_currency_quotes(
            start_date, end_date, selected_currency
        )
        context["symbol"] = currency.symbol if currency else None
        context["quotes"] = quotes
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["selected_currency"] = selected_currency

        return context
