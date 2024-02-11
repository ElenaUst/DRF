from rest_framework import viewsets, generics

from lms.models import Courses, Lessons
from lms.serializers import CoursesSerializer, LessonsSerializer


class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CoursesSerializer
    queryset = Courses.objects.all()


class LessonsCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsSerializer


class LessonsUpdateAPIView(generics.UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer



