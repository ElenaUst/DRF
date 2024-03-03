from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Courses, Lessons
from lms.paginators import CustomPagination
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CoursesSerializer, LessonsSerializer


class CoursesViewSet(viewsets.ModelViewSet):
    """Вьюсет для действий с курсами"""
    serializer_class = CoursesSerializer
    queryset = Courses.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Метод для автоматической привязки курса к создателю"""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Метод описания доступов к действиям с уроками"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonsCreateAPIView(generics.CreateAPIView):
    """Класс для создания урока"""
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


    def perform_create(self, serializer):
        """Метод для автоматической привязки урока к создателю"""
        serializer.save(owner=self.request.user)


class LessonsUpdateAPIView(generics.UpdateAPIView):
    """Класс для изменения урока"""
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonsRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для просмотра урока"""
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonsListAPIView(generics.ListAPIView):
    """Класс для просмотра списка уроков"""
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CustomPagination


class LessonsDestroyAPIView(generics.DestroyAPIView):
    """Класс для удаления урока"""
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsOwner]






