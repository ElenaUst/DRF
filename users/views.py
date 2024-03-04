from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from lms.models import Courses
from users.models import Payments, User, Subscription
from users.serializers import PaymentsSerializer, UserSerializer, UserRegisterSerializer, SubscriptionSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class UserRegister(generics.CreateAPIView):
    """Класс для регистрации пользователя"""
    serializer_class = UserRegisterSerializer

    def create(self, request):
        """Метод для хэширования пароля пользователя в БД"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieve(generics.RetrieveAPIView):
    """Класс для просмотра пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdate(generics.UpdateAPIView):
    """Класс для обновления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserList(generics.ListAPIView):
    """Класс для просмотра списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsCreate(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        payment = serializer.save()
        stripe_prod_id = create_stripe_product(payment)
        stripe_price_id = create_stripe_price(payment, stripe_prod_id)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.save()


class PaymentsListView(generics.ListAPIView):
    """Класс для просмотра списка платежей"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_pay']
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class SubscriptionAPIView(APIView):
    """Класс для установки подписки пользователя и на удаление подписки у пользователя."""

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = Courses.objects.get(pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})







