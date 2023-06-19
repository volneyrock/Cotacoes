from django.urls import path

from .views import QuoteListAPIView

app_name = "api"

urlpatterns = [
    path("quotes/", QuoteListAPIView.as_view(), name="quote-list-api"),
]
