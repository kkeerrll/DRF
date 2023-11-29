from rest_framework import serializers

from payment.models import Payment
from payment.services import get_session_by_stripe_id


class PaymentSerializer(serializers.ModelSerializer):
    """
        Сериализатор модели платежа
    """
    class Meta:
        model = Payment
        fields = '__all__'

    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj: Payment):
        session = get_session_by_stripe_id(obj.session)
        return session.url
