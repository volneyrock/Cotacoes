from rest_framework import serializers

from quotes.models import Currency, Quote


class QuoteSerializer(serializers.ModelSerializer):
    target_currency = serializers.StringRelatedField()

    class Meta:
        model = Quote
        fields = ["id", "target_currency", "date", "price"]


class QuoteFilterSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        if (
            "start_date" in data
            and "end_date" in data
            and data["end_date"] < data["start_date"]
        ):
            raise serializers.ValidationError(
                "A data final deve ser maior ou igual a data inicial."
            )

        if (
            "symbol" in data
            and not Currency.objects.filter(symbol=data["symbol"]).exists()
        ):
            raise serializers.ValidationError("Símbolo de moeda inválido.")

        return data
