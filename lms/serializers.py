from rest_framework import serializers

from lms.models import Courses, Lessons


class CoursesSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return [lesson.name for lesson in Lessons.objects.filter(course=course)]

    def get_num_lessons(self, course):
        return Lessons.objects.filter(course=course).count()

    class Meta:
        model = Courses
        fields = '__all__'


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'

