from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer, UserRegisterSerializer


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


class PaymentsListView(generics.ListAPIView):
    """Класс для просмотра списка платежей"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_pay']
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')




