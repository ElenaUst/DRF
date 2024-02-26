from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentsListView, UserRegister, UserUpdate, UserRetrieve, UserList, SubscriptionAPIView

app_name = UsersConfig.name
urlpatterns = [
    path('payments/', PaymentsListView.as_view(), name='payments'),
    path('', UserList.as_view(), name='users-list'),
    path('create/', UserRegister.as_view(), name='users-create'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='users-update'),
    path('detail/<int:pk>/', UserRetrieve.as_view(), name='users-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courses/subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
    ]

