from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.filters import OrderingFilter

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_pay']
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

