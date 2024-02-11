from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CoursesViewSet, LessonsCreateAPIView, LessonsListAPIView, LessonsRetrieveAPIView, \
    LessonsUpdateAPIView, LessonsDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')


urlpatterns = [
      path('lessons/create/', LessonsCreateAPIView.as_view(), name='lessons_create'),
      path('lessons/', LessonsListAPIView.as_view(), name='lessons_list'),
      path('lessons/<int:pk>/', LessonsRetrieveAPIView.as_view(), name='lessons_detail'),
      path('lessons/update/<int:pk>/', LessonsUpdateAPIView.as_view(), name='lessons_update'),
      path('lessons/delete/<int:pk>/', LessonsDestroyAPIView.as_view(), name='lessons_delete'),

    ] + router.urls
