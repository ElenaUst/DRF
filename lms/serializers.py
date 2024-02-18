from rest_framework import serializers

from lms.models import Courses, Lessons


class CoursesSerializer(serializers.ModelSerializer):
    """Класс сериализатора для курса"""
    lessons_count = serializers.SerializerMethodField()
    num_lessons = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        """Метод для вывода списка уроков, входящих в курс"""
        return [lesson.title for lesson in Lessons.objects.filter(course=course)]

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lessons.objects.filter(course=course).count()

    class Meta:
        model = Courses
        fields = '__all__'


class LessonsSerializer(serializers.ModelSerializer):
    """Класс сериализатора для урока"""
    class Meta:
        model = Lessons
        fields = '__all__'

